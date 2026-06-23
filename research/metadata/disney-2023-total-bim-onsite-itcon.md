# disney-2023-total-bim-onsite-itcon

- **Title:** Total BIM on the construction site: a dynamic single source of information
- **Authors / Year:** Disney, O.; Roupé, M.; Johansson, M. (Chalmers); Ris, J.; Höglin, P. (Byggstyrning) — 2023
- **Venue:** Journal of Information Technology in Construction (ITcon), 28, 519–538 · DOI [10.36680/j.itcon.2023.027](https://doi.org/10.36680/j.itcon.2023.027) · [PDF](https://www.itcon.org/papers/2023-27-ITcon-SI-CONVR-Disney.pdf)
- **Status:** influenced · **Cluster:** bim-takt-breakdown · **Verified:** ✔

## Summary
Across four "Total BIM" projects, shows that when the BIM is the **contractual,
legally-binding single source of information** and 2D drawings are abandoned, mobile
cloud-based BIM viewers become the central site communication/management platform —
enabling dynamic information extraction and new on-site methods.

## Key takeaways
- "Total BIM" = the model is the single source of truth, consumed live on site via
  mobile/cloud viewers.
- This is the *deployment context* a takt/zone-time model would live in — the takt plan
  becomes one more queryable layer of the single model, not a separate spreadsheet.
- **Co-authored by Byggstyrning** — this repo's organization — so it's the home-turf
  delivery environment for taktology.

## Distinct contribution
Defines the on-site single-source-of-truth paradigm (the journal/on-site treatment of
Total BIM; the SASBE 2024 "Celsius" paper is the definitional single case).

## Overlap / what it is NOT
Overlaps `disney-2024-total-bim-celsius-sasbe` (same concept, definitional case). Not
about takt itself — it's the model environment takt plugs into.

## How it shapes taktology (intertwine)
Frames the consumer/runtime target in [`docs/03-decisions.md`](../../docs/03-decisions.md)
ADR-6 (RDF vs property graph is a *consumer* decision): in a Total BIM setting the takt
graph is a layer of the single model. Motivates keeping taktology interoperable and
model-linked (`actsOn`/`performedIn`) rather than a standalone schedule file.
