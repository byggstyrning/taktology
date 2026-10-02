# ljung-2026-tbs-integrated-delivery

- **Title:** Structuring Construction Projects for Integrated Delivery — *A Spatio-Temporal BIM Framework Linking Design and Production Information and Teams*
- **Authors / Year:** Ljung, E. (Chalmers / Skanska) — 2026
- **Venue:** Licentiate thesis, Chalmers University of Technology (Technical report 2026:8) · [551855](https://research.chalmers.se/publication/551855) · [PDF](https://research.chalmers.se/publication/551855/file/551855_Fulltext.pdf)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔ (full text read; user-supplied seed)

## Summary
The "kappa" tying together Ljung's five appended papers into one artefact: the
**Spatio-Temporal Breakdown Structure (TBS)**. Core thesis (quoted): *"the core issue
lies not primarily in technology, but in how information is structured."* It names a
**structuring gap**: *"BIM provides an overarching representation of the built asset,
while classification systems offer highly detailed coding schemes. Between these levels, a
critical structuring gap remains largely unarticulated."* The TBS fills that mid-level gap
by integrating temporal (production-based) and spatial (location-based) dimensions, linking
*"what is designed, how it is built, and who is responsible for delivery."*

## Key takeaways (grounded in the full text)
- **TBS = space × time × responsibility.** Not just zones×takts — it adds the
  organisational/responsibility dimension, aligning design info, production planning, and
  who delivers.
- **The TBS artefact (DSR) has three parts:** (1) a *spatio-temporal structuring model*
  (spatial + temporal organisation of info); (2) a *multi-aspect coding and referencing
  logic* linking **product, process, and location** aspects into an interoperable
  structure; (3) a *lifecycle-oriented method* for progressively structuring/managing info.
- **Overarching RQ:** *"How can project information be structured to reduce fragmentation
  between design and production and support an integrated and well-coordinated information
  flow throughout the project lifecycle?"*
- Empirically grounded in **two construction projects**, Design Science Research.
- **Appended papers I–V**: I = `viklund-tallgren-2022-bim-takt-production-control`,
  II = `ljung-2023-prerequisites-bim-takt`, III = `ljung-2024-work-preparation-ccc`,
  IV = `ljung-2024-phasing-iso81346-arcom`, V = `viklund-tallgren-2026-bim-design-to-production-total-bim`
  (added 2026-10-02; an earlier note here listed only I–IV). The licentiate is their synthesis.
- **Terminology moved between papers.** Paper II's "deliverables" became **production phases**
  (*produktionsskeden*) and its "construction scope" became **production zones**
  (*produktionszoner*). Read Paper II with that mapping.
- **Evidence base is wider than "two projects".** Four cases (Hovås Tak 59 apts; Eriksberget
  130 apts and the SIM-house testbed; Klassrummet 135 apts; exploratory material from an
  office in Lund and a residential building in Gothenburg). The artefact was developed in two
  prototypes and evaluated on the SIM-house, not formally case-studied. Evaluation is
  qualitative; productivity/cost/schedule effects are not measured (thesis §12.1).
- **Derived requirements R1–R6 / principles DP1–DP5** (thesis §9.2, §10.1): shared product+process
  structure, design–production integration, production-oriented (takt/flow) structuring,
  collaborative/visual access, socio-technical usability, structured data for feedback.
- **Short form:** the SBUF 14237 final report, `ljung-2026-sbuf-14237-slutrapport`, summarises
  this thesis with the project record and the Swedish terms.

## Distinct contribution
The clearest research-level statement that the *structure unifying space and time (and
responsibility)* is the enabling artifact for integrated, flow-oriented delivery — and the
only source that gives this structure a name (TBS).

## Overlap / what it is NOT
A thesis framing/artefact, not an ontology or tool. The TBS's component studies are its
appended papers; cite those for the empirical detail.

## How it shapes taktology (intertwine)
- **Grounds `takt:partOfProcess`** (added v0.4.0): binding process membership
  (`partOfProcess → dtc:Process`) together with `performedIn` (space) and `hasTaktTime`
  (time) makes a takt task one cell of a TBS — the licentiate is the `dcterms:source` for
  that property in [`ontology/takt.ttl`](../../ontology/takt.ttl).
- **Eases INDEX gap #3:** gives a citable name (TBS) for taktology's `TaktZone`×`TaktTime`
  core (the wagon/train *naming* remains ours).
- The TBS's "multi-aspect product/process/location coding" parallels taktology's
  alignments (`actsOn`=product, `partOfProcess`=process, `performedIn`=location) and points
  at a zone identifier scheme (see Paper IV, ISO 81346).
