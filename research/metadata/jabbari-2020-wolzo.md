# jabbari-2020-wolzo

- **Title:** Workload leveling based on work space zoning for takt planning
- **Authors / Year:** Jabbari, A.; Tommelein, I. D.; Kaminsky, P. M. — 2020
- **Venue:** Automation in Construction, 118, 103223 · DOI [10.1016/j.autcon.2020.103223](https://doi.org/10.1016/j.autcon.2020.103223) · OA [NSF PAR](https://par.nsf.gov/servlets/purl/10300949)
- **Status:** adopted · **Cluster:** takt-bim-automation · **Verified:** ✔

## Summary
Formalizes the Work-space-Zoning (WoLZo) problem and gives a mathematical-
optimization algorithm that partitions a work space into zones while leveling work
densities across trades, minimizing the peak per-zone workload. Finds the marginal
benefit of adding zones flattens out due to the spatial distribution of work density.

## Key takeaways
- Takt-zone identification can be posed as a formal optimization, not just expert
  judgment — relevant to *automated* zone generation.
- Operates over a **work-density representation**, not raw BIM/IFC geometry.
- More zones ≠ monotonically better; there's a practical ceiling.

## Distinct contribution
The algorithmic, optimization-based route to deriving takt zones from work-density
data — the method neighbor to BIMTakt's geometry-driven zone identification.

## Overlap / what it is NOT
NOT geometry-driven zoning. Cite it for *zoning-as-optimization*, not for "derive
zones from the model's geometry" — that geometry path is a corpus **gap** (see
INDEX gap #2).

## How it shapes taktology (intertwine)
Informs the `applies(wagon, zone)` and zone-derivation thinking in
[`scripts/takt_production_ingester_plan.md`](../../scripts/takt_production_ingester_plan.md),
and substantiates that automated zoning is tractable. Boundary with the
geometry/topology gap is recorded in [INDEX.md](../INDEX.md) gap #2.
