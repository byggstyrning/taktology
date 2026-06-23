# Taktology

A minimal, modular interchange vocabulary for **takt / Lean construction production
planning** — the kind of plan you build as a coloured grid of *wagons* flowing
through *takt zones* over time.

It models the **process** half of takt planning (takt tasks, wagons, trains, crews,
takt time) as a thin layer on top of the [TopologicPy ontology](https://wassimj.github.io/topologicpy/ontology/topologicpy.ttl)
(`top:`), which supplies the **spatial** half (zones, elements, geometry, graph) and
already aligns to both [BOT](https://w3id.org/bot#) and IFC. Takt terms are aligned
to IFC process concepts (`IfcTask`, `IfcRelSequence`, …) by `skos:closeMatch`
annotation — **not** by importing the heavy ifcOWL schema.

> Origin: this repo is the synthesis of a research conversation working from the
> BIMTakt paper (Becker & Tschickardt, 2023) toward an interoperable,
> manufacturer-neutral model. See [docs/](docs/) for the full reasoning.

## What's here

| Path | What it is |
|---|---|
| [`ontology/takt.ttl`](ontology/takt.ttl) | **The vocabulary** (T-Box). ~24 terms: 6 classes, 8 object properties, 10 datatype properties. |
| [`examples/lumi-b5-1.ttl`](examples/lumi-b5-1.ttl) | A worked **A-Box** — wagon 5.2 in zone B5:1 from a real takt plan, exercising every term, with duration computed end-to-end. |
| [`schema/takt-topology-schema.yaml`](schema/takt-topology-schema.yaml) | Node + edge definitions for a **property-graph build** (Neo4j / NetworkX / rdflib), plus the generation loop. |
| [`scripts/takt_production_ingester_plan.md`](scripts/takt_production_ingester_plan.md) | Implementation plan for an **IFC + wagon-table → takt graph** ingester. |
| [`docs/`](docs/) | Architecture, vocabulary, design decisions (ADRs), and BIMTakt background. |

## The core idea in one picture

```
  WagonType ──instantiates── TaktTask ──performedIn── TaktZone ──containsElement── Element
   (rate,                      │  │                     (top:                        (top:
    crew)                      │  └──actsOn──────────────────────────────────────────►│
                               │     operand subset → drives duration                 area/
                  hasSuccessor │                                                      volume)
                               ▼
                            TaktTask   (next wagon → the train = a top:Path)
```

A **wagon** is a trade's work package; its per-zone occurrences are **takt tasks**;
the ordered chain of tasks is the **train**; the **takt zone** is the work area they
flow through. One graph traversal runs from a task to the geometry that drives its
duration (`task → actsOn → element → area`) — which a spreadsheet cannot do.

## Design stance (the short version)

- **Author only the gap.** `top:` already provides zones, elements, geometry, graph,
  and the BOT+IFC alignments. This repo adds *only* the process layer `top:` lacks.
- **`closeMatch`, not import.** IFC is the semantic anchor via annotation; ifcOWL's
  ~14k axioms are never imported. Round-tripping to `.ifc` is a converter's job.
- **You haven't left IFC.** You keep IFC's process model as the reference; you only
  choose whether the `.ifc` file is your transport format. Format ≠ semantics.
- **`actsOn` ≠ `performedIn`.** A task's *operand* (the elements it builds/operates
  on) is a distinct, direct link — separate from the *location* (the zone). The
  duration formula reads the operand, not the zone total.

Full rationale in [docs/03-decisions.md](docs/03-decisions.md).

## Validating the ontology

No network was available when these files were authored, so they were syntax-checked
structurally, **not** parsed by a real RDF engine. Before relying on them:

```bash
# Apache Jena
riot --validate ontology/takt.ttl examples/lumi-b5-1.ttl
# or load both in Protégé and run a reasoner for a consistency check
```

## Open items before publishing

- **Namespace.** `https://w3id.org/taktology#` is the *intended* permanent
  namespace; the w3id.org redirect must be registered first. Until then it is a
  placeholder and does not resolve.
- **`top:` namespace URI.** Verify the exact TopologicPy ontology namespace against
  the published `.ttl` before relying on `top:FunctionalZone` / `top:Element` /
  `top:Path` / `top:area`.
- **License.** Not yet chosen — see note below.
- **Train Reading A vs B.** The vocabulary encodes Reading A (cross-trade convoy).
  Confirm with the team; it changes where every sequence edge goes.

## License

[CC BY 4.0](LICENSE) — Creative Commons Attribution 4.0 International. Reuse and
adapt freely (including commercially) with attribution. The referenced TopologicPy
ontology is AGPLv3, but this repo only references its namespace (it imports no
TopologicPy code), so it is not bound by AGPL.
