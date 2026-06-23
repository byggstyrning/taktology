# Architecture — the layered stack

Taktology is deliberately **thin**. It owns only the process half of takt planning
and composes with maintained ontologies for everything else.

```
┌─────────────────────────────────────────────────────────────────────┐
│  takt:   (THIS repo — ~24 terms)                                      │
│          TaktTask, WagonType, Train, Crew, TaktTime, TaktZone         │
│          performedIn, actsOn, instantiates, hasSuccessor, hasTaktTime │
│          + the takt-specific values: productionRate, crewSize, …      │
│                                                                       │
│   subclasses / references ↓                                           │
├─────────────────────────────────────────────────────────────────────┤
│  top:    (TopologicPy ontology, v0.1.0, published)                    │
│          Zone / FunctionalZone / Cell / Element / Graph / Path        │
│          containsElement, area, volume + graph analytics              │
│          ALREADY aligns to bot: (subClassOf) AND ifc: (closeMatch)    │
├─────────────────────────────────────────────────────────────────────┤
│  bot:    topology vocabulary  ·  ifc:  process concept anchor          │
│  prov:   provenance for database-derived rates                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Why this shape

The conversation worked through the obvious alternatives and discarded them:

- **A full takt-zone ontology** — over-engineering. `top:FunctionalZone` already is
  "a zone grouped by function or programme," which is exactly a takt zone. The zone
  is **one subclass**, not an ontology.
- **Extending BOT directly** — unnecessary. `top:` already binds its spatial classes
  to `bot:` *and* `ifc:` simultaneously (`top:Zone rdfs:subClassOf bot:Zone`,
  `skos:closeMatch ifc:IfcZone`). The alignment work is already done and maintained.
- **Importing ifcOWL** — wrong dependency. ifcOWL is a faithful but ~14k-axiom
  translation of the EXPRESS schema; importing it to anchor a handful of takt terms
  destroys the modularity and slows reasoning. Use `ifc:` as a `closeMatch` target
  only. (See [03-decisions.md](03-decisions.md).)

## The one thing `top:` does NOT provide

`top:` covers topology + geometry + graph + spatial analytics + IFC/BOT alignment +
provenance. It has **no process, task, sequence, resource or schedule classes**.
That gap is the entire reason this repo exists, and it is small.

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
