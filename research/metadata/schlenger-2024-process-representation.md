# schlenger-2024-process-representation

- **Title:** Advanced Process Representation for Semi-Automated Linking between Construction Schedules and IFC Files
- **Authors / Year:** Schlenger, J.; Borrmann, A. — 2024
- **Venue:** LDAC 2024; CEUR-WS Vol. 3824, 36–49 · OA [PDF](https://ceur-ws.org/Vol-3824/paper3.pdf)
- **Status:** candidate · **Cluster:** ifc-ontology-graph · **Verified:** ✔

## Summary
Proposes a **minimal ontology for construction-schedule processes** capturing the
hierarchy of activities and their dependencies (which XML/spreadsheet schedule formats
lose), and a method for semi-automated linking of schedule processes to IFC product
geometry.

## Key takeaways
- Directly addresses taktology's core problem: tasks + hierarchy + dependencies as a
  graph, bound to building elements.
- Cites the larger DTC ontology (`dtc-ontology-spec`) as its foundation — it's the
  focused process slice of that schema.

## Distinct contribution
The closest existing prior art to taktology's process layer — a *minimal* schedule
ontology + schedule↔IFC linking.

## Overlap / what it is NOT
Not takt-specific (no wagon/train/takt-time concepts). A general schedule-process
vocabulary.

## How it shapes taktology (intertwine)
**This is the reuse-vs-mint decision.** INDEX gap #1 names it: before finalizing
`takt:` process terms, evaluate whether to subclass/map to this ontology (and DTC)
rather than mint our own. Recorded as an open decision in
[`research/decisions/ADR-001-research-grounding.md`](../decisions/ADR-001-research-grounding.md).
