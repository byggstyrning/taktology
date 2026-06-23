# bsi-ifc43-process-extension

- **Title:** IFC 4.3 – IfcProcessExtension (IfcTask, IfcRelSequence, IfcWorkSchedule, IfcTaskTime, …)
- **Authors / Year:** buildingSMART International — 2024 (IFC 4.3.2.0; ISO 16739-1)
- **Venue:** Official IFC 4.3 documentation · [content page](https://ifc43-docs.standards.buildingsmart.org/IFC/RELEASE/IFC4x3/HTML/ifcprocessextension/content.html)
- **Status:** adopted · **Cluster:** ifc-ontology-graph · **Verified:** ✔

## Summary
The normative schema for representing construction processes and scheduling in IFC:
tasks (`IfcTask`), task sequencing (`IfcRelSequence` with `SequenceType` and lag),
work schedules/plans/calendars, and timing carried on `IfcTask.TaskTime`
(`IfcTaskTime`/`IfcTaskTimeRecurring`). Extends `IfcProcess` from the kernel.

## Key takeaways
- `IfcRelAssignsToProduct` binds a task to a product/location (overloaded for both —
  the location vs operand distinction taktology keeps separate).
- `IfcRelAssignsToProcess` binds resources (e.g. `IfcCrewResource`) to tasks.
- Recurring-task mechanism fits the repeating-wagon pattern.
- The reified `IfcRel*` relationships map naturally to property-graph edges.

## Distinct contribution
The lingua franca target schema — the standard other ontologies and tools map to.

## Overlap / what it is NOT
The data **structure**, not an OWL re-modelling (that's ifcOWL / DTC). taktology
references it as the `skos:closeMatch` anchor, not as an import.

## How it shapes taktology (intertwine)
Every `skos:closeMatch` in [`ontology/takt.ttl`](../../ontology/takt.ttl) points here
(`takt:TaktTask`→`IfcTask`, `hasSuccessor`→`IfcRelSequence`,
`performedIn`/`actsOn`→`IfcRelAssignsToProduct`, `performedBy`→`IfcRelAssignsToProcess`,
`TaktTime`→`IfcTaskTime`). Grounds the full IFC mapping table in
[`docs/02-vocabulary.md`](../../docs/02-vocabulary.md) and the "you haven't left IFC"
stance of ADR-6.
