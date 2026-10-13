"""
MAKE ART: draws the Kenyan bead artwork as SVG files.

    python tools/make_art.py

It writes:
  Images/illustrated/bracelet.svg   the woven flag bracelet, bead by bead
  Images/illustrated/ngao-beads.svg the shield day on the Progress bracelet
  Images/icons/bead.svg             one bead, for the stat chip

Why draw it with code instead of using a photo?
  - Photos online belong to the people who took them. This art is ours.
  - Every bead is placed by a rule, the same way a real bracelet is
    woven: row colours from the flag, and the shield and spears in the
    middle are just beads that change colour inside a shape.
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

BLACK, WHITE, RED, GREEN = "#141414", "#f5f2ec", "#c8102e", "#0a7a3b"

# The flag, top to bottom, as 8 rows of beads (like the real bracelet)
ROWS = [BLACK, BLACK, WHITE, RED, RED, WHITE, GREEN, GREEN]

COLS = 41          # beads along the band (odd, so there's a true middle)
STEP = 12          # distance between bead centres
R = 5.2            # bead radius
PAD = 14           # space around the band


def bead_colour(col, row, cols=COLS, width=2.6, reach=9, spread=2.2):
    """Which colour is the bead at this column and row?
    cols   = how many columns the whole piece has
    width  = how wide the shield is (in beads, from the middle)
    reach  = how far the spears stick out from the middle
    spread = how steep the spears are"""
    mid_x = (cols - 1) / 2
    mid_y = (len(ROWS) - 1) / 2
    dx = (col - mid_x) / width    # the shield is an oval: narrow ...
    dy = (row - mid_y) / 4.3      # ... and tall
    inside = dx * dx + dy * dy

    if inside <= 1.0:
        if col == mid_x:                  # white line down the middle
            return WHITE
        if inside >= 0.55:                # black rim of the shield
            return BLACK
        return RED                        # red face of the shield

    # The two spears: white beads on two diagonal lines through the middle
    for slope in (1.25, -1.25):
        if abs((row - mid_y) - slope * (col - mid_x) / spread) < 0.5 and abs(col - mid_x) < reach:
            return WHITE

    return ROWS[row]


def bead(cx, cy, colour):
    # One bead: a circle, plus a small shine so it looks round
    return (f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{R}" fill="{colour}"/>'
            f'<circle cx="{cx - 1.6:.1f}" cy="{cy - 1.8:.1f}" r="1.5" fill="#fff" fill-opacity=".45"/>')


def bracelet():
    w = PAD * 2 + STEP * (COLS - 1)
    h = PAD * 2 + STEP * (len(ROWS) - 1)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
             f'role="img" aria-label="A Kenyan flag bracelet made of beads, with the Maasai shield and spears in the middle">']
    for col in range(COLS):
        for row in range(len(ROWS)):
            parts.append(bead(PAD + col * STEP, PAD + row * STEP, bead_colour(col, row)))
    parts.append("</svg>")
    return "\n".join(parts)


def ngao():
    """The shield day on the Progress bracelet: a CHARM sitting on the beads.
    Behind: 9 columns of normal flag beads. On top: the two crossed spears
    and the Maasai shield from the flag, drawn as smooth shapes so they're
    clear even when the bracelet is small. styles.css uses this picture
    for .day--ngao. No padding, so it lines up with the other days."""
    cols, step, r = 9, 12, 5.2
    w, h = cols * step, len(ROWS) * step
    cx, cy = w / 2, h / 2
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" aria-hidden="true">']
    # 1. the beads behind
    for col in range(cols):
        for row in range(len(ROWS)):
            parts.append(bead(step / 2 + col * step, step / 2 + row * step, ROWS[row]))
    # 2. the spears: a white shaft with a dark outline, crossed in an X
    for x1, x2 in ((6, w - 6), (w - 6, 6)):
        parts.append(f'<line x1="{x1}" y1="5" x2="{x2}" y2="{h - 5}" stroke="{BLACK}" stroke-width="6" stroke-linecap="round"/>'
                     f'<line x1="{x1}" y1="5" x2="{x2}" y2="{h - 5}" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>')
    # 3. the shield: black edge, red face, white band down the middle
    parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="44" fill="{BLACK}"/>'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="17" ry="39" fill="{RED}"/>'
                 f'<path d="M{cx - 4} {cy - 37} Q{cx} {cy - 41} {cx + 4} {cy - 37} V{cy + 37} Q{cx} {cy + 41} {cx - 4} {cy + 37} Z" fill="{WHITE}"/>'
                 f'<ellipse cx="{cx}" cy="{cy}" rx="3" ry="9" fill="{BLACK}"/>'
                 f'<ellipse cx="{cx - 6}" cy="{cy - 14}" rx="4" ry="10" fill="#fff" fill-opacity=".25"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def bead_icon():
    # A single bead with the flag's stripes inside it
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" aria-hidden="true">
<defs><clipPath id="c"><circle cx="12" cy="12" r="10"/></clipPath></defs>
<g clip-path="url(#c)">
<rect width="24" height="7" y="2" fill="#141414"/><rect width="24" height="2" y="9" fill="#f5f2ec"/>
<rect width="24" height="4" y="11" fill="#c8102e"/><rect width="24" height="2" y="15" fill="#f5f2ec"/>
<rect width="24" height="7" y="17" fill="#0a7a3b"/></g>
<circle cx="12" cy="12" r="10" fill="none" stroke="#f5f2ec" stroke-width="1.5"/>
<circle cx="8.5" cy="7.5" r="2" fill="#fff" fill-opacity=".5"/>
</svg>'''


if __name__ == "__main__":
    (ROOT / "Images/illustrated/bracelet.svg").write_text(bracelet(), encoding="utf-8")
    (ROOT / "Images/illustrated/ngao-beads.svg").write_text(ngao(), encoding="utf-8")
    (ROOT / "Images/icons/bead.svg").write_text(bead_icon(), encoding="utf-8")
    print("Drew bracelet.svg, ngao-beads.svg and bead.svg")
