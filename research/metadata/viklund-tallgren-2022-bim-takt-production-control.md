# viklund-tallgren-2022-bim-takt-production-control

- **Title:** Developing support for BIM-based takt time schedules for production control
- **Authors / Year:** Viklund Tallgren, M.; Johansson, M.; Roupé, M. (Chalmers); Ljung, E. (Skanska) — 2022
- **Venue:** CONVR 2022, Seoul, 723–730 · [533892](https://research.chalmers.se/publication/533892) · [PDF](https://research.chalmers.se/publication/533892/file/533892_Fulltext.pdf)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔

## Summary
Analyzes three construction cases to find obstacles to combining takt time planning
with BIM, concluding that integrating the two through a collaborative planning system
is viable and would create **direct links between takt schedules and model objects**.

## Key takeaways
- The value is the schedule↔model-object link (a takt task should point at the elements
  it builds) — exactly taktology's `actsOn`.
- Takt control (holding the rhythm) benefits from the model being live during execution.

## Distinct contribution
The group's most explicit "BIM + takt for production control" statement before the 2023
prerequisites paper — motivates the schedule-to-object binding concretely.

## Overlap / what it is NOT
Strong overlap with the 2023 CONVR seed (`ljung-2023-prerequisites-bim-takt`); this is
the earlier, control-focused companion. Not an ontology.

## How it shapes taktology (intertwine)
Direct practitioner-grounded support for the **operand link** (ADR-4, `takt:actsOn`)
and for keeping IFC's process model as the anchor (so schedules bind to model objects).
Reinforces the ingester plan ([`scripts/`](../../scripts/takt_production_ingester_plan.md)).
