# ADR-001 — Research grounding for the taktology vocabulary

- **Status:** accepted (2026-06-23)
- **Context method:** [research-grounded-agents](../../../.claude/skills/research-grounded-agents/) skill; corpus at [`research/`](../)

## Decision

The taktology design decisions recorded in
[`docs/03-decisions.md`](../../docs/03-decisions.md) are **grounded in the corpus**,
not in intuition. This ADR is the *intertwine* link: every `adopted`/`influenced`
source traces to a taktology choice, and every choice names its sources.

## Grounding map (decision → sources)

| taktology decision | grounded by |
|---|---|
| **Exists at all** — interoperable, manufacturer-neutral takt model | `becker-tschickardt-2023-bimtakt` (calls for *herstellerneutraler Datenaustausch*) |
| **ADR-1** — spatial layer on `top:`/TopologicPy (computed topology), BOT-aligned | `jabi-2018-topologic`, `topologicpy-ontology`, `rasmussen-2020-bot` |
| **ADR-2** — author the *process* layer, not a zone ontology; takt zone = one subclass | `dlouhy-2016-three-level` (zone is a programme construct), `rasmussen-2020-bot` (extend, don't refatten) |
| **ADR-3** — align to IFC by `skos:closeMatch`, never import ifcOWL | `pauwels-terkaj-2016-ifcowl` (ifcOWL is a ~14k-axiom full mirror), `bsi-ifc43-process-extension` (the closeMatch targets) |
| **ADR-4** — `actsOn` (operand) distinct from `performedIn` (location); duration from operand | `tommelein-2022-wdm` (zone→one trade per takt; work density), `bsi-ifc43-process-extension` (IFC overloads `IfcRelAssignsToProduct`) |
| **ADR-5** — property-graph; `IfcRel*` become edges | `bsi-ifc43-process-extension` (reified relations), `zhu-2025-ifc-graph` (IFC-as-LPG) |
| **ADR-6** — RDF vs property graph is a consumer choice; IFC stays the semantic anchor | `frandson-2015-lbms-vs-takt` (scope), `bsi-ifc43-process-extension`, `zhu-2025-ifc-graph` |
| **Vocabulary** (wagon/train/zone, takt vs control) | `haghsheno-2016-history`, `binninger-2017-technical-takt`, `dlouhy-2016-three-level`, `frandson-2013-cladding` |
| **Two-flows rationale** ("two halves, one graph"; train Readings A/B) | `lehtovaara-2021-flow-cme` (location flow vs trade flow) |
| **Generation loop / quantity→duration** | `frandson-2014-crc-takt-plan-development` (six-step method), `tommelein-2022-wdm`, `jabbari-2020-wolzo` |

## Open decision (surfaced by the corpus — not yet resolved)

**Reuse-vs-mint for the process layer.** INDEX gap #1: a takt-specific ontology does
not exist, but two general construction-process ontologies do —
`schlenger-2024-process-representation` (minimal schedule ontology, schedule↔IFC
linking) and `dtc-ontology-spec` (DTC, imports BOT).

> **RESOLVED 2026-06-23 → REUSE DTC.** `takt.ttl` v0.3.0 specializes DTC
> (`TaktTask ⊑ dtc:WorkPackage`, `TaktZone ⊑ dtc:AsPlannedWorkingZone`,
> `Crew ⊑ dtc:AsPlannedWorkerCrew`, `performedIn ⊑ dtc:isPerformedIn`,
> `actsOn ⊑ dtc:hasTarget`) by *reference*, not `owl:imports`. DTC's published TTL was
> read and found a near-exact fit. Schlenger 2024 builds **on** DTC, so this aligns to
> it too — but Schlenger's own ontology terms were **not** extracted (its PDF was not
> machine-readable with the tools available), so a finer Schlenger-specific mapping is
> deferred. See [`docs/03-decisions.md`](../../docs/03-decisions.md) **ADR-7**.
> *Still open:* confirm DTC **version** (a v2 exists) before pinning.

## Consequences / known evidence gaps

These taktology elements are currently designed with **thin or no prior art** (see
[INDEX.md](../INDEX.md) gaps) — treat as build risks, not settled:
- **Geometry/topology-driven takt zoning** — no canonical source; `jabbari-2020-wolzo`
  works on a work-density abstraction, not geometry (gap #2).
- **Wagon/train formal vocabulary** — our synthesis; no single source (gap #3).
- **Takt genealogy root** (Bulhões 2005) and **LOB origin** (Lumsden 1968) unverified
  (gap #4) — hedge genealogy claims.

## Notes

Do not edit this ADR in place once superseded — add ADR-002, etc. Re-run discovery for
`candidate` sources and to close the open decision above.
