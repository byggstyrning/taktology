# Design decisions (ADRs)

Condensed records of the choices made while developing this vocabulary. Each is a
fork the conversation actually walked, with the reasoning preserved.

---

## ADR-1 — Build the spatial layer on `top:`, not a hand-rolled BOT extension

**Decision.** Use the TopologicPy ontology (`top:`, v0.1.0) for zones, elements,
geometry and the graph. Do not author a BOT extension for topology.

**Why.** `top:` already binds its spatial classes to **both** `bot:` (via
`rdfs:subClassOf`) and `ifc:` (via `skos:closeMatch`) simultaneously — e.g.
`top:Zone ⊑ top:Cell, ⊑ bot:Zone, closeMatch ifc:IfcZone`. The "extend BOT vs align
to IFC" dilemma is **pre-solved** as a maintained artifact. `top:` also *computes*
adjacency/containment/intersection from geometry (its NMT core), which is strictly
more than a vocabulary like BOT gives you, and directly helps the vertical-shaft /
stairwell cases BIMTakt flagged as hard.

**Consequence.** The takt zone is a single subclass — `takt:TaktZone ⊑
top:FunctionalZone` — inheriting Cell + bot:Zone + IFC alignment + `containsElement`
+ `area`/`volume` for free.

---

## ADR-2 — Do NOT author a takt-zone ontology; author a takt-**process** vocabulary

**Decision.** The new vocabulary is the *process* half (tasks, sequence, resources,
takt time). Zones get one subclass, no more.

**Why.** The conversation drifted zone-centric, but `top:` already won the zone.
The real gap is process, which neither `top:` nor `bot:` model at all. Calling the
result a "takt-zone ontology" misframes it.

---

## ADR-3 — Align to IFC by `skos:closeMatch`, never `owl:imports` ifcOWL

**Decision.** `ifc:` is used only as a resolvable target for `closeMatch`
annotations. ifcOWL is **not** imported.

**Why.** ifcOWL is a faithful EXPRESS→OWL translation — ~1300 classes, ~1580 object
properties, ~14k axioms, with OWL-list machinery for EXPRESS collections. Importing
it to anchor ~24 takt terms destroys modularity and slows reasoning. Note `top:`
itself made exactly this choice (`closeMatch ifc:IfcZone`, no import). ifcOWL is the
right tool only for **full-fidelity IFC round-tripping in RDF** — a different project.

**Consequence.** `closeMatch` is an *interchange* bridge, not a *reasoning* bridge.
It does not let a reasoner treat `takt:TaktTask` ≡ `ifc:IfcTask`. Round-tripping to
`.ifc` is a converter's job (IfcOpenShell), not these axioms'.

---

## ADR-4 — `actsOn` is a distinct task→element link, separate from `performedIn`

**Decision.** Add `takt:actsOn` (task → `top:Element`, the operand) **alongside**
`takt:performedIn` (task → zone, the location). Do not fold them together, and do
not rely on the transitive `task → zone → containsElement` path for the operand.

**Why.** 4D-BIM practice links `IfcTask` **directly** to the built element via
`IfcRelAssignsToProduct` — the task's operand, not merely "an element in the same
zone." A single takt zone holds elements for *many* trades; `containsElement` gives
the whole work-area inventory, while `actsOn` picks out the slice this task's
quantity and duration depend on.

**Consequence — the bug this prevents.** The duration formula must sum quantity over
`actsOn`, **not** the zone total. Reading the zone total makes every trade in the
zone inherit the same quantity, which is wrong. Both `performedIn` and `actsOn`
`closeMatch IfcRelAssignsToProduct`, mirroring IFC's own overloading of that
relationship for location vs operand.

**Caveat.** IFC frames the product side as the "resulting product." That fits
*constructive* tasks (build a wall) but not *operative* ones (paint an existing
wall). `actsOn` is deliberately broader — it covers produced **and** operated-on
elements — so the `closeMatch` to IFC is slightly narrower than the property.

---

## ADR-5 — The model is a property graph (LPG); `IfcRel*` become edges

**Decision.** Represent the takt plan as a labelled property graph — nodes for
entities, typed directed edges for `IfcRel*` relationships, with properties on edges.

**Why.** In IFC/STEP, `IfcRel*` relationships are **reified** (objectified entities
with attributes like `SequenceType`, `lag`). LPG edges carry properties, so each
reified relationship collapses to one labelled edge-with-properties — a cleaner fit
than RDF, which forces reification or RDF-star. `top:` already models this layer
(`top:Graph`, `top:Node`, `top:DirectedRelationship`, `top:Path`), so the train is a
`top:Path` and bottleneck analysis is a centrality query on the zone graph.

**Edge vs node per relationship.** `IfcRelSequence` (1:1) and the location link →
edges. 1:N/N:M relations (`assigns-to-process`, `nests`) → fan out to multiple
edges; promote to an intermediate node only if you need set-level attributes.

---

## ADR-6 — RDF vs property graph is a CONSUMER decision, not a semantic one

**Decision.** Author/compute where TopologicPy gives computed topology; choose the
serialization by who consumes it.

- **Internal pipeline / own tooling** → a property graph (or `top:`’s `Graph` in
  Python) with your labels. No OWL, no SHACL, no reasoner needed.
- **Cross-organisation interchange / publishing** → RDF (Turtle) with `takt:` +
  `top:`. This is the "herstellerneutraler Datenaustausch" the BIMTakt authors call
  for.

**Key point.** You are **not** shifting away from IFC's process model — you keep it
as the semantic anchor (every term `closeMatch`es its IFC counterpart). You only
choose whether the **.ifc file** is your transport format. Format ≠ semantics. A
converter (driven by the `closeMatch` mappings) bridges to IFC-native tools when
needed.
