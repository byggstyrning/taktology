# Takt production graph ingester — implementation plan

A plan for the script that turns an IFC spatial model **+** a wagon table into a
takt production graph (RDF aligned to `ontology/takt.ttl` + `top:`, and/or a
property graph / IFC-SPF export).

It is written to slot into the **same Ingester / Element / Relationship pattern**
as an existing egress-circulation graph builder, so it reuses that framework's
storey-assignment, adjacency, and TopologicPy gating rather than reinventing them.

```
SCRIPT_NAME = "TaktProduction"
DESCRIPTION = "Build wagon -> zone -> sequence production edges from IFC + a wagon table"
```

---

## The load-bearing decision: process is NOT geometry

An egress script reads everything from IFC because doors *are* geometry. **Wagons,
rates and crews are not geometry** — they are a planning table. So this ingester
takes **two inputs**, and the IFC is consulted only for zones and quantities.

> If the agent tries to stuff wagon data into IFC property sets, that is the wrong
> instinct. The table is authoritative for process; IFC is authoritative for space
> and quantity.

---

## 0. Inputs

```
ifc_files:   List[Path]   # spatial model: IfcSpace / IfcSpatialZone + elements
wagon_table: Path         # CSV/JSON — the activity structure (BIMTakt Bild 5):
                          #   wagon_id, name, crew_code, production_rate, crew_size,
                          #   quantity_unit, predecessor_wagon_id, applies_to
takt_config: dict         # takt_length ("P1W"), hours_per_day, zone_grouping rule,
                          #   train_reading ("A" | "B")
```

## 1. Zone resolution  (reuse egress storey-assignment)

`resolve_takt_zones(ifc) -> Dict[zone_id, ZoneRec]` with a fallback ladder:

1. `IfcSpatialZone` tagged via `ObjectType`/Pset as a takt zone *(preferred)*
2. `IfcZone` grouping of `IfcSpace` via `IfcRelAssignsToGroup`
3. derive: group `IfcSpace` by storey + a partition rule from `takt_config`
   (the "B5:1" half-floor / fire-compartment split)

Emit `Element(type="takt:TaktZone")`. **Lift the egress storey-assignment helper
as-is** (IFC containment -> room-number prefix -> Z-centroid).

## 2. Quantity extraction  (the `top:` hook — new vs egress)

For each zone, walk `zone -> contained elements` and sum area/volume **per element,
classified by trade**, then attach `top:area` / `top:volume`. Prefer `Qto_*`
quantity sets; else compute from geometry via `ifcopenshell.geom`.

## 3. Wagon types  (template level, no spatial dependency)

One `Element(type="takt:WagonType")` per table row; dedup `Element(type="takt:Crew")`.

## 4. Occurrence generation  (the core loop)

```python
for wagon in wagon_types:
    for zone in zones where applies(wagon, zone):       # applicability filter
        t = Element("takt:TaktTask", id=f"{wagon.id}@{zone.id}")
        Relationship(t, wagon, "takt:instantiates")
        Relationship(t, zone,  "takt:performedIn")       # WHERE
        Relationship(crew[wagon.crew_code], t, "takt:performedBy")

        operands = [e for e in zone.elements if e.trade == wagon.id]
        for e in operands:
            Relationship(t, e, "takt:actsOn")            # WHAT  (operand)

        qty   = sum(e.area if wagon.quantity_unit=="AREA" else e.volume
                    for e in operands)                   # operand subset, NOT zone total
        hours = qty * wagon.production_rate
        days  = hours / (wagon.crew_size * takt_config.hours_per_day)
        Relationship(t, TaktTime(duration=takt_length, ...), "takt:hasTaktTime")
```

## 5. Sequence / train edges

- **Reading A (default):** per zone, order tasks by wagon order, link consecutive
  with `takt:hasSuccessor`; emit a `takt:Train` with `hasMember` edges.
- **Reading B:** sequence same-wagon occurrences across **adjacent** zones (use the
  egress adjacency graph to order). Switch via `takt_config.train_reading`.

## 6. Optional TopologicPy pass  (gate exactly like egress)

Guard with `HAS_TOPOLOGICPY` and the entity ceiling. Use it ONLY for:
- computing zone adjacency (Cell/CellComplex) to order trains in step 5
- emitting `top:` triples via the topograph adapter

**Do NOT** use it for the process layer — `top:` has no task/sequence classes.

## 7. Serialize

- RDF (Turtle) using `takt:` + `top:` — the `Element`/`Relationship` objects map
  1:1 onto `examples/lumi-b5-1.ttl`. Keep `ifc:` as `closeMatch` annotations only;
  **do not import ifcOWL**.
- Optional **separate** IFC-SPF converter (`IfcTask`/`IfcRelSequence`/
  `IfcSpatialZone`) for handoff to IFC-native tools. The `closeMatch` mappings make
  it mechanical, but it is a converter, not a serialization toggle.

---

## What the agent must verify / decide before coding

1. **Framework signatures.** Confirm the actual `Ingester` / `_Base` / `Element` /
   `Relationship` / `topograph` method shapes — this plan infers them.
2. **`applies(wagon, zone)`** — pluggable predicate, project-specific. Not hardcoded.
3. **Element trade classification** (which wagon owns which element) — new,
   project-specific work, keyed on `IfcType` + material or a Pset. Required to
   populate `actsOn`; without it, fall back to the zone total **and flag it as a stub**.
4. **Train Reading A vs B** — changes where every sequence edge goes. Default A.
5. **Duration must not be faked** — reading a duration straight off the sheet defeats
   the model. It is `operand_quantity x rate / crew`. Stubbing quantities to get it
   running is fine *if flagged*; do not mistake a stub for real output.
