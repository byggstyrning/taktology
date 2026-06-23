# Discovery run — 2026-06-23 initial sweep

Raw record of the first discovery pass. Ephemeral per corpus-method: kept for
provenance; the keepers were promoted into [manifest.json](../manifest.json) /
[INDEX.md](../INDEX.md) / [metadata/](../metadata/).

## Method
Five parallel discovery agents (research-grounded-agents skill, `corpus-method.md`
§Discovery), one per cluster, each instructed to return only sources with a verified
URL and to flag unverified fields. Tools: WebSearch + WebFetch (Google Scholar,
iglc.net, ASCE, Wiley, Elsevier, MDPI, CEUR-WS, buildingSMART, W3C, repositories).

| Agent | Cluster | Net promoted |
|-------|---------|--------------|
| 1 | Takt foundations & theory | 8 |
| 2 | Location-based planning (LBMS/LOB/flowline) | 5 |
| 3 | Takt + BIM & automation | 7 |
| 4 | IFC schema, ontologies & graph | 11 |
| 5 | Implementation, case studies & control | 6 |

After de-duplication (Frandson 2013/14/15 and Tommelein WDM surfaced in two agents
each — useful cross-confirmation) the corpus holds **37 unique sources**.

## Conflicts resolved during promotion
- **Frandson 2013 (exterior cladding) IGLC id:** 902 vs 910 → confirmed **902** by
  fetching the iglc.net Details page.
- **Tommelein 2022 WDM article number:** 04022134 vs 04022127 → confirmed
  **04022134** (JCEM 148/12) via search; DOI 10.1061/(ASCE)CO.1943-7862.0002398.
- **New candidate found while verifying:** `singh-tommelein-2023-visual-workload-zoning`
  (JCEM 149/10) — promoted as candidate.

## Unverified leads NOT promoted (re-run discovery later)
- Bulhões et al. (2005) — cited as first IGLC use of "takt"; primary not located.
- Lumsden (1968) *The Line-of-Balance Method* — LOB origin; not located.
- KIT German theses/monographs (Binninger, Dlouhy) on KITopen.
- ASCE JCEMD4.COENG-16062 (2025) "Patterns, 4D Simulations, and AI… Workspace
  Management" — title/venue only; authors+abstract unverified.
- "Indicators for Takt Production Performance Assessment" (Buildings) — would close
  the maturity/standardization gap (#5) if verified.
- Becker/Tschickardt related German BIM-4D work (Gateway Gardens; Jaster et al. 2024
  Etagenlogistikplanung) — for a deeper German takt/BIM sub-cluster.

## Next discovery targets (from INDEX gaps)
1. Geometry/topology-driven takt zoning (gap #2) — search "IFC space topology graph
   zoning takt", König/Borrmann group.
2. Read `schlenger-2024-process-representation` + `dtc-ontology-spec` in full for the
   reuse-vs-mint decision (ADR-001 open decision).
3. Verify the 9 `partial` rows' flagged fields.
