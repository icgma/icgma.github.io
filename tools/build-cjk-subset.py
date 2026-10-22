#!/usr/bin/env python3
"""Regenerate assets/fonts/noto-serif-sc-subset.woff2 from the site's actual text.

Run this after changing any copy in *.html. The subset keeps only the glyphs the
site uses; characters added later but not in the subset fall back to a system
serif, which looks visibly different next to the subset text.

    python tools/build-cjk-subset.py

Requires fonttools and brotli:
    pip install fonttools brotli
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = sorted(ROOT.glob("*.html"))
OUT = ROOT / "assets" / "fonts" / "noto-serif-sc-subset.woff2"
SOURCE_URL = (
    "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifsc/"
    "NotoSerifSC%5Bwght%5D.ttf"
)
# Subset must retain these OpenType features. kern/liga/locl/ccmp cover Latin
# kerning, CJK ligatures, localized forms and glyph composition. Dropping the
# rest (vert, palt, ruby, hist, ...) saves ~50 KB; none are used by this site.
LAYOUT_FEATURES = "kern,liga,locl,ccmp"


def site_characters() -> list[str]:
    chars: set[str] = set()
    for page in PAGES:
        text = page.read_text(encoding="utf-8")
        text = re.sub(r"<script.*?</script>|<style.*?</style>", "", text, flags=re.S)
        text = re.sub(r"<[^>]+>", "", text)
        chars |= set(html.unescape(text))
    # Characters produced by CSS content and generated text, plus ASCII digits.
    chars |= set("0123456789·×²αχ—–→↔&")
    return sorted(c for c in chars if c.strip())


def build(chars: list[str], source: Path, output: Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as fh:
        fh.write("".join(chars))
        charfile = Path(fh.name)
    try:
        subprocess.run(
            [
                "pyftsubset", str(source),
                f"--text-file={charfile}",
                f"--output-file={output}",
                "--flavor=woff2",
                f"--layout-features={LAYOUT_FEATURES}",
                "--no-hinting",
            ],
            check=True,
        )
    finally:
        charfile.unlink(missing_ok=True)


def main() -> int:
    chars = site_characters()
    if not chars:
        print("No characters found — check that *.html files exist.", file=sys.stderr)
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "NotoSerifSC[wght].ttf"
        print(f"Downloading source font ({SOURCE_URL.rsplit('/', 1)[-1]}) ...")
        urllib.request.urlretrieve(SOURCE_URL, source)
        build(chars, source, OUT)
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(chars)} characters, {OUT.stat().st_size / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
