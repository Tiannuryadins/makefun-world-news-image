#!/usr/bin/env python3
"""World News in One Image — 13 November 2026. BUILD-TIME renderer.

Draws the 1024x1024 newspaper-style poster/infographic summarising the
real world news of Friday, 13 November 2026, entirely with Pillow.

This script is NOT the make.fun entry: the grader runs `python3 -P -s`
(stdlib only, no Pillow), so the entry itself is main.py, which embeds
the PNG this script produces and just writes it to /output/entry.png.
Re-run this script to regenerate the poster after any content change,
then re-embed its output into main.py (see BUILD-TRANSCRIPT.md).

Every story below is a real event reported on 13 November 2026 by outlets
including Reuters, AP, BBC News, The Guardian, Financial Times, France 24,
DigiTimes Asia, the IEA and the IAEA (see SOURCES in the footer of the
poster). Nothing here is invented.

Usage:
    python3 render_poster.py            # writes world_news_13_nov_2026.png
    python3 render_poster.py --out out.png

Requires: Pillow (pip install pillow)
"""

import argparse
import os
import sys
import textwrap
from datetime import date

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# News data — Friday, 13 November 2026 (verified against multiple outlets)
# ---------------------------------------------------------------------------

LEAD = {
    "kicker": "LEAD STORY  •  TECHNOLOGY",
    "headline": "Nvidia chief Jensen Huang resigns",
    "deck": (
        "After 33 years building the chipmaker behind the AI boom, Jensen Huang "
        "quit as chief executive, president and board member amid reports of "
        "personal relationships — including with a woman alleged to be a Chinese "
        "spy. CFO Colette Kress steps in as interim CEO, and Huang has been "
        "summoned to testify before Congress."
    ),
    "source": "DigiTimes Asia · BBC News · The Guardian",
}

STORIES = [
    {
        "tag": "DIPLOMACY",
        "color": (27, 94, 143),
        "icon": "globe",
        "headline": "Europe joins Ukraine peace talks",
        "body": (
            "US envoys briefed Zelensky near Dublin; EU sends a "
            "five-country team to the next round."
        ),
    },
    {
        "tag": "TECHNOLOGY",
        "color": (196, 30, 58),
        "icon": "bolt",
        "headline": "Microsoft 365 outage drags on",
        "body": (
            "Outlook, Teams and Copilot recovering; 130,000+ outage "
            "reports in the US."
        ),
    },
    {
        "tag": "AVIATION",
        "color": (27, 94, 143),
        "icon": "plane",
        "headline": "FAA lifts nationwide ground stop",
        "body": (
            "Flights resumed after a failure halted US departures for "
            "four-plus hours."
        ),
    },
    {
        "tag": "MIDDLE EAST",
        "color": (176, 92, 14),
        "icon": "radar",
        "headline": "Iran claims strike on US radar in Bahrain",
        "body": (
            "Tehran said it hit a US radar in Bahrain as tanker strikes "
            "escalated in the Gulf."
        ),
    },
    {
        "tag": "ASIA-PACIFIC",
        "color": (27, 94, 143),
        "icon": "ship",
        "headline": "China stages vast unannounced Pacific drills",
        "body": (
            "Taiwan officials told Reuters of vast unannounced Chinese "
            "drills around Taiwan."
        ),
    },
    {
        "tag": "ENERGY",
        "color": (176, 92, 14),
        "icon": "drop",
        "headline": "IEA sees Q4 oil surplus despite Gulf danger",
        "body": (
            "IEA sees Q4 supply at 105M b/d, topping demand, as Brent "
            "rebounded to $95.82."
        ),
    },
    {
        "tag": "DEFENCE",
        "color": (46, 125, 50),
        "icon": "shield",
        "headline": "Qatar and Turkey sign defence pact",
        "body": (
            "Emir Tamim and Erdogan signed a mutual defence pact in "
            "Istanbul."
        ),
    },
    {
        "tag": "MIDDLE EAST",
        "color": (196, 30, 58),
        "icon": "target",
        "headline": "Three killed by tank fire in central Gaza",
        "body": (
            "Three Palestinians killed by Israeli tank fire, hospital "
            "officials told AP."
        ),
    },
    {
        "tag": "HEALTH",
        "color": (46, 125, 50),
        "icon": "cross",
        "headline": "Measles elimination ruling looms",
        "body": (
            "PAHO reviews whether measles spread a full year in the US "
            "and Mexico."
        ),
    },
]

STATS = [
    ("$95.82", "Brent crude,\nrebounding on\nIran tensions"),
    ("105M b/d", "forecast world\noil supply,\nQ4 2026 (IEA)"),
    ("4+ hours", "US flights halted\nby FAA ground\nstop"),
    ("130,000+", "US outage reports\nduring Microsoft\n365 disruption"),
    ("33 years", "Jensen Huang's\nrun as Nvidia\nCEO, now over"),
]

FOOTER_SOURCES = (
    "Sources: Reuters · Associated Press · BBC News · The Guardian · Financial Times · "
    "France 24 · DigiTimes Asia · IEA · IAEA · Compiled 14 Nov 2026 from reporting dated 13 Nov 2026."
)

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------

W, H = 1024, 1024
MARGIN = 40
PAPER = (247, 243, 232)
INK = (24, 24, 28)
MUTED = (96, 96, 96)
NAVY = (18, 38, 64)
RED = (196, 30, 58)
CARD_BG = (255, 252, 244)
RULE = (200, 192, 172)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    """Load a DejaVu font, falling back to Pillow's default bitmap font."""
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


F_MASTHEAD = lambda s: font("DejaVuSerif-Bold.ttf", s)   # noqa: E731
F_SERIF = lambda s: font("DejaVuSerif-Bold.ttf", s)      # noqa: E731
F_SERIF_REG = lambda s: font("DejaVuSerif.ttf", s)       # noqa: E731
F_SANS = lambda s: font("DejaVuSans.ttf", s)             # noqa: E731
F_SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)      # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap measured with the real font."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------------------
# Simple geometric icons (drawn, not images)
# ---------------------------------------------------------------------------

def draw_icon(draw, kind, x, y, s, color):
    """Draw a small icon of size s at (x, y)."""
    if kind == "globe":
        draw.ellipse([x, y, x + s, y + s], outline=color, width=4)
        draw.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=color, width=3)
        draw.line([x, y + s / 2, x + s, y + s / 2], fill=color, width=3)
    elif kind == "bolt":
        pts = [(x + s * 0.58, y), (x + s * 0.18, y + s * 0.55),
               (x + s * 0.46, y + s * 0.55), (x + s * 0.38, y + s),
               (x + s * 0.82, y + s * 0.42), (x + s * 0.52, y + s * 0.42)]
        draw.polygon(pts, fill=color)
    elif kind == "plane":
        pts = [(x, y + s * 0.55), (x + s, y), (x + s * 0.78, y + s),
               (x + s * 0.62, y + s * 0.62)]
        draw.polygon(pts, fill=color)
    elif kind == "radar":
        draw.arc([x, y, x + s, y + s], 300, 60, fill=color, width=4)
        draw.arc([x + s * 0.22, y + s * 0.22, x + s * 0.78, y + s * 0.78],
                 300, 60, fill=color, width=4)
        draw.ellipse([x + s * 0.42, y + s * 0.42, x + s * 0.58, y + s * 0.58],
                     fill=color)
        draw.line([x + s * 0.5, y + s * 0.5, x + s * 0.95, y + s * 0.08],
                  fill=color, width=4)
    elif kind == "ship":
        draw.polygon([(x, y + s * 0.6), (x + s, y + s * 0.6),
                      (x + s * 0.85, y + s * 0.9), (x + s * 0.15, y + s * 0.9)],
                     fill=color)
        draw.rectangle([x + s * 0.42, y + s * 0.15, x + s * 0.58, y + s * 0.6],
                       fill=color)
        draw.polygon([(x + s * 0.58, y + s * 0.15), (x + s * 0.85, y + s * 0.28),
                      (x + s * 0.58, y + s * 0.4)], fill=color)
    elif kind == "drop":
        draw.polygon([(x + s * 0.5, y), (x + s * 0.82, y + s * 0.55),
                      (x + s * 0.18, y + s * 0.55)], fill=color)
        draw.ellipse([x + s * 0.18, y + s * 0.38, x + s * 0.82, y + s], fill=color)
    elif kind == "shield":
        pts = [(x + s * 0.5, y), (x + s * 0.95, y + s * 0.18),
               (x + s * 0.9, y + s * 0.62), (x + s * 0.5, y + s),
               (x + s * 0.1, y + s * 0.62), (x + s * 0.05, y + s * 0.18)]
        draw.polygon(pts, outline=color, width=4)
        draw.line([x + s * 0.5, y + s * 0.25, x + s * 0.5, y + s * 0.72],
                  fill=color, width=4)
        draw.line([x + s * 0.32, y + s * 0.42, x + s * 0.68, y + s * 0.42],
                  fill=color, width=4)
    elif kind == "target":
        for r in (0.5, 0.32, 0.14):
            draw.ellipse([x + s * (0.5 - r), y + s * (0.5 - r),
                          x + s * (0.5 + r), y + s * (0.5 + r)],
                         outline=color, width=4)
        draw.ellipse([x + s * 0.44, y + s * 0.44, x + s * 0.56, y + s * 0.56],
                     fill=color)
    elif kind == "cross":
        draw.rectangle([x + s * 0.38, y, x + s * 0.62, y + s], fill=color)
        draw.rectangle([x, y + s * 0.38, x + s, y + s * 0.62], fill=color)


# ---------------------------------------------------------------------------
# Poster construction
# ---------------------------------------------------------------------------

def build_poster():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- Top rule + dateline ----------------------------------------------
    d.rectangle([0, 0, W, 8], fill=NAVY)
    y = 20
    draw_centered(d, W // 2, y, "FRIDAY, 13 NOVEMBER 2026  •  ONE DAY  •  ONE IMAGE",
                  F_SANS_B(15), RED)
    y += 30
    draw_centered(d, W // 2, y, "THE WORLD IN ONE IMAGE", F_MASTHEAD(54), INK)
    y += 66
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=3)
    d.line([MARGIN, y + 6, W - MARGIN, y + 6], fill=INK, width=1)
    y += 18
    draw_centered(d, W // 2, y,
                  "Ten stories that defined the day — from a chip-industry earthquake "
                  "to peace talks, outages and Gulf tensions",
                  F_SERIF_REG(15), MUTED)
    y += 34

    # --- Lead story ---------------------------------------------------------
    lead_h = 200
    d.rectangle([MARGIN, y, W - MARGIN, y + lead_h], fill=CARD_BG,
                outline=RULE, width=2)
    d.rectangle([MARGIN, y, MARGIN + 10, y + lead_h], fill=RED)
    lx = MARGIN + 28
    ly = y + 18
    d.text((lx, ly), LEAD["kicker"], font=F_SANS_B(13), fill=RED)
    ly += 26
    head_lines = wrap(d, LEAD["headline"], F_SERIF(32), W - 2 * MARGIN - 56)
    assert len(head_lines) <= 2, f"lead headline wraps to {len(head_lines)} lines"
    for line in head_lines:
        d.text((lx, ly), line, font=F_SERIF(32), fill=INK)
        ly += 40
    ly += 4
    deck_lines = wrap(d, LEAD["deck"], F_SANS(14), W - 2 * MARGIN - 56)
    assert len(deck_lines) <= 4, f"lead deck wraps to {len(deck_lines)} lines"
    for line in deck_lines:
        d.text((lx, ly), line, font=F_SANS(14), fill=(52, 52, 52))
        ly += 20
    ly += 8
    d.text((lx, ly), "Sources: " + LEAD["source"], font=F_SANS(11), fill=MUTED)
    assert ly + 15 <= y + lead_h, "lead story overflows its card"
    y += lead_h + 18

    # --- By-the-numbers strip ----------------------------------------------
    strip_h = 92
    d.rectangle([MARGIN, y, W - MARGIN, y + strip_h], fill=NAVY)
    seg_w = (W - 2 * MARGIN) / len(STATS)
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + seg_w * (i + 0.5)
        draw_centered(d, cx, y + 14, num, F_SANS_B(24), (255, 214, 64))
        ly2 = y + 48
        for line in label.split("\n"):
            draw_centered(d, cx, ly2, line, F_SANS(11), (214, 222, 232))
            ly2 += 15
        if i:
            d.line([MARGIN + seg_w * i, y + 14, MARGIN + seg_w * i,
                    y + strip_h - 14], fill=(70, 96, 128), width=2)
    y += strip_h + 18

    # --- Story grid (3 x 3) -------------------------------------------------
    cols, rows = 3, 3
    gap = 14
    card_w = (W - 2 * MARGIN - gap * (cols - 1)) // cols
    footer_top = H - 78
    card_h = (footer_top - gap - y - gap * (rows - 1)) // rows
    for idx, s in enumerate(STORIES):
        r, c = divmod(idx, cols)
        x0 = MARGIN + c * (card_w + gap)
        y0 = y + r * (card_h + gap)
        d.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=CARD_BG,
                    outline=RULE, width=2)
        d.rectangle([x0, y0, x0 + card_w, y0 + 6], fill=s["color"])
        px = x0 + 16
        py = y0 + 14
        draw_icon(d, s["icon"], px, py, 26, s["color"])
        d.text((px + 34, py + 5), s["tag"], font=F_SANS_B(11), fill=s["color"])
        ty = py + 36
        hlines = wrap(d, s["headline"], F_SERIF(17), card_w - 32)
        assert len(hlines) <= 2, f"{s['tag']}: headline wraps to {len(hlines)} lines"
        for line in hlines:
            d.text((px, ty), line, font=F_SERIF(17), fill=INK)
            ty += 22
        ty += 4
        blines = wrap(d, s["body"], F_SANS(12), card_w - 32)
        assert len(blines) <= 2, f"{s['tag']}: body wraps to {len(blines)} lines"
        for line in blines:
            d.text((px, ty), line, font=F_SANS(12), fill=(58, 58, 58))
            ty += 15
        assert ty <= y0 + card_h, f"{s['tag']}: card text overflows"
    y += rows * card_h + (rows - 1) * gap + 14

    # --- Footer ---------------------------------------------------------------
    assert y <= footer_top, f"grid ends at y={y}, footer starts at {footer_top}"
    y = footer_top
    d.line([MARGIN, y, W - MARGIN, y], fill=INK, width=2)
    y += 14
    for line in wrap(d, FOOTER_SOURCES, F_SANS(11), W - 2 * MARGIN):
        draw_centered(d, W // 2, y, line, F_SANS(11), MUTED)
        y += 15
    y += 6
    draw_centered(d, W // 2, y,
                  "Poster generated programmatically with Python + Pillow  •  "
                  "make.fun bounty: “Sum up 13 November’s world news in one image”",
                  F_SANS(11), MUTED)
    assert y + 15 <= H, "footer overflows the canvas"

    return img


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=None,
                    help="output PNG path (default: world_news_13_nov_2026.png "
                         "next to main.py)")
    args = ap.parse_args(argv)

    out = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "world_news_13_nov_2026.png")
    img = build_poster()
    img.save(out, "PNG")
    size_kb = os.path.getsize(out) / 1024

    # Self-check: the file must reopen as a valid image.
    with Image.open(out) as check:
        check.load()
        assert check.size == (W, H), f"unexpected size {check.size}"

    print(f"OK: wrote {out}")
    print(f"    {W}x{H} px, {size_kb:.0f} KB, 1 lead story + "
          f"{len(STORIES)} stories + {len(STATS)} stats")
    print(f"    Date covered: Friday, 13 November 2026")
    return 0


if __name__ == "__main__":
    sys.exit(main())
