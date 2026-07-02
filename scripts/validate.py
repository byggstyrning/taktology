#!/usr/bin/env python3
# =============================================================================
# validate.py
# -----------------------------------------------------------------------------
# The one validation gate for the taktology repo: exit 0 = green, exit 1 = red.
#
# Checks, in order:
#   1. PARSE      ontology/takt.ttl and every examples/*.ttl parse as Turtle.
#   2. TERMS      every takt: IRI used in an example is defined in the T-Box
#                 (no example may invent vocabulary).
#   3. HYGIENE    every takt: term carries rdfs:label, rdfs:comment,
#                 rdfs:isDefinedBy and dcterms:source (the research grounding).
#   4. SHACL      every example A-Box conforms to shapes/takt-shapes.ttl.
#                 pySHACL runs with the T-Box merged into the data graph and
#                 RDFS inference ON, so subproperty edges (hasSuccessorSameZone
#                 / hasSuccessorSameWagon) are visible to the generic
#                 hasSuccessor constraints. The shapes are SELF-TESTED against
#                 a seeded broken plan first — a shapes file that catches
#                 nothing must not be trusted to pass anything.
#   5. QUERIES    every queries/*.rq runs against the merged T-Box + example
#                 graphs; row counts are REPORTED, never gated (expected counts
#                 are documented in the query headers themselves).
#   6. UPSTREAMS  (--online only) refetch each upstream pinned in
#                 ontology/alignments.lock.json: sha256 drift is a WARNING
#                 (a signal to re-verify, not necessarily a break), but a
#                 terms_relied_on IRI missing upstream is a FAILURE.
#
# Run:
#     python scripts/validate.py             # offline gate (what CI runs)
#     python scripts/validate.py --online    # + upstream drift / existence
#
# Dependencies: rdflib + pyshacl (see scripts/requirements.txt).
# =============================================================================
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

try:
    import rdflib
    from rdflib import RDF, RDFS, Literal, Namespace, URIRef
    from rdflib.namespace import DCTERMS, XSD
    from pyshacl import validate as shacl_validate
except ImportError as exc:  # pragma: no cover - guidance only
    sys.exit(f"missing dependency: {exc}. Run: pip install -r scripts/requirements.txt")

ROOT = Path(__file__).resolve().parent.parent
TTL = ROOT / "ontology" / "takt.ttl"
EXAMPLES_DIR = ROOT / "examples"
SHAPES = ROOT / "shapes" / "takt-shapes.ttl"
QUERIES_DIR = ROOT / "queries"
LOCK = ROOT / "ontology" / "alignments.lock.json"

TAKT = Namespace("https://w3id.org/taktology#")
SH = Namespace("http://www.w3.org/ns/shacl#")

FAILURES: list[str] = []
WARNINGS: list[str] = []


# =============================================================================
# Reporting — every check prints one OK/WARN/FAIL line; main() sums up.
# =============================================================================
def section(title: str) -> None:
    print(f"\n== {title}")


def ok(msg: str) -> None:
    print(f"  OK    {msg}")


def warn(msg: str) -> None:
    WARNINGS.append(msg)
    print(f"  WARN  {msg}")


def fail(msg: str) -> None:
    FAILURES.append(msg)
    print(f"  FAIL  {msg}")


def graph_union(*graphs: rdflib.Graph) -> rdflib.Graph:
    merged = rdflib.Graph()
    for g in graphs:
        for triple in g:
            merged.add(triple)
    return merged


# =============================================================================
# 1. Parse the T-Box and every example A-Box
# =============================================================================
def load_graphs() -> tuple[rdflib.Graph, dict[Path, rdflib.Graph]]:
    section("parse")
    try:
        tbox = rdflib.Graph()
        tbox.parse(TTL, format="turtle")
        ok(f"{TTL.relative_to(ROOT).as_posix()} ({len(tbox)} triples)")
    except Exception as exc:
        fail(f"{TTL.relative_to(ROOT).as_posix()}: {exc}")
        sys.exit(1)  # nothing downstream can run without the T-Box

    examples: dict[Path, rdflib.Graph] = {}
    example_files = sorted(EXAMPLES_DIR.glob("*.ttl"))
    if not example_files:
        fail(f"no examples/*.ttl found in {EXAMPLES_DIR.relative_to(ROOT).as_posix()}")
    for path in example_files:
        try:
            g = rdflib.Graph()
            g.parse(path, format="turtle")
            examples[path] = g
            ok(f"{path.relative_to(ROOT).as_posix()} ({len(g)} triples)")
        except Exception as exc:
            fail(f"{path.relative_to(ROOT).as_posix()}: {exc}")
    return tbox, examples


# =============================================================================
# 2. Term consistency — examples may only use takt: IRIs the T-Box defines
# =============================================================================
def check_term_consistency(tbox: rdflib.Graph, examples: dict[Path, rdflib.Graph]) -> None:
    section("term consistency (A-Box uses only defined takt: terms)")
    defined = {s for s in tbox.subjects() if str(s).startswith(str(TAKT))}
    for path, g in examples.items():
        used = {
            node
            for triple in g
            for node in triple
            if isinstance(node, URIRef) and str(node).startswith(str(TAKT))
        }
        missing = sorted(str(t) for t in used - defined)
        if missing:
            fail(f"{path.relative_to(ROOT).as_posix()}: undefined takt: terms: {', '.join(missing)}")
        else:
            ok(f"{path.relative_to(ROOT).as_posix()}: {len(used)} takt: terms, all defined")


# =============================================================================
# 3. T-Box hygiene — every term is labelled, documented and research-grounded
# =============================================================================
def check_hygiene(tbox: rdflib.Graph) -> None:
    section("T-Box hygiene (label / comment / isDefinedBy / source on every term)")
    required = [
        (RDFS.label, "rdfs:label"),
        (RDFS.comment, "rdfs:comment"),
        (RDFS.isDefinedBy, "rdfs:isDefinedBy"),
        (DCTERMS.source, "dcterms:source"),
    ]
    terms = sorted(
        {s for s in tbox.subjects() if isinstance(s, URIRef) and str(s).startswith(str(TAKT))},
        key=str,
    )
    clean = True
    for term in terms:
        gaps = [name for prop, name in required if tbox.value(term, prop) is None]
        if gaps:
            clean = False
            fail(f"{term.replace(str(TAKT), 'takt:')}: missing {', '.join(gaps)}")
    if clean:
        ok(f"all {len(terms)} takt: terms carry label, comment, isDefinedBy and source")


# =============================================================================
# 4. SHACL — self-test the shapes on a seeded broken plan, then gate examples
# =============================================================================
def shacl_results(data: rdflib.Graph, shapes: rdflib.Graph) -> tuple[list[str], list[str]]:
    """Run pySHACL and split the results by severity (violations, warnings)."""
    _, results_graph, _ = shacl_validate(
        data_graph=data,
        shacl_graph=shapes,
        inference="rdfs",       # materializes subproperty edges (needs T-Box in data)
        allow_warnings=True,
    )
    violations, warnings = [], []
    for result in results_graph.subjects(RDF.type, SH.ValidationResult):
        severity = results_graph.value(result, SH.resultSeverity)
        focus = results_graph.value(result, SH.focusNode)
        message = results_graph.value(result, SH.resultMessage)
        line = f"{focus}: {message}"
        (violations if severity == SH.Violation else warnings).append(line)
    return sorted(violations), sorted(warnings)


def seeded_broken_plan(tbox: rdflib.Graph) -> rdflib.Graph:
    """T-Box + a deliberately broken A-Box: 3 violations the shapes MUST catch."""
    g = graph_union(tbox)
    bad = Namespace("urn:takt-selftest:")
    # 1+2: a task with no performedIn zone and a 0-based slot
    g.add((bad.floating_task, RDF.type, TAKT.TaktTask))
    g.add((bad.floating_task, TAKT.slot, Literal(0)))
    # 3: a hasSuccessorSameZone edge whose ends sit in DIFFERENT zones
    for zone in (bad.zone_a, bad.zone_b):
        g.add((zone, RDF.type, TAKT.TaktZone))
        g.add((zone, RDFS.label, Literal(str(zone))))
    g.add((bad.task_1, RDF.type, TAKT.TaktTask))
    g.add((bad.task_1, TAKT.performedIn, bad.zone_a))
    g.add((bad.task_1, TAKT.slot, Literal(1)))
    g.add((bad.task_1, TAKT.hasSuccessorSameZone, bad.task_2))
    g.add((bad.task_2, RDF.type, TAKT.TaktTask))
    g.add((bad.task_2, TAKT.performedIn, bad.zone_b))
    g.add((bad.task_2, TAKT.slot, Literal(2)))
    return g


def check_shacl(tbox: rdflib.Graph, examples: dict[Path, rdflib.Graph]) -> None:
    section("SHACL (shapes/takt-shapes.ttl, pySHACL + RDFS inference)")
    if not SHAPES.exists():
        fail(f"shapes file not found: {SHAPES.relative_to(ROOT).as_posix()}")
        return
    try:
        shapes = rdflib.Graph()
        shapes.parse(SHAPES, format="turtle")
    except Exception as exc:
        fail(f"{SHAPES.relative_to(ROOT).as_posix()}: {exc}")
        return

    # Self-test: the shapes must catch all 3 seeded violations (missing zone,
    # slot < 1, cross-zone same-zone edge) before their PASS verdict counts.
    violations, _ = shacl_results(seeded_broken_plan(tbox), shapes)
    if len(violations) < 3:
        fail(f"self-test: shapes caught only {len(violations)}/3 seeded violations — "
             f"the shapes file is not constraining what it should")
        for v in violations:
            print(f"          caught: {v}")
        return
    ok(f"self-test: shapes catch a seeded broken plan ({len(violations)} violations)")

    # The real gate: every example A-Box (+ T-Box for inference) must conform.
    for path, g in examples.items():
        violations, warnings = shacl_results(graph_union(tbox, g), shapes)
        rel = path.relative_to(ROOT).as_posix()
        for w in warnings:
            warn(f"{rel}: {w}")
        if violations:
            fail(f"{rel}: {len(violations)} SHACL violation(s)")
            for v in violations:
                print(f"          {v}")
        else:
            ok(f"{rel}: conforms" + (f" ({len(warnings)} warning(s))" if warnings else ""))


# =============================================================================
# 5. Competency queries — run and report; counts are documented in the .rq files
# =============================================================================
def run_queries(tbox: rdflib.Graph, examples: dict[Path, rdflib.Graph]) -> None:
    if not QUERIES_DIR.is_dir():
        return
    section("competency queries (row counts reported, not gated)")
    merged = graph_union(tbox, *examples.values())
    query_files = sorted(QUERIES_DIR.glob("*.rq"))
    if not query_files:
        warn(f"{QUERIES_DIR.relative_to(ROOT).as_posix()}/ exists but holds no .rq files")
        return
    for path in query_files:
        rel = path.relative_to(ROOT).as_posix()
        try:
            result = merged.query(path.read_text(encoding="utf-8"))
        except Exception as exc:
            fail(f"{rel}: query did not run ({exc})")
            continue
        if result.type == "SELECT":
            ok(f"{rel}: {len(result)} row(s)")
        elif result.type == "ASK":
            ok(f"{rel}: ASK -> {result.askAnswer}")
        else:  # CONSTRUCT / DESCRIBE
            ok(f"{rel}: {len(result.graph)} triple(s)")


# =============================================================================
# 6. Upstream pins (--online) — refetch, hash, and verify relied-on terms exist
# =============================================================================
def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={
        "Accept": "text/turtle, application/rdf+xml;q=0.9, */*;q=0.1",
        "User-Agent": "taktology-validate (scripts/validate.py)",
    })
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def parse_fetched(raw: bytes) -> rdflib.Graph | None:
    for fmt in ("turtle", "xml", "json-ld"):
        g = rdflib.Graph()
        try:
            g.parse(data=raw, format=fmt)
            return g
        except Exception:
            continue
    return None


def check_upstreams() -> None:
    section("upstream pins (ontology/alignments.lock.json, --online)")
    try:
        lock = json.loads(LOCK.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{LOCK.relative_to(ROOT).as_posix()}: {exc}")
        return
    for key, entry in lock.get("upstreams", {}).items():
        url = entry.get("url")
        try:
            raw = fetch(url)
        except Exception as exc:
            fail(f"{key}: fetch failed for {url} ({exc})")
            continue

        # Hash drift is a WARNING: a signal to re-verify the alignment, not
        # proof it broke — the terms_relied_on check below is the hard gate.
        pinned = entry.get("sha256")
        digest = hashlib.sha256(raw).hexdigest()
        if pinned is None:
            ok(f"{key}: no pinned sha256 (hash check skipped)")
        elif digest == pinned:
            ok(f"{key}: sha256 matches pin")
        else:
            warn(f"{key}: sha256 drift — upstream changed since {lock.get('verified', '?')} "
                 f"(pinned {pinned[:12]}…, fetched {digest[:12]}…); re-verify the alignment")

        fetched = parse_fetched(raw)
        if fetched is None:
            fail(f"{key}: fetched file did not parse as turtle / rdf-xml / json-ld")
            continue
        namespace = entry.get("namespace", "")
        subjects = {s for s in fetched.subjects() if isinstance(s, URIRef)}
        missing = [term for term in entry.get("terms_relied_on", [])
                   if URIRef(namespace + term.split(":", 1)[1]) not in subjects]
        if missing:
            fail(f"{key}: relied-on terms MISSING upstream: {', '.join(missing)}")
        else:
            count = len(entry.get("terms_relied_on", []))
            ok(f"{key}: all {count} relied-on terms exist upstream ({len(fetched)} triples)")


# =============================================================================
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate the taktology ontology, examples, shapes and queries.")
    parser.add_argument("--online", action="store_true",
                        help="also refetch the upstreams pinned in "
                             "ontology/alignments.lock.json and verify them")
    args = parser.parse_args()

    tbox, examples = load_graphs()
    check_term_consistency(tbox, examples)
    check_hygiene(tbox)
    check_shacl(tbox, examples)
    run_queries(tbox, examples)
    if args.online:
        check_upstreams()

    print(f"\n{'RED' if FAILURES else 'GREEN'}: "
          f"{len(FAILURES)} failure(s), {len(WARNINGS)} warning(s)")
    if FAILURES:
        sys.exit(1)


if __name__ == "__main__":
    main()
