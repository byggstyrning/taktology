# The TopologicPy TGraph pairing contract

How a takt plan moves between **RDF (ontology/takt.ttl v0.5.0)** and a
**TopologicPy `TGraph`** — and back — without losing its takt semantics.

This is the contract `examples/tgraph_pairing_demo.py` executes and
`scripts/takt_production_ingester_plan.md` builds against. Every claim below was
verified against the TopologicPy sources (`TGraph.py`, `Ontology.py`,
`KnowledgeGraph.py`) and the published `topologicpy.ttl` **v0.2.0**
(namespace `http://w3id.org/topologicpy#`, modified 2026-06-27) — the snapshot
pinned in `ontology/alignments.lock.json`. Line numbers refer to that snapshot
and will drift with upstream releases; method names are the stable anchor.

---

## a. Why TGraph

`TGraph` is TopologicPy's compiled-kernel graph class: vertices are stable
indexed records carrying plain Python dictionaries, edges are `src`/`dst` index
records with their own dictionaries, and geometry is an *optional*
representation attached to a record — not the substrate (`TGraph.py` class
docstring). That inversion is exactly what a takt plan needs: wagon types,
tasks and crews have no geometry, zones may or may not, and everything must
carry typed attributes. The same class ships the semantic machinery the pairing
uses — `OntologyTriples`/`TTLString` for RDF export, `KnowledgeGraph`/`Infer`
for reasoning, `ByIFCFile`/`ByIFCPath` for IFC ingestion, and
`ByTopology`/`BySpatialRelationships` for computing zone adjacency from
geometry — so one object is simultaneously the working data structure, the RDF
projection source, and the LPG projection source.

## b. Instance projection — the dictionary keys

Takt individuals ride TGraph **dictionaries**. The exporters read a small set of
reserved keys; everything else becomes a literal-valued triple.

### Vertex dictionary

| key | example | consumed by |
|---|---|---|
| `uri` | `"ex:t_51_B51"` | Becomes the RDF **subject** verbatim when it contains `:` (`Ontology._uri_for_topology`, Ontology.py:590–593; `TGraph._OntologySubjectFromDictionary`, TGraph.py:16261–16266). Without it, subjects are minted from guid/id/label — set it explicitly for stable round-trips. |
| `ontology_class` | `"takt:Wagon"` | Becomes the `rdf:type` **object verbatim** — any QName works, not just `top:` (`Ontology.Triples`: `triples.append((subject, "rdf:type", ontologyClass))`, Ontology.py:1459–1460). |
| `label` | `"5.1 @ B5:1"` | `rdfs:label` literal (Ontology.py:1466–1467). |
| `category` | `"space"` | `top:category` literal (Ontology.py:1469–1470). Must be set **explicitly** for takt classes — `CategoryByClass` has no `takt:` entries. |
| any QName key | `"takt:slot": 1` | Key containing `:` passes through `PropertyQName` **unprefixed** and becomes the predicate verbatim (Ontology.py:1688–1689): `ex:t_51_B51 takt:slot "1"^^xsd:integer`. |
| any bare key | `"area": 184.0` | Aliased then prefixed `top:` (Ontology.py:1690–1691): emits `top:area` — see §g before relying on this. |

`ontology_class`, `ontology_uri`, `label`, `category`, `uri` are the exporter's
skip-set (Ontology.py:1489–1495) — they are consumed structurally, never
re-emitted as literals. Set class + derived `ontology_uri` in one call with
`TGraph.SetOntologyClass(g, "takt:Wagon", element="vertex", index=i)`
(TGraph.py:18868–18894; the URI derivation needs the prefix registered, §c), or
simply put `ontology_class` in the `AddVertex` dictionary.

`AddVertex` injects bookkeeping keys `index`, `active` into the dictionary
(TGraph.py:988–989); `AddEdge` injects `index`, `src`, `dst`, `directed`,
`active` (TGraph.py:823). These export as undeclared `top:index`/`top:src`/…
literals — tolerate or filter them (§d).

### Edge dictionary

| key | example | consumed by |
|---|---|---|
| `ontology_predicate` | `"takt:hasSuccessorSameZone"` | The **semantic carrier**. The published TTL says so itself: a Relationship's "semantic RDF predicate … is carried by top:hasPredicate or by the emitted ontology_predicate dictionary value" (topologicpy.ttl:101–103). Consumed by `TGraph.OntologyTriples`' fallback branch (TGraph.py:16374–16380) — but see the export gap, §d. |
| `inverse_predicate` | *(optional)* | Emits the inverse triple in the same fallback branch (TGraph.py:16375, 16379–16380). |
| `relationship` | `"performed_in"` | snake_case label → `top:relationship` literal (declared in the published TTL, topologicpy.ttl:442–444). |

### Graph dictionary (the plan itself)

The graph node is typed from the graph dictionary's `ontology_class`
(`Ontology.GraphTriples` → `Ontology.Triples` on the graph subject,
Ontology.py:1552–1559; fallback default `"top:Graph"`, TGraph.py:16302).
Annotate it as the takt plan:

```python
TGraph.AnnotateOntology(g, ontologyClass="takt:TaktGraph", category="graph",
                        label="Train demo plan", uri="ex:plan",
                        generatedBy="taktology-ingester")   # element defaults to "graph"
```

(`AnnotateOntology`, TGraph.py:1593–1654.) `takt:TaktGraph ⊑ top:KnowledgeGraph
+ dtc:ConstructionSchedule` (ADR-15) makes the export self-describing while
TopologicPy's own axioms still entail `top:Graph`. Plan-wide rhythm literals go
in the same dictionary as QName keys: `"takt:taktDuration": "P7D"`,
`"takt:planStart": "2024-03-04"`. Plan membership (`dtc:hasProcess`) is **not**
derivable from the graph dictionary — append it in the export pass (§d);
`top:hasNode`/`top:hasRelationship` carry the implicit membership.

### Datatype caveat

`Ontology._rdf_literal` types only bool/int/float (Ontology.py:572–580).
**Strings export untyped**: `"P7D"` gets no `^^xsd:duration`, `"2024-03-04"` no
`^^xsd:date`. SHACL shapes and consumers must accept plain literals for
`takt:taktDuration`/`takt:planStart` in TGraph-emitted data (hand-authored
A-Boxes like `examples/takt-train-demo.ttl` keep the typed literals).

## c. Namespace registration — there is no public API

`Ontology.NAMESPACES` (Ontology.py:71–79) is the process-global prefix
registry: `bot`, `brick`, `rdf`, `rdfs`, `xsd`, `owl`, `top` — **no `takt:`, no
`dtc:`, no `ex:`**. `Ontology.Namespaces()` returns a **copy**
(`return dict(Ontology.NAMESPACES)`, Ontology.py:626) — mutating its return
value does nothing. There is no registration method. The supported pattern is
the one TopologicPy uses on itself (its own patch block calls
`Ontology.NAMESPACES.update({...})` to add `ifc`/`dcterms`/`skos`/…,
Ontology.py:2955–2963):

```python
from topologicpy.Ontology import Ontology
Ontology.NAMESPACES.update({
    "takt": "https://w3id.org/taktology#",
    "dtc":  "https://dtc-ontology.cms.ed.tum.de/ontology/v2#",
    "ex":   "https://w3id.org/taktology/examples/train#",   # your instance ns
})
```

Do this **once, before any export or annotation**. It feeds every consumer at
once: Turtle headers (`TurtleFromTriples` defaults to `Ontology.NAMESPACES`,
Ontology.py:1641), QName expansion (`ExpandQName` → `SetClass`/
`SetOntologyClass` `ontology_uri` derivation, Ontology.py:743–746), RDF reload
QName resolution (`GraphByRDFGraph`, Ontology.py:2557–2574), and
`KnowledgeGraph.Namespaces()` (which copies `Ontology.NAMESPACES` and adds
setdefaults, KnowledgeGraph.py:217–232). It is process-global mutable state —
idiomatic upstream, but keep the call in one place.

Per-call alternatives exist but are partial: `Ontology.TurtleFromTriples(
triples, namespaces={...})` fixes only the header; `KnowledgeGraph.Namespaces(
extra={...})` is per-call. Neither helps `ExpandQName` or reload. **Fallback**
when you cannot mutate the registry (e.g. post-processing Turtle produced
elsewhere): prepend the missing `@prefix` lines to the emitted Turtle before
parsing — the triple bodies are plain QName tokens, so the header is the only
thing missing.

## d. The export gap — `ontology_predicate` never becomes a triple

`TGraph.TTLString`/`ExportTTL` → `TGraph.OntologyTriples`, which **delegates to
`Ontology.GraphTriples` whenever Ontology.py is importable** (TGraph.py:
16287–16297) — i.e. always, in a normal install. `Ontology.GraphTriples`' edge
loop (Ontology.py:1576–1607) has **no `ontology_predicate` handling**. Per edge
it emits only:

```
inst:graph  top:hasRelationship  inst:edge_1_0_2 .
inst:edge_1_0_2  top:ontology_predicate  "takt:performedIn" .   # a LITERAL, via the dictionary pass
inst:edge_1_0_2  top:startsAt  ex:t_51_B51 .
inst:edge_1_0_2  top:endsAt    ex:zone_B5_1 .
ex:t_51_B51  top:connectsTo  ex:zone_B5_1 .
```

The direct semantic triple `ex:t_51_B51 takt:performedIn ex:zone_B5_1` and
`top:hasPredicate` are emitted **only** by `TGraph.OntologyTriples`' fallback
branch (TGraph.py:16374–16380), which is unreachable when Ontology.py imports.
Left alone, *every* takt object property — `performedIn`, `actsOn`,
`instantiates`, `performedBy`, `hasSuccessor*`, `partOfProcess` — is silently
absent from the export. (`KnowledgeGraph.ByTopology` uses the same
`GraphTriples`, KnowledgeGraph.py:976–984, so the reasoning path has the same
gap. Upstream issue-worthy: the published TTL promises the carrier the shipped
exporter drops.)

**The workaround is the canonical exporter** — two-phase:

```python
triples = TGraph.OntologyTriples(g)                       # phase 1: delegated export
plan_uri = TGraph.Dictionary(g).get("uri")
for rec in TGraph.Edges(g):                               # phase 2: active edge records
    d = rec.get("dictionary", {})
    p = d.get("ontology_predicate")
    if not p:
        continue
    s = g.VertexDictionary(rec["src"]).get("uri")         # matches the phase-1 subject:
    o = g.VertexDictionary(rec["dst"]).get("uri")         # _uri_for_topology reads "uri" first
    if s and o:
        triples.append((s, p, o))
        if d.get("inverse_predicate"):
            triples.append((o, d["inverse_predicate"], s))
for rec in TGraph.Vertices(g):                            # plan membership (see §b)
    vd = rec.get("dictionary", {})
    if vd.get("ontology_class") == "takt:Wagon" and plan_uri and vd.get("uri"):
        triples.append((plan_uri, "dtc:hasProcess", vd["uri"]))
ttl = Ontology.TurtleFromTriples(triples)                 # header from Ontology.NAMESPACES (§c)
```

Because every vertex carries a `uri` with a `:` in it (§b), the appended triples
join the reified records on identical subjects. Still set `ontology_predicate`
on every edge regardless — it is the documented carrier, it feeds the LPG
exports, and it is the only takt semantics that *survives* a TGraph reload
(§f). Optionally filter the bookkeeping literals in the same pass (drop triples
whose predicate is `top:index`, `top:src`, `top:dst`, `top:directed`,
`top:active` — undeclared in the published TTL) or document them as
non-vocabulary noise.

## e. Reasoning — merge takt.ttl BEFORE inferring

`TGraph.InferOntology(g, profile="rdfs", includeOntologyAxioms=True)`
(TGraph.py:150–168, impl 23304–23359) injects **only TopologicPy's built-in
axioms** (`Reasoner.AddOntologyAxioms` on the in-code class/property tables —
TGraph.py:23264–23267; `Ontology.OntologyTriples`, Ontology.py:1694–1766). It
never loads `ontology/takt.ttl`, and takt.ttl's alignment-by-reference design
means no `dtc:`/`bot:` hierarchy travels with the instance data either. Merge
the T-Box first:

```python
from topologicpy.KnowledgeGraph import KnowledgeGraph
kg = KnowledgeGraph.ByTGraph(g)                    # instance triples (delegated GraphTriples)
kg.AddTriples(direct_takt_triples)                 # the §d phase-2 triples (AddTriples, KnowledgeGraph.py:694)
kg = kg.Merge("ontology/takt.ttl")                 # T-Box. Merge is NOT in-place by default —
                                                   # capture the result or pass inplace=True
                                                   # (Merge accepts a path, a KnowledgeGraph, or triples;
                                                   #  KnowledgeGraph.py:1188–1198, 1243–1261)
inferred = kg.Infer(profile="rdfs", includeOntologyAxioms=True)
# entailed: ex:zone_B5_1 rdf:type bot:Zone   (takt:TaktZone ⊑ bot:Zone, ADR-13)
#           ex:t_51_B51  rdf:type dtc:AsPlannedProcess, dtc:Process ... needs DTC v2 merged too
```

Because ADR-13 re-parented `takt:TaktZone` **directly** to `bot:Zone`, merging
`takt.ttl` alone is enough to reach `bot:Zone` — the entailment is independent
of TopologicPy's built-ins and works in any generic RDFS reasoner or external
triple store (single-file). `dtc:` entailments deeper than the directly
asserted parents additionally require merging the DTC v2 TTL (consistent with
takt.ttl implementer note 1). The `rdfs` profile suffices for everything
takt.ttl asserts (`subClassOf`/`subPropertyOf`/`domain`/`range` only).
Optionally write the inferred types back into vertex dictionaries for
property-graph consumers with `TGraph.ApplyInferences(g, result=...)`
(TGraph.py:178–186).

## f. Round-trip — what survives a reload, and the conventions that keep takt typing lossless

`Ontology.GraphByRDFFile`/`GraphByTTLString` → `GraphByRDFGraph` rehydrates
selectively (Ontology.py:2508–2768):

- **Requires the TGraph wrapper.** No subject with `top:hasNode` → `None`
  (Ontology.py:2610–2617). A plain takt A-Box (`examples/takt-train-demo.ttl`)
  is not loadable this way at all.
- **Only `top:`-prefixed `rdf:type`s repopulate `ontology_class`**
  (`if … q.startswith("top:")`, Ontology.py:2626). `rdf:type takt:Wagon`
  survives in the RDF file but is dropped from the reloaded dictionary.
- **Only Literal-valued predicates are copied into dictionaries**
  (Ontology.py:2647–2650). The direct takt object triples appended in §d are
  ignored on reload.
- **The graph dictionary is demoted** to `setdefault("ontology_class",
  "top:Graph")` (Ontology.py:2735–2737) even though the `rdf:type
  takt:TaktGraph` triple survives in the file.

What **does** survive: the reified structure (`top:hasNode`,
`top:hasRelationship`, `top:startsAt`/`endsAt`), the `uri` (the subject QName is
stored back under `uri`, Ontology.py:2623), and **every literal key — including
`ontology_predicate`**: the `top:ontology_predicate "takt:performedIn"` literal
reloads as dictionary key `ontology_predicate` via `local_key`
(Ontology.py:2582–2590, 2647–2650). Hence the conventions:

1. **Never strip the wrapper triples** (graph node, `top:hasNode`,
   `top:hasRelationship`, `top:startsAt`/`endsAt`) from files intended for
   TGraph reload.
2. **Treat the edge-dictionary `ontology_predicate` literal as the
   authoritative takt-semantics carrier across round-trips.** After a reload,
   regenerate the direct takt triples from it (the reverse of §d phase 2);
   `rdf:type takt:*` in dictionaries does not round-trip, `ontology_predicate`
   does.
3. **Dual-type geometry-backed instances.** Zones computed by TopologicPy may
   additionally assert `rdf:type top:Zone` (takt.ttl licenses this
   instance-level typing) — reload then restores
   `ontology_class="top:Zone"`/`category="space"`, and the `takt:TaktZone` type
   is recovered from the RDF file itself.
4. **Keep the dual `ontology_class` + `uri` keys** on every record (§b) so
   subjects and types re-join deterministically.

**Known breakage in the pinned snapshot:** the backwards-compat shim
`_GraphByRDFGraph_TTLAligned` (Ontology.py:3243–3258) drops the
`namespacePrefix`/`tolerance` kwargs that `GraphByRDFFile` passes (the
`TypeError` is swallowed as "Could not parse RDF file. Returning None.") and
forwards `directed=` which the core implementation does not accept — so the
`GraphByRDFFile` path currently fails for **all** inputs. Until that is fixed
upstream, reload via **`KnowledgeGraph.ByFile(path).ToTGraph()`**
(KnowledgeGraph.py:885–917, 1334+) — lossless (every triple becomes an edge
carrying `predicate`/`relationship` keys) at the cost of a triple-shaped, not
plan-shaped, graph — or parse with rdflib directly. Treat conventions 1–3 as
the contract for the repaired `GraphByRDFFile` path.

## g. Quantities — dictionary keys, `top:Quantity`, and the published-TTL divergence

The published `top:` v0.2.0 declares **no** `top:area`/`top:volume` — its
datatype-property section is `top:category`, `top:relationship`,
`top:hasX/Y/Z` only (topologicpy.ttl:434–459). The **in-code** vocabulary does
declare them (`Ontology.DATA_PROPERTIES`: `"top:area": ("top:Topology",
"xsd:double", …)`, Ontology.py:3188–3189), and bare dictionary keys
`area`/`volume` pass `PROPERTY_ALIASES` → are emitted as `top:area`/`top:volume`
literals (Ontology.py:3151–3152, 1690–1691). This code-vs-published divergence
is recorded as `known_divergence` in `ontology/alignments.lock.json`; the
published TTL is normative for taktology's T-Box, so **treat emitted
`top:area`/`top:volume` triples as engine-specific instance data, not
vocabulary**.

The contract: quantities ride TGraph **dictionary keys `area`/`volume`**
(floats), sourced in order of preference:

1. **IFC `Qto_*` quantity sets** — `TGraph.ByIFCFile`/`ByIFCPath` with
   `dictionaryMode="psets"` (or `"all"`/`"full"`) flattens property/quantity
   sets into `"Pset.Prop"` dictionary keys, e.g.
   `Qto_WallBaseQuantities.NetSideArea` (`_flatten_psets` via
   `ifcopenshell.util.element.get_psets`, TGraph.py:3548–3571). Copy the value
   onto the plain `area`/`volume` key. `IfcElementQuantity` entities themselves
   map to `top:Quantity` nodes (TGraph.py:3597; topologicpy.ttl:196–198), so
   quantity records also exist as first-class vertices when relationships are
   imported.
2. **ifcopenshell directly** (`ifcopenshell.util.element`) when no TGraph IFC
   pass runs.
3. **Geometry at build time** (`Face.Area`/`Cell.Volume`) when the ingester
   already builds topology.

takt.ttl keeps quantities a consumer concern (implementer note 2, ADR-10): the
fits-in-takt check reads the `area`/`volume` of the `takt:actsOn` operand
subset, never the zone total.

## h. Graph stores

For labelled-property-graph targets, the TopologicPy code base pairs TGraph
with dedicated adapters — `Neo4j.py`, `Kuzu.py`, `GQL.py` — that consume the
same vertex/edge dictionaries this contract standardizes (these modules sit
outside the three sources verified for this document; verify their signatures
before use). **`schema/takt-topology-schema.yaml` is the takt LPG spec**: its
node types carry the `ontology_class`/`uri`/`label`/`category` projection keys
and its edge types the `ontology_predicate`/`relationship` keys, so the LPG
projection and the RDF projection of one plan stay join-compatible by
construction.

---

*Worked end-to-end script: `examples/tgraph_pairing_demo.py` (run with
`--dry-run` for the rdflib-only half). Decisions: ADR-13, ADR-15
(docs/03-decisions.md). Upstream pins: ontology/alignments.lock.json.*
