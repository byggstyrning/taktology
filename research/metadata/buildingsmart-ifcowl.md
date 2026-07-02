# buildingsmart-ifcowl

> **(stub — bibliographic data from manifest; full read pending)**

- **Title:** ifcOWL (official buildingSMART ifcOWL ontology page)
- **Authors / Year:** buildingSMART International (Linked Data Working Group) — n.d.
- **Venue:** buildingSMART Technical (standards body) · [technical.buildingsmart.org](https://technical.buildingsmart.org/standards/ifc/ifc-formats/ifcowl/)
- **Status:** reference · **Cluster:** ifc-ontology-graph · **Verified:** ✔

## Role in the ontology
Per the manifest: the authoritative ifcOWL artifact page (IFC 2x3–4.0).
`dcterms:source` target in [`ontology/takt.ttl`](../../ontology/takt.ttl) for
`takt:instantiates` (IFC's type mechanism) and `takt:isMilestone` (mirrors
IfcTask.IsMilestone). The `ifc:` prefix in takt.ttl targets the published IFC4
ADD2_TC1 ifcOWL served from here — there is no official IFC4.3 ifcOWL — pinned
in [`ontology/alignments.lock.json`](../../ontology/alignments.lock.json). For
the ifcOWL *methodology*, see `pauwels-terkaj-2016-ifcowl`.
