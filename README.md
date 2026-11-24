# THE WORLD TODAY — Tuesday 24 November 2026

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/testheroku000012-hub/news-image-20261124-frey/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/testheroku000012-hub/news-image-20261124-frey/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

News-image entry for the make.fun bounty `news-image-20261124`
("Sum up 24 November's world news in one image").
Bounty page: https://make.fun/bounty/news-image-20261124

## Entry

- `entry.png` — 1024×1024 RGB front page, ≤ 1 MiB.
- Hero: **WALL ST ROARS BACK** — Monday 23 Nov verified closes:
  Nasdaq +6.5% (24,089.56), S&P +4.7% (7,237.17), Dow +3.0%
  (49,595.31); Nvidia +31.5% (closed $165.05, +$39.52 from Friday's
  $125.53, best day since 2003) as Jensen Huang returns as CEO.
- Leads: **TRUMP-IRAN STANDOFF** (48-hour Hormuz offer, New Year
  strike line) and **PRABOWO PICKS TWO VPS** (Amran Sulaiman +
  Sugiono, parliament votes 11 Dec).
- Six illustrated small stories: Merkury, Rohingya (ICJ 9–6),
  Shenzhen, GTA VI ($3.79B), Tokyo, Dushanbe.
- Schematic **WHERE IT HAPPENED** map (8 dots), numbered **ALSO ON**
  (5 items), and a **DATE CHECK + SOURCES** footer. Every story
  carries its own date.

## How it is built

- `build.py` draws `entry.png` at build time with Pillow. It is
  the only file that imports Pillow.
- `main.py` is the submitted entry point. It uses only the Python
  standard library (os, struct, sys): it validates the PNG header
  (signature + IHDR 1024×1024, ≤ 1 MiB) and copies `entry.png`
  into `MAKEFUN_OUTPUT_DIR`.

## Verification

- Two-run determinism (PYTHONHASHSEED=0): byte-identical `entry.png`.
- IHDR checked independently before copy (1024×1024, ≤ 1 MiB).
- Clean environment without Pillow: `main.py` runs and reproduces
  the same hash. `python3 -S` passes. No PIL/ImageFont/cv2/numpy
  in `main.py`.
- All market figures are verified Monday closes (Finnhub, Fool,
  AP/CNBC, Reuters, TradingView), not intraday snapshots.

## Rebuild note

This is a from-scratch rebuild (24 Nov 2026, afternoon session) of
the revised 9cc74c7 entry. The earlier build failed the kit check on
`thinking_in_window` (its session started before the competition
opened at 07:00 WIB) and `thinking_reproduces` (its `main.py` was
copied, not authored). This rebuild writes `build.py` and `main.py`
fresh in a session started after the opening, with the same verified
content and layout.
