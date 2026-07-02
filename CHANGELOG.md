# Changelog

All notable changes to the taktology vocabulary (`ontology/takt.ttl`) are
documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/);
versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

**Version-bump policy (effective from 0.5.0, forward-looking).** While pre-1.0:

- **MINOR** — any semantics-affecting change: term additions, removals, renames,
  domain/range changes, alignment retargets (parent class/property or upstream
  namespace changes).
- **PATCH** — annotations, documentation, examples and diagram-only changes.
- **MAJOR** — reserved for the 1.0.0 stabilization.

Every bump updates `owl:versionInfo`, `owl:versionIRI` and `owl:priorVersion`
**together** (see the release checklist in [docs/07-publishing.md](docs/07-publishing.md)).
Entries below 0.5.0 are reconstructed from git history and the ADRs in
[docs/03-decisions.md](docs/03-decisions.md); they predate this policy and did
not follow it (0.3.1 retargeted an alignment as a patch; 0.4.1 removed terms as
a patch). Versions before 0.2.0 predate this repository and are not tracked.

## [0.5.0] — 2026-07-01

The consumability release: alignments verified against pinned upstream
snapshots, invalid patterns purged, the plan container added. **Three breaking
changes** — see the migration guide below. 15 → 19 terms
(5 classes, 8 object properties, 6 datatype properties). ADR-12…ADR-16.

### Added

- **`takt:TaktGraph`** — the takt plan itself, subclassing `top:KnowledgeGraph`
  (what a TopologicPy TGraph-built plan projects into) **and**
  `dtc:ConstructionSchedule` (plan membership via the reused `dtc:hasProcess`,
  not a minted property). Supersedes ADR-7's "plan container stays out". (ADR-15)
- **`takt:planStart`** (`xsd:date`, domain `TaktGraph`) — the calendar anchor.
  Planned task dates now **derive**: `start(task) = planStart + (slot − 1) × taktDuration`. (ADR-14)
- **`takt:hasSuccessorSameZone`** (Reading A — location flow: the cross-trade
  convoy through one zone) and **`takt:hasSuccessorSameWagon`** (Reading B —
  trade flow: one wagon across zones), both `⊑ takt:hasSuccessor`, making the
  two flow directions machine-distinguishable. (ADR-16)
- **`takt:isBuffer`** (`xsd:boolean`, `TaktTask`) — capacity-buffer cells, the
  concept that differentiates takt from LBMS planning. (ADR-16)
- **`takt:trade`** (`xsd:string`, `WagonType`) — the trade/discipline join key. (ADR-16)
- Ontology header publishing metadata: `owl:versionIRI`, `owl:priorVersion`,
  `dcterms:created`/`modified`/`creator`, `vann:preferredNamespacePrefix`/`Uri`.
- `ontology/alignments.lock.json` — pinned upstream snapshots (DTC v2,
  `top:` v0.2.0, ifcOWL IFC4 ADD2_TC1) the alignments were verified against.
- `contexts/takt.context.jsonld` — JSON-LD context for JSON/property-graph
  consumers (all 19 terms, with `@id`/datatype coercions).
- `examples/takt-train-demo.ttl` — the train across two zones: both successor
  readings on one plan, plus a capacity buffer.
- `CHANGELOG.md` (this file) and `docs/07-publishing.md` (namespace publishing
  plan, w3id payload under `w3id/`).

### Changed

- **BREAKING:** the `dtc:` alignment migrated to **DTC v2** — prefix re-pointed
  from `https://dtc-ontology.cms.ed.tum.de/ontology#` to
  `https://dtc-ontology.cms.ed.tum.de/ontology/v2#`, and terms re-parented:
  `takt:TaktTask ⊑ dtc:AsPlannedProcess` (v1's `WorkPackage` is gone in v2),
  `takt:performedIn ⊑ dtc:isPerformedIn`, `takt:actsOn ⊑ dtc:hasTarget`
  (both now level-correct: v2 gives them domain `Process`). (ADR-12)
- **BREAKING:** the `top:` alignment fixed to the published TopologicPy
  ontology v0.2.0 — namespace corrected to `http://w3id.org/topologicpy#`
  (the old `wassimj.github.io` URI is stale), and `takt:TaktZone` re-parented
  from the nonexistent `top:FunctionalZone` to **`bot:Zone` directly** +
  `dtc:AsPlannedWorkingZone`; `top:Zone` is now a `skos:relatedMatch`
  (no engine coupling). (ADR-13)
- `takt:slot` moved onto `takt:TaktTask` (was on the dissolved `TaktTime`);
  `takt:taktDuration` lost its fixed domain — assert it once on the
  `takt:TaktGraph` for the plan-wide beat, or per task where trains genuinely
  run different rhythms. (ADR-14)
- Examples: storey placement now uses BOT-native `bot:containsZone`
  (v1's `dtc:isLocatedIn` does not exist in DTC v2).

### Removed

- **BREAKING:** `takt:TaktTime` and `takt:hasTaktTime` — the reified time node
  earned nothing and invited misuse of DTC's observation properties. The rhythm
  lives on the plan; dates derive. (ADR-14)
- `dtc:startTime`/`dtc:endTime` from all examples — they are **as-performed
  observations** in DTC (both versions), never planned dates. As-performed
  control data belongs on DTC's as-performed side, outside this core. (ADR-14/16)

### Fixed

- Invalid duration literal `"P1W"^^xsd:duration` — XSD durations have no week
  designator; the canonical beat is `P7D`. (ADR-14)
- Ghost upstream references: `top:FunctionalZone`, `top:area`/`top:volume` do
  not exist in the published `top:` v0.2.0 and are gone from ontology, docs and
  examples (quantities travel per the TGraph pairing contract, ADR-15).
- The de-facto (undeclared) DTC v1 pin — upstream versions are now explicit in
  `ontology/alignments.lock.json`.

### Migration guide: v0.4.1 data → 0.5.0

1. **Re-prefix** — `dtc:` → `https://dtc-ontology.cms.ed.tum.de/ontology/v2#`;
   `top:` → `http://w3id.org/topologicpy#`.
2. **Dissolve TaktTime nodes** — copy `takt:slot` off the `TaktTime` node onto
   its `takt:TaktTask`; copy `takt:taktDuration` onto the plan (create a
   `takt:TaktGraph` if you have none and link the tasks with `dtc:hasProcess`);
   delete the `TaktTime` individuals and all `takt:hasTaktTime` edges.
3. **Drop planned dates** — remove `dtc:startTime`/`dtc:endTime` from planned
   tasks; assert `takt:planStart` once on the plan and *derive* task dates from
   `planStart + (slot − 1) × taktDuration`.
4. **Fix durations** — replace `"P1W"` with `"P7D"` (and any `PnW` with `P(7n)D`).
5. **Storey placement** (if used) — replace `dtc:isLocatedIn` with
   `bot:containsZone` (storey → zone; note the inverted direction).

## [0.4.1] — 2026-06-23

### Removed

- The work-density / quantity-takeoff layer: `takt:productionRate`,
  `takt:crewSize`, `takt:quantityUnit`. Duration computation is a downstream
  consumer concern; the vocabulary models the structural takt backbone.
  18 → 15 terms. (ADR-10)

## [0.4.0] — 2026-06-23

### Added

- `takt:partOfProcess` (`TaktTask` → `dtc:Process`) — the process/responsibility
  axis of the space × time × process breakdown (Ljung 2026 TBS).
  17 → 18 terms. (ADR-9)

## [0.3.1] — 2026-06-23

### Changed

- `takt:TaktZone` re-parented to subclass `top:FunctionalZone` (hence, via
  `top:Zone`, a `bot:Zone`) alongside its DTC working-zone parent, giving takt
  zones BOT adjacency/containment. (ADR-8; superseded by ADR-13 in 0.5.0 —
  `top:FunctionalZone` turned out not to exist in the published `top:` v0.2.0.)
- A-Box switched to `bot:containsElement` and `bot:adjacentZone`.

## [0.3.0] — 2026-06-23

### Changed

- Rewritten as a **minimal core reusing the DTC ontology** for the
  process/zone/resource backbone — alignment by reference
  (`rdfs:subClassOf`/`subPropertyOf`), no `owl:imports`. Every term carries
  `dcterms:source` into the research corpus. 24 → 17 terms. (ADR-7)

### Removed

- The `Train` class (the train is the `hasSuccessor` chain, a path, not a
  class), `hasPredecessor`, `hasMember`, `crewCode`, `start`/`finish`, `plan`. (ADR-7)

## [0.2.0] — 2026-06-23

### Added

- Initial published version: self-contained takt vocabulary (24 terms,
  including the `Train` class), IFC alignment sketch, research corpus.
  Pre-0.2.0 iterations predate this repository and are not tracked.
