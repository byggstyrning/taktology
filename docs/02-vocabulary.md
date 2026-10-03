# Vocabulary — wagon, train, zone, and the IFC mapping

The takt metaphor is a railway: work moves through the building like trains running
on a track. "Wagon" and "train" are Lean/takt terms; `IfcTask`/`IfcProcess` are
schema entities — and they do **not** map one-to-one.

## The terms

| Takt / Lean term | What it is | In this repo (v0.8.0) |
|---|---|---|
| **Takt zone** (track segment / station) | The spatial unit work flows through. A train "stops" at each zone for one takt. The demo plan's `B5:1`, `C5`, `A5:1`. | `takt:TaktZone` ⊑ `bot:Zone` + `dtc:AsPlannedWorkingZone` (relatedMatch `top:Zone`) |
| **Wagon** (definition) | A single trade's work package as a reusable template — work content + crew + a fixed takt duration. It has no owner (see below). The coloured numbers (5.1, 5.2, …) are wagon ids. | `takt:WagonType` (no DTC parent — fills DTC's missing type layer; carries the template defaults `takt:trade`, `takt:slotSpan`, `takt:defaultCrew`) |
| **Wagon** (occurrence) | One cell: this trade, this zone, this takt. | `takt:Wagon` ⊑ `dtc:AsPlannedProcess` |
| **Train** | A **cross-disciplinary** convoy: the wagons of several trades running together through a sequence of zones. Its order through a zone is the `hasSuccessorSameZone` chain. Never one trade (ADR-19). | the chain; **plus** optional `takt:Train` ⊑ `dtc:AsPlannedProcess` — an addressable handle minted *only* to carry a train-scope override (its own `taktDuration`) or a name (ADR-17) |
| **Takt time** (the beat) | The fixed rhythm (1 week in the demo plan) each wagon occupies. | *no class* — `takt:taktDuration` on the plan (overridable per train / wagon / task, ADR-17), `takt:slot` on each task; dates derive from `takt:planStart` (ADR-14) |
| **The plan** (the grid) | The coloured wagon × zone grid itself, as one artifact. | `takt:TaktGraph` ⊑ `top:KnowledgeGraph` + `dtc:ConstructionSchedule` |
| **Crew** (the `SUB-xx` code) | The gang performing a wagon. | `takt:Crew` ⊑ `dtc:AsPlannedWorkerCrew` |

## "Wagon" and "train" are not single entities — the key subtlety

- A **wagon** is really a *pair*: the `WagonType` (definition) and its many `Wagon`
  occurrences (one per zone), linked by `instantiates`. When a planner says "wagon
  5.2" they mean the type; when they point at a cell, an occurrence. Same word, two
  levels.
- A **train** is **cross-disciplinary** and, by default, *not a class* — it is a
  **relationship structure**: the wagons of several trades, ordered through each zone
  by the `hasSuccessorSameZone` chain. (v0.2.0 had a `takt:Train` class; v0.3.0
  dropped it; v0.6.0 brought it back as an *optional* handle, ADR-17.) If a spec says
  "create a task called 'train'," push back — query the sequence chain, which
  preserves the queryability of the wagons inside it. One trade's run across zones
  (e.g. "the drywall train") is a **wagon's run**, not a train — see below.

## Two flow readings: location flow (the train) vs trade flow

| | Reading A — location flow | Reading B — trade flow |
|---|---|---|
| It is… | the **train's convoy order** through one zone: 5.1 → 5.2 → 5.3 → 6.1 → … (several trades) | one **wagon's run** across all zones: 5.1 in B5:1 → A5:1 → C5 … (one trade) |
| A train? | **yes** — a train is cross-disciplinary | **no** — a trade's run is not a train |
| The property | `takt:hasSuccessorSameZone` | `takt:hasSuccessorSameWagon` |
| Successive tasks share | the zone (differ in wagon) | the wagon type (differ in zone) |
| Matches | the demo plan rows read left-to-right | a single trade tracked across the sheet |

Since v0.5.0 the two readings are **subproperties** of the reading-agnostic
`takt:hasSuccessor` (ADR-16): one plan graph can carry location flow and trade flow
machine-distinguishably, and a reader that only knows the generic property still sees
one coherent chain. On ingest the ambiguity remains real — one line of the generation
loop changes between them and it changes the entire graph shape, so **confirm with the
team which reading your source data encodes** before generating edges. A source that
calls a single-trade run a "train" encodes Reading B; since v0.8.0 that is trade flow,
and the train is the cross-disciplinary convoy (ADR-19).

## Ownership: wagons have none (ADR-19)

No wagon, wagon type, train or zone is owned by an actor. `takt:trade` classifies the
work content ("drywall"), it does not name who does it or who answers for it;
`takt:Crew` is the planned resource that performs a wagon (`performedBy`), not an
owner. The vocabulary asserts no company, delivery team or responsible party anywhere.
If a project needs "who is responsible", that is a separate assertion made by the
consumer, not a property of the wagon.

## Zone scope: a zone is a cut of space, not a possession of a plan or train

A `takt:TaktZone` belongs to no plan, train or trade. It is a cut of space. Two
consequences follow, and one source motivates them.

- **Different trains may cut the same space differently.** In the Chalmers TBS work
  each production phase carries its own zone subdivision
  (`ljung-2026-sbuf-14237-slutrapport`): a structure train might run by half-storey,
  an interiors train by apartment cluster, a façade train by elevation bay. The same
  room then sits in a different zone for each train.
- **Zones of different trains may nest or overlap.** Express it with `bot:containsZone`
  and shared `bot:containsElement`. Nothing in the vocabulary forbids it: `performedIn`
  accepts any zone.
- **"Same zone" means "same cut".** `hasSuccessorSameZone` links wagons that share a
  zone, which is what you want inside a train, whose wagons share its cut. It says
  nothing about wagons of another train that touch the same space.
- **Cross-train conflict is a spatial question.** Identity-based queries (zone
  occupancy, CQ01; buffers per zone, CQ06) only see wagons in the *same* zone
  individual. Two trains that overlap in space but use different cuts are invisible to
  them; read the overlap from the spatial relation instead.

The vocabulary does not name which cut a train uses (there is no train → zone
property). That is left open on purpose; see ADR-19.

## Full mapping — `takt:` ↔ DTC ↔ IFC

Each takt term reuses DTC v2 (`rdfs:subClassOf`/`subPropertyOf`, or `seeAlso` where
DTC's shape differs). The IFC alignment splits by metamodel level: **classes** get
`skos:closeMatch` to IFC classes; **object properties** only reference the objectified
`IfcRel*` relationship entities via `rdfs:seeAlso` (a property and a
relationship-entity live at different metamodel levels).

| `takt:` term | DTC v2 (reused) | IFC |
|---|---|---|
| `WagonType` | — *(DTC has no type layer)* | closeMatch `IfcTaskType` |
| `Wagon` | ⊑ `dtc:AsPlannedProcess` | closeMatch `IfcTask` |
| `TaktZone` | ⊑ `dtc:AsPlannedWorkingZone` **+** ⊑ `bot:Zone` (relatedMatch `top:Zone`) | closeMatch `IfcSpatialZone` |
| `Crew` | ⊑ `dtc:AsPlannedWorkerCrew` | closeMatch `IfcCrewResource` |
| `TaktGraph` | ⊑ `dtc:ConstructionSchedule` (+ ⊑ `top:KnowledgeGraph`); membership = `dtc:hasProcess` | closeMatch `IfcWorkSchedule` |
| `Train` | ⊑ `dtc:AsPlannedProcess` (optional override bearer for a cross-disciplinary convoy; membership via `partOfProcess`) | — |
| `instantiates` | — *(no type layer to link to)* | seeAlso `IfcRelDefinesByType` |
| `performedIn` (WHERE) | ⊑ `dtc:isPerformedIn` | seeAlso `IfcRelAssignsToProduct` (location) |
| `actsOn` (WHAT) | ⊑ `dtc:hasTarget` | seeAlso `IfcRelAssignsToProduct` (product) |
| `performedBy` | seeAlso `dtc:hasResourceAssignment`/`requiresResource` (reified) | seeAlso `IfcRelAssignsToProcess` |
| `hasSuccessor` (+ `SameZone`/`SameWagon`) | seeAlso `dtc:requiresProcess` (reified) | seeAlso `IfcRelSequence` |
| `partOfProcess` | domain `Wagon` ∪ `Train`; range `dtc:Process`; seeAlso `dtc:isDecomposedInto`/`hasChildProcess` | seeAlso `IfcRelNests` |
| `defaultCrew` | — *(template default; `performedBy` overrides per task)* | — |
| `taktDuration` / `slot` / `planStart` | — *(the rhythm; dates derive from it)* | — *(conceptual pointer: `IfcTaskTime`)* |
| `isMilestone` | — *(cell flag)* | `IfcTask.IsMilestone` (attribute) |
| `isBuffer` / `trade` | — *(takt-specific)* | — |
| `slotSpan` | — *(multi-takt wagons; template default on `WagonType`, task override; ADR-17)* | — |

Three notes. (1) IFC overloads `IfcRelAssignsToProduct` for **both** location and
operand — which is why `performedIn` and `actsOn` both point at it; the takt layer
keeps the distinction sharp. (2) DTC **reifies** sequencing and resource assignment
(precondition/assignment objects); takt uses direct edges for simplicity, so those
map by `seeAlso`, not `subPropertyOf`. (3) Planned dates are never asserted — they
**derive** as `planStart + (slot − 1) × taktDuration`; DTC's `startTime`/`endTime`
are *as-performed observations* and must not carry planned dates. The whole takt
plan is now in the core as `takt:TaktGraph` (closeMatch `IfcWorkSchedule`) — ADR-15
superseded ADR-7's exclusion; see [03-decisions.md](03-decisions.md).
