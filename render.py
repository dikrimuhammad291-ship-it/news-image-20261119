#!/usr/bin/env python3
"""Draw the front page summing up Thursday 19 November 2026.

A newspaper-style infographic (1024x1024 PNG): the first three-way
Trump-Xi-Putin summit in Shenzhen, the ICJ ruling on Myanmar, the
third Crimean Bridge strike in a week, Iran's attacks on Gulf states,
the COP31 deadlock in Antalya and Anthropic's record IPO, plus briefs
and Thursday's market close. Run it and it writes entry.png beside it.
"""

import math

from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
EDGE = 26
COL = 474
GUT = 24
LEFT = EDGE
RIGHT = EDGE + COL + GUT

CREAM = (250, 246, 236)
INK = (24, 24, 24)
CRIMSON = (176, 32, 28)
FAINT = (203, 196, 176)
MUTED = (112, 107, 92)
PALE = (240, 235, 217)
OCEAN = (112, 156, 186)
PALE_SKY = (216, 231, 241)
SAND = (234, 224, 198)
DEEP = (30, 72, 108)
ORANGE = (214, 90, 20)
GREEN = (58, 138, 62)
GOLD = (198, 158, 38)

FONTS = "/usr/share/fonts/truetype/dejavu"


def bold_serif(px):
    return ImageFont.truetype(f"{FONTS}/DejaVuSerif-Bold.ttf", px)


def plain_serif(px):
    return ImageFont.truetype(f"{FONTS}/DejaVuSerif.ttf", px)


def bold_sans(px):
    return ImageFont.truetype(f"{FONTS}/DejaVuSans-Bold.ttf", px)


def plain_sans(px):
    return ImageFont.truetype(f"{FONTS}/DejaVuSans.ttf", px)


def wrap_text(d, text, font, width):
    """Split text into lines no wider than width pixels."""
    out, cur = [], ""
    for word in text.split():
        cand = (cur + " " + word).strip()
        if d.textlength(cand, font=font) <= width:
            cur = cand
        else:
            if cur:
                out.append(cur)
            cur = word
    if cur:
        out.append(cur)
    return out


def put_lines(d, x, y, lines, font, colour, step):
    """Draw lines top to bottom; return y below the last line."""
    for line in lines:
        d.text((x, y), line, font=font, fill=colour)
        y += step
    return y


def burst(d, cx, cy, outer, inner, spikes, colour):
    """Starburst polygon centred at (cx, cy)."""
    pts = []
    for i in range(spikes * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / spikes - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=colour)


def art_summit(d, x, y, w, h):
    """Shenzhen skyline with three flag circles: US, China, Russia."""
    d.rectangle([x, y, x + w, y + h], fill=PALE_SKY, outline=INK, width=1)
    # Skyline silhouettes.
    base = y + h
    for bx, bw, bh in ((0.04, 0.10, 0.55), (0.16, 0.08, 0.72),
                       (0.27, 0.12, 0.45), (0.41, 0.09, 0.80),
                       (0.53, 0.11, 0.52), (0.67, 0.08, 0.68),
                       (0.78, 0.10, 0.42), (0.90, 0.08, 0.60)):
        d.rectangle([x + w * bx, base - h * bh, x + w * (bx + bw), base],
                    fill=DEEP)
    # A tall tower with a spire in the middle.
    tx = x + w * 0.46
    d.rectangle([tx, base - h * 0.95, tx + 14, base], fill=DEEP)
    d.line([(tx + 7, base - h * 0.95), (tx + 7, y + 6)], fill=DEEP, width=3)
    d.text((x + 10, y + 8), "SHENZHEN", font=bold_sans(11), fill=DEEP)
    d.text((x + w - 52, y + 8), "APEC", font=bold_sans(11), fill=DEEP)
    # Three leaders as flag circles above the skyline.
    circles = [
        (0.22, (178, 34, 30), "USA"),
        (0.50, (222, 41, 16), "CHINA"),
        (0.78, (31, 73, 110), "RUSSIA"),
    ]
    cy = y + h * 0.42
    for frac, colour, label in circles:
        cx = x + w * frac
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=colour,
                  outline=(255, 255, 255), width=3)
        d.text((cx, cy + 32), label, font=bold_sans(11), fill=INK,
               anchor="mt")
    # A table line joining the three circles.
    d.line([(x + w * 0.22, cy + 26), (x + w * 0.78, cy + 26)],
           fill=INK, width=2)


def art_court(d, x, y, w, h):
    """The Peace Palace in The Hague with the scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill=PALE_SKY, outline=INK, width=1)
    base = y + h
    # Courthouse block and columns.
    d.rectangle([x + w * 0.18, y + h * 0.42, x + w * 0.82, base - 8],
                fill=SAND, outline=INK, width=1)
    for i in range(5):
        cx = x + w * (0.26 + i * 0.12)
        d.rectangle([cx - 7, y + h * 0.52, cx + 7, base - 8], fill=(255, 255, 255),
                    outline=INK, width=1)
    # Triangular pediment and flag.
    d.polygon([(x + w * 0.14, y + h * 0.42), (x + w * 0.86, y + h * 0.42),
               (x + w * 0.50, y + h * 0.20)], fill=CRIMSON)
    d.line([(x + w * 0.50, y + h * 0.20), (x + w * 0.50, y + 6)], fill=INK,
           width=2)
    d.polygon([(x + w * 0.50, y + 6), (x + w * 0.50 + 22, y + 12),
               (x + w * 0.50, y + 18)], fill=DEEP)
    d.text((x + 10, y + 8), "THE HAGUE", font=bold_sans(11), fill=DEEP)
    # Scales of justice floating top right, clear of the roofline.
    sx, sy = x + w * 0.84, y + h * 0.17
    d.line([(sx, sy - 16), (sx, sy + 16)], fill=INK, width=2)
    d.line([(sx - 18, sy - 14), (sx + 18, sy - 14)], fill=INK, width=2)
    for ex in (sx - 18, sx + 18):
        d.line([(ex, sy - 14), (ex, sy + 2)], fill=INK, width=1)
        d.polygon([(ex - 9, sy + 2), (ex + 9, sy + 2), (ex, sy + 12)],
                  fill=GOLD)
    d.ellipse([sx - 4, sy + 16, sx + 4, sy + 24], fill=INK)


def art_bridge(d, x, y, w, h):
    """The Crimean Bridge with a road span dropped into the strait."""
    d.rectangle([x, y, x + w, y + h], fill=PALE_SKY, outline=INK, width=1)
    sea_y = y + int(h * 0.60)
    d.rectangle([x, sea_y, x + w, y + h], fill=OCEAN)
    deck = sea_y - 24
    left_end = x + int(w * 0.52)
    right_start = x + int(w * 0.74)
    d.rectangle([x, deck, left_end, deck + 8], fill=(56, 56, 56))
    d.rectangle([right_start, deck, x + w, deck + 8], fill=(56, 56, 56))
    for px in (x + int(w * 0.18), x + int(w * 0.86)):
        d.rectangle([px, deck - 32, px + 6, deck], fill=(56, 56, 56))
        d.line([(px + 3, deck - 32), (px - 32, deck)], fill=(96, 96, 96),
               width=2)
        d.line([(px + 3, deck - 32), (px + 38, deck)], fill=(96, 96, 96),
               width=2)
    d.polygon([(left_end + 4, deck + 28), (right_start - 6, deck + 50),
               (right_start - 2, deck + 58), (left_end + 8, deck + 36)],
              fill=(56, 56, 56))
    for sx, sy, sr in ((left_end + 24, deck - 20, 10),
                       (left_end + 40, deck - 32, 13),
                       (left_end + 56, deck - 18, 9)):
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(205, 205, 205))
    burst(d, left_end + 38, deck - 4, 12, 5, 8, ORANGE)
    d.text((x + 10, y + h - 22), "KERCH STRAIT", font=bold_sans(10),
           fill=(255, 255, 255))


def art_gulf(d, x, y, w, h):
    """The Gulf in a narrow panel: Iran above, strikes marked."""
    d.rectangle([x, y, x + w, y + h], fill=(198, 221, 235), outline=INK,
                width=1)
    d.polygon([(x + w * 0.55, y), (x + w, y), (x + w, y + h * 0.42),
               (x + w * 0.68, y + h * 0.38), (x + w * 0.60, y + h * 0.16)],
              fill=SAND)
    d.polygon([(x, y + h * 0.66), (x + w * 0.34, y + h * 0.62),
               (x + w * 0.38, y + h), (x, y + h)], fill=SAND)
    small = bold_sans(10)
    d.text((x + w * 0.78, y + 6), "IRAN", font=small, fill=MUTED)
    d.text((x + 8, y + 6), "GULF", font=small, fill=DEEP)
    qx, qy = x + w * 0.66, y + h * 0.50
    d.ellipse([qx - 13, qy - 6, qx + 13, qy + 6], fill=SAND, outline=DEEP)
    burst(d, qx, qy - 11, 12, 5, 8, ORANGE)
    d.text((qx - 18, qy + 9), "QESHM", font=bold_sans(10), fill=CRIMSON)
    for fx, fy, name in ((x + w * 0.22, y + h * 0.60, "KUWAIT"),
                         (x + w * 0.30, y + h * 0.74, "BAHRAIN")):
        d.ellipse([fx - 4, fy - 4, fx + 4, fy + 4], fill=DEEP)
        d.text((fx + 7, fy - 6), name, font=bold_sans(9), fill=DEEP)
    d.text((x + 8, y + h - 18), "RIYADH \u2192", font=bold_sans(9),
           fill=CRIMSON)


def art_climate(d, x, y, w, h):
    """A warming globe over Antalya's coast, talks stalled."""
    d.rectangle([x, y, x + w, y + h], fill=PALE_SKY, outline=INK, width=1)
    cx, cy, r = x + w * 0.42, y + h * 0.50, 30
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=OCEAN, outline=INK,
              width=1)
    d.ellipse([cx - r * 0.55, cy - r * 0.75, cx + r * 0.10, cy - r * 0.10],
              fill=GREEN)
    d.ellipse([cx - r * 0.10, cy + r * 0.15, cx + r * 0.60, cy + r * 0.70],
              fill=GREEN)
    d.ellipse([cx - r, cy - r, cx + r, cy - r * 0.62], fill=(255, 255, 255))
    d.text((x + 8, y + 6), "ANTALYA", font=bold_sans(10), fill=DEEP)
    d.text((x + w - 44, y + 6), "COP31", font=bold_sans(10), fill=CRIMSON)
    # A red thermometer climbing beside the globe.
    tx = x + w * 0.88
    d.rectangle([tx, y + 30, tx + 9, y + h - 24], outline=INK, width=1,
                fill=(255, 255, 255))
    d.rectangle([tx, y + 36, tx + 9, y + 56], fill=CRIMSON)
    d.ellipse([tx - 4, y + h - 30, tx + 13, y + h - 12], fill=CRIMSON,
              outline=INK, width=1)
    d.text((x + 8, y + h - 18), "TALKS STALLED", font=bold_sans(9),
           fill=CRIMSON)


def art_ipo(d, x, y, w, h):
    """A share-price chart climbing to a record high."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=INK,
                width=1)
    for i in range(4):
        gy = y + 18 + i * 26
        d.line([(x + 12, gy), (x + w - 12, gy)], fill=(228, 228, 228),
               width=1)
    pts = [(x + 14, y + h - 26), (x + w * 0.28, y + h - 44),
           (x + w * 0.46, y + h - 34), (x + w * 0.64, y + h - 58),
           (x + w * 0.82, y + h - 44), (x + w - 16, y + 26)]
    d.line(pts, fill=GREEN, width=4, joint="curve")
    d.ellipse([pts[-1][0] - 6, pts[-1][1] - 6, pts[-1][0] + 6, pts[-1][1] + 6],
              fill=CRIMSON)
    d.text((x + 12, y + 8), "$83 A SHARE", font=bold_sans(12), fill=INK)
    d.text((x + w - 92, y + h - 24), "RECORD IPO", font=bold_sans(11),
           fill=GREEN)


def lead_story(d, x, y, kicker, art, headline, deck):
    """Kicker, art panel, headline and deck for a lead story."""
    d.text((x, y), kicker, font=bold_sans(15), fill=CRIMSON)
    art(d, x, y + 24, COL, 118)
    font = bold_serif(30)
    lines = wrap_text(d, headline, font, COL)
    ny = put_lines(d, x, y + 150, lines, font, INK, 36)
    body = wrap_text(d, deck, plain_sans(16), COL)
    put_lines(d, x, ny + 6, body, plain_sans(16), INK, 21)


def grid_card(d, x, y, kicker, headline, body, art):
    """One bordered card of the 2x2 grid, art panel on the right.

    Text is wrapped to the strip left of the art so nothing runs
    underneath the picture.
    """
    d.rectangle([x, y, x + COL, y + 148], outline=FAINT, width=1)
    pad = 12
    art_w = 110
    art(d, x + COL - art_w - 8, y + 8, art_w, 132)
    text_w = COL - pad * 2 - art_w - 8
    d.text((x + pad, y + 10), kicker, font=bold_sans(13), fill=CRIMSON)
    font = bold_serif(20)
    lines = wrap_text(d, headline, font, text_w)
    ny = put_lines(d, x + pad, y + 32, lines, font, INK, 25)
    blines = wrap_text(d, body, plain_sans(14), text_w)
    put_lines(d, x + pad, ny + 4, blines, plain_sans(14), INK, 19)


def build_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), CREAM)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.line([(EDGE, 20), (PAGE_W - EDGE, 20)], fill=INK, width=2)
    d.line([(EDGE, 24), (PAGE_W - EDGE, 24)], fill=INK, width=1)
    d.text((PAGE_W // 2, 28), "THE WORLD TODAY", font=bold_serif(58),
           fill=INK, anchor="mt")

    # Date band: the day this page sums up.
    d.rectangle([EDGE, 102, PAGE_W - EDGE, 142], fill=INK)
    d.text((PAGE_W // 2, 122), "THURSDAY, 19 NOVEMBER 2026",
           font=bold_sans(28), fill=(255, 255, 255), anchor="mm")

    # Two lead stories.
    lead_story(d, LEFT, 152, "DIPLOMACY  \u2022  SHENZHEN", art_summit,
               "TRUMP, XI AND PUTIN MEET IN SHENZHEN",
               "The first three-way summit, on the APEC sidelines, covers "
               "Ukraine, Iran, nuclear weapons, trade and AI. Trump expects "
               "\u201cwonderful things\u201d from the talks with Putin.")
    lead_story(d, RIGHT, 152, "JUSTICE  \u2022  THE HAGUE", art_court,
               "ICJ RULES ON MYANMAR GENOCIDE CASE",
               "The International Court of Justice rules on Gambia\u2019s "
               "genocide case against Myanmar over the Rohingya.")
    d.line([(PAGE_W // 2, 152), (PAGE_W // 2, 442)], fill=FAINT, width=1)
    d.line([(EDGE, 452), (PAGE_W - EDGE, 452)], fill=INK, width=2)

    # Four more stories.
    grid_card(d, LEFT, 464, "UKRAINE  \u2022  CRIMEA",
              "Bridge to Crimea hit for a third time in a week",
              "Ukraine struck the bridge again; traffic was suspended "
              "after a road section fell into the strait.",
              art_bridge)
    grid_card(d, RIGHT, 464, "MIDDLE EAST  \u2022  THE GULF",
              "Iran attacks Gulf states after U.S. strike",
              "Tehran hit back after the U.S. strike on Qeshm island. "
              "Kuwait repelled an Iranian attack; a Houthi missile "
              "targeted Riyadh.",
              art_gulf)
    grid_card(d, LEFT, 624, "CLIMATE  \u2022  ANTALYA",
              "COP31 deadlock persists as ministers meet",
              "Negotiators in Antalya are still stuck as ministers try "
              "to unblock the climate talks.",
              art_climate)
    grid_card(d, RIGHT, 624, "TECHNOLOGY  \u2022  AI",
              "Anthropic prices record IPO at $83 a share",
              "The AI lab\u2019s listing values it at up to $1.5 trillion "
              "\u2014 the largest IPO on record.",
              art_ipo)

    # In brief.
    by = 784
    d.text((EDGE, by), "IN BRIEF", font=bold_sans(15), fill=INK)
    d.line([(EDGE + 96, by + 10), (PAGE_W - EDGE, by + 10)], fill=FAINT,
           width=1)
    briefs = [
        "Van Gogh sells for a record $190.4m at Sotheby\u2019s",
        "IAEA: North Korea expanded uranium enrichment",
        "Unrest in Bangladesh: Yunus\u2019s home torched, 28 districts hit",
        "EU proposes a \u20ac45bn loan for Ukraine",
        "U.S. and Venezuela restore military cooperation",
        "Cyclone Aqwan heads for India\u2019s east coast",
        "Grand Theft Auto VI goes on sale after a 13-year wait",
        "Record rain from an atmospheric river hits California",
    ]
    # Keep six of the eight so each line stays on one line.
    briefs = briefs[:6]
    for i, item in enumerate(briefs):
        bx = LEFT if i % 2 == 0 else RIGHT
        yy = by + 28 + (i // 2) * 24
        d.text((bx, yy), "\u25aa  " + item, font=plain_sans(14), fill=INK)

    # Markets strip.
    my = 896
    d.rectangle([EDGE, my, PAGE_W - EDGE, my + 54], fill=PALE,
                outline=FAINT, width=1)
    d.text((EDGE + 14, my + 8), "MARKETS \u2014 THURSDAY CLOSE",
           font=bold_sans(14), fill=INK)
    d.text((EDGE + 14, my + 29),
           "S&P 500  7,324  \u25bc 0.23%    FTSE 100  10,551  \u25bc 1.30%    "
           "Hang Seng  \u25bc 2.78%    Brent  $89.3  \u25b2 0.15%",
           font=plain_sans(14), fill=INK)

    # Footer.
    d.text((PAGE_W // 2, 962),
           "All events of Thursday 19 November 2026, as reported by BBC, "
           "Reuters, Al Jazeera, AP and Bloomberg.",
           font=plain_sans(12), fill=MUTED, anchor="mt")
    d.line([(EDGE, 992), (PAGE_W - EDGE, 992)], fill=INK, width=2)

    return img


def main():
    page = build_page()
    page.save("entry.png", optimize=True)
    print("wrote entry.png", page.size)


if __name__ == "__main__":
    main()
