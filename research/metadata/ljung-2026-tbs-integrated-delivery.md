# ljung-2026-tbs-integrated-delivery

- **Title:** Structuring Construction Projects for Integrated Delivery
- **Authors / Year:** Ljung, E. (Chalmers / Skanska) — 2026
- **Venue:** Licentiate thesis, Chalmers University of Technology · [551855](https://research.chalmers.se/publication/551855) · [PDF](https://research.chalmers.se/publication/551855/file/551855_Fulltext.pdf)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔ (user-supplied seed)

## Summary
Argues the core problem in construction fragmentation is **how information is
structured**, not technology. Proposes a **Spatio-Temporal Breakdown Structure (TBS)**
that unifies the spatial and temporal dimensions to align design, production planning,
and organizational responsibility — tested across two projects with Design Science
Research, surfacing hidden interdependencies and showing existing structures don't
support flow-oriented (takt) production.

## Key takeaways
- The TBS = space × time as one breakdown — the same product the takt grid is (zones ×
  takts). It generalizes WBS/LBS into a combined spatio-temporal partition.
- Flow/takt production needs the breakdown structure to carry *both* dimensions; siloed
  spatial or temporal structures hide interdependencies.
- Sits in a "Total BIM" context (model as single source of truth).

## Distinct contribution
The clearest articulation that the *structure* unifying space and time is the enabling
artifact for integrated, flow-oriented delivery — a research-level statement of exactly
what taktology encodes.

## Overlap / what it is NOT
A licentiate framing/argument, not an ontology or a tool. Overlaps with the same
author's CCC/ARCOM 2024 breakdown-structure papers (the TBS's component studies).

## How it shapes taktology (intertwine)
Direct conceptual backing for taktology's core: `takt:TaktZone` (spatial) ×
`takt:TaktTime` (temporal) bound on `takt:TaktTask` **is** a spatio-temporal breakdown.
Grounds [`docs/01-architecture.md`](../../docs/01-architecture.md) "two halves, one
graph" and supports the zone-time modelling decisions. Names a real, citable concept
(TBS) for what the corpus previously flagged as our own synthesis (INDEX gap #3).
