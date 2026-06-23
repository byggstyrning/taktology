# tommelein-2022-wdm

- **Title:** Work Density Method for Takt Planning of Construction Processes with Nonrepetitive Work
- **Authors / Year:** Tommelein, I. D. — 2022
- **Venue:** Journal of Construction Engineering and Management (ASCE), 148(12), 04022134 · DOI [10.1061/(ASCE)CO.1943-7862.0002398](https://doi.org/10.1061/(ASCE)CO.1943-7862.0002398) · OA [eScholarship](https://escholarship.org/content/qt7tk8182k/qt7tk8182k.pdf)
- **Status:** adopted · **Cluster:** takt-foundations · **Verified:** ✔ (article no. 04022134 confirmed)

## Summary
Peer-reviewed formalization of the Work Density Method (WDM): planners achieve
one-piece workflow by dividing space into zones, assigning each zone exclusively to
one trade for a fixed takt, and using *work density* (work content per unit area) to
balance loads across zones — generalizing takt to non-repetitive work.

## Key takeaways
- Work density is the quantitative primitive for sizing and locating takt zones.
- A zone is assigned to **one trade** for the takt — the operand of a takt task is a
  trade-specific subset of the zone's content, not the whole zone.
- Conference origin is `tommelein-2017-collaborative-nonrepetitive`; companion
  `singh-tommelein-2023-visual-workload-zoning` adds visual leveling.

## Distinct contribution
The rigorous, citable definition of work density and zone-balancing logic — the
method counterpart to BIMTakt's database-matched effort values.

## Overlap / what it is NOT
WDM is the takt answer to LBMS-style quantity/location takeoff; do not conflate with
LBMS flowline analysis (see `frandson-2015-lbms-vs-takt`).

## How it shapes taktology (intertwine)
Grounds the **`takt:actsOn` decision** (ADR-4 in
[`docs/03-decisions.md`](../../docs/03-decisions.md)): because a zone is assigned to
one trade per takt, duration must be computed from the trade-specific operand
(`actsOn`), not the zone total. Also underpins `productionRate`/`crewSize` on
`takt:WagonType` and the quantity→duration formula in `schema/`.
