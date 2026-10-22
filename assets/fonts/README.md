# Fonts

`noto-serif-sc-subset.woff2` — Noto Serif SC, subset to the site's actual text
(426 characters, weight axis 200–900 kept). Generated from the upstream variable
font; do not edit by hand.

Regenerate after changing any visible copy:

```
python tools/build-cjk-subset.py
```

Character coverage is a snapshot. A character not in the subset falls back to
`Source Han Serif SC` / `SimSun` / system serif, which renders noticeably
different from the subset — if new copy looks like a different typeface, rerun
the script.

Latin text uses EB Garamond and IBM Plex Mono from Google Fonts, loaded
separately in each page's `<head>`.

## License

Noto Serif SC is licensed under the SIL Open Font License 1.1 — see `OFL.txt`.
