#!/usr/bin/env python3
"""Regenerate self-hosted WOFF2 subsets in assets/fonts/.

By default, rebuilds `noto-serif-sc-subset.woff2` from the site's actual text
(HTML body copy, title/meta/aria attributes, and assets/site.js). If any Latin
subset is missing — or when `--all` is passed — also rebuilds the EB Garamond
(roman + italic variable) and IBM Plex Mono (400 + 500) Latin subsets.

    python tools/build-cjk-subset.py          # CJK snapshot (+ missing Latin)
    python tools/build-cjk-subset.py --all    # rebuild CJK + all Latin subsets

Requires fonttools and brotli:
    pip install fonttools brotli
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "assets" / "fonts"
CACHE_DIR = Path(tempfile.gettempdir()) / "icgma-site-font-cache"

CJK_OUT = FONT_DIR / "noto-serif-sc-subset.woff2"
CJK_SOURCE = (
    "NotoSerifSC[wght].ttf",
    "https://raw.githubusercontent.com/google/fonts/main/ofl/notoserifsc/NotoSerifSC%5Bwght%5D.ttf",
)

LATIN_FONTS = [
    (
        "eb-garamond-latin.woff2",
        "EBGaramond[wght].ttf",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond%5Bwght%5D.ttf",
    ),
    (
        "eb-garamond-italic-latin.woff2",
        "EBGaramond-Italic[wght].ttf",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/ebgaramond/EBGaramond-Italic%5Bwght%5D.ttf",
    ),
    (
        "ibm-plex-mono-400-latin.woff2",
        "IBMPlexMono-Regular.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Regular.ttf",
    ),
    (
        "ibm-plex-mono-500-latin.woff2",
        "IBMPlexMono-Medium.ttf",
        "https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/IBMPlexMono-Medium.ttf",
    ),
]

# Basic Latin, Latin-1 Supplement, Greek (α, χ, κ...), General Punctuation,
# superscripts, arrows (→, ↔, ←), and common mathematical operators.
LATIN_UNICODES = (
    "U+0020-007E,U+00A0-00FF,U+0391-03C9,"
    "U+2010-2027,U+2030-203A,U+2070-209F,"
    "U+2190-2199,U+2200-222B,U+2248,U+2260-2265"
)

LAYOUT_FEATURES = "kern,liga,locl,ccmp"
ATTR_RE = re.compile(
    r'\b(?:data-title-zh|data-title-en|title|aria-label|content)\s*=\s*"([^"]*)"'
)


def site_characters() -> list[str]:
    chars: set[str] = set()
    for page in sorted(ROOT.glob("*.html")):
        raw = page.read_text(encoding="utf-8")
        for attr_val in ATTR_RE.findall(raw):
            chars |= set(html.unescape(attr_val))
        body = re.sub(r"<script.*?</script>|<style.*?</style>", "", raw, flags=re.S)
        body = re.sub(r"<[^>]+>", "", body)
        chars |= set(html.unescape(body))

    js_path = ROOT / "assets" / "site.js"
    if js_path.exists():
        js_text = re.sub(r"/\*.*?\*/|//[^\n]*", "", js_path.read_text(encoding="utf-8"), flags=re.S)
        for lit in re.findall(r"'([^'\\]*(?:\\.[^'\\]*)*)'|\"([^\"\\]*(?:\\.[^\"\\]*)*)\"", js_text):
            chars |= set(lit[0] or lit[1])

    # Characters produced by CSS content and generated text, plus ASCII digits.
    chars |= set("0123456789·×²αχ—–→↔&")
    return sorted(c for c in chars if c.strip())


def fetch_source(filename: str, url: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    target = CACHE_DIR / filename
    if not target.exists() or target.stat().st_size == 0:
        print(f"Downloading {filename} ...")
        urllib.request.urlretrieve(url, target)
    return target


def build_cjk(chars: list[str]) -> None:
    source = fetch_source(*CJK_SOURCE)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as fh:
        fh.write("".join(chars))
        charfile = Path(fh.name)
    try:
        subprocess.run(
            [
                "pyftsubset", str(source),
                f"--text-file={charfile}",
                f"--output-file={CJK_OUT}",
                "--flavor=woff2",
                f"--layout-features={LAYOUT_FEATURES}",
                "--no-hinting",
            ],
            check=True,
        )
    finally:
        charfile.unlink(missing_ok=True)
    print(f"Wrote {CJK_OUT.relative_to(ROOT)}: {len(chars)} characters, {CJK_OUT.stat().st_size / 1024:.1f} KB")


def build_latin(out_name: str, src_name: str, url: str) -> None:
    source = fetch_source(src_name, url)
    out_path = FONT_DIR / out_name
    subprocess.run(
        [
            "pyftsubset", str(source),
            f"--unicodes={LATIN_UNICODES}",
            f"--output-file={out_path}",
            "--flavor=woff2",
            f"--layout-features={LAYOUT_FEATURES}",
        ],
        check=True,
    )
    print(f"Wrote {out_path.relative_to(ROOT)}: {out_path.stat().st_size / 1024:.1f} KB")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Rebuild CJK and all Latin font subsets.")
    args = parser.parse_args()

    chars = site_characters()
    if not chars:
        print("No characters found — check that *.html files exist.", file=sys.stderr)
        return 1

    FONT_DIR.mkdir(parents=True, exist_ok=True)
    build_cjk(chars)

    for out_name, src_name, url in LATIN_FONTS:
        if args.all or not (FONT_DIR / out_name).exists():
            build_latin(out_name, src_name, url)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
