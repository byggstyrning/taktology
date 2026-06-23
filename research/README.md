# research/ — the taktology research corpus

A curated, indexed set of sources grounding the taktology vocabulary, built with the
[research-grounded-agents](../../.claude/skills/research-grounded-agents/) skill. The
governing principle: **every source traces to a decision, and every decision traces
back to its sources** (the *intertwine* rule).

## Layout

```
research/
├── manifest.json     machine bibliography — 48 sources (id, authors, url, status, …)
├── INDEX.md          human catalog — status table, overlap clusters, topic matrix, GAPS
├── metadata/<id>.md  per-source notes for the design-driving sources
├── decisions/        ADRs linking the corpus to the taktology design
├── discoveries/      raw discovery runs (ephemeral until promoted)
└── pdfs/             acquired files (empty — none committed; see below)
```

## How to read it (mining a corpus)

1. Open [INDEX.md](INDEX.md). Find the **cluster** your task sits in and its
   **overlap-risk** note. Read the **gaps** — those are the blind spots.
2. Read the cluster **anchor's** [metadata/](metadata/) note, then the others'
   *distinct contribution* and *overlap* sections.
3. Honor the overlap risks (the classic traps: LBMS≠takt, vocabulary≠method,
   lightweight BOT≠full ifcOWL, RDF≠LPG).

## Status & honesty

- **48 sources**: 22 adopted · 9 influenced · 12 reference · 5 candidate (six clusters,
  incl. a Chalmers cluster of 11: BIM-takt, breakdown structures, Total BIM).
- **38 fully verified**, 10 `partial` (one field — DOI/authors/venue/version — still
  needs a manual confirm; flagged per row in `manifest.json` and INDEX).
- **No PDFs are committed** — licenses unchecked, and many are paywalled.
  Open-access mirrors (IGLC, eScholarship, Aaltodoc, NSF PAR, CEUR, repositories) are
  linked in the manifest. Drop acquired OA files in `pdfs/` (gitignored by default if
  large) only after a license check.

## The headline finding

**No takt-specific ontology exists in the literature** — the closest are the general
DTC ontology and Schlenger's minimal schedule ontology. taktology fills a real gap.
The flip side (INDEX gaps): geometry/topology-driven takt zoning and the formal
wagon/train vocabulary have little or no prior art, so those parts of the design are
*our synthesis* and carry build risk. See
[decisions/ADR-001](decisions/ADR-001-research-grounding.md).

## Extending the corpus

Follow `corpus-method.md` in the skill: check INDEX clusters for duplicates → add a
`manifest.json` entry → write a `metadata/<id>.md` note → place it in a cluster +
update the topic matrix → if it closes a gap, mark the gap **closed** with a dated
note. Re-run discovery for `candidate` rows and the open ADR-001 decision.
