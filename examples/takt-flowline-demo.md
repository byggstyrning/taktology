# Takt flowline — anonymized pattern

A small, **fully anonymized** slice of a real takt production plan
(*Produktionstidplan*), kept here as a concrete pattern to discuss the
[ontology](../ontology/takt.ttl) against. It is the companion *source* for the
worked A-Box in [`takt-flowline-demo-b5-1.ttl`](takt-flowline-demo-b5-1.ttl); for
the multi-zone **train** (both successor readings, buffers), see
[`takt-train-demo.ttl`](takt-train-demo.ttl).

Files:

| File | What |
|------|------|
| [`takt-flowline-demo.xlsx`](takt-flowline-demo.xlsx) | Workbook: `Wagons`, `Zones`, `Flowline`, `Legend` sheets, trade-coloured. |
| [`takt-flowline-demo.csv`](takt-flowline-demo.csv) | The flowline matrix (zone × takt week), machine-readable. |

### What was anonymized

- Project / client / estate names, project number, and named third-party firms — **removed**.
- Subcontractor codes — remapped **1:1** to neutral `SUB-01…SUB-20` (so the flowline relationships stay intact).
- Swedish activity text — replaced with **generic English trade labels**.
- The real calendar — replaced with **relative takt weeks** `T01…`; buffers (gaps) preserved.
- Wagon ids and zone coordinates are generic and **kept** — they carry the structure, not the identity.

Nothing from the source flows through verbatim except generic wagon ids and zone
coordinates; the artifact is rebuilt entirely from a controlled mapping.

---

## 1. The takt train (wagon catalog)

One row = one **`takt:WagonType`**: a reusable work package the train repeats in
every zone. The beat (`takt:taktDuration`) is **one week**. `Crew` is the
anonymized responsible actor; `Unit` is the quantity kind (area / count) work would
be metered against — a downstream concern, not part of the takt schema.

| Wagon | Crew | Activity (generic trade) | Unit |
|:-----:|:----:|--------------------------|:----:|
| 3 | SUB-01 | Survey & layout — wall set-out | AREA |
| 3 | SUB-02 | Core drilling — penetrations | COUNT |
| 5.1 | SUB-03 | Drywall — first-side boarding | AREA |
| 5.2 | SUB-04 | MEP in-wall — conduit & pipework | AREA |
| 5.3 | SUB-03 | Drywall — second-side / close-up | AREA |
| 6.1 | SUB-06 | Painting — filling & first coat | AREA |
| 7 | SUB-07 | Suspended ceiling — grid & boards | AREA |
| 8 | SUB-08 | Sprinkler — mains & drops | AREA |
| 9 | SUB-09 | Ventilation — ducts & terminals | AREA |
| 10 | SUB-05 | Plumbing — mains, branches, pressure test | AREA |
| 11.1 | SUB-04 | Electrical — cable trays / close-up | AREA |
| 12.1 | SUB-04 | Electrical — cabling & distribution boards | AREA |
| 13 | SUB-04 | Electrical — data & fire-alarm cabling | AREA |
| 14 | SUB-11 | BMS / security / IT — cabling | AREA |
| 17.1 | SUB-06 | Painting & tiling — wet rooms, final coats | AREA |
| 18 | SUB-14 | Flooring — levelling & finishes | AREA |
| 20.1 | SUB-16 | Joinery — kitchenette, doors, trims | COUNT |
| 21 | SUB-11 | MEP / BMS — fit-out completion | AREA |
| 22 | SUB-04 | Commissioning — electrical & controls | AREA |
| 23 | SUB-19 | Final cleaning & handover | AREA |

## 2. The takt zones (building B)

Six **`takt:TaktZone`** instances — coordinate is `building : floor : sub-zone`.
Areas are illustrative (real areas are TopologicPy-computed quantities carried as
TGraph dictionary values — see [docs/05-tgraph-pairing.md](../docs/05-tgraph-pairing.md)).

| Zone | Floor | Sub-zone | Area m² *(illustrative)* |
|:----:|:-----:|:--------:|:----:|
| B5:1 | Plan 5 | 1 | 184 |
| B5:2 | Plan 5 | 2 | 176 |
| B4:1 | Plan 4 | 1 | 179 |
| B4:2 | Plan 4 | 2 | 181 |
| B2:1 | Plan 2 | 1 | 171 |
| B2:2 | Plan 2 | 2 | 168 |

## 3. The flowline

Each filled cell is a **`takt:TaktTask`** — one occurrence of a wagon, in one
zone, in one takt week. Read it as a train: the same wagon walks zone-to-zone,
and the building fills floor-by-floor (Plan 5 → 4 → 2). The week each zone is
*entered* (wagon 3 arrives) shows the cascade:

| Wagon 3 enters | B5:1 | B5:2 | B4:1 | B4:2 | B2:1 | B2:2 |
|:--------------:|:----:|:----:|:----:|:----:|:----:|:----:|
| takt week | T01 | T06 | T23 | T23 | T28 | T28 |

### Floor 5 in detail

The full wagon sequence for the two Plan-5 zones, week by week. Blanks are
**buffers** — deliberate slack between trades, not missing data. (The complete
6-zone × 59-week matrix is in the `.xlsx` / `.csv`.)

| Takt week | B5:1 | B5:2 |
|:---------:|:----:|:----:|
| T01 | 3 | |
| T02 | | |
| T03 | | |
| T04 | 5.1 | |
| T05 | 5.2 | |
| T06 | 5.3 | 3 |
| T07 | 6.1 | |
| T08 | 7 | 5.1 |
| T09 | 8 | 5.2 |
| T10 | 9 | 5.3 |
| T11 | 9 | 6.1 |
| T12 | 10 | 7 |
| T13 | 10 | 8 |
| T14 | 11.1 | 9 |
| T15 | 12.1 | 9 |
| T16 | 13 | 10 |
| T17 | 14 | 10 |
| T18 | 17.1 | 11.1 |
| T19 | 21 | 12.1 |
| T20 | 18 | 13 |
| T21 | | |
| T22 | 18 | |
| T23 | | 14 |
| T24 | | 17.1 |
| T25 | 20.1 | 21 |
| T26 | 22 | |
| T27 | 23 | |
| T28 | 23 | |

---

## How it maps to the ontology

A single coloured cell — say **wagon `5.1` in zone `B5:1` at `T04`** — becomes:

```
WagonType  5.1  ──instantiates──▶  TaktTask
                                     ├─ performedIn  ▶ TaktZone  B5:1
                                     ├─ actsOn       ▶ Element   (the operand → quantity)
                                     ├─ performedBy  ▶ Crew      SUB-03
                                     ├─ slot         ▶ 4         (T04; the plan carries taktDuration P7D + planStart)
                                     └─ hasSuccessorSameZone ▶ TaktTask  5.2 @ B5:1   (the train edge)
```

- **The chain *is* the train.** `hasSuccessorSameZone` walks down a zone column
  (5.1 → 5.2 → 5.3 …); its sibling `hasSuccessorSameWagon` tracks one wagon
  zone-to-zone. Both specialize the reading-agnostic `hasSuccessor`.
- **Duration is a consumer concern, not in the schema:** a consumer reads the operand's
  area off `actsOn` (a TGraph dictionary value — see
  [docs/05-tgraph-pairing.md](../docs/05-tgraph-pairing.md)) and applies its own
  rate/crew model to check the work fits the one-week beat
  (see [ADR-10](../docs/03-decisions.md)). The structural mapping is what the A-Box
  [`takt-flowline-demo-b5-1.ttl`](takt-flowline-demo-b5-1.ttl) shows.
- **Buffers** (the blanks) are first-class in takt — and, since v0.5.0, in the
  vocabulary: an empty cell is a `TaktTask` with `takt:isBuffer true`
  (see [ADR-16](../docs/03-decisions.md) and [`takt-train-demo.ttl`](takt-train-demo.ttl)).

### Worth discussing

- One **wagon id with two crews** (e.g. `3` = survey *and* core-drilling) — is a wagon a
  single `WagonType`, or a bundle of parallel sub-tasks sharing a slot?
- The `5.1 / 5.2 / 5.3` **sub-takt** numbering — a wagon that internally splits across trades.
- Zones on a floor are entered several takts apart, not one — the real stagger is messier than
  the textbook "one zone per takt"; does the model need to capture per-zone start offsets?
