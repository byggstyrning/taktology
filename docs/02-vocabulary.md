# Vocabulary — wagon, train, zone, and the IFC mapping

The takt metaphor is a railway: work moves through the building like trains running
on a track. "Wagon" and "train" are Lean/takt terms; `IfcTask`/`IfcProcess` are
schema entities — and they do **not** map one-to-one.

## The terms

| Takt / Lean term | What it is | In this repo |
|---|---|---|
| **Takt zone** (track segment / station) | The spatial unit work flows through. A train "stops" at each zone for one takt. The LUMI sheet's `B5:1`, `C5`, `A5:1`. | `takt:TaktZone` ⊑ `top:FunctionalZone` |
| **Wagon** (definition) | A single trade's work package as a reusable template — work content + crew + a fixed takt duration. The coloured numbers (5.1, 5.2, …) are wagon ids. | `takt:WagonType` |
| **Wagon** (occurrence) | One cell: this trade, this zone, this takt. | `takt:TaktTask` |
| **Train** | The ordered convoy of wagons. **Not a single entity** — a path through the task graph. | `takt:Train` ⊑ `top:Path` |
| **Takt time** | The fixed rhythm (1 week in the LUMI plan) each wagon occupies. | `takt:TaktTime` |
| **Crew** (Dexx) | The gang performing a wagon. | `takt:Crew` |

## "Wagon" and "train" are not single entities — the key subtlety

- A **wagon** is really a *pair*: the `WagonType` (definition) and its many `TaktTask`
  occurrences (one per zone), linked by `instantiates`. When a planner says "wagon
  5.2" they mean the type; when they point at a cell, an occurrence. Same word, two
  levels.
- A **train** is *not a class you instantiate as a thing* — it is a **relationship
  structure**: the ordered `hasSuccessor` chain over a set of wagons. If a spec says
  "create a task called 'train'," push back — model it as the sequence chain (and a
  `top:Path` bundle), which preserves the queryability of the wagons inside it.

## Train: Reading A vs Reading B — pin this down before generating

| | Reading A *(default)* | Reading B |
|---|---|---|
| A train is… | the **cross-trade convoy** through one zone: 5.1 → 5.2 → 5.3 → 6.1 → … | one **wagon's run** across all zones: 5.2 in B5:1 → A5:1 → C5 … |
| `hasSuccessor` goes between | different wagons, same zone | same wagon, adjacent zones |
| Matches | the LUMI rows read left-to-right | a single trade tracked across the sheet |

The LUMI sheet almost certainly encodes **Reading A**. One line of the generation
loop changes between them — but it changes the entire graph shape, so confirm with
the team.

## Full IFC mapping

| Takt concept | IFC | `takt:` term |
|---|---|---|
| Wagon (template) | `IfcTaskType` | `WagonType` |
| Wagon (occurrence / cell) | `IfcTask` | `TaktTask` |
| Takt zone | `IfcSpatialZone` | `TaktZone` |
| Crew | `IfcCrewResource` / `IfcLaborResource` | `Crew` |
| occurrence → template | `IfcRelDefinesByType` | `instantiates` |
| task → location (WHERE) | `IfcRelAssignsToProduct` (location sense) | `performedIn` |
| task → operand (WHAT) | `IfcRelAssignsToProduct` (product sense) | `actsOn` |
| crew → task | `IfcRelAssignsToProcess` | `performedBy` |
| predecessor → successor (the **train**) | `IfcRelSequence` | `hasSuccessor` |
| takt time / rhythm | `IfcTaskTime` / `IfcTaskTimeRecurring` | `TaktTime` |
| whole takt plan | `IfcWorkSchedule` (+ `IfcRelAssignsToControl`) | *(out of scope — converter)* |
| milestone (Inflytt, Dem. bygghiss) | `IfcTask` with `IsMilestone=TRUE` | `isMilestone true` |

Note IFC overloads `IfcRelAssignsToProduct` for **both** location and operand —
which is why `performedIn` and `actsOn` both `closeMatch` it. The richer takt layer
keeps the distinction sharp; it collapses to one relationship only on IFC export.
