# Design decisions (ADRs)

Condensed records of the choices made while developing this vocabulary. Each is a
fork the conversation actually walked, with the reasoning preserved.

---

## ADR-1 — Build the spatial layer on `top:`, not a hand-rolled BOT extension

> **Status: partially superseded by ADR-13 (v0.5.0).** The `top:` v0.1.0 facts this
> ADR relied on (`top:FunctionalZone`, `top:Zone ⊑ top:Cell`, `top:area`/`volume`,
> the old `wassimj.github.io` namespace) do not exist in the published `top:` v0.2.0
> (`http://w3id.org/topologicpy#`). The spatial parent moved to `bot:Zone` directly;
> TopologicPy remains the compute engine and the graph substrate (ADR-15).

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

---

## ADR-7 — Reuse the DTC ontology; ship a minimal core (v0.3.0)

> **Status: partially superseded.** The DTC *version* question this ADR left open is
> resolved by ADR-12 (v2 migration; `WorkPackage` → `AsPlannedProcess`); the "plan
> container stays out" consequence is superseded by ADR-15 (`takt:TaktGraph`).

**Decision.** Rebuild `takt.ttl` as a **minimal core** (5 classes, 6 object, 6
datatype = 17 terms) that **reuses the Digital Twin Construction (DTC) ontology** for
the process / working-zone / resource backbone, instead of minting a self-contained
vocabulary. Alignment is by *reference* (`rdfs:subClassOf`/`subPropertyOf`), **not**
`owl:imports` — consistent with ADR-3's "don't import the heavy thing."

**Why.** This resolves the open reuse-vs-mint question from
[`research/decisions/ADR-001`](../research/decisions/ADR-001-research-grounding.md)
(corpus gap #1: no takt ontology exists, but DTC and Schlenger's schedule ontology
do). Reading DTC's published TTL showed it already provides `WorkPackage`/`Activity`/
`Task`, `AsPlannedWorkingZone`, `AsPlannedWorkerCrew`, `isPerformedIn` and `hasTarget`
— a near-exact fit. Schlenger & Borrmann (2024), the schedule↔IFC linking method,
*builds on DTC*, so aligning to DTC aligns to that work too.

**What taktology still owns** (the residue DTC lacks): the wagon **type** layer
(`WagonType`, closeMatch `IfcTaskType`), the takt **rhythm** (`taktDuration`,
`TaktTime`), the **work-density** values (`productionRate`, `crewSize`,
`quantityUnit`; *later removed — see ADR-10*), and direct-edge **simplifications**
(`hasSuccessor`, `performedBy`) over DTC's reified precondition/assignment patterns.

**Consequences.**
- Dropped from v0.2.0: the `Train` class (the train is the `hasSuccessor` chain),
  `hasPredecessor`, `hasMember`, `crewCode`, `start`/`finish` (use `dtc:startTime`/
  `endTime`), `plan`. Net 24 → 17 terms.
- Every term carries `dcterms:source` → the grounding corpus source(s).
- DTC reifies sequencing/assignment; takt's direct edges relate by `seeAlso`, not
  `subPropertyOf` — a deliberate, documented divergence.
- The whole takt plan (`IfcWorkSchedule`) stays **out** of the minimal core; add it
  (or `dtc:ConstructionSchedule`) only if a plan-level container is needed.
- Open: verify the DTC **version** (a v2 exists) and extract Schlenger's specific
  terms (its PDF was not machine-readable here) before any finer Schlenger mapping.

---

## ADR-8 — The takt zone is a `bot:Zone` (via `top:FunctionalZone`) (v0.3.1)

> **Status: superseded by ADR-13 (v0.5.0).** `top:FunctionalZone` does not exist in
> the published `top:` v0.2.0; the goal of this ADR (BOT membership for adjacency/flow)
> stands and is now achieved by a direct `bot:Zone` parent.

**Decision.** Make `takt:TaktZone` subclass **both** `top:FunctionalZone` and
`dtc:AsPlannedWorkingZone`. Since `top:FunctionalZone ⊑ top:Zone ⊑ bot:Zone`, a takt
zone is now a `bot:Zone` — it lives in the BOT topology graph and carries
`bot:adjacentZone`, `bot:containsElement`, and TopologicPy-computed geometry — while
remaining a DTC planned working zone for the LBS/process semantics.

**Why.** Reading DTC's published TTL revealed that DTC's `WorkingZone` is a **standalone
class — NOT** a `bot:Zone`; it only relates to BOT via `dtc:isLocatedIn` (range
`bot:Zone`). So under v0.3.0 (`TaktZone ⊑ dtc:AsPlannedWorkingZone` only), takt zones sat
*outside* the BOT topology graph and had no adjacency. But takt planning is fundamentally
about **flow between adjacent work areas**, and BOT models exactly that
(`bot:adjacentZone`, `bot:intersectsZone` — the latter is also the right primitive for the
vertical shafts/stairwells BIMTakt flagged as hard). Grounded in `rasmussen-2020-bot`
(BOT's "subclass `bot:Zone`" extension pattern).

**Why via `top:FunctionalZone` (the chosen option B), not a direct `bot:Zone` parent
(option A).** `top:FunctionalZone` already *is* a `bot:Zone`, so subclassing it yields
BOT membership **and** the TopologicPy geometry/adjacency computation in one parent —
the engine that actually produces the zones and their `top:area`/adjacency. A direct
`bot:Zone` parent (option A) would also work and couple less to TopologicPy, but the
project already computes its spatial layer with TopologicPy, so option B is the natural
fit. DTC-faithful option C (BOT only via `isLocatedIn`) was rejected: it leaves takt
zones as non-topological, losing the adjacency takt needs.

**Consequences.**
- Multi-parent class: `takt:TaktZone ⊑ top:FunctionalZone, dtc:AsPlannedWorkingZone`.
  Logically clean — DTC never declares `WorkingZone` disjoint from `bot:Zone`.
- A-Box now uses `bot:containsElement` (was `top:containsElement`; the former is the
  BOT-standard super-property), `bot:adjacentZone` (new — the flow/handoff graph), and
  `dtc:isLocatedIn` to place the zone in its `bot:Storey`.
- Couples the zone's spatial identity to TopologicPy (`top:`). Acceptable: TopologicPy
  is the project's compute engine. If that coupling is ever unwanted, switch to a direct
  `bot:Zone` parent (option A) — a one-line change.
- A mild divergence from DTC's intent (it deliberately separates working zone from
  topology zone); justified for takt because adjacency/flow is the point.

---

## ADR-9 — Add the process layer: a takt task is `partOfProcess` a `dtc:Process` (v0.4.0)

**Decision.** Add one object property `takt:partOfProcess` (domain `TaktTask`, range
`dtc:Process`). Reuse DTC's process backbone by *reference* — do **not** mint a takt
process class, and keep the train as the `hasSuccessor` path (not a class).

**Why.** Ljung (2026)'s **Spatio-Temporal Breakdown Structure (TBS)** frames a takt task
as one cell of a space × time × responsibility breakdown. The task already carried
**space** (`performedIn` → `TaktZone`) and **time** (`hasTaktTime` → `TaktTime`);
`partOfProcess` makes the missing **process / responsibility** membership explicit. This
closes gap #1 in [`research/decisions/ADR-001`](../research/decisions/ADR-001-research-grounding.md)
(reuse-vs-mint for the process layer). Aligned to IFC by `skos:closeMatch ifc:IfcRelNests`
(task-in-process nesting); `rdfs:seeAlso` Schlenger & Borrmann (2024).

**Consequences.**
- 17 → 18 terms. `dtc:Process` is referenced, not imported (consistent with ADR-3/ADR-7).
- The diagram renders `dtc:Process` as a reused-external node above `TaktTask`.
- A tighter `rdfs:subPropertyOf dtc:<…>` is deferred until the exact DTC property is
  verified against the published TTL; `closeMatch`-only ships now (as `instantiates` /
  `hasTaktTime` already do).

---

## ADR-10 — Drop the work-density / quantity-takeoff layer (v0.4.1)

**Decision.** Remove `takt:productionRate`, `takt:crewSize` and `takt:quantityUnit`. The
vocabulary models the **structural** takt backbone — task, process, zone, element
containment, operand, rhythm — not quantity take-off or duration computation.

**Why.** The duration model (`qty(actsOn) × productionRate ÷ crewSize`, must fit within
`taktDuration`) is a **downstream consumer concern**, not part of a minimal interchange
vocabulary. A consumer that wants Work-Density durations supplies the rate/crew from its
own reference DB and reads `top:area` off the elements — the structural graph is what it
needs from `takt:`, and that graph is complete without the numbers. Carrying a half-formula
in the core (a rate, but no labour calendar or productivity model) was scope the vocabulary
shouldn't own. Supersedes the "work-density values" residue claimed in ADR-7.

**Consequences.**
- 18 → 15 terms (5 classes, 7 object, **3** datatype). `WagonType` keeps only its identity
  (`rdfs:label`, `closeMatch IfcTaskType`); the surviving datatypes are the rhythm
  (`taktDuration`, `slot`) and the `isMilestone` flag.
- Element geometry (`top:area`) stays — it is TopologicPy's, not a `takt:` term, so the
  "element + geometry" topology pillar is unaffected.
- The A-Box drops the rate/crew triples and the end-to-end duration narrative; the diagram's
  datatype footer drops the `WagonType` group automatically (it is data-driven).

---

## ADR-11 — Elements are zone-scoped; split an element that spans zones

**Decision.** A `top:Element` instance belongs to **one** takt zone; its `top:area` is the
per-zone quantity. A physical element that spans several zones is **split** into one
instance per zone (as the A-Box does: `ex:gipsvagg_B5_1` is the wall *set in B5:1*).

**Why.** One element worked by many trades is a **fan-in** — multiple `actsOn` edges into a
single element node — which the graph handles natively, with no quantity term and no new
class (the element is defined once, referenced by every task that touches it). The only
ambiguity is an element that crosses a zone boundary, where `top:area` would otherwise be
the whole thing and `containsElement` would become many-to-many. Zone-scoping keeps
`containsElement` and `actsOn` cleanly many-to-one, matching how takt zoning already
partitions space.

**Consequence.** A modeling **convention**, not an ontology change. If per-task *partial*
operands are ever needed (a task acting on only part of an element), that is a separate
decision — deliberately **not** taken here, to keep the core structural (see ADR-10).

---

## ADR-12 — Migrate the DTC alignment to **DTC v2** (v0.5.0)

**Decision.** Re-point the `dtc:` prefix from v1 (`…/ontology#`) to **v2**
(`https://dtc-ontology.cms.ed.tum.de/ontology/v2#`) and re-parent accordingly:
`takt:TaktTask ⊑ dtc:AsPlannedProcess` (v1's `WorkPackage` is gone in v2),
`takt:Crew ⊑ dtc:AsPlannedWorkerCrew`, `takt:TaktZone ⊑ dtc:AsPlannedWorkingZone`
(both survive), `takt:performedIn ⊑ dtc:isPerformedIn`, `takt:actsOn ⊑ dtc:hasTarget`.

**Why.** The v0.4.x file was de-facto pinned to v1 without saying so — and v1's shape
actively hurt: `dtc:hasTarget` (v1 domain `Action ∪ Task`) clashed with
`TaktTask ⊑ WorkPackage`, mis-tiering every acting task. Reading the published v2 TTL
(modified 2024-07-31) showed v2 **dissolves** these problems and is a strictly better
substrate for takt:

- `hasTarget` and `isPerformedIn` take **domain `Process`** — level-correct for a takt
  task once `TaktTask ⊑ AsPlannedProcess`; `hasTarget`'s range is **`bot:Element`**.
- v2 **imports BOT 0.3.2** (and GeoSPARQL + the BuildingElement ontology), so `dtc:`
  and `bot:` now compose *by design*, and `dtc:alignsWithZone` (WorkingZone → `bot:Zone`)
  exists as the conformant zone-link (see ADR-13).
- The **as-planned / as-performed split** (`AsPlannedProcess` / `AsPerformedProcess`,
  disjoint resources) is the natural seam for takt **control** later — plan cells stay
  as-planned; observations go on the as-performed side. v2's comments confirm
  `dtc:startTime`/`endTime` are **as-performed observations** — which the v0.4.x A-Box
  misused for planned dates (fixed by ADR-14's derivation rule).
- `dtc:ConstructionSchedule` + `dtc:hasProcess` model the plan container (used by ADR-15).

**Consequences.**
- Breaking change for v0.4.x consumers (namespace + parents); v1 correspondences are
  noted in term comments where names differ (`WorkPackage` → `AsPlannedProcess`).
- v1's `dtc:isLocatedIn` (used by the old A-Box for storey placement) is gone in v2;
  the examples now use BOT-native `bot:containsZone` (storey → zone).
- The v2 snapshot this was verified against is pinned in `ontology/alignments.lock.json`.

---

## ADR-13 — TaktZone re-parents to **`bot:Zone` directly**; `top:Zone` becomes a `skos:relatedMatch` (v0.5.0)

**Decision.** `takt:TaktZone ⊑ bot:Zone + dtc:AsPlannedWorkingZone` (ADR-8's option A).
The TopologicPy link becomes `skos:relatedMatch top:Zone` — instances computed by
TopologicPy *may* additionally be typed `top:Zone`, but the class no longer commits
every takt zone to being a TopologicPy topology.

**Why.** ADR-8 chose `top:FunctionalZone` as the parent, but the published `top:` v0.2.0
(`http://w3id.org/topologicpy#`, modified 2026-06-27) has **no `FunctionalZone`** — the
axiom pointed at a ghost class under a stale namespace, so the BOT membership ADR-8
existed to deliver never actually held. The live `top:Zone` is
`⊑ top:Topology, bot:Zone`: subclassing it would entail every takt zone is a
*TopologicPy topological entity*, which is engine coupling the vocabulary shouldn't
carry (zones drawn by hand in a takt workshop are still takt zones). A direct
`bot:Zone` parent delivers the adjacency/containment/nesting semantics with no
engine commitment — exactly the "one-line change" ADR-8 pre-authorized.

**The tension this keeps (explicit, on purpose).** DTC deliberately separates the
working zone from the topological zone (`dtc:alignsWithZone`: WorkingZone → `bot:Zone`).
Takt collapses them: in takt planning **space is the resource**, so the planned work
area is *delineated as* a spatial zone. No disjointness axiom in DTC v2 or BOT blocks
the dual parent (checked; v2's only disjointness is AsPerformed ⊥ AsPlanned Resource).
Consumers needing DTC's separation can keep a working-zone individual and
`dtc:alignsWithZone` it to the spatial zone — the vocabulary doesn't forbid the
conformant pattern, it just doesn't require the indirection.

**Consequences.** Zone nesting for the three-level method (macro/norm/micro) comes
free via `bot:containsZone` — no takt-minted level machinery. `top:area`/`top:volume`
references disappear from docs/examples (they don't exist in `top:` v0.2.0; quantities
travel per ADR-15's pairing contract).

---

## ADR-14 — Dissolve `TaktTime`; the rhythm lives on the plan, dates **derive** (v0.5.0)

**Decision.** Remove `takt:TaktTime` and `takt:hasTaktTime`. `takt:slot` moves onto
`takt:TaktTask`; `takt:taktDuration` loses its fixed domain (assert once on the
`takt:TaktGraph` for the plan-wide beat, or per task where trains genuinely differ);
new `takt:planStart` (domain `TaktGraph`, `xsd:date`) anchors the grid on the calendar.
Planned task dates are **derived**, not asserted:
`start(task) = planStart + (slot − 1) × taktDuration`.

**Why.** The reified time payload earned nothing: it held two literals, cost every
query a hop, and actively broke DTC composition — the A-Box put `dtc:startTime`/
`endTime` on the TaktTime node, violating DTC's domain (`Process ∪ Resource…`) *and*
its semantics (both are **as-performed observations** in both DTC versions — wrong for
planned dates everywhere, not just on the wrong node). Deriving planned dates from
`planStart × slot × taktDuration` is exactly how a takt grid works — the fixed rhythm
IS the calendar model (Binninger 2017) — and it removes the temptation to re-misuse
DTC's observation properties. As-performed control data belongs on DTC's as-performed
side (`AsPerformedProcess` + `startTime`/`endTime`), outside the core (see ADR-16).
Also fixed here: `"P1W"^^xsd:duration` was an **invalid literal** (XSD durations have
no week designator) — the canonical beat is now written `P7D`.

**Consequences.** Net −2 terms from the dissolution; `IfcTaskTime`'s closeMatch
disappears with the class (the slot/duration comments keep the conceptual pointer).
Queries lose a join; the A-Boxes lose their misuse; v0.4.x data migrates by copying
`slot`/`taktDuration` off the TaktTime node onto the task/plan.

---

## ADR-15 — `takt:TaktGraph ⊑ top:KnowledgeGraph + dtc:ConstructionSchedule`; the TGraph pairing contract (v0.5.0)

**Decision.** Add one class for the plan itself: `takt:TaktGraph`, subclassing **both**
`top:KnowledgeGraph` (the semantic graph a TopologicPy **TGraph** emits/consumes) and
`dtc:ConstructionSchedule` (so plan membership is `dtc:hasProcess`, reused not minted).
`skos:closeMatch ifc:IfcWorkSchedule`. Alongside it, document the **pairing contract**
with TopologicPy's new TGraph class (`docs/05-tgraph-pairing.md`):

- **Instance projection:** takt individuals ride TGraph vertex/edge dictionaries —
  `ontology_class` (QName, e.g. `takt:TaktTask`), `uri`, `label`, and edge
  `ontology_predicate` (e.g. `takt:hasSuccessorSameZone`).
- **Namespace registration:** TopologicPy has no public prefix-registration API; the
  supported pattern is documented (register `takt:`/`dtc:` in `Ontology.NAMESPACES`
  before export, or post-process the emitted Turtle).
- **Export gap:** TGraph's shipped TTL export drops edge `ontology_predicate`
  semantics on some paths — the pairing doc's exporter appends the predicate triples.
- **Reasoning recipe:** merge `takt.ttl` into the emitted graph **before**
  `InferOntology` (TGraph's `includeOntologyAxioms` only injects TopologicPy's own
  axioms); then `TaktZone → bot:Zone` etc. entail.
- **Quantities:** the published `top:` v0.2.0 declares **no** `top:area`/`top:volume`;
  areas/volumes travel as TGraph dictionary values (keys `area`/`volume`) or as
  `top:Quantity` records from IFC quantity sets. Treat emitted quantity triples as
  engine-specific until TopologicPy publishes the terms (upstream divergence tracked
  in `alignments.lock.json`).

**Why.** This supersedes ADR-7's "the plan container stays out" — the TGraph pairing
gave the container a concrete job: a TGraph-built takt plan needs something to *be*
in RDF, and `top:KnowledgeGraph` is the published hook TopologicPy itself provides
("TopologicPy TGraph vertices may be projected as nodes" — `top:Node`'s own comment).
The DTC parent answers the plan-membership competency question with an existing
property. The plan-level `taktDuration`/`planStart` (ADR-14) need a home; the plan is it.

**Consequences.** ADR-5's stale `top:` graph-class names (`top:DirectedRelationship`,
`top:Path`) are corrected by reference: the live v0.2.0 layer is `top:Graph` (+
`AdjacencyGraph`… subclasses), `top:KnowledgeGraph`, `top:Node`, `top:Relationship`,
`top:hasPredicate`. A worked end-to-end script lives at `examples/tgraph_pairing_demo.py`.

---

## ADR-16 — Reading A/B become subproperties; buffers and trade enter the core; takt **control** stays out (v0.5.0)

**Decision.** Three additions, one recorded exclusion:

1. **`takt:hasSuccessorSameZone`** (Reading A — location flow: the cross-trade convoy
   through one zone) and **`takt:hasSuccessorSameWagon`** (Reading B — trade flow: one
   wagon across zones), both `⊑ takt:hasSuccessor`. One dataset can now carry both
   flows, machine-distinguishably; the generic property stays for readers that don't care.
2. **`takt:isBuffer`** (boolean, TaktTask): capacity-buffer cells — the concept the
   corpus itself says *differentiates* takt from LBMS (capacity buffers, not time
   buffers; Frandson 2015) — were inexpressible in v0.4.x. A buffer is an empty wagon
   slot: a TaktTask with `isBuffer true` and typically no `instantiates`.
3. **`takt:trade`** (string, WagonType): the trade/discipline key that operand
   classification and trade-flow queries join on. A plain literal — owning a trade
   taxonomy is out of scope.
4. **Exclusion (recorded, was silent):** takt **control/steering** — progress
   observations, status boards, re-planning — is a corpus-primary theme and stays OUT
   of the core. The seam is DTC v2's as-performed side (`AsPerformedProcess`,
   `startTime`/`endTime`, `hasStatusType`); a future `takt-control` module can
   specialize it without touching this vocabulary.

**Why.** The Reading A/B ambiguity was an *undetectable* data-corruption risk: one
property encoded two incompatible graph shapes, and no query could tell which it got.
The v0.4.x README flagged it as an open item; subproperties resolve it without
breaking the generic chain. Buffers and trade close the two domain gaps the
research-grounding audit ranked takt-defining; both ground in already-adopted corpus
sources. `isMilestone`/`isBuffer` on TaktTask are a *documented* rigidity pragmatism:
every cell of the grid stays one TaktTask (mirroring `IfcTask.IsMilestone`) rather
than growing a cell-role class hierarchy.

**Consequences.** v0.5.0 nets 15 → 19 terms (5 classes, 8 object, 6 datatype) — still
minimal, every addition closing a verified finding with corpus grounding. SHACL shapes
(`shapes/takt-shapes.ttl`) encode the conventions (buffers don't instantiate; slots
are ≥ 1; same-zone successors share a zone; same-wagon successors share a wagon type).
