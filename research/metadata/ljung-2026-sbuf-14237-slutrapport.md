# ljung-2026-sbuf-14237-slutrapport

- **Title:** Byggprojekt strukturer för integrerad leverans — *Ett Spatial-Temporalt BIM ramverk som länkar samman projekterings- och produktionsinformation samt projektorganisation* (SBUF 14237, slutrapport)
- **Authors / Year:** Ljung, E. (Skanska Sverige AB); Roupé, M.; Viklund Tallgren, M.; Johansson, M. (Chalmers) — report dated 2026-08-12
- **Venue:** SBUF (Svenska Byggbranschens Utvecklingsfond) project 14237 · [project page](https://www.sbuf.se/projektresultat/projekt?id=321bfa5a-35fd-478e-8192-f7f8b22368b8) · [final report PDF](https://vpp.sbuf.se/Public/Documents/ProjectDocuments/321bfa5a-35fd-478e-8192-f7f8b22368b8/FinalReport/SBUF%2014237%20Slutrapport%20Byggprojekt%20strukturer%20f%C3%B6r%20integrerad%20leverans.pdf) (28 pp., open)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔ (full text read 2026-10-02; project facts from the SBUF page)

## Project record
"BIM baserad virtuell taktplanering" (the SBUF project title; the report title differs).
Project 2023-08-06 → 2026-06-30, status *Avslutat*. Leader: Efraim Ljung (industrial PhD,
Skanska Sverige AB, the responsible organisation), carried out at Chalmers CME. Funded by
SBUF, Skanska and CMB. Steering group = project leader + supervisors (Skanska: R. Wahlström,
P. Samuelsson; Chalmers: Roupé, Viklund Tallgren, Johansson). **Reference group included
Johannes Riis, Byggstyrning**, alongside Skanska Norge/Tampere, VVS Miljö, NCC, Implenia,
Chalmers and Peab. SBUF's own keyword tags: Klimat & miljö, Digitalisering, Husbyggnad,
Management, Installation. Its other published document is the 113-page licentiate
(`ljung-2026-tbs-integrated-delivery`).

## Summary
Practitioner-facing synthesis of the TBS (*Tids-Rumslig Nedbrytningsstruktur*, Spatio-Temporal
Breakdown Structure). Problem statement: the information needed to build already exists
digitally, but product information (what: building parts, systems) and process information
(how: schedule, work preparation, logistics, takt) are structured by different logics, so
the model is manually restructured between design and production. TBS adds two dimensions
on top of existing standards, and is explicitly **not** a new classification system.

## Key takeaways (grounded in the full text)
- **Two dimensions.** *Produktionsskeden* (production phases, temporal–organisational):
  discipline-independent partial deliveries, each owned by a delivery team. *Produktionszoner*
  (production zones, spatial–operational): the geographic subdivision of each phase
  (stairwell, part of a storey, part of a façade, part of the ground area).
- **Vad / Vem / När / Var.** Product × organisation answer *what* and *who*; time × space
  answer *when* and *where*. Same model filtered by phase, zone and responsible team instead
  of restructured in separate systems.
- **Takt link, stated directly.** Within a phase the work is sequenced through its zones, and
  the report calls that execution sequence the takt train (*takttåg*). Planned vs performed work
  is compared per zone; a completed phase is verified against the designed information and then
  validated against requirements (V-model / *systematiskt färdigställande*) before the next
  phase starts. BAS-P/BAS-U and kontrollansvarig checks follow phase boundaries.
- **Positioned against standards.** Completes ISO 21511 (breakdown structures, via
  Gebremichael's Unified Breakdown Structure: PBS + FBS), ISO 19650-2 (delivery teams),
  ISO 12006-2 and ISO/IEC 81346 (adds time and place of production to the multi-aspect
  model). Classification (BSAB, CoClass, Uniclass, OmniClass) says *what* a thing is, not how
  it is produced.
- **Six information categories** (requirements, product, process, operations, experience,
  rules/standards) × two dimensions (design vs production domain; product vs process logic).
- **Findings (five).** Fragmentation is between *structuring logics*, not IT systems; a shared
  execution structure is needed; phases + zones improve coordination; model-based planning
  gets simpler; **the structure must be established early**; introduced late in a project it
  became hard to link model, schedule and other structures.
- **Method and evidence.** Design Science Research; two primary projects as testbeds plus the
  *SIM-house* reference environment. Qualitative (workshops, interviews, project study).
  **No measured productivity, cost or schedule effect** — the thesis lists this as a
  limitation, so do not cite the report for effect sizes.

## Distinct contribution
Adds the **project-level provenance and the Swedish vocabulary** that the thesis note lacks,
and states the takt relationship (zones-within-a-phase = train) in one sentence. For
anything beyond the five findings (cases, design requirements R1–R6, design principles
DP1–DP5, the SIM-house evaluation) go to the thesis.

## Overlap / what it is NOT
- Same artefact as `ljung-2026-tbs-integrated-delivery`; the report is the short form. Cite
  the thesis for method and empirical detail, the report for the SBUF record and Swedish terms.
- Not takt method: the report mentions takt planning as one consumer of TBS. For takt
  mechanics see Cluster A.
- Not a coding scheme. The coding side is `ljung-2024-phasing-iso81346-arcom`.
- The report's reference list has three entries with no venue and titles that match no
  corpus source: Ljung et al. 2023 "BIM-based structuring of production information for
  integrated delivery", Ljung et al. 2024 "Structuring construction information through
  spatio-temporal production logic", and Viklund Tallgren et al. 2025 "Model-based production
  planning and integrated delivery in construction projects". They may be working titles of
  Papers II, III and V. **Unresolved, not added.**

## How it shapes taktology (intertwine)
Observations for the vocabulary; none is a decision yet.
- **`takt:TaktZone` ≈ production zone** — confirmed by the report, which also fixes the
  scoping: zones subdivide a *phase*, so the zone set can differ from phase to phase.
  taktology treats zones as plan-scoped; worth a check against a multi-phase plan.
- **Production phase has no direct taktology class, and "train" is a false friend.** The report's
  *takttåg* is the cross-discipline sequence of a phase's zones. `takt:Train` is one trade's
  chain of wagons ("the MEP train"). A phase therefore spans several taktology trains; the
  nearest taktology handles are `takt:partOfProcess` (train → wider on-site process) and the
  plan (`TaktGraph`). Neither carries the **Vem** dimension: a phase is owned by a delivery
  team, whereas `Crew` is the planned production crew.
- **Phase-boundary verification** (right product, right zone, right phase, then validate
  against requirements) is a conformance check over zone × phase; it belongs on the check
  plane next to takt integrity, not in the vocabulary.
- **Eases INDEX gap #3** a little further (a citable name for the structure), but the
  wagon/train vocabulary is still ours.
