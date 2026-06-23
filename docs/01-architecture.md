# Architecture — the layered stack

Taktology is deliberately **thin**. It owns only the process half of takt planning
and composes with maintained ontologies for everything else.

As of **v0.3.0** the process/zone/resource backbone is reused from the **DTC**
(Digital Twin Construction) ontology; takt only specializes it and adds the
takt-specific layer. Alignment is by *reference* (no `owl:imports`) to stay light.

```
┌─────────────────────────────────────────────────────────────────────┐
│  takt:   (THIS repo — v0.3.0 minimal core, 17 terms)                  │
│          TaktTask, WagonType, Crew, TaktTime, TaktZone                │
│          performedIn, actsOn, instantiates, hasSuccessor, hasTaktTime │
│          + takt-specific values: productionRate, crewSize, taktDuration│
│   subClassOf / subPropertyOf ↓      skos:closeMatch → ifc:            │
├─────────────────────────────────────────────────────────────────────┤
│  dtc:    Digital Twin Construction ontology (process backbone)        │
│          WorkPackage, Activity, AsPlannedWorkerCrew,                  │
│          AsPlannedWorkingZone, isPerformedIn, hasTarget               │
│          (imports bot:; reified sequence & resource patterns)         │
├─────────────────────────────────────────────────────────────────────┤
│  top:    TopologicPy — GEOMETRY/GRAPH engine (rdfs:seeAlso)           │
│          Cell/Element/Path, area, volume, containsElement            │
│  bot:    topology vocabulary (reached via dtc: and top:)              │
│  ifc:    IFC 4.3 process schema — closeMatch interchange anchor       │
│  prov:   provenance for database-derived rates                       │
└─────────────────────────────────────────────────────────────────────┘
```

`dtc:` (the semantic schema) and `top:` (the compute engine that produces zones and
quantities) meet at `bot:`, which both align to — so they compose without conflict.

## Why this shape

The conversation worked through the obvious alternatives and discarded them:

- **A full takt-zone ontology** — over-engineering. DTC's `AsPlannedWorkingZone`
  ("construction site subdivision") is exactly a takt zone, and `top:FunctionalZone`
  computes its geometry. The zone is **one subclass**, not an ontology.
- **Extending BOT directly** — unnecessary. `top:` already binds its spatial classes
  to `bot:` *and* `ifc:` simultaneously (`top:Zone rdfs:subClassOf bot:Zone`,
  `skos:closeMatch ifc:IfcZone`). The alignment work is already done and maintained.
- **Importing ifcOWL** — wrong dependency. ifcOWL is a faithful but ~14k-axiom
  translation of the EXPRESS schema; importing it to anchor a handful of takt terms
  destroys the modularity and slows reasoning. Use `ifc:` as a `closeMatch` target
  only. (See [03-decisions.md](03-decisions.md).)

## What taktology still adds on top of DTC

DTC already models the process (`WorkPackage`/`Activity`/`Task`), working zones
(`AsPlannedWorkingZone`), worker crews (`AsPlannedWorkerCrew`), the task→element
target (`hasTarget`) and task→zone location (`isPerformedIn`). After reusing all of
that, taktology adds only what DTC lacks:

- **A wagon TYPE layer** (`takt:WagonType`) — DTC has no task-type; this aligns to
  `ifc:IfcTaskType`.
- **The takt rhythm** (`takt:taktDuration`, `takt:TaktTime`) — DTC has start/end
  timestamps but no concept of a fixed takt beat.
- **Work-density effort values** (`takt:productionRate` h/m², `crewSize`,
  `quantityUnit`) — the BIMTakt / Work Density Method primitives.
- **Direct-edge simplifications** (`hasSuccessor`, `performedBy`) over DTC's reified
  precondition/assignment patterns — `rdfs:seeAlso`-related, not subproperties.

That residue is the entire reason this repo exists, and it is small.

## Two halves, one graph

```
  WagonType ──instantiates── TaktTask ──performedIn── TaktZone ──containsElement── Element
   (rate,                      │  │                     (top:                        (top:
    crew)                      │  └──actsOn─────────────────────────────────────────►│
                               │     (operand subset — drives duration)              area/
                  hasSuccessor │                                                      volume)
                               ▼
                            TaktTask  (next wagon → the train)
```

The payoff of putting both halves in one graph: a single traversal goes from a task
all the way down to the geometry that drives its duration
(`task → actsOn → element → area`). A spreadsheet cannot do that — its quantities
live in a different model entirely.

See [02-vocabulary.md](02-vocabulary.md) for the wagon/train/zone terms and the full
IFC mapping table, and [03-decisions.md](03-decisions.md) for the rationale behind
each choice.
