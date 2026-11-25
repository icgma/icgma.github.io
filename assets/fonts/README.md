# Fonts

All typefaces are self-hosted WOFF2 subsets — zero requests to external CDNs:

- `noto-serif-sc-subset.woff2` — Noto Serif SC variable font (`200–900`), subset
  to the site's actual characters (HTML body, title/meta/aria attributes, and
  `assets/site.js`).
- `eb-garamond-latin.woff2` & `eb-garamond-italic-latin.woff2` — EB Garamond
  variable font (`400–800`, roman & italic), subset to Latin, Greek (`α`, `χ`,
  `κ`…), punctuation, superscripts and arrows.
- `ibm-plex-mono-400-latin.woff2` & `ibm-plex-mono-500-latin.woff2` — IBM Plex
  Mono (`400` & `500`), subset to the same Latin & technical symbol range.

Regenerate the CJK snapshot after changing any visible Chinese copy:

```bash
python tools/build-cjk-subset.py
```

Rebuild both CJK and all Latin subsets from upstream sources:

```bash
python tools/build-cjk-subset.py --all
```

A Chinese character not in the CJK subset falls back to `Source Han Serif SC` /
`SimSun` / system serif, which renders noticeably different from the subset — if
new copy looks like a different typeface, rerun the script.

## License

Noto Serif SC, EB Garamond, and IBM Plex Mono are all licensed under the SIL
Open Font License 1.1 — see `OFL.txt`.
