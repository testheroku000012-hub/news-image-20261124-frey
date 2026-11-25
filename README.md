# THE WORLD TODAY — Tuesday 24 November 2026 (v2 re-entry)

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/testheroku000012-hub/news-image-20261124-frey/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/testheroku000012-hub/news-image-20261124-frey/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

News-image entry for the make.fun bounty `news-image-20261124`
("Sum up 24 November's world news in one image").
Bounty page: https://make.fun/bounty/news-image-20261124

## Entry

- `entry.png` — 1024×1024 RGB front page, ≤ 1 MiB.
- Hero is the NUMBER: **Nvidia +31.5%** as a giant condensed figure
  with a rising candlestick chart scene — closed $165.05, +$39.52
  from Friday's $125.53, best day since 2003, as Jensen Huang
  returns as CEO 11 days after resigning. Verified close, not the
  +33.8% intraday print.
- Indices band: Nasdaq Composite +6.5% (24,089.56), S&P 500 +4.7%
  (7,237.17), Dow +3.0% (49,595.31) — all verified Monday closes.
  (Composite, not the Nasdaq-100 at 26,746.10, +6.86%.)
- Leads as layered scenes in their own palettes:
  **TRUMP-IRAN STANDOFF** (navy, Gulf waves + 48 HOURS — Tehran
  offers Hormuz open in 48 hours; Trump vows strikes after New
  Year) and **PRABOWO PICKS TWO VPS** (red, ballot scene + 2 —
  Amran Sulaiman + Sugiono, parliament votes 11 Dec).
- Six illustrated small stories, each with its own drawn mini-scene
  and date: Merkury, Rohingya (ICJ 9-6), Shenzhen, GTA VI ($3.79B),
  Tokyo, Dushanbe.
- Trust layer: **MON 23 NOV CLOSE** tag (Monday's close, labelled
  MON throughout — kicker, tag, sub, chart, indices band — so the
  Tuesday dateline cannot be misread), **DATE CHECK** (every
  story's own date) and **SOURCES** footer. Dateline Tue 24 Nov 2026.

## How it is built

- `build.py` draws `entry.png` at build time with Pillow, at 4x
  supersampling, downsampled with LANCZOS. It is the only file
  that imports Pillow.
- `main.py` is the submitted entry point. It uses only the Python
  standard library: it validates the PNG (signature, IHDR
  1024×1024, ≤ 1 MiB) and copies `entry.png` into
  `MAKEFUN_OUTPUT_DIR`.

## Verification

- Two-run determinism (PYTHONHASHSEED=0): byte-identical `entry.png`.
- Clean environment without Pillow: `main.py` runs and reproduces
  the same hash. `python3 -S` passes. No PIL/ImageFont/cv2/numpy
  in `main.py`.
- All market figures are verified Monday closes (Finnhub, WSJ,
  Fool, MarketWatch, financefeeds), not intraday snapshots.
- Every name and number in the render was re-checked against
  primary sources before submit.

## Re-entry note

This is a from-scratch v2 re-entry (25 Nov 2026, evening session),
a major rework of the v1 entry (R3 #13413, 31.40%): the hero is
rebuilt around the giant +31.5% number with a chart scene, the
leads are layered scenes instead of flat text panels, and the
schematic map was dropped for denser briefs. Built in a session
started after the competition opened, `build.py` and `main.py`
written fresh here.
