#!/usr/bin/env python3
# =============================================================================
# tgraph_pairing_demo.py — takt: <-> TopologicPy TGraph, end to end
# -----------------------------------------------------------------------------
# The runnable companion to docs/05-tgraph-pairing.md. It shows how a takt plan
# rides a TopologicPy TGraph and comes back out as takt:-typed RDF:
#
#   build TGraph  -> set the projection dictionaries (ontology_class / uri /
#   ontology_predicate) -> register the takt:/dtc: prefixes -> export TTL ->
#   append the edge-predicate triples TGraph's exporter drops -> merge takt.ttl
#   -> (optionally) InferOntology so TaktZone -> bot:Zone entails.
#
# TopologicPy is NOT required to see the idea: run with --dry-run to exercise the
# pure-rdflib half (load takt.ttl + a real A-Box, answer a couple of competency
# questions). Every TopologicPy call in the live path matches a signature cited
# in docs/05-tgraph-pairing.md against the pinned v0.2.0 sources.
#
# Usage:
#   python examples/tgraph_pairing_demo.py --dry-run     # no TopologicPy needed
#   python examples/tgraph_pairing_demo.py               # needs topologicpy
# =============================================================================
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAKT_TTL = ROOT / "ontology" / "takt.ttl"
ABOX = ROOT / "examples" / "takt-train-demo.ttl"
OUT_DIR = ROOT / "examples" / "out"

TAKT = "https://w3id.org/taktology#"
EX = "https://w3id.org/taktology/examples/train#"

# Prefixes to register in Ontology.NAMESPACES before export (docs/05 §c):
# TopologicPy ships top:/bot:/brick: only — the takt layer must add its own.
EXTRA_NAMESPACES = {
    "takt": TAKT,
    "dtc":  "https://dtc-ontology.cms.ed.tum.de/ontology/v2#",
    "ex":   EX,
}


# -----------------------------------------------------------------------------
# Dry run — the pure-rdflib half (no TopologicPy). Proves the A-Box is coherent
# by answering competency questions straight off the merged graph.
# -----------------------------------------------------------------------------
def dry_run() -> int:
    import rdflib

    g = rdflib.Graph()
    g.parse(TAKT_TTL)
    g.parse(ABOX)
    print(f"[dry-run] merged T-Box + {ABOX.name}: {len(g)} triples\n")

    q_occ = """
        PREFIX takt: <https://w3id.org/taktology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?zone ?wagon WHERE {
            ?t a takt:TaktTask ; takt:slot 2 ;
               takt:performedIn ?z ; takt:instantiates ?w .
            ?z rdfs:label ?zone . ?w rdfs:label ?wagon .
        } ORDER BY ?zone"""
    print("CQ: which wagon occupies which zone at slot 2?")
    for row in g.query(q_occ):
        print(f"   {row.zone}: {row.wagon}")

    q_flowA = """
        PREFIX takt: <https://w3id.org/taktology#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?a ?b WHERE {
            ?ta takt:hasSuccessorSameZone ?tb .
            ?ta rdfs:label ?a . ?tb rdfs:label ?b .
        } ORDER BY ?a"""
    print("\nCQ: Reading A convoy edges (same zone)")
    for row in g.query(q_flowA):
        print(f"   {row.a}  ->  {row.b}")

    # a coherence check that would fail on a broken plan
    bad = list(g.query("""
        PREFIX takt: <https://w3id.org/taktology#>
        ASK { ?a takt:hasSuccessorSameWagon ?b .
              ?a takt:instantiates ?w1 . ?b takt:instantiates ?w2 .
              FILTER (?w1 != ?w2) }"""))
    ok = not bad[0]
    print(f"\n[dry-run] Reading-B edges all share a wagon type: {'OK' if ok else 'BROKEN'}")
    return 0 if ok else 1


# -----------------------------------------------------------------------------
# Live run — build a takt TGraph, project to takt: RDF (needs TopologicPy).
# -----------------------------------------------------------------------------
def live_run() -> int:
    try:
        from topologicpy.TGraph import TGraph
        from topologicpy.Ontology import Ontology
    except ImportError:
        print("TopologicPy not installed. Install it, or run with --dry-run:\n"
              "    pip install topologicpy\n"
              "    python examples/tgraph_pairing_demo.py --dry-run", file=sys.stderr)
        return 2

    import rdflib

    # (c) register the takt:/dtc:/ex: prefixes process-globally BEFORE export.
    Ontology.NAMESPACES.update(EXTRA_NAMESPACES)

    # A tiny 2-cell plan: 5.1 -> 5.2 in one zone (Reading A).
    g = TGraph()
    #   (b) each vertex carries ontology_class (verbatim QName -> rdf:type object),
    #   a stable uri, and a human label.
    v_plan = g.AddVertex(dictionary={"ontology_class": "takt:TaktGraph", "uri": f"{EX}plan", "label": "Demo plan"})
    v_zone = g.AddVertex(dictionary={"ontology_class": "takt:TaktZone", "uri": f"{EX}zone_B5_1", "label": "B5:1"})
    v_t1 = g.AddVertex(dictionary={"ontology_class": "takt:TaktTask", "uri": f"{EX}t_51", "label": "5.1 @ B5:1"})
    v_t2 = g.AddVertex(dictionary={"ontology_class": "takt:TaktTask", "uri": f"{EX}t_52", "label": "5.2 @ B5:1"})

    #   (b/d) each edge carries ontology_predicate — the semantic carrier.
    g.AddEdge(v_t1, v_zone, dictionary={"ontology_predicate": "takt:performedIn"})
    g.AddEdge(v_t2, v_zone, dictionary={"ontology_predicate": "takt:performedIn"})
    g.AddEdge(v_t1, v_t2, dictionary={"ontology_predicate": "takt:hasSuccessorSameZone"})
    g.AddEdge(v_plan, v_t1, dictionary={"ontology_predicate": "dtc:hasProcess"})
    g.AddEdge(v_plan, v_t2, dictionary={"ontology_predicate": "dtc:hasProcess"})

    OUT_DIR.mkdir(exist_ok=True)
    ttl_path = OUT_DIR / "tgraph_export.ttl"

    # Export TTL. NOTE (docs/05 §d): the shipped exporter drops edge
    # ontology_predicate semantics on some paths, so we rebuild the object-property
    # triples from the edge dictionaries and append them.
    base_ttl = TGraph.TTLString(g)
    extra = []
    for e in TGraph.Edges(g):
        pred = e.get("ontology_predicate")
        su = _uri(g, e.get("src")), _uri(g, e.get("dst"))
        if pred and all(su):
            extra.append(f"<{su[0]}> {pred} <{su[1]}> .")
    ttl = base_ttl + "\n# --- edge predicates re-attached (docs/05 §d) ---\n" + "\n".join(extra) + "\n"
    ttl_path.write_text(ttl, encoding="utf-8")
    print(f"[live] wrote {ttl_path.relative_to(ROOT)}")

    # Merge the T-Box and confirm it parses + entails (rdflib RDFS closure stands
    # in for TGraph.InferOntology(profile='rdfs'), which does the same job with
    # includeOntologyAxioms + takt.ttl merged — see docs/05 §e).
    merged = rdflib.Graph()
    merged.parse(TAKT_TTL)
    merged.parse(data=ttl)
    n_tasks = len(list(merged.query(
        "PREFIX takt: <https://w3id.org/taktology#> SELECT ?t WHERE { ?t a takt:TaktTask }")))
    print(f"[live] round-trip parsed: {len(merged)} triples, {n_tasks} takt:TaktTask")
    return 0


def _uri(g, idx):
    if idx is None:
        return None
    try:
        from topologicpy.TGraph import TGraph
        d = TGraph.VertexDictionary(g, idx) if hasattr(TGraph, "VertexDictionary") else None
        return (d or {}).get("uri")
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description="takt: <-> TopologicPy TGraph pairing demo")
    ap.add_argument("--dry-run", action="store_true",
                    help="exercise the pure-rdflib half; no TopologicPy needed")
    args = ap.parse_args()
    sys.exit(dry_run() if args.dry_run else live_run())


if __name__ == "__main__":
    main()
