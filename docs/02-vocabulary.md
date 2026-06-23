# Vocabulary — wagon, train, zone, and the IFC mapping

The takt metaphor is a railway: work moves through the building like trains running
on a track. "Wagon" and "train" are Lean/takt terms; `IfcTask`/`IfcProcess` are
schema entities — and they do **not** map one-to-one.

## The terms

| Takt / Lean term | What it is | In this repo (v0.3.0) |
|---|---|---|
| **Takt zone** (track segment / station) | The spatial unit work flows through. A train "stops" at each zone for one takt. The demo plan's `B5:1`, `C5`, `A5:1`. | `takt:TaktZone` ⊑ `top:FunctionalZone` (⊑ `bot:Zone`) + `dtc:AsPlannedWorkingZone` |
| **Wagon** (definition) | A single trade's work package as a reusable template — work content + crew + a fixed takt duration. The coloured numbers (5.1, 5.2, …) are wagon ids. | `takt:WagonType` (no DTC parent — fills DTC's missing type layer) |
| **Wagon** (occurrence) | One cell: this trade, this zone, this takt. | `takt:TaktTask` ⊑ `dtc:WorkPackage` |
| **Train** | The ordered convoy of wagons. **Not an entity** — the `hasSuccessor` chain (a path). | *no class* — query the `takt:hasSuccessor` chain |
| **Takt time** | The fixed rhythm (1 week in the demo plan) each wagon occupies. | `takt:TaktTime` (the beat = `takt:taktDuration`) |
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

## Train: Reading A vs Reading B — pin this down before generating

| | Reading A *(default)* | Reading B |
|---|---|---|
| A train is… | the **cross-trade convoy** through one zone: 5.1 → 5.2 → 5.3 → 6.1 → … | one **wagon's run** across all zones: 5.1 in B5:1 → A5:1 → C5 … |
| `hasSuccessor` goes between | different wagons, same zone | same wagon, adjacent zones |
| Matches | the demo plan rows read left-to-right | a single trade tracked across the sheet |

The demo plan almost certainly encodes **Reading A**. One line of the generation
loop changes between them — but it changes the entire graph shape, so confirm with
the team.

## Full mapping — `takt:` ↔ DTC ↔ IFC

Each takt term reuses DTC (`rdfs:subClassOf`/`subPropertyOf`, or `seeAlso` where DTC's
shape differs) and `skos:closeMatch`es IFC.

| `takt:` term | DTC (reused) | IFC (closeMatch) |
|---|---|---|
| `WagonType` | — *(DTC has no type layer)* | `IfcTaskType` |
| `TaktTask` | ⊑ `dtc:WorkPackage` | `IfcTask` |
| `TaktZone` | ⊑ `dtc:AsPlannedWorkingZone` **+** ⊑ `top:FunctionalZone` (⊑ `bot:Zone`) | `IfcSpatialZone` |
| `Crew` | ⊑ `dtc:AsPlannedWorkerCrew` | `IfcCrewResource` |
| `TaktTime` | seeAlso `dtc:startTime`/`endTime` | `IfcTaskTime` |
| `instantiates` | seeAlso `dtc:hasActivity` | `IfcRelDefinesByType` |
| `performedIn` (WHERE) | ⊑ `dtc:isPerformedIn` | `IfcRelAssignsToProduct` (location) |
| `actsOn` (WHAT) | ⊑ `dtc:hasTarget` | `IfcRelAssignsToProduct` (product) |
| `performedBy` | seeAlso `dtc:hasResourceAssignment`/`requiresResource` | `IfcRelAssignsToProcess` |
| `hasSuccessor` (the **train**) | seeAlso `dtc:requiresProcess` (reified) | `IfcRelSequence` |
| `partOfProcess` | range `dtc:Process` | `IfcRelNests` |
| `hasTaktTime` | — *(takt-specific)* | — |
| `taktDuration`/`slot` | — *(takt-specific)* | — |
| milestone | — | `IfcTask.IsMilestone` |

Two notes. (1) IFC overloads `IfcRelAssignsToProduct` for **both** location and operand
— which is why `performedIn` and `actsOn` both `closeMatch` it; the takt layer keeps
the distinction sharp. (2) DTC **reifies** sequencing and resource assignment
(precondition/assignment objects); takt uses direct edges for simplicity, so those map
by `seeAlso`, not `subPropertyOf`. The whole takt plan (`IfcWorkSchedule`) is out of the
minimal core — see [03-decisions.md](03-decisions.md) ADR-7.
