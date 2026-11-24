#!/usr/bin/env python3
"""Draw entry.png for news-image-20261124 — THE WORLD TODAY, Tue 24 Nov 2026.

A 1024x1024 newspaper front page, rendered with Pillow at build time.
Sections: masthead, hero (Wall St rebound, verified Monday closes),
two leads (Gulf standoff, Jakarta VP picks), six illustrated small
stories, a schematic WHERE IT HAPPENED map, a numbered ALSO ON list,
and a DATE CHECK + SOURCES footer. Style per the "less stiff" note:
big serif hero, tilted sticker badge, sticker-disc icons, red number
chips, rounded panels, red date pill.

All figures are verified closes, not intraday prints: Nasdaq +6.5%
(24,089.56), S&P +4.7% (7,237.17), Dow +3.0% (49,595.31),
Nvidia +31.5% (closed $165.05, +$39.52 from Friday $125.53, best
day since 2003, Huang back as CEO 11 days after resigning).
Deterministic: fixed fonts, fixed geometry, no randomness, no clock.
"""
import hashlib
import os

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(HERE, "entry.png")

PAL = {
    "paper": (245, 240, 230),
    "ink": (20, 32, 46),
    "navy": (16, 35, 59),
    "red": (196, 58, 42),
    "darkred": (122, 30, 22),
    "green": (30, 77, 51),
    "orange": (232, 120, 36),
    "gold": (217, 164, 65),
    "card": (253, 252, 247),
    "border": (201, 194, 178),
    "muted": (90, 100, 112),
    "ocean": (205, 222, 232),
    "land": (233, 219, 172),
    "sky": (46, 111, 142),
    "white": (255, 255, 255),
    "pale": (224, 236, 228),
    "paleblue": (216, 224, 232),
    "palered": (240, 222, 216),
    "bar": (120, 200, 140),
}

FONT_FOLDER = "/usr/share/fonts/truetype/dejavu"


def typeface(style, size):
    """Load a DejaVu face. style: 'serif'/'serif-bold'/'sans'/'sans-bold'."""
    names = {
        "serif": "DejaVuSerif.ttf",
        "serif-bold": "DejaVuSerif-Bold.ttf",
        "sans": "DejaVuSans.ttf",
        "sans-bold": "DejaVuSans-Bold.ttf",
    }
    return ImageFont.truetype(os.path.join(FONT_FOLDER, names[style]), size)


def measure(drawing, text, face):
    return drawing.textlength(text, font=face)


def flow(drawing, text, face, limit):
    """Greedy word wrap into lines no wider than limit."""
    out, current = [], ""
    for word in text.split():
        attempt = (current + " " + word).strip()
        if measure(drawing, attempt, face) <= limit or not current:
            current = attempt
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def block(drawing, x, y, lines, face, colour, leading=None, gap=0):
    """Paint lines top-down; return the y just below the last line."""
    step = leading if leading is not None else int(face.size * 1.25)
    for n, line in enumerate(lines):
        drawing.text((x, y + n * (step + gap)), line, font=face, fill=colour)
    return y + len(lines) * (step + gap)


def hline(drawing, x0, y, x1, thick=2, colour=None):
    drawing.line([(x0, y), (x1, y)], fill=colour or PAL["ink"], width=thick)


def check_fit(section, bottom, ceiling):
    if bottom > ceiling:
        raise SystemExit(f"FIT FAIL {section}: {bottom} > {ceiling}")


def store_png(image, path):
    image.save(path, format="PNG", optimize=True)
    with open(path, "rb") as handle:
        blob = handle.read()
    print("SIZE", len(blob), "bytes; <=1MiB:", len(blob) <= 1024 * 1024)
    print("SHA256", hashlib.sha256(blob).hexdigest())
    print("MODE", image.mode, "DIMS", image.size)


def paint_masthead(drawing):
    left, right = 36, 988
    drawing.rectangle([left, 18, right, 22], fill=PAL["red"])
    drawing.text((left, 26), "THE WORLD IN ONE DAY",
                 font=typeface("sans-bold", 15), fill=PAL["red"])
    tag = "TUESDAY EDITION"
    drawing.text((right - measure(drawing, tag, typeface("sans-bold", 14)), 28),
                 tag, font=typeface("sans-bold", 14), fill=PAL["muted"])
    drawing.text((left, 48), "THE WORLD TODAY",
                 font=typeface("serif-bold", 54), fill=PAL["ink"])
    stamp = "TUESDAY 24 NOV 2026"
    sw = measure(drawing, stamp, typeface("sans-bold", 21))
    drawing.rounded_rectangle([right - sw - 24, 66, right, 100], radius=17,
                              fill=PAL["red"])
    drawing.text((right - sw - 12, 74), stamp,
                 font=typeface("sans-bold", 21), fill=PAL["white"])
    hline(drawing, left, 112, right, 3)
    hline(drawing, left, 117, right, 1, PAL["gold"])
    check_fit("masthead", 119, 124)


def sticker(canvas, cx, cy, w, h, label, tilt, bg, fg):
    """Tilted pill badge: draw on its own layer, rotate, paste."""
    layer = Image.new("RGBA", (w * 2, h * 2), (0, 0, 0, 0))
    pen = ImageDraw.Draw(layer)
    pen.rounded_rectangle([w // 2, h // 2, w // 2 + w, h // 2 + h],
                          radius=h // 2, fill=bg)
    face = typeface("sans-bold", 15)
    tw = pen.textlength(label, font=face)
    pen.text((w // 2 + (w - tw) / 2, h // 2 + (h - 15) / 2), label,
             font=face, fill=fg)
    layer = layer.rotate(tilt, resample=Image.BICUBIC, center=(w, h))
    canvas.paste(layer, (cx - w, cy - h), layer)


def paint_hero(drawing):
    x0, y0, x1, y1 = 36, 126, 640, 400
    drawing.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=PAL["green"])
    drawing.rounded_rectangle([x0, y0, x1, y1], radius=10,
                              outline=PAL["gold"], width=2)
    tx = x0 + 26
    drawing.text((tx, y0 + 14), "MARKETS  ·  WALL STREET  ·  MON 23 NOV",
                 font=typeface("sans-bold", 14), fill=PAL["gold"])
    drawing.text((tx, y0 + 32), "WALL ST",
                 font=typeface("serif-bold", 58), fill=PAL["white"])
    drawing.text((tx, y0 + 94), "ROARS BACK",
                 font=typeface("serif-bold", 58), fill=PAL["white"])
    deck = ("Stocks storm back from Friday's rout as Nvidia posts its "
            "best day since 2003 on Huang's comeback.")
    lines = flow(drawing, deck, typeface("sans", 16), 552)
    bottom = block(drawing, tx, y0 + 156, lines, typeface("sans", 16),
                   PAL["pale"], leading=19)
    bars = [("Nasdaq", "+6.5%", 6.5), ("S&P 500", "+4.7%", 4.7),
            ("Dow", "+3.0%", 3.0)]
    bx, span = tx + 104, 250
    y = bottom + 6
    for name, value, size in bars:
        drawing.text((tx, y), name, font=typeface("sans-bold", 15),
                     fill=PAL["white"])
        width = int(span * size / 6.5)
        drawing.rectangle([bx, y + 2, bx + width, y + 15], fill=PAL["bar"])
        drawing.text((bx + span + 10, y), value,
                     font=typeface("sans-bold", 15), fill=PAL["white"])
        y += 18
    drawing.text((tx, y + 2),
                 "NVIDIA +31.5%  ·  HUANG BACK 11 DAYS AFTER QUITTING  ·  10-YR 4.94%",
                 font=typeface("sans-bold", 13), fill=PAL["gold"])
    check_fit("hero", y + 16, y1)


def paint_lead2(drawing):
    x0, y0, x1, y1 = 652, 126, 988, 256
    drawing.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=PAL["navy"])
    drawing.rounded_rectangle([x0, y0, x1, y1], radius=8,
                              outline=PAL["gold"], width=2)
    tx = x0 + 18
    drawing.text((tx, y0 + 12), "GULF  ·  HORMUZ  ·  SUN–MON",
                 font=typeface("sans-bold", 12), fill=PAL["gold"])
    drawing.text((tx, y0 + 28), "TRUMP-IRAN",
                 font=typeface("serif-bold", 28), fill=PAL["white"])
    drawing.text((tx, y0 + 58), "STANDOFF",
                 font=typeface("serif-bold", 28), fill=PAL["white"])
    deck = ("Tehran offers Hormuz open in 48 hours; Trump vows strikes "
            "after New Year.")
    lines = flow(drawing, deck, typeface("sans", 13), x1 - x0 - 36)
    bottom = block(drawing, tx, y0 + 90, lines, typeface("sans", 13),
                   PAL["paleblue"], leading=16)
    check_fit("lead2", bottom, y1)


def paint_lead3(drawing):
    x0, y0, x1, y1 = 652, 268, 988, 400
    drawing.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=PAL["darkred"])
    drawing.rounded_rectangle([x0, y0, x1, y1], radius=8,
                              outline=PAL["gold"], width=2)
    tx = x0 + 18
    drawing.text((tx, y0 + 12), "INDONESIA  ·  JAKARTA  ·  MON 23 NOV",
                 font=typeface("sans-bold", 12), fill=PAL["gold"])
    drawing.text((tx, y0 + 28), "PRABOWO PICKS",
                 font=typeface("serif-bold", 28), fill=PAL["white"])
    drawing.text((tx, y0 + 58), "TWO VPS",
                 font=typeface("serif-bold", 28), fill=PAL["white"])
    deck = ("Amran Sulaiman and Sugiono named as VP candidates; "
            "parliament votes 11 Dec.")
    lines = flow(drawing, deck, typeface("sans", 13), x1 - x0 - 36)
    bottom = block(drawing, tx, y0 + 90, lines, typeface("sans", 13),
                   PAL["palered"], leading=16)
    check_fit("lead3", bottom, y1)


def _glyph_ship(drawing, x, y, c):
    drawing.polygon([(x + 2, y + 22), (x + 34, y + 22), (x + 28, y + 32),
                     (x + 8, y + 32)], fill=c)
    drawing.line([(x + 18, y + 22), (x + 18, y + 6)], fill=c, width=3)
    drawing.polygon([(x + 18, y + 6), (x + 30, y + 18), (x + 18, y + 18)],
                    fill=c)
    drawing.line([(x + 2, y + 34), (x + 34, y + 34)], fill=c, width=2)


def _glyph_scales(drawing, x, y, c):
    drawing.line([(x + 18, y + 4), (x + 18, y + 30)], fill=c, width=3)
    drawing.line([(x + 6, y + 10), (x + 30, y + 10)], fill=c, width=3)
    drawing.polygon([(x + 2, y + 10), (x + 10, y + 10), (x + 6, y + 18)],
                    outline=c, width=2)
    drawing.polygon([(x + 26, y + 10), (x + 34, y + 10), (x + 30, y + 18)],
                    outline=c, width=2)
    drawing.line([(x + 10, y + 30), (x + 26, y + 30)], fill=c, width=3)


def _glyph_flags(drawing, x, y, c):
    for fx in (x + 6, x + 16, x + 26):
        drawing.line([(fx, y + 6), (fx, y + 32)], fill=c, width=2)
        drawing.polygon([(fx, y + 6), (fx + 9, y + 10), (fx, y + 14)],
                        fill=c)


def _glyph_pad(drawing, x, y, c):
    drawing.rounded_rectangle([x + 3, y + 10, x + 33, y + 28], radius=8,
                              outline=c, width=3)
    drawing.line([(x + 9, y + 19), (x + 15, y + 19)], fill=c, width=2)
    drawing.line([(x + 12, y + 16), (x + 12, y + 22)], fill=c, width=2)
    drawing.ellipse([x + 22, y + 15, x + 25, y + 18], fill=c)
    drawing.ellipse([x + 27, y + 19, x + 30, y + 22], fill=c)


def _glyph_chart(drawing, x, y, c):
    drawing.line([(x + 4, y + 30), (x + 32, y + 30)], fill=c, width=2)
    drawing.rectangle([x + 6, y + 22, x + 11, y + 30], fill=c)
    drawing.rectangle([x + 14, y + 16, x + 19, y + 30], fill=c)
    drawing.rectangle([x + 22, y + 9, x + 27, y + 30], fill=c)
    drawing.line([(x + 4, y + 14), (x + 32, y + 4)], fill=c, width=2)
    drawing.polygon([(x + 32, y + 4), (x + 26, y + 4), (x + 32, y + 10)],
                    fill=c)


def _glyph_court(drawing, x, y, c):
    drawing.polygon([(x + 4, y + 12), (x + 18, y + 4), (x + 32, y + 12)],
                    fill=c)
    for cx in (x + 8, x + 16, x + 24):
        drawing.line([(cx, y + 14), (cx, y + 28)], fill=c, width=3)
    drawing.rectangle([x + 4, y + 28, x + 32, y + 32], fill=c)


GLYPHS = {
    "ship": _glyph_ship,
    "scales": _glyph_scales,
    "flags": _glyph_flags,
    "pad": _glyph_pad,
    "chart": _glyph_chart,
    "court": _glyph_court,
}


def paint_icon(drawing, kind, x, y, colour):
    """White pictogram on a 36px coloured sticker disc."""
    drawing.ellipse([x, y, x + 36, y + 36], fill=colour)
    GLYPHS[kind](drawing, x, y, PAL["card"])


# Six small stories: (icon kind, headline, body, date, disc colour).
STORIES = [
    {"icon": "ship", "head": "MERKURY SUNK",
     "body": "Ukraine sinks a Russian corvette off Benghazi with seven "
             "sea drones.", "date": "SUN 22 NOV", "colour": "red"},
    {"icon": "scales", "head": "ROHINGYA: GENOCIDE",
     "body": "World court rules 9–6 that Myanmar committed genocide; "
             "a first.", "date": "THU 19 NOV", "colour": "navy"},
    {"icon": "flags", "head": "SHENZHEN: NO DEAL",
     "body": "Trump, Xi and Putin sign a 4-point peace note — no Ukraine, "
             "no Iran.", "date": "THU 19 NOV", "colour": "red"},
    {"icon": "pad", "head": "GTA VI: $3.79B",
     "body": "Biggest entertainment launch ever: $3.79B on day one, "
             "32.5M pre-sold.", "date": "THU 19 NOV", "colour": "green"},
    {"icon": "chart", "head": "TOKYO REOPENS",
     "body": "Nikkei resumes after Friday's 5.1% plunge and a Monday "
             "holiday.", "date": "TUE 24 NOV", "colour": "red"},
    {"icon": "court", "head": "DUSHANBE QUITS",
     "body": "Tajikistan tells the UN it is leaving the ICC as Putin "
             "visits.", "date": "FRI 20 NOV", "colour": "red"},
]


def paint_small(drawing):
    x0, y0, x1 = 36, 412, 988
    drawing.rectangle([x0 - 14, y0 + 2, x0 - 4, y0 + 12], fill=PAL["red"])
    drawing.text((x0, y0), "AROUND THE WORLD",
                 font=typeface("sans-bold", 17), fill=PAL["ink"])
    hline(drawing, x0, y0 + 22, x1, 2)
    col_w, gap = 306, 16
    gy = y0 + 32
    bottom = gy
    for row in range(2):
        row_h = 0
        for col in range(3):
            item = STORIES[row * 3 + col]
            bx = x0 + col * (col_w + gap)
            paint_icon(drawing, item["icon"], bx, gy, PAL[item["colour"]])
            drawing.text((bx, gy + 40), item["head"],
                         font=typeface("sans-bold", 13), fill=PAL["ink"])
            lines = flow(drawing, item["body"], typeface("sans", 12), col_w)
            end = block(drawing, bx, gy + 60, lines, typeface("sans", 12),
                        PAL["ink"], leading=15)
            drawing.text((bx, end + 2), item["date"],
                         font=typeface("sans-bold", 10), fill=PAL["muted"])
            row_h = max(row_h, end + 16 - gy)
        bottom = gy + row_h
        gy += row_h + 8
    check_fit("small stories", bottom, 700)


# Map pins: (x, y, label, label dx, label dy).
PINS = [
    (185, 782, "NEW YORK", 8, -4),
    (318, 758, "THE HAGUE", -20, -13),
    (344, 806, "BENGHAZI", -56, 5),
    (402, 802, "HORMUZ", 8, -4),
    (428, 772, "DUSHANBE", -12, -13),
    (492, 802, "SHENZHEN", 8, -4),
    (478, 848, "JAKARTA", -16, 7),
    (532, 780, "TOKYO", 8, -4),
]

# Schematic land masses (ellipses inside the ocean box).
LAND_BLOBS = [
    (110, 745, 250, 825), (205, 845, 255, 905),
    (300, 745, 375, 790), (330, 800, 395, 880),
    (400, 745, 560, 820), (450, 820, 520, 870),
    (540, 860, 590, 895),
]


def paint_map(drawing):
    x0, y0, x1, y1 = 36, 708, 620, 922
    drawing.rectangle([x0 - 14, y0 + 2, x0 - 4, y0 + 12], fill=PAL["red"])
    drawing.text((x0, y0), "WHERE IT HAPPENED",
                 font=typeface("sans-bold", 17), fill=PAL["ink"])
    drawing.text((x0 + 208, y0 + 2), "SCHEMATIC MAP",
                 font=typeface("sans-bold", 11), fill=PAL["muted"])
    mx0, my0, mx1, my1 = 48, 736, 608, 912
    drawing.rectangle([mx0, my0, mx1, my1], fill=PAL["ocean"],
                      outline=PAL["border"], width=1)
    for box in LAND_BLOBS:
        drawing.ellipse(box, fill=PAL["land"])
    for dx, dy, label, lx, ly in PINS:
        drawing.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=PAL["red"],
                        outline=PAL["white"], width=1)
        drawing.text((dx + lx, dy + ly), label,
                     font=typeface("sans-bold", 9), fill=PAL["ink"],
                     stroke_width=2, stroke_fill=PAL["paper"])
    check_fit("map", my1, y1)


ALSO = [
    ("EL NIÑO", "Super El Niño intensifies; peak into 2027."),
    ("MEASLES", "Resurgence spreads; US congenital cases rise."),
    ("THAI–CAMBODIA", "Border fighting on hold after a truce."),
    ("BANGLADESH", "Mass typhoid vaccination drive under way."),
    ("ACROPOLIS", "Athens reopens its museum after 20 years."),
]


def paint_also(drawing):
    x0, y0, x1 = 636, 708, 988
    drawing.rectangle([x0 - 14, y0 + 2, x0 - 4, y0 + 12], fill=PAL["red"])
    drawing.text((x0, y0), "ALSO ON",
                 font=typeface("sans-bold", 17), fill=PAL["ink"])
    hline(drawing, x0, y0 + 22, x1, 2)
    y = y0 + 30
    for n, (head, body) in enumerate(ALSO, 1):
        drawing.ellipse([x0, y + 1, x0 + 18, y + 19], fill=PAL["red"])
        digit = str(n)
        nw = measure(drawing, digit, typeface("sans-bold", 12))
        drawing.text((x0 + 9 - nw / 2, y + 3), digit,
                     font=typeface("sans-bold", 12), fill=PAL["white"])
        drawing.text((x0 + 24, y), head,
                     font=typeface("sans-bold", 13), fill=PAL["ink"])
        lines = flow(drawing, body, typeface("sans", 12), x1 - x0 - 24)
        end = block(drawing, x0 + 24, y + 17, lines, typeface("sans", 12),
                    PAL["ink"], leading=14)
        y = end + 4
    check_fit("also on", y, 922)


def paint_footer(drawing):
    x0, x1 = 36, 988
    hline(drawing, x0, 932, x1, 2)
    dc = ("DATE CHECK: Markets — Mon 23 Nov · Gulf — "
          "Sun 22–Mon 23 Nov · Jakarta — Mon 23 Nov · Merkury — Sun 22 Nov "
          "· ICJ — Thu 19 Nov · Shenzhen — Thu 19 Nov · GTA VI — Thu 19 Nov "
          "· Tokyo — Tue 24 Nov · Dushanbe — Fri 20 Nov · Also on — "
          "reported Mon 23 Nov")
    lines = flow(drawing, dc, typeface("sans-bold", 11), x1 - x0)
    end = block(drawing, x0, 940, lines, typeface("sans-bold", 11),
                PAL["ink"], leading=14)
    src = ("SOURCES: REUTERS · AP · AFP · DPA-AFX · HRW · WHITE HOUSE · "
           "TAKE-TWO · MORNINGSTAR · BLOOMBERG LAW")
    drawing.text((x0, end + 6), src, font=typeface("sans", 11),
                 fill=PAL["muted"])
    check_fit("footer", end + 18, 1010)


def render():
    canvas = Image.new("RGB", (PAGE_W, PAGE_H), PAL["paper"])
    pen = ImageDraw.Draw(canvas)
    paint_masthead(pen)
    paint_hero(pen)
    sticker(canvas, 555, 152, 150, 34, "NASDAQ +6.5%", -6,
            PAL["orange"], PAL["white"])
    paint_lead2(pen)
    paint_lead3(pen)
    paint_small(pen)
    paint_map(pen)
    paint_also(pen)
    paint_footer(pen)
    store_png(canvas, OUT_PATH)
    print("WROTE", OUT_PATH)


if __name__ == "__main__":
    render()
