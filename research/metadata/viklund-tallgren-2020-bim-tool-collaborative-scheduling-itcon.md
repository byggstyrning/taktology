# viklund-tallgren-2020-bim-tool-collaborative-scheduling-itcon

- **Title:** BIM-tool development enhancing collaborative scheduling for pre-construction
- **Authors / Year:** Viklund Tallgren, M.; Roupé, M.; Johansson, M.; Bosch-Sijtsema, P. (Chalmers) — 2020
- **Venue:** Journal of Information Technology in Construction (ITcon), 25, 374–397 · DOI [10.36680/j.itcon.2020.022](https://doi.org/10.36680/j.itcon.2020.022) · [PDF](https://research.chalmers.se/publication/521210/file/521210_Fulltext.pdf)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔ (full text read)

## Summary
Design-Science development of the **Visual Project Planner (VPP)** — a BIM-integrated,
collaborative pre-construction scheduling tool. Argues the bottleneck is *socio-technical*,
not tooling: conventional schedulers are *"geared towards experienced users such as expert
planners"* and pre-construction is choked by *"high complexity, an extensive amount of
information, and a lack of site managers' time."* The fix is to let the people who do the
work co-create the plan.

## Key takeaways (grounded in the full text)
- **The manual practice is already zone-based and proto-takt.** The project is split
  *"into levels and zones … by dividing and colouring plan views,"* then each trade plans
  per zone on **sticky notes, a unique colour per discipline**, each note carrying the
  *activity name, duration in full days, and required number of resources (persons)*. That
  sticky note is, field-for-field, a takt cell.
- **Ownership comes from authoring.** Lean requirement **L7 "Involvement creates ownership
  of work"** and **L6 "Workers should plan"** — subcontractors must be active contributors,
  not *"passive consumer roles."*
- **Nine requirements blend CSCW + Lean.** Awareness of others' work to surface *tacit
  knowledge* → shared understanding (C1); co-creation *"simultaneous, parallel, and
  serial"* (C2); build on others' work (C3); individual reflection (C4); reduce complexity
  (L3); project breakdown (L4); ownership (L7).
- **VPP = a digital whiteboard** where participants *"drag and drop their activities and
  connect them with links"* (dependencies), colour-coded per discipline, anchored to the
  BIM model (4D). It *"has potential to reduce time for pre-construction planning regardless
  of the planning approach used."*
- Grounds location-based scheduling in Kenley & Seppänen (decompose into locations to cut
  per-location complexity and see concurrent activities).

## Distinct contribution
A user-centric, socio-technical tool + a CSCW-and-Lean requirements set for *collaborative*
schedule authoring — the bottom-up counterpart to BIMTakt's top-down auto-generation.

## Overlap / what it is NOT
NOT takt-specific — it is collaborative pre-construction scheduling (Swedish "Integrated
Planning," location-based, Lean-inspired). Reports a sub-result of
`viklund-tallgren-2021-collaborative-planning-phd`; overlaps the 4D-ITcon paper.

## How it shapes taktology (intertwine)
- **External validation of the data model:** sticky note = `TaktZone` + `Crew`/colour +
  `WagonType` + duration + `crewSize`; drag-links = `takt:hasSuccessor`.
- **Exposes a design gap:** authoring/ownership ≠ execution. taktology has `performedBy`
  (who *executes*) but nothing for *who planned/committed* a task — a `prov:wasAttributedTo`
  dimension if plans are co-created. (Noted as a candidate, not yet in the T-Box.)
- **Two producers, one graph:** generation (BIMTakt) is top-down; VPP-style collaborative
  authoring is bottom-up — both populate the same `takt:` graph. Reinforces ADR-6 (consumer
  decision) and the Total BIM deployment context.
