# Diagram generators

The two pictures at the top of the [project README](../README.md) are **rendered from the
repo**, not drawn by hand — both emit transparent PNGs to
[`../docs/diagrams/`](../docs/diagrams/) that read on light or dark GitHub themes:

- [`generate_ontology_diagram.py`](generate_ontology_diagram.py) parses
  [`../ontology/takt.ttl`](../ontology/takt.ttl) (the T-Box). The version label, term
  count, every `⊑` (DTC `subClassOf`) and `≈` (IFC `closeMatch`) alignment, the
  object-property arrows and the datatype footer all come from the Turtle — so bumping
  `owl:versionInfo` and re-running gives a new, in-sync picture.
- [`generate_takt_scheme.py`](generate_takt_scheme.py) reads the demo flowline
  [`../examples/takt-flowline-demo.csv`](../examples/takt-flowline-demo.csv) and lays it
  out as a normal takt board — zones × weeks, one coloured cell per takt task, the
  diagonal *train* cascading floor by floor; the amber marker is the one cell the worked
  A-Box [`../examples/takt-flowline-demo-b5-1.ttl`](../examples/takt-flowline-demo-b5-1.ttl)
  models.

Run from the repo root:

```bash
pip install -r scripts/requirements.txt   # rdflib + Pillow (one-time)
python scripts/generate_ontology_diagram.py
python scripts/generate_takt_scheme.py
```

## They run themselves on commit

A git pre-commit hook ([`../.githooks/pre-commit`](../.githooks/pre-commit)) regenerates
both PNGs and repoints the README image blocks automatically on any commit that touches
the ontology, the demo flowline, or either generator, and re-stages the result — so a
stale diagram can't be committed. The hook ships in the repo, but the `core.hooksPath`
setting lives in `.git/config` (not committed), so enable it **once per clone**:

```bash
git config core.hooksPath .githooks
```

It chains to any globally-configured hook first (e.g. an Aikido secret scan), so enabling
it doesn't disable your global hooks; the [CI guard](../.github/workflows/diagram.yml)
re-checks on push as a backstop.

## They validate as they render

The ontology script **fails** if the ontology grows a class or object property its layout
doesn't place (add the box/arrow in `NODES` / `EDGES`, then re-run); the scheme script
**fails** if the flowline uses a wagon its `WAGONS` colour table doesn't define. Output is
pure Pillow — no SVG rasteriser, Graphviz or browser needed — with fonts bundled under
[`assets/fonts/`](assets/fonts/) so the result is identical on every OS and in CI.
