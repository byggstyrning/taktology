# ljung-2023-prerequisites-bim-takt

- **Title:** Identifying and Developing Prerequisites for Takt Planning in a BIM-Based Construction Process
- **Authors / Year:** Ljung, E. (lead, Skanska); Viklund Tallgren, M.; Roupé, M.; Johansson, M. (Chalmers) — 2023
- **Venue:** CONVR 2023, Florence (pp. 574–584, Firenze University Press) · DOI [10.36253/979-12-215-0289-3.56](https://doi.org/10.36253/979-12-215-0289-3.56) · [PDF](https://research.chalmers.se/publication/538637/file/538637_Fulltext.pdf)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔ (full text read; user-supplied seed; Paper II of the TBS licentiate)

## Summary
Ljung's lead-authored study (he led the empirical work on the **Hovås Tak** project) on
what must be in place to run takt planning on a BIM-based process. Identifies the gap
directly: *"there is a lack of real-world studies exploring BIM and takt planning where
information is structured according to takt planning."* The headline claim: *"A takt
planning structure for all BIM-models would bring a more holistic understanding of what is
to be done, controlled, and reported back."*

## Key takeaways (grounded in the full text)
- **A shared denominator is the prerequisite.** Findings highlight *"the importance of a
  shared denominator to get a holistic approach to project management and enabling takt
  planning throughout all phases."*
- **Three-stage method:** (1) a focus group of disciplines derives a shared structure in a
  lab/conceptual setting; (2) implement it on detailed design info for a real case
  (workshops); (3) evaluate with site staff. Keywords: **WBS**, BIM, project management.
- **The WBS gap:** cites that *"a standardized WBS structure is missing"* (Makarfi Ibrahim
  2009) and argues for a shared classification structure carrying flow from design →
  production → O&M; proposes adding **deliverables and construction scope** to classification
  to aid cross-discipline/phase communication.

## Distinct contribution
Practitioner-grounded prerequisites for BIM-driven takt — the empirical, bottom-up
counterpart to BIMTakt's automation *concept*. Validated with Skanska site staff, not just
conceptually.

## Overlap / what it is NOT
Companion to `viklund-tallgren-2022-bim-takt-production-control` (Paper I, the earlier
control-focused study) and a component of the TBS licentiate
(`ljung-2026-tbs-integrated-delivery`). Prerequisites, not a method/tool.

## How it shapes taktology (intertwine)
Substantiates that a BIM-linked takt schedule needs a **shared object↔schedule structure** —
exactly what taktology provides via `actsOn`/`performedIn` (task↔element/zone),
`partOfProcess` (task↔process), and the `WagonType`/`TaktTask` type-occurrence split. The
"takt structure for *all* BIM-models" framing supports the single-graph stance (ADR-6) and
the ingester plan's element-classification step.
