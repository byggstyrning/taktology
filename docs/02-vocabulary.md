# Vocabulary — wagon, train, zone, and the IFC mapping

The takt metaphor is a railway: work moves through the building like trains running
on a track. "Wagon" and "train" are Lean/takt terms; `IfcTask`/`IfcProcess` are
schema entities — and they do **not** map one-to-one.

## The terms

| Takt / Lean term | What it is | In this repo (v0.5.0) |
|---|---|---|
| **Takt zone** (track segment / station) | The spatial unit work flows through. A train "stops" at each zone for one takt. The demo plan's `B5:1`, `C5`, `A5:1`. | `takt:TaktZone` ⊑ `bot:Zone` + `dtc:AsPlannedWorkingZone` (relatedMatch `top:Zone`) |
| **Wagon** (definition) | A single trade's work package as a reusable template — work content + crew + a fixed takt duration. The coloured numbers (5.1, 5.2, …) are wagon ids. | `takt:WagonType` (no DTC parent — fills DTC's missing type layer; carries `takt:trade`) |
| **Wagon** (occurrence) | One cell: this trade, this zone, this takt. | `takt:TaktTask` ⊑ `dtc:AsPlannedProcess` |
| **Train** | The ordered convoy of wagons. **Not an entity** — the `hasSuccessor` chain (a path). | *no class* — query the `takt:hasSuccessor` chain (subproperties pin the reading, below) |
| **Takt time** (the beat) | The fixed rhythm (1 week in the demo plan) each wagon occupies. | *no class* — `takt:taktDuration` on the plan, `takt:slot` on each task; dates derive from `takt:planStart` (ADR-14) |
| **The plan** (the grid) | The coloured wagon × zone grid itself, as one artifact. | `takt:TaktGraph` ⊑ `top:KnowledgeGraph` + `dtc:ConstructionSchedule` |
| **Crew** (the `SUB-xx` code) | The gang performing a wagon. | `takt:Crew` ⊑ `dtc:AsPlannedWorkerCrew` |

## "Wagon" and "train" are not single entities — the key subtlety

- A **wagon** is really a *pair*: the `WagonType` (definition) and its many `TaktTask`
  occurrences (one per zone), linked by `instantiates`. When a planner says "wagon
  5.2" they mean the type; when they point at a cell, an occurrence. Same word, two
  levels.
- A **train** is *not a class* — it is a **relationship structure**: the ordered
  `hasSuccessor` chain over a set of wagons. (v0.2.0 had a `takt:Train` class; v0.3.0
  dropped it — the minimal core represents the train purely as the chain.) If a spec
  says "create a task called 'train'," push back — query the sequence chain, which
  preserves the queryability of the wagons inside it.

## Train: Reading A vs Reading B — formalized as subproperties

| | Reading A | Reading B |
|---|---|---|
| A train is… | the **cross-trade convoy** through one zone: 5.1 → 5.2 → 5.3 → 6.1 → … | one **wagon's run** across all zones: 5.1 in B5:1 → A5:1 → C5 … |
| The property | `takt:hasSuccessorSameZone` | `takt:hasSuccessorSameWagon` |
| Successive tasks share | the zone (differ in wagon) | the wagon type (differ in zone) |
| Matches | the demo plan rows read left-to-right | a single trade tracked across the sheet |

Since v0.5.0 the two readings are **subproperties** of the reading-agnostic
`takt:hasSuccessor` (ADR-16): one plan graph can carry location flow and trade flow
machine-distinguishably, and a reader that only knows the generic property still sees
one coherent chain. On ingest the ambiguity remains real — the demo plan almost
certainly encodes Reading A, but one line of the generation loop changes between
them and it changes the entire graph shape, so **confirm with the team which reading
your source data encodes** before generating edges.

## Full mapping — `takt:` ↔ DTC ↔ IFC

Each takt term reuses DTC v2 (`rdfs:subClassOf`/`subPropertyOf`, or `seeAlso` where
DTC's shape differs). The IFC alignment splits by metamodel level: **classes** get
`skos:closeMatch` to IFC classes; **object properties** only reference the objectified
`IfcRel*` relationship entities via `rdfs:seeAlso` (a property and a
relationship-entity live at different metamodel levels).

| `takt:` term | DTC v2 (reused) | IFC |
|---|---|---|
| `WagonType` | — *(DTC has no type layer)* | closeMatch `IfcTaskType` |
| `TaktTask` | ⊑ `dtc:AsPlannedProcess` | closeMatch `IfcTask` |
| `TaktZone` | ⊑ `dtc:AsPlannedWorkingZone` **+** ⊑ `bot:Zone` (relatedMatch `top:Zone`) | closeMatch `IfcSpatialZone` |
| `Crew` | ⊑ `dtc:AsPlannedWorkerCrew` | closeMatch `IfcCrewResource` |
| `TaktGraph` | ⊑ `dtc:ConstructionSchedule` (+ ⊑ `top:KnowledgeGraph`); membership = `dtc:hasProcess` | closeMatch `IfcWorkSchedule` |
| `instantiates` | — *(no type layer to link to)* | seeAlso `IfcRelDefinesByType` |
| `performedIn` (WHERE) | ⊑ `dtc:isPerformedIn` | seeAlso `IfcRelAssignsToProduct` (location) |
| `actsOn` (WHAT) | ⊑ `dtc:hasTarget` | seeAlso `IfcRelAssignsToProduct` (product) |
| `performedBy` | seeAlso `dtc:hasResourceAssignment`/`requiresResource` (reified) | seeAlso `IfcRelAssignsToProcess` |
| `hasSuccessor` (+ `SameZone`/`SameWagon`) | seeAlso `dtc:requiresProcess` (reified) | seeAlso `IfcRelSequence` |
| `partOfProcess` | range `dtc:Process`; seeAlso `dtc:isDecomposedInto`/`hasChildProcess` | seeAlso `IfcRelNests` |
| `taktDuration` / `slot` / `planStart` | — *(the rhythm; dates derive from it)* | — *(conceptual pointer: `IfcTaskTime`)* |
| `isMilestone` | — *(cell flag)* | `IfcTask.IsMilestone` (attribute) |
| `isBuffer` / `trade` | — *(takt-specific)* | — |

Three notes. (1) IFC overloads `IfcRelAssignsToProduct` for **both** location and
operand — which is why `performedIn` and `actsOn` both point at it; the takt layer
keeps the distinction sharp. (2) DTC **reifies** sequencing and resource assignment
(precondition/assignment objects); takt uses direct edges for simplicity, so those
map by `seeAlso`, not `subPropertyOf`. (3) Planned dates are never asserted — they
**derive** as `planStart + (slot − 1) × taktDuration`; DTC's `startTime`/`endTime`
are *as-performed observations* and must not carry planned dates. The whole takt
plan is now in the core as `takt:TaktGraph` (closeMatch `IfcWorkSchedule`) — ADR-15
superseded ADR-7's exclusion; see [03-decisions.md](03-decisions.md).
