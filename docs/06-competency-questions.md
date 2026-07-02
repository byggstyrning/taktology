# Competency questions — the acceptance suite

**This is the acceptance artifact for the vocabulary.** Each competency question
(CQ) below is a question the ontology exists to answer, paired with a runnable
SPARQL query in `queries/` and its expected result against the two example
A-Boxes. The suite is the executable definition of done: **a change to
`ontology/takt.ttl` or the examples that breaks a CQ is a breaking change** —
either fix the change or version the vocabulary and update the suite
deliberately.

Every query runs against the **merged** graph:

```python
import rdflib
g = rdflib.Graph()
g.parse("ontology/takt.ttl")
g.parse("examples/takt-flowline-demo-b5-1.ttl")   # single zone, generic hasSuccessor edge
g.parse("examples/takt-train-demo.ttl")           # 2 zones, both readings, buffer
g.query(open("queries/cq01-zone-occupancy.rq").read())
```

Plain rdflib, **no reasoner**: the queries are written to work without RDFS
inference (e.g. CQ02 unions the `hasSuccessor` subproperties explicitly, CQ05
checks `bot:adjacentZone` in both directions itself).

The two examples are independent graphs that intentionally reuse names — both
contain a zone labelled `B5:1 (PLAN 5)`, a task labelled `5.1 @ B5:1` and a crew
labelled `SUB-03`, under *different* IRIs. Where that shows up in a result it is
called out, and CQ07 demonstrates why grouping is on IRIs, not labels.

## The suite

| CQ | Question | Why it matters for takt | Query | Expected against the examples |
|---|---|---|---|---|
| CQ01 | Which wagon / task occupies zone Z at slot t? | The plan grid cell lookup — the planner's basic read. | [`cq01-zone-occupancy.rq`](../queries/cq01-zone-occupancy.rq) | 1 row: `6.1 @ B5:1` (Screed) in B5:1 at slot 2 |
| CQ02 | In what order do wagons pull into zone Z? | Reading A / location flow: the cross-trade convoy through one station. | [`cq02-train-order-through-zone.rq`](../queries/cq02-train-order-through-zone.rq) | 7 rows: 5.1 → 6.1 → buffer (train B5:1), 5.1 → 6.1 (C5), 5.1 → 5.2 (flowline B5:1) |
| CQ03 | Where does one wagon (trade) go next, across zones? | Reading B / trade flow: one trade tracked across the building. | [`cq03-trade-flow-across-zones.rq`](../queries/cq03-trade-flow-across-zones.rq) | 2 rows: drywall B5:1 → C5, screed B5:1 → C5 |
| CQ04 | Which element(s) does a task act on? | The operand (`takt:actsOn`) is the trade subset, not the zone total — everything quantity-based reads this edge. | [`cq04-task-operand.rq`](../queries/cq04-task-operand.rq) | 5 rows: 5.1 tasks → gypsum walls, 6.1 tasks → slabs; the buffer acts on nothing |
| CQ05 | Do same-wagon successors sit in adjacent zones? | The topology check ADR-8 re-parented TaktZone under `bot:Zone` for; returns *violations*. | [`cq05-flow-adjacency-check.rq`](../queries/cq05-flow-adjacency-check.rq) | **0 rows** (both hops run B5:1 → C5, which are adjacent) |
| CQ06 | Where are the capacity buffers, per zone? | Capacity buffers are what differentiate takt from LBMS; the plan must surface them. | [`cq06-buffers-per-zone.rq`](../queries/cq06-buffers-per-zone.rq) | 1 row: `buffer @ B5:1` at slot 3 (`isBuffer false` must not match) |
| CQ07 | How many tasks does each crew carry per slot? | Load > 1 in a slot = a double-booked crew — a plan defect. | [`cq07-crew-load-per-slot.rq`](../queries/cq07-crew-load-per-slot.rq) | 5 rows, all load = 1 |
| CQ08 | On what calendar date does each task begin? | Planned dates DERIVE from the plan (ADR-14): `planStart + (slot−1) × taktDuration`. | [`cq08-derived-planned-start.rq`](../queries/cq08-derived-planned-start.rq) | 7 rows; e.g. flowline slot 4 → 2024-01-22, train slot 3 → 2024-03-18 |
| CQ09 | Which tasks belong to which takt plan? | Plan membership is DTC's own `dtc:hasProcess` (ADR-15) — reused, not minted. | [`cq09-plan-membership.rq`](../queries/cq09-plan-membership.rq) | 7 rows: flowline plan holds 2 tasks, train plan holds 5 |
| CQ10 | Which cells are milestones? | Milestone cells are flagged (`isMilestone`), not subclassed, mirroring `IfcTask.IsMilestone`. | [`cq10-milestones.rq`](../queries/cq10-milestones.rq) | **0 rows** (no milestone in the examples; `isMilestone false` must not match) |

## Derived vs asserted dates (ADR-14)

CQ08 is the suite's load-bearing design check. Per-task calendar dates are
**never asserted** in a taktology A-Box — the grid derives them from two facts
on the `takt:TaktGraph`:

```
task start = takt:planStart + (takt:slot − 1) × takt:taktDuration
```

`dtc:startTime`/`dtc:endTime` are **as-performed observations** in DTC and must
never carry planned dates. Engine note: SPARQL/XPath date arithmetic is defined
over `xsd:dayTimeDuration`; rdflib 7.6 evaluates `xsd:date + xsd:dayTimeDuration`
but not a computed `xsd:duration`, so cq08 extracts the day count from the
(day-valued, per `takt:taktDuration` policy — `P7D`, never `P1W`) duration
literal, scales it, and rebuilds a `dayTimeDuration`. On an engine without
duration arithmetic, the query still returns the components (`?planStart`,
`?slot`, `?offsetDays`) to apply the formula downstream.

## Actual results

Verified 2026-07-01 with Python 3.13 / rdflib 7.6.0 against
`ontology/takt.ttl` + both examples merged (294 triples). These tables are the
expected output; re-run after any ontology or example change.

### CQ01 — zone occupancy (1 row)

| task | taskLabel | wagonLabel |
|---|---|---|
| `train#t_61_B51` | 6.1 @ B5:1 | Screed |

### CQ02 — train order through a zone (7 rows)

| zoneLabel | slot | taskLabel |
|---|---|---|
| B5:1 (PLAN 5) | 1 | 5.1 @ B5:1 |
| B5:1 (PLAN 5) | 2 | 6.1 @ B5:1 |
| B5:1 (PLAN 5) | 3 | buffer @ B5:1 |
| B5:1 (PLAN 5) | 4 | 5.1 @ B5:1 |
| B5:1 (PLAN 5) | 5 | 5.2 @ B5:1 |
| C5 (PLAN 5) | 2 | 5.1 @ C5 |
| C5 (PLAN 5) | 3 | 6.1 @ C5 |

Slots 1–3 are the train demo's B5:1 convoy (via `hasSuccessorSameZone`);
slots 4–5 are the flowline demo's *distinct* zone with the same label, reached
through the generic-`hasSuccessor` fallback.

### CQ03 — trade flow across zones (2 rows)

| wagonLabel | fromZoneLabel | fromSlot | toZoneLabel | toSlot |
|---|---|---|---|---|
| Drywall — first-side boarding | B5:1 (PLAN 5) | 1 | C5 (PLAN 5) | 2 |
| Screed | B5:1 (PLAN 5) | 2 | C5 (PLAN 5) | 3 |

### CQ04 — task operand (5 rows)

| taskLabel | elementLabel |
|---|---|
| 5.1 @ B5:1 | Gypsum wall set, B5:1 |
| 5.1 @ B5:1 | Gypsum walls, B5:1 |
| 5.1 @ C5 | Gypsum walls, C5 |
| 6.1 @ B5:1 | Floor slab, B5:1 |
| 6.1 @ C5 | Floor slab, C5 |

The first two rows are the flowline-demo and train-demo tasks that share the
label `5.1 @ B5:1`. Each task reads *its* elements only — the slab sharing the
drywall task's zone does not appear on the drywall rows.

### CQ05 — flow-adjacency check (0 rows)

Empty result = no violations: every `hasSuccessorSameWagon` hop crosses a
`bot:adjacentZone` boundary (checked in both directions, since the train demo
asserts adjacency one way only).

### CQ06 — buffers per zone (1 row)

| zoneLabel | taskLabel | slot |
|---|---|---|
| B5:1 (PLAN 5) | buffer @ B5:1 | 3 |

### CQ07 — crew load per slot (5 rows)

| crewLabel | slot | load |
|---|---|---|
| SUB-03 | 1 | 1 |
| SUB-03 | 2 | 1 |
| SUB-03 | 4 | 1 |
| SUB-07 | 2 | 1 |
| SUB-07 | 3 | 1 |

All loads are 1 — nobody double-booked. The slot-4 `SUB-03` is the flowline
demo's own crew IRI; grouping on the IRI keeps the two `SUB-03`s apart.

### CQ08 — derived planned start (7 rows)

| taskLabel | slot | planStart | taktDuration | offsetDays | derivedStart |
|---|---|---|---|---|---|
| 5.1 @ B5:1 | 4 | 2024-01-01 | P7D | 21 | 2024-01-22 |
| 5.2 @ B5:1 | 5 | 2024-01-01 | P7D | 28 | 2024-01-29 |
| 5.1 @ B5:1 | 1 | 2024-03-04 | P7D | 0 | 2024-03-04 |
| 5.1 @ C5 | 2 | 2024-03-04 | P7D | 7 | 2024-03-11 |
| 6.1 @ B5:1 | 2 | 2024-03-04 | P7D | 7 | 2024-03-11 |
| 6.1 @ C5 | 3 | 2024-03-04 | P7D | 14 | 2024-03-18 |
| buffer @ B5:1 | 3 | 2024-03-04 | P7D | 14 | 2024-03-18 |

No date is asserted on any task; every `derivedStart` is computed by the query.
The buffer gets a date like any other cell — it occupies its slot.

### CQ09 — plan membership (7 rows)

| planLabel | taskLabel |
|---|---|
| Takt-flowline demo plan | 5.1 @ B5:1 |
| Takt-flowline demo plan | 5.2 @ B5:1 |
| Train demo plan | 5.1 @ B5:1 |
| Train demo plan | 5.1 @ C5 |
| Train demo plan | 6.1 @ B5:1 |
| Train demo plan | 6.1 @ C5 |
| Train demo plan | buffer @ B5:1 |

### CQ10 — milestones (0 rows)

Empty result: neither example contains a milestone cell, and the flowline
demo's explicit `isMilestone false` correctly does not match. The query is the
reusable pattern for real plans.
