# Background — BIMTakt and where this work starts

Source: **Becker & Tschickardt (2023), "BIMTakt — Optimierung der Produktionsplanung
durch ganzheitliche Integration von BIM und Lean Construction."** Open-access,
peer-reviewed (submitted Oct 2022, accepted Jan 2023).

## The paper in brief

A **conceptual model for automatically generating detailed takt plans directly from
a BIM**. Three core components:

1. **Automated takt-zone identification** — a *project-structure* attribute
   (`TaktZone`) finds repeating spatial units against predefined geometric conditions.
2. **Automated task/effort definition** — an *activity-structure* attribute linked to
   a database of completed projects suggests optimal crew sizes (MA/Kol) and
   production rates.
3. **Fully automated takt-plan generation** including variant calculation.

Limitations the authors themselves stress: developed for **high-repetition** projects;
struggles with non-repeating zones, critical trades (drywall), and vertical elements
(shafts, risers, stairwells); the prototype lives inside one vendor's API; and the
whole thing depends on a large, well-prepared reference database plus a
matching algorithm that **still needs to be programmed and trained**. They close by
calling for *herstellerneutraler Datenaustausch* (manufacturer-neutral exchange).

## How the paper automates task definition (the part this repo builds on)

Per takt zone, the **activity structure** holds, for each work step, three values:

- **Quantity** (`Massenwerte`) — computed from a stored formula: floor **area** for a
  2D activity (screed), **volume** for a 3D one. These come from the BIM geometry.
- **Resources** — crew size per column (MA/Kol).
- **Production rate** — person-hours per unit, e.g. `0.58 h/m²` for Estrich.

The resource/effort values are **not** entered by hand — a rule-based algorithm
matches the current building (typology + geometry) against comparable completed
projects in a data store and outputs suggested crew strength and rate. Tasks carry a
`Vorgänger` (predecessor) field, and a shared/superordinate ID links the
project-structure (geometry) and activity-structure (process) entries into a timed
sequence.

## The through-line to this repo

The paper's `TaktZone` / project-structure → **`takt:TaktZone` ⊑ `top:FunctionalZone`**
(geometry). Its activity-structure → **`takt:WagonType` + `takt:TaktTask`**
(predecessor = `hasSuccessor`). Its quantity/duration formula (`actsOn` quantity × rate
÷ crew) sits **outside** this schema — a downstream consumer concern: taktology holds
the structural graph and the element geometry (`top:area`), and a consumer supplies its
own rate/crew model (see [ADR-10](03-decisions.md)).

What the paper leaves as open work (the reference DB, the matching algorithm) stays
out of scope here by design — this repo is the **interchange model** for the result,
not the inference engine that produces the rates.
