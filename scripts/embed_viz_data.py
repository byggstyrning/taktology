#!/usr/bin/env python3
# =============================================================================
# embed_viz_data.py
# -----------------------------------------------------------------------------
# Sync the embedded Turtle snapshot inside viz/index.html with
# examples/takt-viz-demo.ttl, so the visualizer keeps working when opened
# straight from disk (file://), where fetch() of the example is blocked.
#
# Run after any edit to the example:
#     python scripts/embed_viz_data.py
# =============================================================================
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TTL = ROOT / "examples" / "takt-building-demo.ttl"
HTML = ROOT / "viz" / "index.html"

BLOCK = re.compile(
    r'(<script id="embeddedTtl" type="text/turtle">\n).*?(</script>)',
    re.DOTALL,
)


def main() -> None:
    ttl = TTL.read_text(encoding="utf-8")
    if "</script" in ttl.lower():
        sys.exit("refusing to embed: TTL contains '</script'")
    html = HTML.read_text(encoding="utf-8")
    if not BLOCK.search(html):
        sys.exit("embed block not found in viz/index.html")
    html = BLOCK.sub(lambda m: m.group(1) + ttl + m.group(2), html, count=1)
    HTML.write_text(html, encoding="utf-8", newline="\n")
    print(f"embedded {TTL.name} ({len(ttl)} chars) into {HTML.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
