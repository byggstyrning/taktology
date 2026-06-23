# ljung-2023-prerequisites-bim-takt

- **Title:** Identifying and Developing Prerequisites for Takt Planning in a BIM-Based Construction Process
- **Authors / Year:** Ljung, E. (Skanska); Viklund Tallgren, M.; Roupé, M.; Johansson, M. (Chalmers) — 2023
- **Venue:** CONVR 2023, Florence · DOI [10.36253/979-12-215-0289-3.56](https://doi.org/10.36253/979-12-215-0289-3.56) · [PDF](https://research.chalmers.se/publication/538637/file/538637_Fulltext.pdf)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔ (user-supplied seed)

## Summary
A three-stage study (conceptual focus groups → design workshops → site-staff
evaluation) on how BIM and takt planning integrate to improve coordination. Finds that
a **shared denominator / breakdown** is what lets takt planning span construction phases
holistically.

## Key takeaways
- Takt + BIM integration is gated by *prerequisites* — chiefly a shared breakdown (WBS)
  linking model objects to schedule.
- Validated bottom-up with practitioners (Skanska site staff), not just conceptually.

## Distinct contribution
An empirically-grounded list of what must be in place for BIM-driven takt — the
practitioner counterpart to the BIMTakt automation concept.

## Overlap / what it is NOT
Companion to `viklund-tallgren-2022-bim-takt-production-control` (the earlier,
control-focused paper) and to the TBS licentiate. Prerequisites, not a method/tool.

## How it shapes taktology (intertwine)
Substantiates that a BIM-linked takt schedule needs a shared object↔schedule breakdown —
which taktology provides via `actsOn`/`performedIn` (task↔element/zone) and the
`WagonType`/`TaktTask` type-occurrence split. Reinforces ADR-4 (operand link) and the
ingester plan's element-classification step.
