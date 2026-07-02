# Architecture — the layered stack

Taktology is deliberately **thin**. It owns only the process half of takt planning
and composes with maintained ontologies for everything else.

As of **v0.5.0** the process/zone/resource/schedule backbone is reused from the
**DTC** (Digital Twin Construction) ontology **v2**; takt only specializes it and
adds the takt-specific layer. Alignment is by *reference* (no `owl:imports`) to
stay light.

```
┌────────────────────────────────────────────────────────────────────────┐
│  takt:   (THIS repo — v0.5.0 minimal core, 19 terms)                   │
│          TaktTask, WagonType, Crew, TaktZone, TaktGraph                │
│          performedIn, actsOn, instantiates, performedBy, partOfProcess,│
│          hasSuccessor (+SameZone / +SameWagon)                         │
│          + rhythm/flag values: taktDuration, slot, planStart,          │
│            isMilestone, isBuffer, trade                                │
│   subClassOf / subPropertyOf ↓      skos:closeMatch → ifc: (classes)   │
├────────────────────────────────────────────────────────────────────────┤
│  dtc:    Digital Twin Construction ontology v2 (process backbone)      │
│          AsPlannedProcess, AsPlannedWorkerCrew, AsPlannedWorkingZone,  │
│          ConstructionSchedule + hasProcess, isPerformedIn, hasTarget   │
│          (imports bot:; reified sequence & resource patterns)          │
├────────────────────────────────────────────────────────────────────────┤
│  bot:    topology — TaktZone ⊑ bot:Zone DIRECTLY: adjacency            │
│          (adjacentZone), containment (containsElement), nesting        │
│          (containsZone — the macro/norm/micro zone hierarchy)          │
│  top:    TopologicPy — compute engine + graph substrate:               │
│          TaktGraph ⊑ top:KnowledgeGraph; TaktZone relatedMatch         │
│          top:Zone; quantities via TGraph dictionaries / top:Quantity   │
│  ifc:    IFC4 ifcOWL (ADD2_TC1) — closeMatch interchange anchor        │
│          (IFC 4.3's process extension is the conceptual reference)     │
│  prov:   provenance for database-derived rates                         │
└────────────────────────────────────────────────────────────────────────┘
```

`dtc:` (the semantic schema) and `top:` (the compute engine that produces zones,
quantities and the plan graph itself) compose at `bot:` — DTC v2 **imports** BOT, and
`takt:TaktZone` subclasses `bot:Zone` **directly**. As of **v0.5.0**, `takt:TaktZone`
subclasses **both** `bot:Zone` (3D extent, `bot:adjacentZone`, `bot:containsElement`,
`bot:containsZone` nesting) **and** `dtc:AsPlannedWorkingZone` (the LBS/process
semantics). This matters because DTC's own working zone is *not* a `bot:Zone` (it only
`alignsWithZone` one), so without the direct `bot:Zone` parent, takt zones would sit
outside the BOT topology graph and lose adjacency/flow reasoning. The TopologicPy link
is deliberately looser — `skos:relatedMatch top:Zone`: engine-computed zone instances
may add the type, but the class carries no engine commitment. See
[03-decisions.md](03-decisions.md) ADR-13.

## Why this shape

The conversation worked through the obvious alternatives and discarded them:

- **A full takt-zone ontology** — over-engineering. DTC's `AsPlannedWorkingZone`
  ("construction site subdivision") is exactly a takt zone, and TopologicPy computes
  its geometry. The zone is **one subclass**, not an ontology.
- **A takt spatial model** — unnecessary. BOT already provides everything a takt zone
  needs spatially (adjacency, containment, nesting), DTC v2 imports BOT, and
  TopologicPy's own `top:Zone` is a `bot:Zone` too. `TaktZone` subclasses `bot:Zone`
  directly; the spatial work is already done and maintained.
- **Importing ifcOWL** — wrong dependency. ifcOWL is a faithful but ~14k-axiom
  translation of the EXPRESS schema; importing it to anchor a handful of takt terms
  destroys the modularity and slows reasoning. Use `ifc:` (IFC4 ADD2_TC1 — the latest
  published ifcOWL; no official IFC 4.3 ifcOWL exists) as a `closeMatch` target
  only. (See [03-decisions.md](03-decisions.md).)

## What taktology still adds on top of DTC

DTC v2 already models the planned process (`AsPlannedProcess`), working zones
(`AsPlannedWorkingZone`), worker crews (`AsPlannedWorkerCrew`), the task→element
target (`hasTarget`), the task→zone location (`isPerformedIn`) and the schedule
container (`ConstructionSchedule` + `hasProcess`). After reusing all of that,
taktology adds only what DTC lacks:

- **A wagon TYPE layer** (`takt:WagonType` + `takt:trade`) — DTC has no task-type;
  this aligns to `ifc:IfcTaskType`.
- **The takt rhythm** (`takt:taktDuration`, `takt:slot`, `takt:planStart`) — DTC's
  `startTime`/`endTime` are *as-performed observations*, never planned dates; planned
  dates **derive**: `planStart + (slot − 1) × taktDuration` (ADR-14).
- **The plan as a graph** (`takt:TaktGraph` ⊑ `top:KnowledgeGraph` +
  `dtc:ConstructionSchedule`) — what a TopologicPy TGraph-built plan projects into;
  see [05-tgraph-pairing.md](05-tgraph-pairing.md) for the pairing contract.
- **A process-layer link** (`takt:partOfProcess` → `dtc:Process`) — places the task in
  the on-site production process (Ljung 2026, spatio-temporal breakdown structure).
- **Direct-edge simplifications** (`hasSuccessor` with its Reading-A/B subproperties,
  `performedBy`) over DTC's reified precondition/assignment patterns —
  `rdfs:seeAlso`-related, not subproperties.

That residue is the entire reason this repo exists, and it is small.

## Two halves, one graph

```
  WagonType ──instantiates── TaktTask ──performedIn── TaktZone ──bot:containsElement── Element
   (trade,                     │  │                    (bot:Zone —                        │
    crew)                      │  └──actsOn────────────adjacency, nesting)                │
                               │     (operand subset — drives duration)      TGraph-computed
                  hasSuccessor │                                             quantity (dictionary /
                               ▼                                             top:Quantity)
                            TaktTask  (next wagon → the train)
```

The payoff of putting both halves in one graph: a single traversal goes from a task
all the way down to the quantity that drives its duration (`task → actsOn → element →`
TopologicPy-computed quantity — a TGraph dictionary value / `top:Quantity`, see
[05-tgraph-pairing.md](05-tgraph-pairing.md)). A spreadsheet cannot do that — its
quantities live in a different model entirely.

See [02-vocabulary.md](02-vocabulary.md) for the wagon/train/zone terms and the full
IFC mapping table, [03-decisions.md](03-decisions.md) for the rationale behind each
choice, and [05-tgraph-pairing.md](05-tgraph-pairing.md) for how a TGraph-built plan
carries all of this.
