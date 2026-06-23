# becker-tschickardt-2023-bimtakt

- **Title:** BIMTakt – Optimierung der Produktionsplanung durch ganzheitliche Integration von BIM und Lean Construction
- **Authors / Year:** Becker, S.; Tschickardt, T. — 2023
- **Venue:** Bautechnik (Wiley), 100(2), 75–85 · DOI [10.1002/bate.202200088](https://doi.org/10.1002/bate.202200088)
- **Status:** adopted · **Cluster:** takt-bim-automation · **Verified:** ✔ (confirm OA PDF manually)

## Summary
The corpus anchor. A conceptual model for automatically generating detailed takt
plans directly from a BIM, via three components: automated takt-zone identification
from geometry (a *project-structure* attribute), automated task/effort definition
from a reference database (an *activity-structure* attribute), and fully automated
takt-plan generation with variant calculation. Prototyped inside a vendor BIM API.

## Key takeaways
- Quantities come from BIM geometry (area for 2D activities, volume for 3D); effort
  values (crew size, production rate h/m²) are matched from a database of completed
  projects, not entered by hand.
- Tasks carry a predecessor field; a shared/superordinate ID links the
  project-structure (geometry) and activity-structure (process) entries.
- Authors explicitly call for *herstellerneutraler Datenaustausch*
  (manufacturer-neutral exchange) — the motivation for an interoperable model.
- Stated limitations: built for high-repetition projects; struggles with
  non-repeating zones, critical trades (drywall), vertical elements; depends on a
  large reference DB and an unbuilt matching algorithm.

## Distinct contribution
The named, peer-reviewed statement of *BIM-integrated, automated* takt production
planning. Not generic 4D visualization — it is takt/Lean-centric.

## Overlap / what it is NOT
Distinct from generic German BIM-4D method papers. The reference-database matching
algorithm is application logic, deliberately **outside** any schema.

## How it shapes taktology (intertwine)
The foundational driver of the whole repo. Feeds:
[`docs/04-bimtakt-background.md`](../../docs/04-bimtakt-background.md) (direct
summary), the `takt:TaktZone`/`WagonType`/`TaktTask` decomposition, and the
quantity→duration rule. The "manufacturer-neutral exchange" call grounds the
interchange-ontology stance in [`docs/03-decisions.md`](../../docs/03-decisions.md).
