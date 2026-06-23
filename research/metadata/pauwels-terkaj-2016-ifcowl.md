# pauwels-terkaj-2016-ifcowl

- **Title:** EXPRESS to OWL for construction industry: Towards a recommendable and usable ifcOWL ontology
- **Authors / Year:** Pauwels, P.; Terkaj, W. — 2016
- **Venue:** Automation in Construction, 63, 100–133 · DOI [10.1016/j.autcon.2015.12.003](https://doi.org/10.1016/j.autcon.2015.12.003) · OA [CNR IRIS](https://iris.cnr.it/bitstream/20.500.14243/311657/1/)
- **Status:** influenced · **Cluster:** ifc-ontology-graph · **Verified:** ✔

## Summary
Defines the recommendable EXPRESS-to-OWL conversion procedure and the resulting
ifcOWL ontology, converging prior fragmentary efforts into one usable representation
— the basis buildingSMART adopted for officially published ifcOWL (IFC 2x3–4.0).

## Key takeaways
- ifcOWL is a faithful, **complete mirror** of the IFC EXPRESS schema → very large
  (≈1300 classes, ≈1580 object properties, ~14k axioms for IFC4) with OWL-list
  machinery for EXPRESS collections.
- That fidelity is precisely what makes it heavyweight and reasoning-unfriendly for a
  small domain extension.

## Distinct contribution
The authoritative method + artifact for IFC-as-RDF. The right tool for **full-fidelity
IFC round-tripping in RDF** — a different goal from a thin takt vocabulary.

## Overlap / what it is NOT
NOT a modelling vocabulary to build on — it's the interop/serialization layer. Opposite
philosophy to BOT (`rasmussen-2020-bot`).

## How it shapes taktology (intertwine)
The direct evidence behind **ADR-3** ("align to IFC by `skos:closeMatch`, never
`owl:imports` ifcOWL") in [`docs/03-decisions.md`](../../docs/03-decisions.md).
taktology points `ifc:` at the schema as a closeMatch target only; round-tripping is a
converter's job, not an import.
