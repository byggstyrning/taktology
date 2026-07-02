# topologicpy-ontology

- **Title:** TopologicPy ontology and documentation (top:)
- **Authors / Year:** Jabi, W. (TopologicPy project) — 2026
- **Venue:** Software documentation / OWL artifact · canonical IRI [w3id.org/topologicpy](http://w3id.org/topologicpy) · published [TTL](https://wassimj.github.io/topologicpy/ontology/topologicpy.ttl)
- **Status:** adopted · **Cluster:** ifc-ontology-graph · **Verified:** ✔ (re-verified FULL 2026-07-01 against the published TTL)

## Summary
The OWL/RDFS vocabulary TopologicPy emits — in its own words "a compact OWL/RDFS
vocabulary for TopologicPy topology, graph, IFC/BOT/Brick alignment, dictionary
metadata, and semantic edge predicates emitted by TopologicPy". Version **0.2.0**
(issued 2026-05-24, modified 2026-06-27), prefix `top:`, namespace
`http://w3id.org/topologicpy#` resolving via w3id. No peer-reviewed ontology paper
exists — cite this TTL plus the software docs (topologicpy.readthedocs.io); the
peer-reviewed foundation for the *engine* is `jabi-2018-topologic`.

## Key takeaways
- **Topology core:** `top:Topology` with subclasses `Vertex`, `Edge`, `Wire`,
  `Face`, `Shell`, … — the computed spatial substrate ADR-1 builds on. BOT and
  Brick terms are referenced for interoperability, not redefined.
- **Graph layer (v0.2.0):** `top:Graph` with ten subclasses —
  `top:KnowledgeGraph` ("A semantic graph or RDF-compatible knowledge graph
  representation") plus AdjacencyGraph, CirculationGraph, ConnectivityGraph,
  HasseDiagram, LineGraph, QuotientGraph, SpatialGraph, Tree, VisibilityGraph —
  and the record classes `top:Node` / `top:Relationship` with `top:hasPredicate`
  (domain `top:Relationship`, range `rdf:Property`).
- `top:Node`'s comment names the pairing directly: *"A graph node record.
  TopologicPy TGraph vertices may be projected as nodes."*
- **TGraph** is the library's new "topology-first graph class" (`TGraph.py`):
  vertices and edges are stable indexed records with dictionaries, geometry
  optional. It builds from models and data (`ByIFCFile`, `ByJSONFile`,
  `ByCSVPath`, …) and exports/reasons semantically (`ExportTTL`, `RDFGraph`,
  `InferOntology`, `Reason`, `KnowledgeGraph`/`ToKnowledgeGraph`).
- **In-code divergence to know:** the published v0.2.0 TTL declares **no
  `top:FunctionalZone`** and **no `top:area`/`top:volume`** datatype properties.
  The in-code vocabulary (`Ontology.py`) still carries them —
  `Ontology.TOP_SUPERCLASSES` keeps `top:FunctionalZone ⊑ top:Zone` and
  `Ontology.DATA_PROPERTIES` maps `area`/`volume` — so TGraph-emitted instance
  data may contain terms the published TTL never declares. The published TTL is
  normative for taktology's T-Box.

## Distinct contribution
The only vocabulary in the corpus that types both the *computed* spatial graph
and its knowledge-graph projection — the bridge from geometry to semantics.

## Overlap / what it is NOT
A software artifact versioned with the library, not a standardized or
peer-reviewed ontology — hence taktology pins it (version + sha256 in
[`ontology/alignments.lock.json`](../../ontology/alignments.lock.json)) instead
of trusting the artifact to stay stable. Don't confuse it with
`jabi-2018-topologic` (the engine paper) or with BOT (`rasmussen-2020-bot`,
which it aligns to but does not replace).

## How it shapes taktology (intertwine)
**ADR-15** in [`docs/03-decisions.md`](../../docs/03-decisions.md):
`takt:TaktGraph ⊑ top:KnowledgeGraph` — the takt plan is the graph a
TopologicPy TGraph-built model projects into; the pairing contract lives in
`docs/05-tgraph-pairing.md`. **ADR-13**: `takt:TaktZone` re-parents to
`bot:Zone` directly and `top:Zone` becomes a `skos:relatedMatch`. **ADR-1**
(spatial layer on `top:`/TopologicPy) continues to hold. Upstream pin:
`ontology/alignments.lock.json` (v0.2.0, modified 2026-06-27, sha256).
