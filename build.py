#!/usr/bin/env python3
"""THE WORLD TODAY -- news-image-20261124 v2 (Frey, @il1-bam).

Renders Tuesday 24 November 2026 in one 1024x1024 image. The image is
drawn at 4x (4096x4096) and downsampled with LANCZOS for crisp text.
Build-time only: needs Pillow. The entry point (main.py, stdlib only)
copies the rendered entry.png to the output directory.

Design -- v2 is a major rework of v1 (R3 #13413, 31.40%):
- The hero IS the number: Nvidia +31.5% as a giant condensed figure
  with a rising chart scene beside it, not a text headline.
- The two leads are layered scenes in their own palettes (navy Gulf
  waves + 48 HOURS; red Jakarta ballot + 2).
- Six briefs, each with its own drawn mini-scene and its own date.
- Trust layer: VERIFIED CLOSE tag, DATE CHECK, SOURCES, Tue 24 Nov 2026.

Facts (re-verified 25 Nov 2026 against Finnhub / WSJ / Fool /
MarketWatch / financefeeds): Nvidia closed Mon 23 Nov at $165.05,
+31.48% from Friday's $125.53, best day since 9 May 2003; board
reinstated Jensen Huang as CEO 23 Nov, 11 days after he resigned
12 Nov. Nasdaq Composite +6.51% (24,089.56) -- NOT the Nasdaq-100
(26,746.10, +6.86%); S&P 500 +4.73% (7,237.17), Dow +3.01%
(49,595.31). The +33.8% figure was an intraday print, never the
close -- it is not used anywhere here. Tuesday 24 Nov NVDA fell
to $155.38 (-5.86%, Finnhub/Fool) -- not printed; the hero is
Monday's close, labelled MON throughout (kicker, tag, sub, chart,
indices band), so the Tuesday dateline cannot be misread.
"""
import hashlib
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
S = 4  # supersampling factor; final image is downsampled with LANCZOS

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- fonts
NOTO = "/usr/share/fonts/truetype/noto"
SERIF_BLACK = NOTO + "/NotoSerifDisplay-Black.ttf"
COND_BLACK = NOTO + "/NotoSans-CondensedBlack.ttf"
COND_XBOLD = NOTO + "/NotoSans-CondensedExtraBold.ttf"
SANS_BLACK = NOTO + "/NotoSans-Black.ttf"
SANS_BOLD = NOTO + "/NotoSans-Bold.ttf"
SANS_REG = NOTO + "/NotoSans-Regular.ttf"
FALLBACK = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    """Load a font at supersampled size, falling back to DejaVu."""
    try:
        return ImageFont.truetype(path, size * S)
    except OSError:
        return ImageFont.truetype(FALLBACK, size * S)


def sc(v):
    return v * S


# ---------------------------------------------------------------- palette
PAPER = (247, 242, 230)
INK = (20, 33, 61)
INK_SOFT = (70, 80, 96)
RED = (178, 34, 28)
RED_DEEP = (124, 29, 24)
GREEN = (13, 59, 46)
GREEN_MID = (27, 94, 70)
GREEN_LIGHT = (120, 190, 150)
GOLD = (232, 163, 23)
GOLD_PALE = (245, 205, 110)
CREAM = (250, 246, 235)
CREAM_DIM = (214, 226, 205)
NAVY = (16, 42, 77)
NAVY_LIGHT = (96, 140, 190)
NAVY_PALE = (168, 196, 224)
WHITE = (255, 255, 255)
SLATE = (91, 100, 112)


# ---------------------------------------------------------------- helpers
def wrap(d, text, font, maxw):
    """Greedy word wrap; returns a list of lines that fit maxw."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= maxw * S:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, maxw, text, font, fill, leading, max_lines=None, name=""):
    """Draw wrapped text; returns the y just below the last line."""
    lines = wrap(d, text, font, maxw)
    if max_lines is not None:
        assert len(lines) <= max_lines, (
            "%s: %d lines > %d allowed (%r)" % (name, len(lines), max_lines, text)
        )
    for ln in lines:
        d.text((sc(x), sc(y)), ln, font=font, fill=fill)
        y += leading
    return y


def rrect(d, x0, y0, x1, y1, radius, fill=None, outline=None, width=1):
    d.rounded_rectangle(
        [sc(x0), sc(y0), sc(x1), sc(y1)],
        radius=sc(radius),
        fill=fill,
        outline=outline,
        width=sc(width),
    )


def hline(d, x0, x1, y, fill, width=2):
    d.line([(sc(x0), sc(y)), (sc(x1), sc(y))], fill=fill, width=sc(width))


# ---------------------------------------------------------------- scenes
def paint_chart(d, x0, y0, x1, y1):
    """Rising candlestick + line scene inside the hero, right side."""
    # faint horizontal grid
    for i in range(5):
        gy = y0 + (y1 - y0) * i / 4.0
        d.line([(sc(x0), sc(gy)), (sc(x1), sc(gy))],
               fill=(27, 94, 70), width=sc(1))
    # deterministic climb: closes as fractions of the panel height
    closes = [0.86, 0.82, 0.84, 0.78, 0.74, 0.70, 0.62, 0.55, 0.42, 0.30, 0.16]
    n = len(closes)
    step = (x1 - x0) / float(n)
    pts = []
    for i, c in enumerate(closes):
        cx = x0 + step * (i + 0.5)
        cy = y0 + (y1 - y0) * c
        pts.append((cx, cy))
        # candlestick body + wick
        bw = step * 0.42
        top = y0 + (y1 - y0) * (c - 0.05)
        bot = y0 + (y1 - y0) * (c + 0.05)
        d.line([(sc(cx), sc(y0 + (y1 - y0) * (c - 0.09))),
                (sc(cx), sc(y0 + (y1 - y0) * (c + 0.09)))],
               fill=GREEN_LIGHT, width=sc(2))
        d.rectangle([sc(cx - bw / 2), sc(top), sc(cx + bw / 2), sc(bot)],
                    fill=GREEN_LIGHT)
    # bold gold line over the candles, ending in an arrowhead
    d.line([(sc(px), sc(py)) for px, py in pts], fill=GOLD, width=sc(6),
           joint="curve")
    ex, ey = pts[-1]
    d.polygon([(sc(ex + 26), sc(ey)), (sc(ex - 2), sc(ey - 12)),
               (sc(ex - 2), sc(ey + 12))], fill=GOLD)
    # end dot
    d.ellipse([sc(ex - 9), sc(ey - 9), sc(ex + 9), sc(ey + 9)], fill=GOLD)


def paint_waves(d, x0, y0, x1, y1, color):
    """Three stacked wave lines for the Gulf lead scene."""
    for k in range(3):
        wy = y0 + k * (y1 - y0) / 2.4
        pts = []
        for i in range(41):
            px = x0 + (x1 - x0) * i / 40.0
            py = wy + 7 * math.sin(i * 0.55 + k * 1.3)
            pts.append((sc(px), sc(py)))
        d.line(pts, fill=color, width=sc(3), joint="curve")


def paint_ship(d, x0, y0, x1, y1, color):
    """Small cargo-ship silhouette for the Gulf lead scene."""
    hull = [(x0, y0 + 16), (x1, y0 + 16), (x1 - 8, y1), (x0 + 8, y1)]
    d.polygon([(sc(px), sc(py)) for px, py in hull], fill=color)
    d.rectangle([sc(x0 + 12), sc(y0), sc(x0 + 34), sc(y0 + 16)], fill=color)
    d.rectangle([sc(x0 + 40), sc(y0 + 6), sc(x0 + 58), sc(y0 + 16)], fill=color)


def paint_ballot(d, x0, y0, x1, y1, color):
    """Ballot box with a paper slip for the Jakarta lead scene."""
    d.rectangle([sc(x0), sc(y0 + 18), sc(x1), sc(y1)], fill=color)
    d.line([(sc(x0 + 14), sc(y0 + 18)), (sc(x1 - 14), sc(y0 + 18))],
           fill=(245, 205, 110), width=sc(4))
    d.polygon([(sc(x0 + 22), sc(y0 + 18)), (sc(x0 + 30), sc(y0 - 12)),
               (sc(x0 + 46), sc(y0 - 12)), (sc(x0 + 38), sc(y0 + 18))],
              fill=GOLD_PALE)


def disc_icon(d, cx, cy, r, kind):
    """Per-story mini-scene inside a coloured disc (briefs)."""
    if kind == "ship":
        d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  fill=(24, 68, 120))
        paint_ship(d, cx - r * 0.52, cy - r * 0.28, cx + r * 0.52,
                   cy + r * 0.42, WHITE)
        paint_waves(d, cx - r * 0.62, cy + r * 0.52, cx + r * 0.62,
                    cy + r * 0.72, (168, 196, 224))
    elif kind == "scales":
        d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  fill=(178, 132, 28))
        d.line([(sc(cx), sc(cy - r * 0.55)), (sc(cx), sc(cy + r * 0.55))],
               fill=WHITE, width=sc(3))
        d.line([(sc(cx - r * 0.55), sc(cy - r * 0.30)),
                (sc(cx + r * 0.55), sc(cy - r * 0.30))],
               fill=WHITE, width=sc(3))
        for sx in (cx - r * 0.55, cx + r * 0.55):
            d.line([(sc(sx), sc(cy - r * 0.30)), (sc(sx), sc(cy + r * 0.10))],
                   fill=WHITE, width=sc(2))
            d.arc([sc(sx - r * 0.28), sc(cy - r * 0.12),
                   sc(sx + r * 0.28), sc(cy + r * 0.42)],
                  0, 180, fill=WHITE, width=sc(3))
        d.ellipse([sc(cx - r * 0.14), sc(cy - r * 0.72),
                   sc(cx + r * 0.14), sc(cy - r * 0.44)], fill=WHITE)
    elif kind == "flags":
        d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  fill=(27, 94, 70))
        for i, col in enumerate(((178, 34, 28), (24, 68, 120), WHITE)):
            fx = cx - r * 0.52 + i * r * 0.52
            d.line([(sc(fx), sc(cy - r * 0.55)), (sc(fx), sc(cy + r * 0.55))],
                   fill=WHITE, width=sc(2))
            d.polygon([(sc(fx), sc(cy - r * 0.55)), (sc(fx + r * 0.44),
                       sc(cy - r * 0.38)), (sc(fx), sc(cy - r * 0.20))],
                      fill=col)
    elif kind == "pad":
        d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  fill=(20, 33, 61))
        d.rounded_rectangle(
            [sc(cx - r * 0.58), sc(cy - r * 0.30), sc(cx + r * 0.58),
             sc(cy + r * 0.34)], radius=sc(8), outline=WHITE, width=sc(3))
        d.line([(sc(cx - r * 0.34), sc(cy)), (sc(cx - r * 0.10), sc(cy))],
               fill=WHITE, width=sc(3))
        d.line([(sc(cx - r * 0.22), sc(cy - r * 0.12)),
                (sc(cx - r * 0.22), sc(cy + r * 0.12))],
               fill=WHITE, width=sc(3))
        for bx, by in ((r * 0.22, -r * 0.12), (r * 0.38, r * 0.06),
                       (r * 0.22, r * 0.16)):
            d.ellipse([sc(cx + bx - 3), sc(cy + by - 3),
                       sc(cx + bx + 3), sc(cy + by + 3)], fill=WHITE)
    elif kind == "sun":
        d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  fill=(178, 34, 28))
        for a in range(8):
            ang = math.pi * a / 4.0
            x1 = cx + r * 0.30 * math.cos(ang)
            y1 = cy + r * 0.30 * math.sin(ang)
            x2 = cx + r * 0.52 * math.cos(ang)
            y2 = cy + r * 0.52 * math.sin(ang)
            d.line([(sc(x1), sc(y1)), (sc(x2), sc(y2))], fill=WHITE,
                   width=sc(3))
        d.ellipse([sc(cx - r * 0.26), sc(cy - r * 0.26),
                   sc(cx + r * 0.26), sc(cy + r * 0.26)], fill=WHITE)
    elif kind == "court":
        d.ellipse([sc(cx - r), sc(cy - r), sc(cx + r), sc(cy + r)],
                  fill=(70, 80, 96))
        d.polygon([(sc(cx - r * 0.55), sc(cy - r * 0.10)),
                   (sc(cx), sc(cy - r * 0.55)),
                   (sc(cx + r * 0.55), sc(cy - r * 0.10))], fill=WHITE)
        for i in range(3):
            px = cx - r * 0.36 + i * r * 0.36
            d.line([(sc(px), sc(cy - r * 0.06)), (sc(px), sc(cy + r * 0.42))],
                   fill=WHITE, width=sc(4))
        d.line([(sc(cx - r * 0.55), sc(cy + r * 0.50)),
                (sc(cx + r * 0.55), sc(cy + r * 0.50))],
               fill=WHITE, width=sc(4))


# ---------------------------------------------------------------- content
BRIEFS = [
    ("ship", "MERKURY SUNK",
     "Ukraine sinks a Russian corvette off Benghazi with seven sea drones.",
     "SUN 22 NOV"),
    ("scales", "ROHINGYA: GENOCIDE",
     "ICJ votes 9-6: Myanmar committed genocide; a first.",
     "THU 19 NOV"),
    ("flags", "SHENZHEN: NO DEAL",
     "Trump, Xi and Putin sign a 4-point peace note - no Ukraine, no Iran.",
     "THU 19 NOV"),
    ("pad", "GTA VI: $3.79B",
     "Biggest entertainment launch ever: $3.79B on day one, 32.5M pre-sold.",
     "THU 19 NOV"),
    ("sun", "TOKYO REOPENS",
     "Nikkei resumes after Friday's 5.1% plunge and a Monday holiday.",
     "TUE 24 NOV"),
    ("court", "DUSHANBE QUITS",
     "Tajikistan tells the UN it is leaving the ICC as Putin visits.",
     "FRI 20 NOV"),
]

DATE_CHECK = ("DATE CHECK: Markets - Mon 23 Nov - Gulf - Sun 22-Mon 23 Nov - "
              "Jakarta - Mon 23 Nov - Merkury - Sun 22 Nov - ICJ - Thu 19 Nov - "
              "Shenzhen - Thu 19 Nov - GTA VI - Thu 19 Nov - Tokyo - Tue 24 Nov - "
              "Dushanbe - Fri 20 Nov")
SOURCES = ("SOURCES: REUTERS - AP - AFP - DPA-AFX - HRW - WHITE HOUSE - "
           "TAKE-TWO - MORNINGSTAR - BLOOMBERG LAW - FINNHUB")


# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W * S, H * S), PAPER)
    d = ImageDraw.Draw(img)

    f_title = F(SERIF_BLACK, 58)
    f_kick = F(SANS_BOLD, 20)
    f_kick_sm = F(SANS_BOLD, 16)
    f_date = F(SANS_BOLD, 22)
    f_giant = F(COND_BLACK, 195)
    f_nv = F(SANS_BLACK, 44)
    f_sub = F(SANS_BOLD, 21)
    f_close = F(SANS_REG, 19)
    f_tag = F(SANS_BOLD, 15)
    f_lead = F(SANS_BOLD, 34)
    f_lead_body = F(SANS_REG, 16)
    f_big2 = F(COND_BLACK, 64)
    f_big2_lab = F(SANS_BOLD, 15)
    f_idx_num = F(COND_XBOLD, 30)
    f_idx_lab = F(SANS_BOLD, 15)
    f_sect = F(SANS_BOLD, 24)
    f_head = F(SANS_BOLD, 18)
    f_body = F(SANS_REG, 14)
    f_when = F(SANS_BOLD, 12)
    f_foot = F(SANS_BOLD, 13)
    f_src = F(SANS_REG, 12)

    # ---- masthead
    d.text((sc(12), sc(12)), "THE WORLD IN ONE DAY", font=f_kick, fill=RED)
    d.text((sc(1012), sc(14)), "TUESDAY EDITION", font=f_kick_sm,
           fill=INK_SOFT, anchor="ra")
    d.text((sc(12), sc(30)), "THE WORLD TODAY", font=f_title, fill=INK)
    rrect(d, 788, 30, 1012, 78, 24, fill=RED)
    d.text((sc(900), sc(43)), "TUE 24 NOV 2026", font=f_date, fill=WHITE,
           anchor="ma")
    hline(d, 12, 1012, 88, INK, 2)

    # ---- hero: giant number + chart scene
    rrect(d, 12, 96, 1012, 456, 18, fill=GREEN)
    d.text((sc(40), sc(116)), "MARKETS - WALL STREET - MON 23 NOV",
           font=f_kick, fill=GOLD)
    num = "+31.5%"
    num_w = d.textlength(num, font=f_giant)
    d.text((sc(40), sc(142)), num, font=f_giant, fill=CREAM)
    chart_x0 = 40 + num_w / S + 34
    chart_x1 = 984
    if chart_x1 - chart_x0 > 150:
        paint_chart(d, chart_x0, 150, chart_x1, 400)
        d.text((sc(chart_x0), sc(404)), "FRI $125.53", font=f_close,
               fill=CREAM_DIM)
        d.text((sc(chart_x1), sc(150)), "MON $165.05", font=f_close,
               fill=GOLD_PALE, anchor="ra")
    d.text((sc(40), sc(348)), "NVIDIA", font=f_nv, fill=CREAM)
    d.text((sc(40), sc(398)), "BEST DAY SINCE 2003 - HUANG RETURNS AS CEO",
           font=f_sub, fill=GOLD)
    d.text((sc(40), sc(426)),
           "$165.05 MON CLOSE - FROM $125.53 - +$39.52 - +$950B VALUE",
           font=f_close, fill=CREAM)
    rrect(d, 812, 112, 984, 140, 14, outline=GOLD, width=2)
    d.text((sc(898), sc(118)), "MON 23 NOV CLOSE", font=f_tag, fill=GOLD_PALE,
           anchor="ma")

    # ---- indices band
    idx = [("NASDAQ COMPOSITE", "+6.5%", "24,089.56"),
           ("S&P 500", "+4.7%", "7,237.17"),
           ("DOW", "+3.0%", "49,595.31")]
    bw = (1000 - 2 * 12) / 3.0
    for i, (lab, pct, val) in enumerate(idx):
        x0 = 12 + i * bw
        rrect(d, x0, 464, x0 + bw - 12, 524, 12, fill=INK)
        d.text((sc(x0 + 18), sc(474)), lab, font=f_idx_lab, fill=CREAM_DIM)
        d.text((sc(x0 + 18), sc(490)), pct, font=f_idx_num, fill=CREAM)
        pw = d.textlength(pct, font=f_idx_num) / S
        d.text((sc(x0 + 18 + pw + 12), sc(498)), val, font=f_idx_lab,
               fill=GOLD_PALE)

    # ---- leads: layered scenes
    leads = [
        (12, NAVY, "GULF - HORMUZ - SUN-MON", "TRUMP-IRAN",
         "STANDOFF",
         "Tehran offers Hormuz open in 48 hours; Trump vows strikes "
         "after New Year.",
         "48", "HOURS", "waves"),
        (518, RED_DEEP, "INDONESIA - JAKARTA - MON 23 NOV", "PRABOWO NAMES",
         "TWO VP NOMINEES",
         "Amran Sulaiman and Sugiono named as VP candidates; parliament "
         "votes 11 Dec.",
         "2", "NOMINEES", "ballot"),
    ]
    for x0, bg, tag, h1, h2, body, big, biglab, scene in leads:
        rrect(d, x0, 532, x0 + 494, 716, 14, fill=bg)
        d.text((sc(x0 + 20), sc(546)), tag, font=f_tag, fill=GOLD_PALE)
        d.text((sc(x0 + 20), sc(568)), h1, font=f_lead, fill=CREAM)
        d.text((sc(x0 + 20), sc(604)), h2, font=f_lead, fill=CREAM)
        para(d, x0 + 20, 646, 320, body, f_lead_body, CREAM_DIM, 18,
             max_lines=2, name="lead body")
        # scene zone, right side
        sx0, sx1 = x0 + 348, x0 + 478
        d.text((sc(sx0 + 62), sc(556)), big, font=f_big2, fill=CREAM,
               anchor="ma")
        d.text((sc(sx0 + 62), sc(622)), biglab, font=f_big2_lab,
               fill=GOLD_PALE, anchor="ma")
        if scene == "waves":
            paint_waves(d, sx0, 648, sx1, 700, NAVY_LIGHT)
            paint_ship(d, sx0 + 22, 652, sx0 + 104, 692, NAVY_PALE)
        else:
            paint_ballot(d, sx0 + 30, 656, sx0 + 96, 700, (250, 246, 235))

    # ---- briefs
    d.rectangle([sc(12), sc(730), sc(24), sc(742)], fill=RED)
    d.text((sc(32), sc(724)), "AROUND THE WORLD", font=f_sect, fill=INK)
    cols = [12, 349, 686]
    rows = [752, 845]
    for i, (kind, head, body, when) in enumerate(BRIEFS):
        cx = cols[i % 3]
        cy = rows[i // 3]
        disc_icon(d, cx + 27, cy + 27, 27, kind)
        tx = cx + 62
        d.text((sc(tx), sc(cy + 2)), head, font=f_head, fill=INK)
        para(d, tx, cy + 24, 262, body, f_body, INK_SOFT, 17,
             max_lines=2, name="brief " + head)
        d.text((sc(tx), sc(cy + 62)), when, font=f_when, fill=RED)

    # ---- footer: trust layer
    hline(d, 12, 1012, 946, INK, 2)
    para(d, 12, 954, 1000, DATE_CHECK, f_foot, INK, 16,
         max_lines=2, name="date check")
    d.text((sc(12), sc(992)), SOURCES, font=f_src, fill=SLATE)

    out = img.resize((W, H), Image.LANCZOS)
    path = os.path.join(HERE, "entry.png")
    out.save(path, format="PNG", optimize=True)
    data = open(path, "rb").read()
    assert len(data) <= 1048576, "entry.png too big: %d" % len(data)
    assert out.size == (W, H)
    sha = hashlib.sha256(data).hexdigest()
    print("entry.png %d bytes sha256 %s" % (len(data), sha))
    return path


if __name__ == "__main__":
    render()
