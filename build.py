#!/usr/bin/env python3
"""Build entry.png for news-image-20261124 — THE WORLD TODAY, Tuesday 24 Nov 2026.

Fresh PIL drawing (new layout, nothing copied from the 23 Nov renderer).
A 1024x1024 front page: masthead, three leads in three palettes (Wall St
rebound, Gulf standoff, Jakarta VP picks), six illustrated small stories,
a schematic WHERE IT HAPPENED map, a numbered ALSO ON list, and a
DATE CHECK + SOURCES footer. Style per Nemesis 24 Nov 04:23 WIB ("too
stiff" note): bolder type, tilted sticker badge, sticker-disc icons,
number chips, rounded panels, red date pill — lively, not rigid.
Revision (24 Nov ~12:45 WIB, team QA lock): Nvidia hero corrected to
the verified Monday close (+31.5%, best day since 2003 — the +33.8%
was an intraday snapshot); indices corrected to verified closes
(Nasdaq +6.5%, S&P +4.7%, Dow +3.0%); COP31 de-duped out (it is the
hero of the 23 Nov edition); Lead 2 is now the Trump-Iran standoff,
Lead 3 the Jakarta VP picks; small stories trimmed 10 -> 6.
Deterministic: fixed fonts, fixed layout, no randomness, no timestamps.
"""
import hashlib
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (245, 240, 230)
INK = (20, 32, 46)
NAVY = (16, 35, 59)
RED = (196, 58, 42)
DARKRED = (122, 30, 22)
GREEN = (30, 77, 51)
ORANGE = (232, 120, 36)
GOLD = (217, 164, 65)
CARD = (253, 252, 247)
BORDER = (201, 194, 178)
MUTED = (90, 100, 112)
OCEAN = (205, 222, 232)
LAND = (233, 219, 172)
SKY = (46, 111, 142)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def text_w(draw, text, f):
    return draw.textlength(text, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, max_w, lines, f, fill, leading=None, spacing=0):
    """Draw wrapped lines inside a box; returns bottom y."""
    lh = leading if leading is not None else int(f.size * 1.25)
    for i, line in enumerate(lines):
        draw.text((x, y + i * (lh + spacing)), line, font=f, fill=fill)
    return y + len(lines) * (lh + spacing)


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def fit_check(name, used_bottom, limit):
    if used_bottom > limit:
        raise SystemExit(f"FIT FAIL {name}: bottom {used_bottom} > limit {limit}")


def save_png(img, path):
    img.save(path, format="PNG", optimize=True)
    data = open(path, "rb").read()
    print("SIZE", len(data), "bytes; <=1MiB:", len(data) <= 1024 * 1024)
    print("SHA256", hashlib.sha256(data).hexdigest())
    print("MODE", img.mode, "DIMS", img.size)


def draw_masthead(draw):
    x0, x1 = 36, 988
    draw.rectangle([x0, 18, x1, 22], fill=RED)
    draw.text((x0, 26), "THE WORLD IN ONE DAY", font=SANS_B(15), fill=RED)
    right = "TUESDAY EDITION"
    draw.text((x1 - text_w(draw, right, SANS_B(14)), 28), right,
              font=SANS_B(14), fill=MUTED)
    draw.text((x0, 48), "THE WORLD TODAY", font=SERIF_B(54), fill=INK)
    date = "TUESDAY 24 NOV 2026"
    dw = text_w(draw, date, SANS_B(21))
    draw.rounded_rectangle([x1 - dw - 24, 66, x1, 100], radius=17, fill=RED)
    draw.text((x1 - dw - 12, 74), date, font=SANS_B(21),
              fill=(255, 255, 255))
    rule(draw, x0, 112, x1, 3)
    rule(draw, x0, 117, x1, 1, fill=GOLD)
    fit_check("masthead", 119, 124)


def rotated_badge(img, cx, cy, w, h, text, angle, bg, fg):
    """A tilted sticker pill, rendered on its own layer then rotated."""
    badge = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
    bd = ImageDraw.Draw(badge)
    bd.rounded_rectangle([w // 2, h // 2, w // 2 + w, h // 2 + h],
                         radius=h // 2, fill=bg)
    f = SANS_B(15)
    tw = bd.textlength(text, font=f)
    bd.text((w // 2 + (w - tw) / 2, h // 2 + (h - 15) / 2), text, font=f,
            fill=fg)
    badge = badge.rotate(angle, resample=Image.BICUBIC, center=(w, h))
    img.paste(badge, (cx - w, cy - h), badge)


def draw_hero(draw):
    x0, y0, x1, y1 = 36, 126, 640, 400
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=GREEN)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, outline=GOLD,
                           width=2)
    tx = x0 + 26
    draw.text((tx, y0 + 14), "MARKETS  ·  WALL STREET  ·  MON 23 NOV",
              font=SANS_B(14), fill=GOLD)
    draw.text((tx, y0 + 32), "WALL ST", font=SERIF_B(58), fill=(255, 255, 255))
    draw.text((tx, y0 + 94), "ROARS BACK", font=SERIF_B(58), fill=(255, 255, 255))
    deck = ("Stocks storm back from Friday's rout as Nvidia posts its "
            "best day since 2003 on Huang's comeback.")
    lines = wrap(draw, deck, SANS(16), 552)
    end = para(draw, tx, y0 + 156, 552, lines, SANS(16), (224, 236, 228),
               leading=19)
    rows = [("Nasdaq", "+6.5%", 6.5), ("S&P 500", "+4.7%", 4.7),
            ("Dow", "+3.0%", 3.0)]
    bx, bw_max = tx + 104, 250
    y = end + 6
    for label, val, mag in rows:
        draw.text((tx, y), label, font=SANS_B(15), fill=(255, 255, 255))
        bar_w = int(bw_max * mag / 6.5)
        draw.rectangle([bx, y + 2, bx + bar_w, y + 15], fill=(120, 200, 140))
        draw.text((bx + bw_max + 10, y), val, font=SANS_B(15),
                  fill=(255, 255, 255))
        y += 18
    draw.text((tx, y + 2), "NVIDIA +31.5%  ·  HUANG BACK 11 DAYS AFTER QUITTING  ·  10-YR 4.94%",
              font=SANS_B(13), fill=GOLD)
    fit_check("hero", y + 16, y1)


def draw_lead2(draw):
    x0, y0, x1, y1 = 652, 126, 988, 256
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=NAVY)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, outline=GOLD,
                           width=2)
    tx = x0 + 18
    draw.text((tx, y0 + 12), "GULF  ·  HORMUZ  ·  SUN–MON",
              font=SANS_B(12), fill=GOLD)
    draw.text((tx, y0 + 28), "TRUMP-IRAN", font=SERIF_B(28),
              fill=(255, 255, 255))
    draw.text((tx, y0 + 58), "STANDOFF", font=SERIF_B(28),
              fill=(255, 255, 255))
    deck = ("Tehran offers Hormuz open in 48 hours; Trump vows strikes "
            "after New Year.")
    lines = wrap(draw, deck, SANS(13), x1 - x0 - 36)
    end = para(draw, tx, y0 + 90, x1 - x0 - 36, lines, SANS(13),
               (216, 224, 232), leading=16)
    fit_check("lead2", end, y1)


def draw_lead3(draw):
    x0, y0, x1, y1 = 652, 268, 988, 400
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=DARKRED)
    draw.rounded_rectangle([x0, y0, x1, y1], radius=8, outline=GOLD,
                           width=2)
    tx = x0 + 18
    draw.text((tx, y0 + 12), "INDONESIA  ·  JAKARTA  ·  MON 23 NOV",
              font=SANS_B(12), fill=GOLD)
    draw.text((tx, y0 + 28), "PRABOWO PICKS", font=SERIF_B(28),
              fill=(255, 255, 255))
    draw.text((tx, y0 + 58), "TWO VPS", font=SERIF_B(28),
              fill=(255, 255, 255))
    deck = ("Amran Sulaiman and Sugiono named as VP candidates; "
            "parliament votes 11 Dec.")
    lines = wrap(draw, deck, SANS(13), x1 - x0 - 36)
    end = para(draw, tx, y0 + 90, x1 - x0 - 36, lines, SANS(13),
               (240, 222, 216), leading=16)
    fit_check("lead3", end, y1)


def draw_icon(draw, kind, x, y, color):
    """Small 36x36 pictogram: white glyph on a coloured sticker disc."""
    draw.ellipse([x, y, x + 36, y + 36], fill=color)
    c = (253, 252, 247)
    if kind == "ship":
        draw.polygon([(x + 2, y + 22), (x + 34, y + 22), (x + 28, y + 32),
                      (x + 8, y + 32)], fill=c)
        draw.line([(x + 18, y + 22), (x + 18, y + 6)], fill=c, width=3)
        draw.polygon([(x + 18, y + 6), (x + 30, y + 18), (x + 18, y + 18)],
                     fill=c)
        draw.line([(x + 2, y + 34), (x + 34, y + 34)], fill=c, width=2)
    elif kind == "ballot":
        draw.rectangle([x + 4, y + 12, x + 32, y + 32], outline=c, width=3)
        draw.line([(x + 12, y + 12), (x + 24, y + 12)], fill=c, width=3)
        draw.line([(x + 10, y + 22), (x + 16, y + 28), (x + 28, y + 14)],
                  fill=c, width=3)
    elif kind == "scales":
        draw.line([(x + 18, y + 4), (x + 18, y + 30)], fill=c, width=3)
        draw.line([(x + 6, y + 10), (x + 30, y + 10)], fill=c, width=3)
        draw.polygon([(x + 2, y + 10), (x + 10, y + 10), (x + 6, y + 18)],
                     outline=c, width=2)
        draw.polygon([(x + 26, y + 10), (x + 34, y + 10), (x + 30, y + 18)],
                     outline=c, width=2)
        draw.line([(x + 10, y + 30), (x + 26, y + 30)], fill=c, width=3)
    elif kind == "flags":
        for i, fx in enumerate((x + 6, x + 16, x + 26)):
            draw.line([(fx, y + 6), (fx, y + 32)], fill=c, width=2)
            draw.polygon([(fx, y + 6), (fx + 9, y + 10), (fx, y + 14)],
                         fill=c)
    elif kind == "pad":
        draw.rounded_rectangle([x + 3, y + 10, x + 33, y + 28], radius=8,
                               outline=c, width=3)
        draw.line([(x + 9, y + 19), (x + 15, y + 19)], fill=c, width=2)
        draw.line([(x + 12, y + 16), (x + 12, y + 22)], fill=c, width=2)
        draw.ellipse([x + 22, y + 15, x + 25, y + 18], fill=c)
        draw.ellipse([x + 27, y + 19, x + 30, y + 22], fill=c)
    elif kind == "car":
        draw.polygon([(x + 6, y + 20), (x + 10, y + 12), (x + 22, y + 12),
                      (x + 28, y + 20)], fill=c)
        draw.rectangle([x + 4, y + 20, x + 32, y + 26], fill=c)
        draw.ellipse([x + 8, y + 25, x + 14, y + 31], fill=INK)
        draw.ellipse([x + 22, y + 25, x + 28, y + 31], fill=INK)
    elif kind == "chart":
        draw.line([(x + 4, y + 30), (x + 32, y + 30)], fill=c, width=2)
        draw.rectangle([x + 6, y + 22, x + 11, y + 30], fill=c)
        draw.rectangle([x + 14, y + 16, x + 19, y + 30], fill=c)
        draw.rectangle([x + 22, y + 9, x + 27, y + 30], fill=c)
        draw.line([(x + 4, y + 14), (x + 32, y + 4)], fill=c, width=2)
        draw.polygon([(x + 32, y + 4), (x + 26, y + 4), (x + 32, y + 10)],
                     fill=c)
    elif kind == "hippo":
        draw.ellipse([x + 3, y + 14, x + 27, y + 30], fill=c)
        draw.ellipse([x + 21, y + 8, x + 33, y + 20], fill=c)
        draw.ellipse([x + 22, y + 5, x + 26, y + 9], fill=c)
        draw.ellipse([x + 29, y + 12, x + 31, y + 14], fill=INK)
    elif kind == "court":
        draw.polygon([(x + 4, y + 12), (x + 18, y + 4), (x + 32, y + 12)],
                     fill=c)
        for cx in (x + 8, x + 16, x + 24):
            draw.line([(cx, y + 14), (cx, y + 28)], fill=c, width=3)
        draw.rectangle([x + 4, y + 28, x + 32, y + 32], fill=c)
    elif kind == "shield":
        draw.polygon([(x + 18, y + 4), (x + 31, y + 9), (x + 31, y + 20),
                      (x + 18, y + 32), (x + 5, y + 20), (x + 5, y + 9)],
                     outline=c, width=3)
        draw.line([(x + 12, y + 18), (x + 17, y + 23), (x + 25, y + 13)],
                  fill=c, width=3)


SMALL = [
    ("ship", "MERKURY SUNK", "Ukraine sinks a Russian corvette off "
     "Benghazi with seven sea drones.", "SUN 22 NOV", RED),
    ("scales", "ROHINGYA: GENOCIDE", "World court rules 9–6 that Myanmar "
     "committed genocide; a first.", "THU 19 NOV", NAVY),
    ("flags", "SHENZHEN: NO DEAL", "Trump, Xi and Putin sign a 4-point "
     "peace note — no Ukraine, no Iran.", "THU 19 NOV", RED),
    ("pad", "GTA VI: $3.79B", "Biggest entertainment launch ever: $3.79B "
     "on day one, 32.5M pre-sold.", "THU 19 NOV", GREEN),
    ("chart", "TOKYO REOPENS", "Nikkei resumes after Friday's 5.1% "
     "plunge and a Monday holiday.", "TUE 24 NOV", RED),
    ("court", "DUSHANBE QUITS", "Tajikistan tells the UN it is leaving "
     "the ICC as Putin visits.", "FRI 20 NOV", RED),
]


def draw_small(draw):
    x0, y0, x1 = 36, 412, 988
    draw.rectangle([x0 - 14, y0 + 2, x0 - 4, y0 + 12], fill=RED)
    draw.text((x0, y0), "AROUND THE WORLD", font=SANS_B(17), fill=INK)
    rule(draw, x0, y0 + 22, x1, 2)
    col_w, gap = 306, 16
    gy = y0 + 32
    bottom = gy
    for row in range(2):
        row_h = 0
        for col in range(3):
            idx = row * 3 + col
            kind, head, body, date, color = SMALL[idx]
            bx = x0 + col * (col_w + gap)
            draw_icon(draw, kind, bx, gy, color)
            draw.text((bx, gy + 40), head, font=SANS_B(13), fill=INK)
            lines = wrap(draw, body, SANS(12), col_w)
            end = para(draw, bx, gy + 60, col_w, lines, SANS(12), INK,
                       leading=15)
            draw.text((bx, end + 2), date, font=SANS_B(10), fill=MUTED)
            row_h = max(row_h, end + 16 - gy)
        bottom = gy + row_h
        gy += row_h + 8
    fit_check("small stories", bottom, 700)


MAP_DOTS = [
    # (x, y, label, label dx, label dy)
    (185, 782, "NEW YORK", 8, -4),
    (318, 758, "THE HAGUE", -20, -13),
    (344, 806, "BENGHAZI", -56, 5),
    (402, 802, "HORMUZ", 8, -4),
    (428, 772, "DUSHANBE", -12, -13),
    (492, 802, "SHENZHEN", 8, -4),
    (478, 848, "JAKARTA", -16, 7),
    (532, 780, "TOKYO", 8, -4),
]


def draw_map(draw):
    x0, y0, x1, y1 = 36, 708, 620, 922
    draw.rectangle([x0 - 14, y0 + 2, x0 - 4, y0 + 12], fill=RED)
    draw.text((x0, y0), "WHERE IT HAPPENED", font=SANS_B(17), fill=INK)
    draw.text((x0 + 208, y0 + 2), "SCHEMATIC MAP", font=SANS_B(11),
              fill=MUTED)
    mx0, my0, mx1, my1 = 48, 736, 608, 912
    draw.rectangle([mx0, my0, mx1, my1], fill=OCEAN, outline=BORDER, width=1)
    for box in [(110, 745, 250, 825), (205, 845, 255, 905),
                (300, 745, 375, 790), (330, 800, 395, 880),
                (400, 745, 560, 820), (450, 820, 520, 870),
                (540, 860, 590, 895)]:
        draw.ellipse(box, fill=LAND)
    for (dx, dy, label, lx, ly) in MAP_DOTS:
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=RED,
                     outline=(255, 255, 255), width=1)
        draw.text((dx + lx, dy + ly), label, font=SANS_B(9), fill=INK,
                  stroke_width=2, stroke_fill=PAPER)
    fit_check("map", my1, y1)


ALSO_ON = [
    ("EL NIÑO", "Super El Niño intensifies; peak into 2027."),
    ("MEASLES", "Resurgence spreads; US congenital cases rise."),
    ("THAI–CAMBODIA", "Border fighting on hold after a truce."),
    ("BANGLADESH", "Mass typhoid vaccination drive under way."),
    ("ACROPOLIS", "Athens reopens its museum after 20 years."),
]


def draw_also(draw):
    x0, y0, x1 = 636, 708, 988
    draw.rectangle([x0 - 14, y0 + 2, x0 - 4, y0 + 12], fill=RED)
    draw.text((x0, y0), "ALSO ON", font=SANS_B(17), fill=INK)
    rule(draw, x0, y0 + 22, x1, 2)
    y = y0 + 30
    for i, (head, body) in enumerate(ALSO_ON, 1):
        draw.ellipse([x0, y + 1, x0 + 18, y + 19], fill=RED)
        num = str(i)
        nw = text_w(draw, num, SANS_B(12))
        draw.text((x0 + 9 - nw / 2, y + 3), num, font=SANS_B(12),
                  fill=(255, 255, 255))
        draw.text((x0 + 24, y), head, font=SANS_B(13), fill=INK)
        lines = wrap(draw, body, SANS(12), x1 - x0 - 24)
        end = para(draw, x0 + 24, y + 17, x1 - x0 - 24, lines, SANS(12),
                   INK, leading=14)
        y = end + 4
    fit_check("also on", y, 922)


def draw_footer(draw):
    x0, x1 = 36, 988
    rule(draw, x0, 932, x1, 2)
    dc = ("DATE CHECK: Markets — Mon 23 Nov · Gulf — "
          "Sun 22–Mon 23 Nov · Jakarta — Mon 23 Nov · Merkury — Sun 22 Nov "
          "· ICJ — Thu 19 Nov · Shenzhen — Thu 19 Nov · GTA VI — Thu 19 Nov "
          "· Tokyo — Tue 24 Nov · Dushanbe — Fri 20 Nov · Also on — "
          "reported Mon 23 Nov")
    lines = wrap(draw, dc, SANS_B(11), x1 - x0)
    end = para(draw, x0, 940, x1 - x0, lines, SANS_B(11), INK, leading=14)
    src = ("SOURCES: REUTERS · AP · AFP · DPA-AFX · HRW · WHITE HOUSE · "
           "TAKE-TWO · MORNINGSTAR · BLOOMBERG LAW")
    draw.text((x0, end + 6), src, font=SANS(11), fill=MUTED)
    fit_check("footer", end + 18, 1010)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw_masthead(draw)
    draw_hero(draw)
    rotated_badge(img, 555, 152, 150, 34, "NASDAQ +6.5%", -6, ORANGE,
                  (255, 255, 255))
    draw_lead2(draw)
    draw_lead3(draw)
    draw_small(draw)
    draw_map(draw)
    draw_also(draw)
    draw_footer(draw)
    save_png(img, OUT)
    print("WROTE", OUT)


if __name__ == "__main__":
    main()
