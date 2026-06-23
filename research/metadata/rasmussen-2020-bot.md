# rasmussen-2020-bot

- **Title:** BOT: The Building Topology Ontology of the W3C Linked Building Data Group
- **Authors / Year:** Rasmussen, M. H.; Lefrançois, M.; Schneider, G. F.; Pauwels, P. — 2020
- **Venue:** Semantic Web, 12(1), 143–161 · DOI [10.3233/SW-200385](https://doi.org/10.3233/SW-200385) · OA [PDF](https://www.semantic-web-journal.net/system/files/swj2279.pdf)
- **Status:** adopted · **Cluster:** ifc-ontology-graph · **Verified:** ✔

## Summary
Introduces BOT — a deliberately minimal, extensible core ontology for building
topology (sites, buildings, storeys, spaces, zones, elements, interfaces, 3D-model
links). Designed as a lightweight hub other domain ontologies attach to, enabling
BIM "Level 3" linked-data workflows without importing the full IFC schema.

## Key takeaways
- `bot:Zone` + subclasses and `bot:hasElement`/`containsElement` are the spatial
  backbone; BOT scopes **out** process, time, and resources by design.
- Minimal-and-extend is the intended pattern: subclass `bot:Zone`, don't fatten BOT.
- Companion artifact is the live namespace `lbd-cg-bot-spec` (w3id.org/bot).

## Distinct contribution
The canonical *lightweight* topology vocabulary — the opposite philosophy to
ifcOWL's full-schema mirror (`pauwels-terkaj-2016-ifcowl`).

## Overlap / what it is NOT
A **vocabulary** paper (what to call spatial things), not a method. It computes
nothing — adjacency/containment must be asserted or computed elsewhere (that's what
TopologicPy adds; see `jabi-2018-topologic`).

## How it shapes taktology (intertwine)
Grounds ADR-1 (build the spatial layer on a BOT-aligned vocabulary) and ADR-3 (align,
don't import the full schema) in
[`docs/03-decisions.md`](../../docs/03-decisions.md). taktology reaches BOT
*through* `top:` (TopologicPy already binds its classes to `bot:`), so `takt:TaktZone`
inherits `bot:Zone` without a hand-rolled BOT extension — see
[`docs/01-architecture.md`](../../docs/01-architecture.md).
