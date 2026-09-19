#!/usr/bin/env python3
"""Regenerate the proof's SVG figures using only the Python standard library.

Run from any directory with ``python3 scripts/make_figures.py``. All lengths in
the geometric panels are proportional to their stated numerical example. Where
panels have different scales, the diagram explicitly says so.
"""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "figures"
INK = "#173c42"
TEAL = "#167d8d"
TEAL_LIGHT = "#e6f1f0"
AMBER = "#d69b36"
AMBER_LIGHT = "#f4dfb9"
PAPER = "#faf9f6"
MUTED = "#567075"
RULE = "#d6dfdc"
FONT = "Arial, Helvetica, sans-serif"


class Drawing:
    def __init__(self, title, description, height=560):
        self.height = height
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" '
            f'viewBox="0 0 1100 {height}" role="img" aria-labelledby="title desc">',
            f"<title id=\"title\">{escape(title)}</title>",
            f"<desc id=\"desc\">{escape(description)}</desc>",
            '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 0 L 10 5 L 0 10 z" fill="{TEAL}"/></marker></defs>',
        ]
        self.rect(0, 0, 1100, height, PAPER, radius=16)

    def rect(self, x, y, w, h, fill, stroke="none", sw=1, radius=0):
        self.parts.append(
            f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" '
            f'rx="{radius:g}" fill="{fill}" stroke="{stroke}" stroke-width="{sw:g}"/>'
        )

    def line(self, x1, y1, x2, y2, color=INK, width=1.5, dash=None, arrow=False):
        attrs = f' stroke-dasharray="{dash}"' if dash else ""
        if arrow:
            attrs += ' marker-end="url(#arrow)"'
        self.parts.append(
            f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" '
            f'stroke="{color}" stroke-width="{width:g}"{attrs}/>'
        )

    def text(self, x, y, content, size=20, color=INK, weight="normal", anchor="start"):
        self.parts.append(
            f'<text x="{x:g}" y="{y:g}" font-family="{FONT}" font-size="{size:g}" '
            f'fill="{color}" font-weight="{weight}" text-anchor="{anchor}">'
            f"{escape(str(content))}</text>"
        )

    def heading(self, title, subtitle):
        self.text(42, 48, title, 28, weight="bold")
        self.text(42, 80, subtitle, 18, MUTED)

    def hdim(self, x1, x2, y, label, above=True, color=INK):
        self.line(x1, y, x2, y, color, 1.25)
        self.line(x1, y - 5, x1, y + 5, color, 1.25)
        self.line(x2, y - 5, x2, y + 5, color, 1.25)
        self.text((x1 + x2) / 2, y - 10 if above else y + 26, label, 18, color, anchor="middle")

    def strip(self, x, y, a, b, k, scale):
        """k adjacent a-by-b rectangles; a b-square and a b-by-c remainder."""
        width, height = k * a * scale, b * scale
        c = k * a - b
        self.rect(x, y, width, height, TEAL_LIGHT)
        if c:
            self.rect(x + b * scale, y, c * scale, height, AMBER_LIGHT)
        for i in range(1, k):
            self.line(x + i * a * scale, y, x + i * a * scale, y + height, TEAL, 1.3, "5 5")
        self.rect(x, y, width, height, "none", TEAL, 2)
        self.rect(x, y, b * scale, height, "none", INK, 2.5)
        return width, height

    def save(self, filename):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / filename).write_text("\n".join(self.parts + ["</svg>"]) + "\n", encoding="utf-8")


def construction():
    d = Drawing(
        "The rectangle construction: c equals ka minus b",
        "A correctly scaled example with a=8, b=30, k=4. Four adjacent 8-by-30 "
        "rectangles make a 32-by-30 strip. Removing its 30-by-30 square leaves "
        "a 2-by-30 rectangle of area 60. This equals 8 squared minus 4. The "
        "8-by-8 square at right is at the same scale and illustrates area accounting, "
        "not a claimed dissection of that square.",
        580,
    )
    d.heading("A new side appears in the leftover strip", "Example: a = 8, b = 30, k = 4.  Dashed lines mark the original rectangles.")
    x, y, s = 88, 160, 10
    d.strip(x, y, 8, 30, 4, s)
    d.hdim(x, x + 320, 133, "ka = 32")
    d.text(x + 150, y + 146, "b²", 36, weight="bold", anchor="middle")
    d.text(x + 150, y + 176, "30 × 30 = 900", 18, MUTED, anchor="middle")
    d.hdim(x, x + 300, 486, "b = 30", above=False)
    d.line(58, y, 58, y + 300, MUTED, 1.25)
    d.line(53, y, 63, y, MUTED, 1.25)
    d.line(53, y + 300, 63, y + 300, MUTED, 1.25)
    d.parts.append(f'<text x="39" y="310" font-family="{FONT}" font-size="18" fill="{MUTED}" text-anchor="middle" transform="rotate(-90 39 310)">b = 30</text>')
    d.line(398, 461, 435, 489, AMBER, 2)
    d.text(445, 500, "c = 2", 19, INK, weight="bold")
    d.line(470, 137, 470, 452, RULE, 1)

    d.text(524, 151, "LENGTH", 14, TEAL, weight="bold")
    d.text(524, 194, "c = ka − b", 34, weight="bold")
    d.text(524, 229, "2 = 4 · 8 − 30", 21, MUTED)
    d.text(524, 293, "AREA", 14, TEAL, weight="bold")
    d.text(524, 334, "bc = kab − b² = a² − k", 27, weight="bold")
    d.text(524, 370, "60 = 960 − 900 = 64 − 4", 21, MUTED)
    d.rect(524, 409, 80, 80, TEAL_LIGHT, TEAL, 2)
    d.text(564, 442, "a²", 24, weight="bold", anchor="middle")
    d.text(564, 470, "64", 20, MUTED, anchor="middle")
    d.text(628, 440, "The a-square has area bc + k.", 20)
    d.text(628, 470, "Area identity; no dissection is assumed.", 17, MUTED)
    d.text(42, 550, "All shapes use the same length scale.  Amber marks the b × c remainder.", 16, MUTED)
    d.save("construction.svg")


def descent_one():
    d = Drawing(
        "First jump from (30,112) to (8,30)",
        "Four 30-by-112 rectangles make a 120-by-112 strip. After removing the "
        "112-square, its 8-by-112 remainder determines c=8. Re-pairing c with "
        "a=30 gives the new pair (8,30), whose quotient remains 4. The original "
        "strip and the new 8-by-30 rectangle are drawn at different explicitly "
        "stated scales; this is a re-pairing of lengths, not a physical reshaping.",
        560,
    )
    d.heading("Keep the new side; pair it with the old smaller side", "First jump: (a, b) = (30, 112) becomes (c, a) = (8, 30), with k = 4.")
    d.text(54, 125, "1. FIND c IN THE STRIP", 14, TEAL, weight="bold")
    x, y, s = 90, 178, 2.2
    w, h = d.strip(x, y, 30, 112, 4, s)
    d.hdim(x, x + w, 156, "ka = 120")
    d.text(x + 112 * s / 2, y + 115, "112²", 30, weight="bold", anchor="middle")
    d.text(x + 112 * s / 2, y + 145, "removed square", 17, MUTED, anchor="middle")
    d.hdim(x, x + 112 * s, 450, "b = 112", above=False)
    d.line(x + w - 9, y + h, 389, 451, AMBER, 2)
    d.text(399, 462, "c = 8", 20, weight="bold")
    d.text(54, 519, "Remainder: 112 · 8 = 30² − 4.", 19, MUTED)

    d.line(441, 279, 577, 279, TEAL, 2.5, arrow=True)
    d.text(509, 244, "c = 4a − b", 19, anchor="middle")
    d.text(509, 316, "use (c, a)", 18, MUTED, anchor="middle")

    d.text(624, 125, "2. FORM THE NEXT PAIR", 14, TEAL, weight="bold")
    d.rect(642, 180, 64, 240, TEAL_LIGHT, TEAL, 2)
    d.hdim(642, 706, 154, "8")
    d.line(724, 180, 724, 420, MUTED, 1.25)
    d.line(719, 180, 729, 180, MUTED, 1.25)
    d.line(719, 420, 729, 420, MUTED, 1.25)
    d.text(738, 307, "30", 19, MUTED)
    d.text(805, 219, "(8, 30)", 33, weight="bold")
    d.text(805, 267, "Same quotient:", 18, MUTED)
    d.text(805, 305, "8² + 30² = 964", 20)
    d.line(805, 319, 1045, 319, RULE, 1.5)
    d.text(805, 352, "8 · 30 + 1 = 241", 20)
    d.text(805, 400, "964 / 241 = 4", 23, TEAL, weight="bold")
    d.text(624, 473, "The new larger side is 30 < 112.", 20, weight="bold")
    d.text(624, 519, "Panels use different scales; all side ratios are exact.", 15, MUTED)
    d.save("descent-1.svg")


def descent_two():
    d = Drawing(
        "An entire descent with fixed quotient four",
        "The chain (30,112), (8,30), (2,8), (0,2). Each arrow replaces (a,b) "
        "by (4a-b,a). The larger side strictly decreases: 112,30,8,2. The "
        "zero in the final pair is a boundary endpoint, and the invariant "
        "there states 0 squared plus 2 squared equals 4 times (0 times 2 plus 1). "
        "This is a symbolic flow diagram; boxes are not geometric lengths.",
        430,
    )
    d.heading("The same move repeats — until one side is zero", "A complete descent for k = 4.  This is a symbolic chain, not a length-scale diagram.")
    cards = [
        (40, "(30, 112)", "larger side: 112", "4 · 30 − 112 = 8", False),
        (307, "(8, 30)", "larger side: 30", "4 · 8 − 30 = 2", False),
        (574, "(2, 8)", "larger side: 8", "4 · 2 − 8 = 0", False),
        (841, "(0, 2)", "boundary endpoint", "k = 2² = 4", True),
    ]
    for x, pair, smaller, equation, terminal in cards:
        d.rect(x, 138, 219, 178, "#fffefb", AMBER if terminal else RULE, 1.5, 12)
        d.rect(x + 18, 157, 6, 28, AMBER if terminal else TEAL, radius=3)
        d.text(x + 109.5, 201, pair, 29, weight="bold", anchor="middle")
        d.text(x + 109.5, 239, smaller, 17, MUTED, anchor="middle")
        d.line(x + 22, 260, x + 197, 260, RULE, 1)
        d.text(x + 109.5, 292, equation, 18, TEAL if not terminal else INK, weight="bold", anchor="middle")
    for x in [259, 526, 793]:
        d.line(x + 9, 213, x + 39, 213, TEAL, 2.5, arrow=True)
    d.text(550, 371, "112  >  30  >  8  >  2", 29, weight="bold", anchor="middle")
    d.text(550, 404, "A strictly decreasing sequence of nonnegative integer sides cannot continue forever.", 18, MUTED, anchor="middle")
    d.save("descent-2.svg")


def terminal():
    d = Drawing(
        "At the terminal case k is the area of an integer square",
        "For a=2, b=8, k=4, four 2-by-8 rectangles exactly fill an 8-by-8 square. "
        "No strip remains, so c=0 and bc=a squared minus k gives k=a squared. "
        "The accompanying 2-by-2 square is shown at the same scale, divided into "
        "four unit squares, so the terminal quotient is 4=2 squared.",
        560,
    )
    d.heading("At the boundary, the leftover width vanishes", "Terminal jump: (a, b) = (2, 8) becomes (0, 2).  Here ka = b, so c = 0.")
    x, y, s = 86, 164, 36
    d.strip(x, y, 2, 8, 4, s)
    d.hdim(x, x + 288, 139, "ka = b = 8")
    for i in range(4):
        d.text(x + (i + 0.5) * 72, y + 152, "2 × 8", 18, TEAL, anchor="middle")
    d.hdim(x, x + 288, 479, "four rectangles fill one square", above=False)
    d.line(429, 132, 429, 479, RULE, 1)
    d.text(486, 155, "NO REMAINDER", 14, TEAL, weight="bold")
    d.text(486, 201, "bc = a² − k = 0", 31, weight="bold")
    d.text(486, 249, "Therefore k = a².", 33, TEAL, weight="bold")
    d.text(486, 300, "The quotient is an integer square.", 21, MUTED)
    for row in range(2):
        for col in range(2):
            d.rect(486 + col * s, 350 + row * s, s, s, AMBER_LIGHT, PAPER, 2)
    d.rect(486, 350, 72, 72, "none", AMBER, 2)
    d.hdim(486, 558, 444, "a = 2", above=False)
    d.text(595, 377, "4 unit squares", 22, weight="bold")
    d.text(595, 413, "k = 4 = 2²", 27, TEAL, weight="bold")
    d.text(42, 535, "Both squares use the same length scale.  The terminal pair (0, 2) is an auxiliary boundary case.", 16, MUTED)
    d.save("terminal-case.svg")


def main():
    construction()
    descent_one()
    descent_two()
    terminal()
    print("Generated four SVG figures in", OUT)


if __name__ == "__main__":
    main()
