# jabi-2018-topologic

- **Title:** Topologic: A toolkit for spatial and topological modelling
- **Authors / Year:** Jabi, W.; Aish, R.; Lannon, S.; Chatzivasileiadi, A.; Wardhana, N. M. — 2018
- **Venue:** eCAADe 2018 (36th Conference), Łódź · DOI [10.52842/conf.ecaade.2018.2.449](https://doi.org/10.52842/conf.ecaade.2018.2.449) · OA [CumInCAD](https://papers.cumincad.org/data/works/att/ecaade2018_310.pdf)
- **Status:** adopted · **Cluster:** ifc-ontology-graph · **Verified:** ✔

## Summary
Presents Topologic, an open-source library applying non-manifold topology (NMT) to
represent buildings as a coherent hierarchy of cells/faces/edges/vertices, with
conversion to dual graphs — lightweight, connectivity-rich spatial models.

## Key takeaways
- Topologic/TopologicPy **computes** adjacency, containment and intersection from
  geometry — the capability BOT and IFC vocabularies lack.
- Buildings map to Cells/CellComplex; the dual graph is the analysis substrate.
- TopologicPy (the Python successor) ships an OWL ontology (`top:`,
  `topologicpy-ontology`) that already aligns to BOT and IFC.

## Distinct contribution
The geometry-to-graph engine. A **method/tooling** paper (how to compute spatial
graphs), complementary to the vocabulary papers.

## Overlap / what it is NOT
Not a scheduling or process tool — it has no task/sequence concept. It supplies the
spatial graph that takt sequencing runs *over*.

## How it shapes taktology (intertwine)
Citable foundation for **ADR-1** (use `top:`/TopologicPy for the computed spatial
layer) in [`docs/03-decisions.md`](../../docs/03-decisions.md). Directly relevant to
INDEX gap #2 (geometry/topology-driven takt zoning): TopologicPy is *the* tool to
attempt it, with no prior takt-specific art to lean on.
