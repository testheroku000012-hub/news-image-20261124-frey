# THE WORLD TODAY — news-image-20261124

One front page summing up Tuesday 24 November 2026: Wall Street's roar
back as Nvidia posts its best day since 2003 on Huang's return, the
Trump-Iran Gulf standoff, Prabowo's VP picks, and six stories from
Benghazi to Jakarta — plus a map and a numbered ALSO ON list.

- `entry.png` — the rendered 1024x1024 front page (drawn at build time).
- `build.py` — the Pillow renderer that draws `entry.png` (build-time only).
- `main.py` — the entry point: stdlib-only, validates the PNG header and
  copies `entry.png` to `MAKEFUN_OUTPUT_DIR`.
- `story-list-24nov.md` — the researched story list with sources and dates.
- `PRE_SUBMIT_REPORT.md` — verification results and open gates.

Style note (Nemesis, 24 Nov 04:23 WIB): livelier than the 23 Nov edition —
bigger hero type, a tilted sticker badge, sticker-disc story icons,
number chips, rounded panels, a red date pill.

Build: `python3 build.py` (needs Pillow, local build machine only).
Run: `MAKEFUN_OUTPUT_DIR=out python3 main.py`.
