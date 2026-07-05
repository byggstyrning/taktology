# Taktology visualizer

Three application layers over **one** RDF graph — the point taktology exists to
make: the plan a planner edits, the semantic graph underneath it, and the
building it describes are the *same data*, not three exports that drift apart.

![the three layers](../docs/diagrams/taktology-v0.4.1.png)

## Run it

```bash
# from the repo root
python -m http.server 8000
# then open http://localhost:8000/viz/
```

Or just double-click `viz/index.html` — a snapshot of the demo data is embedded
in the page so it works over `file://` too (browsers block `fetch()` there).

## The three layers

| Layer | What it is | Reads from the graph |
|---|---|---|
| **Takt plan grid** (top) | What a takt-planning app shows the planner: wagons × zones × takts, the coloured flowline. Click a cell to select it; hover for a tooltip. | `takt:Wagon` cells by `performedIn` (row) × `slot` (column), coloured by `instantiates` wagon |
| **Knowledge graph** (left) | The ontology as it actually is — tasks, zones, wagons, crews, elements and the typed edges between them. Drag nodes; **hover** highlights a node and its neighbourhood everywhere. | every `takt:` triple; flow edges are `hasSuccessorSameZone` (Reading A) and `hasSuccessorSameWagon` (Reading B) |
| **3D building** (centre) | An anonymized 3-storey building — structural shell + architectural + MEP fit-out — that **builds up takt-by-takt** as you scrub. Toggle disciplines; orbit/zoom; hover picks zones/elements. | zones tint by the wagon active at the current `slot`; each element appears when the task that `actsOn` it reaches its slot |

The **scrubber** (top bar) is the shared clock: move it and all three layers move
together. **Play** runs the train. Selecting or hovering anything in any layer
highlights it in the other two; selection opens it in the **inspector** (every
triple, both directions), hover shows a tooltip.

## Modes & toggles

- **Wagon modes** — click a wagon chip in the legend to toggle that trade
  everywhere at once: its grid cells fade, its graph nodes and edges dim, and its
  fit-out disappears from the building.
- **Graph panel**: `elements` · `crews` · `process` (the `dtc:Process` node +
  `partOfProcess` edges) · `plan` (the `takt:TaktGraph` node + `dtc:hasProcess`
  membership) — these control both the force view *and* the 3D overlay.
- **Building panel**: `structural` · `architectural` · `MEP` discipline layers,
  plus `graph` — the overlay below.

## The graph overlay (Graph Studio strategy)

The `graph` toggle in the building panel draws the knowledge graph **anchored to
the building**, mirroring the overlay strategy of Graph Studio in
`byggstyrning/nobel-project-hub` (`graph-overlay-positions.ts`):

- nodes with geometry (zones, elements) anchor at their **world centroids**;
- geometry-less nodes are placed **from what they relate to** — tasks fan out
  inside the zone they are `performedIn`;
- organizational nodes (wagons, crews, the process, the plan) stack **north of
  the building footprint** at level gaps proportional to the footprint;
- everything is projected to screen space per frame as an SVG overlay
  (view-scaled dots, typed edge colours), hover/click-able like every other view.

## Where the data comes from

The semantics live in [`examples/takt-building-demo.ttl`](../examples/takt-building-demo.ttl)
(a valid takt plan — it passes `scripts/validate.py`). **Geometry does not** —
coordinates are a side-table in `index.html` keyed by the same element IRIs the
generator emits (`ex:{key}_L{s}_{W|E}`). That mirrors how it works in production:
the ontology carries semantics, **TopologicPy's TGraph carries the coordinates and
computes the quantities** (see [`docs/05-tgraph-pairing.md`](../docs/05-tgraph-pairing.md)).
Swap in a real `TGraph`-built plan and the three layers light up the same way.

## Regenerating the demo

```bash
python scripts/generate_building_demo.py   # rebuild examples/takt-building-demo.ttl
python scripts/embed_viz_data.py           # refresh the file:// snapshot in index.html
python scripts/validate.py                 # confirm the plan still conforms
```

## Dependencies

None to install — [N3.js](https://github.com/rdfjs/N3.js) (Turtle parsing),
[D3](https://d3js.org/) (graph), and [three.js](https://threejs.org/) (3D) load
from a CDN, so an internet connection is needed on first load. No build step.
