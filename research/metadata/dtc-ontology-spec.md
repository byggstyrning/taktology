# dtc-ontology-spec

- **Title:** Digital Twin Construction (DTC) Ontology (specification)
- **Authors / Year:** Schlenger, J.; Yeung, T.; Bus, N.; Sacks, R.; Borrmann, A.; et al. — 2023 (v1) / 2024 (v2)
- **Venue:** TU München / BIM2TWIN (EU H2020) · spec [v2](https://dtc-ontology.cms.ed.tum.de/ontology/v2/) · [v2 TTL](https://dtc-ontology.cms.ed.tum.de/ontology/v2/ontology.ttl)
- **Status:** adopted · **Cluster:** ifc-ontology-graph · **Verified:** ✔ (v1 TTL read 2026-06-23; v2 TTL read 2026-07-01 — version caveat resolved)

## Summary
"An ontology focused on construction management during the execution phase for
digital twin use cases" (its own dcterms:description). Two published versions
with **different namespaces**: v1 at
`https://dtc-ontology.cms.ed.tum.de/ontology#` (modified 2023-11-00) and v2 at
`https://dtc-ontology.cms.ed.tum.de/ontology/v2#` (modified 2024-07-31). Both
import BOT 0.3.2, GeoSPARQL 1.1 and the BuildingElement ontology, so `dtc:` and
`bot:` compose by design.

## Key takeaways — v1 → v2 (verified by reading both TTLs)
- v2 **drops** `WorkPackage`, `Activity`, `Task`, `hasActivity` and
  `isLocatedIn` (zero occurrences in the v2 TTL; all declared in v1).
- The process backbone is **restructured**: a generic `Process` with subclasses
  `AsPlannedProcess` (*"As-planned process that is part of a construction
  schedule"*) and `AsPerformedProcess` — the plan-vs-observation split runs
  through the whole vocabulary (processes, resources, crews, zones).
- `hasTarget`: v1 domain `Action ∪ Task` → v2 domain `Process`, range
  `bot:Element` ("the construction element that results from its completion").
- `ConstructionSchedule` + `hasProcess` (domain `ConstructionSchedule`, range
  `Process`) model the plan container.
- v1's `isLocatedIn` (WorkingZone → `bot:Zone`) reappears as `alignsWithZone` —
  same comment text, new name.
- `startTime`/`endTime` are **as-performed observations** in both versions —
  v2: *"Starting time when a construction process actually started based on
  observations made on the construction site."* Never use them for planned
  dates.

## Distinct contribution
The only published construction-execution ontology in the corpus with an
explicit as-planned/as-performed split AND a BOT import — the process / zone /
resource backbone taktology reuses instead of minting its own.

## Overlap / what it is NOT
Not takt-specific: no rhythm, no occurrence-type layer (`dtc:Type` is an
enumeration base), no plan-grid concepts. Don't confuse the spec with
`schlenger-2024-process-representation` (the focused schedule-process ontology
built on it) or `schlenger-2025-dtc-reference-architecture` (the surrounding
architecture paper).

## How it shapes taktology (intertwine)
**taktology v0.5.0 aligns to v2** — [`docs/03-decisions.md`](../../docs/03-decisions.md)
**ADR-12**, superseding the v0.3.x–v0.4.x v1 alignment (ADR-7):
`TaktTask ⊑ dtc:AsPlannedProcess` (v1's `WorkPackage` parent is gone in v2),
`TaktZone ⊑ dtc:AsPlannedWorkingZone`, `Crew ⊑ dtc:AsPlannedWorkerCrew`,
`TaktGraph ⊑ dtc:ConstructionSchedule` with plan membership via
`dtc:hasProcess` (ADR-15), `performedIn ⊑ dtc:isPerformedIn`,
`actsOn ⊑ dtc:hasTarget`. The as-planned/as-performed seam is where takt
CONTROL would attach later — kept out of the v0.5.0 core (ADR-16). Upstream
pin: [`ontology/alignments.lock.json`](../../ontology/alignments.lock.json)
(v2, modified 2024-07-31, sha256).
