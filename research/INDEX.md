# Taktology research corpus — index

Human catalog of the research grounding the taktology vocabulary. Built with the
[research-grounded-agents](../../.claude/skills/research-grounded-agents/) skill —
a discovery sweep on **2026-06-23** across five clusters, then verification — expanded
the same day with a sixth **Chalmers** cluster (BIM-takt, breakdown structures, Total BIM).

- **Machine bibliography:** [manifest.json](manifest.json) (48 sources)
- **Per-source notes:** [metadata/](metadata/) (deep notes for design-driving sources)
- **Decisions the corpus feeds:** [decisions/](decisions/)
- **Raw discovery runs:** [discoveries/](discoveries/) (ephemeral until promoted)

> **Verification status.** Every source has a real, checked URL. 38/48 are fully
> verified; 10 are `partial` (a specific field — DOI, author list, venue, or version
> — still needs a manual confirm; flagged per row and in `manifest.json`). No PDFs
> are committed — open-access mirrors are linked where the publisher copy is paywalled.

---

## Status table

Legend — status: `adopted` (shapes the design, cited in a decision) · `influenced`
(shapes a contract/roadmap) · `reference` (background/benchmark) · `candidate`
(discovered, triage pending). ✔ = fully verified, ◑ = partially verified.

### Cluster A — Takt foundations & theory
| id | source | yr | status | v |
|----|--------|----|--------|---|
| `haghsheno-2016-history` | History & Theoretical Foundations of Takt Planning & Control | 2016 | adopted | ✔ |
| `dlouhy-2016-three-level` | Three-Level Method of Takt Planning & Takt Control | 2016 | adopted | ✔ |
| `binninger-2017-technical-takt` | Technical Takt Planning and Takt Control | 2017 | adopted | ✔ |
| `frandson-2013-cladding` | Takt Time Planning for Exterior Cladding | 2013 | adopted | ✔ |
| `frandson-2014-crc-takt-plan-development` | Development of a Takt-Time Plan: A Case Study | 2014 | adopted | ✔ |
| `tommelein-2017-collaborative-nonrepetitive` | Collaborative Takt Planning of Non-Repetitive Work | 2017 | adopted | ✔ |
| `tommelein-2022-wdm` | Work Density Method for Takt Planning | 2022 | adopted | ✔ |
| `singh-tommelein-2023-visual-workload-zoning` | Visual Workload Leveling & Zoning (WDM) | 2023 | candidate | ◑ |

### Cluster B — Location-based planning
| id | source | yr | status | v |
|----|--------|----|--------|---|
| `kenley-seppanen-2010-lbms-book` | Location-Based Management for Construction (book) | 2010 | adopted | ✔ |
| `frandson-2015-lbms-vs-takt` | Comparison Between LBMS and Takt Time Planning | 2015 | adopted | ✔ |
| `seppanen-ballard-pesonen-2010-lps-lbms` | Combination of Last Planner & LBMS | 2010 | influenced | ✔ |
| `kenley-seppanen-2006-typology` | LBM: A New Typology for Scheduling Methodologies | 2006 | reference | ◑ |
| `seppanen-2025-integrated-forecasting` | Integrated Forecasting for Takt & Location-Based | 2025 | candidate | ◑ |

### Cluster C — Takt + BIM & automation
| id | source | yr | status | v |
|----|--------|----|--------|---|
| `becker-tschickardt-2023-bimtakt` | **BIMTakt** (corpus anchor) | 2023 | adopted | ✔ |
| `jabbari-2020-wolzo` | Workload leveling by work-space zoning (WoLZo) | 2020 | adopted | ✔ |
| `melzner-2019-bim-takt-requirements` | BIM-based Takt Planning & Control: Requirements | 2019 | influenced | ✔ |
| `abbasi-2020-takt-des-jit` | Takt + Discrete-Event Sim for JIT | 2020 | reference | ✔ |
| `silveira-costa-2024-4dbim-lbms-lps` | Automating 4D BIM + LBMS + LPS | 2024 | reference | ✔ |
| `doukari-2022-4d-schedule-creation` | 4D schedule creation: conventional vs automated | 2022 | reference | ✔ |
| `donia-2026-bim-nlp-schedule` | BIM–NLP automated schedule generation | 2026 | candidate | ✔ |

### Cluster D — IFC, ontologies & graph
| id | source | yr | status | v |
|----|--------|----|--------|---|
| `rasmussen-2020-bot` | **BOT** — Building Topology Ontology (journal) | 2020 | adopted | ✔ |
| `lbd-cg-bot-spec` | BOT specification / namespace (w3id.org/bot) | — | adopted | ✔ |
| `bsi-ifc43-process-extension` | IFC 4.3 IfcProcessExtension (IfcTask, IfcRelSequence…) | 2024 | adopted | ✔ |
| `jabi-2018-topologic` | Topologic: spatial & topological modelling toolkit | 2018 | adopted | ✔ |
| `topologicpy-ontology` | TopologicPy ontology (`top:`) — the substrate | 2026 | adopted | ◑ |
| `pauwels-terkaj-2016-ifcowl` | EXPRESS to OWL / ifcOWL | 2016 | influenced | ✔ |
| `schlenger-2025-dtc-reference-architecture` | DTC reference architecture & ontology framework | 2025 | influenced | ◑ |
| `buildingsmart-ifcowl` | Official ifcOWL artifact page | — | reference | ✔ |
| `zhu-2025-ifc-graph` | Internal structure of IFC-Graph (LPG) | 2025 | reference | ◑ |
| `schlenger-2024-process-representation` | Advanced Process Representation (schedule↔IFC) | 2024 | candidate | ✔ |
| `dtc-ontology-spec` | Digital Twin Construction (DTC) Ontology spec | 2023 | candidate | ◑ |

### Cluster E — Implementation, case studies & control
| id | source | yr | status | v |
|----|--------|----|--------|---|
| `frandson-2014-takt-last-planner` | Takt-Time Planning and the Last Planner | 2014 | adopted | ✔ |
| `frandson-2016-interiors-hospital` | Takt Planning of Interiors (pre-cast hospital) | 2016 | adopted | ✔ |
| `lehtovaara-2019-residential` | Implementing Takt Planning & Control in Residential | 2019 | adopted | ✔ |
| `lehtovaara-2021-flow-cme` | How Takt Production Contributes to Production Flow | 2021 | adopted | ✔ |
| `keskiniva-2021-monitoring-renovation` | Takt Production Monitoring & Control (renovation) | 2021 | adopted | ◑ |
| `lerche-2022-takt-kanban-wind` | Takt + Kanban on modular wind turbines | 2022 | candidate | ◑ |

### Cluster F — BIM-takt, breakdown structures & Total BIM (Chalmers group)
| id | source | yr | status | v |
|----|--------|----|--------|---|
| `ljung-2026-tbs-integrated-delivery` | Structuring Construction Projects for Integrated Delivery (TBS) | 2026 | influenced | ✔ |
| `ljung-2023-prerequisites-bim-takt` | Prerequisites for Takt Planning in a BIM-Based Process | 2023 | influenced | ✔ |
| `viklund-tallgren-2022-bim-takt-production-control` | BIM-based takt time schedules for production control | 2022 | influenced | ✔ |
| `viklund-tallgren-2020-bim-tool-collaborative-scheduling-itcon` | BIM-tool for collaborative scheduling (pre-construction) | 2020 | influenced | ✔ |
| `disney-2023-total-bim-onsite-itcon` | Total BIM on the construction site (Byggstyrning co-author) | 2023 | influenced | ✔ |
| `viklund-tallgren-2021-collaborative-planning-phd` | Collaborative production planning with BIM (PhD) | 2021 | reference | ✔ |
| `viklund-tallgren-2021-4d-collaborative-planning-itcon` | 4D modelling via virtual collaborative planning | 2021 | reference | ✔ |
| `viklund-tallgren-2018-collaborative-planning-lic` | Developing a collaborative planning tool (licentiate) | 2018 | reference | ◑ |
| `disney-2024-total-bim-celsius-sasbe` | Embracing BIM in its totality (Total BIM case) | 2024 | reference | ✔ |
| `ljung-2024-work-preparation-ccc` | Significance of a Shared Breakdown Structure (work prep) | 2024 | reference | ✔ |
| `ljung-2024-phasing-iso81346-arcom` | Phasing interoperability via ISO 81346 coding | 2024 | reference | ✔ |

---

## Overlap clusters (and how teams confuse their members)

**Cluster A · Takt theory** — anchor `haghsheno-2016-history`.
*Overlap risk:* the Karlsruhe (KIT) 2016–2017 papers are same-author/same-venue and
easily merged — `haghsheno-2016-history` is the **theory/genealogy**,
`dlouhy-2016-three-level` is the **zone hierarchy**, `binninger-2017-technical-takt`
is the **planning-vs-control mechanics**. Cite the right one. Also: a takt zone is
*not* an LBMS location (see Cluster B).

**Cluster B · Location-based vs takt** — anchor `kenley-seppanen-2010-lbms-book`.
*Overlap risk:* LBMS and takt both treat space as a resource and look alike, but LBMS
optimizes **continuous crew flow with time buffers**, takt fixes a **rhythm per zone
with capacity buffers**. `frandson-2015-lbms-vs-takt` exists precisely to keep them
apart — read it before importing any LBMS concept into the takt model.

**Cluster C · BIM automation** — anchor `becker-tschickardt-2023-bimtakt`.
*Overlap risk:* generic 4D-BIM schedule automation (`doukari-2022`, `donia-2026`) ≠
**takt-specific** automation. And `jabbari-2020-wolzo` automates zoning over a
**work-density abstraction**, not over raw BIM/IFC geometry — don't cite it as
geometry-driven zoning.

**Cluster D · Ontology/graph** — anchor `rasmussen-2020-bot`.
*Overlap risk:* the classic semantic-web traps. (1) **Vocabulary vs method:** BOT
says *what to call* spatial things; it computes nothing. (2) **Lightweight vs
full-schema:** BOT (minimal, extensible) is the opposite philosophy to ifcOWL
(`pauwels-terkaj-2016`, mirrors the whole EXPRESS schema) — taktology uses BOT-style
alignment and deliberately does **not** import ifcOWL. (3) **RDF vs LPG:**
`zhu-2025-ifc-graph` is the property-graph branch; the ontology papers are the RDF
branch — pick deliberately or bridge.

**Cluster E · Implementation** — anchor `lehtovaara-2021-flow-cme`.
*Overlap risk:* takt + LPS (`frandson-2014-takt-last-planner`) is **not** LBMS + LPS
(`seppanen-ballard-pesonen-2010`). Theory papers (`lehtovaara-2021-flow-cme`)
synthesize the case studies they cite — don't treat a synthesis as a single case.

**Cluster F · BIM-takt / breakdown / Total BIM (Chalmers)** — anchor
`viklund-tallgren-2021-collaborative-planning-phd`.
*Overlap risk:* one research group, many overlapping outputs — the ITcon journal papers
report sub-results of the PhD; the two CONVR papers (`viklund-tallgren-2022-...` vs
`ljung-2023-prerequisites-...`) are the control-focused vs prerequisites take on the
*same* BIM+takt idea; the two Total BIM papers (`disney-2023-...` vs `disney-2024-...`)
are the on-site/journal vs definitional-case treatments of *one* concept. Distinct from
KIT's takt theory (Cluster A): this is BIM-integration and breakdown-structure in Swedish
practice, not takt method per se. Cite `ljung-2026-tbs-integrated-delivery` for the
spatio-temporal **structure** and `ljung-2024-phasing-iso81346-arcom` for a zone/phase
**identifier/coding** scheme (relevant to taktology's namespace/coding open item).

---

## Topic coverage matrix

Themes (rows) × where each is covered. ● primary · ◐ substantive.

| Theme | Primary sources | Substantive |
|-------|-----------------|-------------|
| Takt definitions & genealogy | `haghsheno-2016-history` ● | `frandson-2013-cladding` ◐ `binninger-2017-technical-takt` ◐ |
| Takt zoning / work density / work structuring | `tommelein-2022-wdm` ● `jabbari-2020-wolzo` ● | `tommelein-2017-collaborative-nonrepetitive` ◐ `dlouhy-2016-three-level` ◐ `singh-tommelein-2023-visual-workload-zoning` ◐ |
| Takt control / steering (execution) | `binninger-2017-technical-takt` ● `keskiniva-2021-monitoring-renovation` ● | `lehtovaara-2019-residential` ◐ |
| LBMS / flowline & takt-vs-LBMS | `kenley-seppanen-2010-lbms-book` ● `frandson-2015-lbms-vs-takt` ● | `kenley-seppanen-2006-typology` ◐ `seppanen-2025-integrated-forecasting` ◐ |
| LPS / production-control integration | `frandson-2014-takt-last-planner` ● | `seppanen-ballard-pesonen-2010-lps-lbms` ◐ |
| BIM-integrated & automated takt | `becker-tschickardt-2023-bimtakt` ● `jabbari-2020-wolzo` ● | `melzner-2019-bim-takt-requirements` ◐ `abbasi-2020-takt-des-jit` ◐ |
| Quantity → duration from model geometry | `becker-tschickardt-2023-bimtakt` ● | `tommelein-2022-wdm` ◐ |
| Automated 4D schedule generation (generic) | `doukari-2022-4d-schedule-creation` ● `donia-2026-bim-nlp-schedule` ● | `silveira-costa-2024-4dbim-lbms-lps` ◐ |
| IFC process schema & 4D↔model linking | `bsi-ifc43-process-extension` ● | `schlenger-2024-process-representation` ◐ `zhu-2025-ifc-graph` ◐ |
| Ontologies & semantic interop | `rasmussen-2020-bot` ● `pauwels-terkaj-2016-ifcowl` ● | `dtc-ontology-spec` ◐ `schlenger-2025-dtc-reference-architecture` ◐ `lbd-cg-bot-spec` ◐ |
| Topology & property-graph representation | `jabi-2018-topologic` ● `topologicpy-ontology` ● | `zhu-2025-ifc-graph` ◐ |
| Empirical case studies / sectors | `frandson-2016-interiors-hospital` ● `lehtovaara-2019-residential` ● | `lerche-2022-takt-kanban-wind` ◐ |
| Digital takt tools / monitoring | `keskiniva-2021-monitoring-renovation` ● | `melzner-2019-bim-takt-requirements` ◐ |
| Spatio-temporal / work breakdown structures | `ljung-2026-tbs-integrated-delivery` ● | `ljung-2024-work-preparation-ccc` ◐ `ljung-2024-phasing-iso81346-arcom` ◐ `dlouhy-2016-three-level` ◐ |
| BIM-based takt in practice (prerequisites/control) | `viklund-tallgren-2022-bim-takt-production-control` ● `ljung-2023-prerequisites-bim-takt` ● | `becker-tschickardt-2023-bimtakt` ◐ `melzner-2019-bim-takt-requirements` ◐ |
| Collaborative BIM planning & 4D scheduling | `viklund-tallgren-2021-collaborative-planning-phd` ● `viklund-tallgren-2020-bim-tool-collaborative-scheduling-itcon` ● | `viklund-tallgren-2021-4d-collaborative-planning-itcon` ◐ `viklund-tallgren-2018-collaborative-planning-lic` ◐ |
| Total BIM / single source of truth (deployment) | `disney-2023-total-bim-onsite-itcon` ● `disney-2024-total-bim-celsius-sasbe` ● | `ljung-2026-tbs-integrated-delivery` ◐ |

---

## Gaps (where taktology designs with thin evidence — most valuable section)

1. **No dedicated takt ontology exists in the literature.** The closest formal
   process vocabularies are the DTC ontology (`dtc-ontology-spec`) and Schlenger's
   minimal schedule ontology (`schlenger-2024-process-representation`) — neither is
   takt-specific. *This is the gap taktology fills.* — **RESOLVED 2026-06-23:**
   `takt.ttl` v0.3.0 reuses DTC by reference (see
   [decisions/ADR-001](decisions/ADR-001-research-grounding.md) + `docs` ADR-7).
   DTC's TTL was read and mapped; Schlenger's specific terms remain unextracted
   (PDF not machine-readable here) → finer Schlenger mapping deferred.

2. **Automated takt-zone identification directly from BIM/IFC *geometry* is thinly
   sourced.** `jabbari-2020-wolzo` optimizes over a work-density abstraction, not raw
   geometry; no canonical *topology/geometry-driven* takt-zoning paper was found.
   This is exactly where a TopologicPy-based approach (`jabi-2018-topologic`,
   `topologicpy-ontology`) contributes — and where we currently have *no prior art to
   lean on*. Flagged as a build risk, not a solved problem.

3. **The wagon/train metaphor has no single theoretical source.** It's covered
   indirectly (zones via `dlouhy-2016-three-level`, sizing via `tommelein-2022-wdm`)
   but no paper defines the wagon/train vocabulary formally. taktology's
   `docs/02-vocabulary.md` is, in effect, original synthesis here — treat its
   definitions as ours, not as cited fact. *Partially eased 2026-06-23:*
   `ljung-2026-tbs-integrated-delivery` gives a citable name — **Spatio-Temporal
   Breakdown Structure (TBS)** — for the zone×time *structure* (the `TaktZone`×`TaktTime`
   core). The wagon/train *naming* remains ours.

4. **Genealogy root unverified.** Bulhões et al. (2005), cited by
   `haghsheno-2016-history` as the first IGLC use of "takt," was not independently
   located. Line-of-Balance origin (Lumsden 1968) also unverified. Genealogy claims
   should be hedged until these primaries are confirmed.

5. **Takt maturity / standardization model** is thin — `dlouhy-2016-three-level` and
   its KIT extensions are the best available; a dedicated maturity/performance model
   (e.g. an "Indicators for Takt Production Performance" paper surfaced but unverified)
   would close it.

6. **German primary literature under-captured.** The verifiable theory is the
   English IGLC output of the KIT school; the deeper German monographs/dissertations
   (Binninger, Dlouhy theses on KITopen) were not retrieved.

7. **Property-graph (LPG) vs RDF for the runtime store is unsettled in the corpus.**
   `zhu-2025-ifc-graph` (LPG) vs the RDF/OWL branch — taktology's
   `docs/03-decisions.md` ADR-6 makes this a consumer choice, but neither branch is
   evidenced *specifically for takt* yet.

### Closed / in-progress
- **Gap #1 reuse-vs-mint — RESOLVED 2026-06-23** by reusing DTC in `takt.ttl` v0.3.0
  (read DTC's TTL; mapped takt terms as subclasses/subproperties). Follow-ups:
  confirm DTC version (v2 exists), extract Schlenger's ontology terms for a finer map.
- Gaps #2 (geometry-driven zoning), #3 (wagon/train vocabulary), #4 (genealogy roots)
  remain **open** — re-run discovery.
- **Ljung pass — 2026-06-23.** Read the TBS licentiate full text (incl. its appended-papers
  list) + the prerequisites paper. Confirmed Ljung's research = the licentiate + Papers I–IV,
  **all already in the corpus** (no new sources). Resolved both 2024 `partial`s → verified:
  Paper III's authoritative title includes *"a Shared Breakdown Structure"*; Paper IV's
  ARCOM authors/editors (Thomson & Neilson) confirmed. Enriched the notes for the TBS
  licentiate, prerequisites, VPP (2020), and added notes for Papers III & IV. The TBS =
  **space × time × responsibility**, which v0.4.0's `takt:partOfProcess` realizes.
- **Chalmers cluster (F) added 2026-06-23** (11 sources, from two user-supplied seeds):
  strengthens *BIM-based takt in practice*, *collaborative BIM scheduling / 4D*, and
  *Total BIM / single-source-of-truth* coverage. `ljung-2026-tbs-integrated-delivery`
  names the spatio-temporal breakdown structure (eases gap #3's *structure*);
  `disney-2023-total-bim-onsite-itcon` is co-authored by Byggstyrning (this repo's org),
  pinning down the deployment context. Follow-ups: confirm OA/title for the two 2024
  Ljung papers; mine Bosch-Sijtsema's profile; consider ISO 81346 coding for zone IDs.
