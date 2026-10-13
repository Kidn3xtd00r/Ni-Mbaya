"""Draw Malebo as flat SVG illustrations (one kit, many moods).

Used by the English edition (en/). Every picture of Malebo there is built
from the same simple shapes, so all his moods match perfectly.
To change him (skin tone, hoodie colour, a new mood...), edit this file and
run it from the project root:   python Images/illustrated/make_malebo.py
It rewrites the .svg files in this folder.

(This is Python, not part of the website. It's a little "drawing machine"
that writes the SVG files for you. The site itself is still HTML + CSS.)"""
import math, pathlib

OUT = pathlib.Path('Images/illustrated'); OUT.mkdir(parents=True, exist_ok=True)

SKIN = '#8a5434'; SKIN_DARK = '#6e4027'; HAIR = '#151515'; HOODIE = '#1c1c1c'; HOODIE_DARK = '#111'
RED = '#c8102e'; GREEN = '#0f8a3c'; WHITE = '#f2f0ea'; BLACK = '#0b0b0b'

def locs():
    # short twists: rounded capsules fanned over the top of the head
    out = []
    for i in range(13):
        a = math.radians(-160 + i * (140 / 12))          # from left to right over the top
        cx = 100 + 40 * math.cos(a); cy = 86 + 40 * math.sin(a)
        rot = math.degrees(a) + 90
        out.append(f'<rect x="{cx-7:.1f}" y="{cy-15:.1f}" width="14" height="26" rx="7" fill="{HAIR}" transform="rotate({rot:.1f} {cx:.1f} {cy:.1f})"/>')
    # a few on top, pointing up, for volume
    for dx, dy, r in [(-22, 46, -18), (-8, 40, -6), (8, 40, 6), (22, 46, 18), (0, 50, 0)]:
        out.append(f'<rect x="{100+dx-7}" y="{dy-12}" width="14" height="28" rx="7" fill="{HAIR}" transform="rotate({r} {100+dx} {dy})"/>')
    return '\n  '.join(out)

def necklace():
    # flag-order beads along an arc under the chin
    cols = [BLACK, WHITE, RED, WHITE, GREEN]
    out = []
    n = 11
    for i in range(n):
        t = i / (n - 1)
        a = math.radians(200 - t * 220 + 0)               # arc
        x = 100 + 30 * math.cos(math.radians(160 + t * -140 + 180)) * -1
        x = 72 + t * 56
        y = 136 + 10 * math.sin(math.pi * t)
        c = cols[i % 5]
        stroke = ' stroke="#333" stroke-width="1"' if c == BLACK else ''
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.2" fill="{c}"{stroke}/>')
    # the Ngao (shield) charm in the middle
    out.append(f'<g transform="translate(100 150)"><ellipse rx="6" ry="8.5" fill="{RED}" stroke="{BLACK}" stroke-width="2"/>'
               f'<rect x="-1.4" y="-8" width="2.8" height="16" fill="{WHITE}"/></g>')
    return '\n  '.join(out)

def body():
    return f'''<path d="M50 150 C52 118 74 104 100 104 C126 104 148 118 150 150 Z" fill="{HOODIE_DARK}"/>
  <path d="M22 200 C24 158 56 134 100 134 C144 134 176 158 178 200 Z" fill="{HOODIE}"/>
  <path d="M64 140 C70 158 130 158 136 140 C128 132 72 132 64 140 Z" fill="{HOODIE_DARK}"/>
  <!-- shuka over the left shoulder: stripes clipped to a band -->
  <clipPath id="shuka"><path d="M120 136 C150 140 172 160 178 200 L140 200 C136 172 126 152 112 142 Z"/></clipPath>
  <g clip-path="url(#shuka)">
    <rect x="100" y="120" width="90" height="90" fill="{RED}"/>
    <g fill="{BLACK}">
      <rect x="100" y="138" width="90" height="5" transform="rotate(35 140 160)"/>
      <rect x="100" y="158" width="90" height="5" transform="rotate(35 140 160)"/>
      <rect x="100" y="178" width="90" height="5" transform="rotate(35 140 160)"/>
    </g>
    <g fill="{GREEN}">
      <rect x="100" y="147" width="90" height="6" transform="rotate(35 140 160)"/>
      <rect x="100" y="167" width="90" height="6" transform="rotate(35 140 160)"/>
    </g>
  </g>
  <!-- drawstrings -->
  <path d="M88 152 L86 182 M112 152 L114 182" stroke="#3a3a3a" stroke-width="2.4" stroke-linecap="round"/>
  <circle cx="86" cy="184" r="2.6" fill="{WHITE}"/><circle cx="114" cy="184" r="2.6" fill="{WHITE}"/>
  <!-- neck -->
  <rect x="88" y="114" width="24" height="24" rx="8" fill="{SKIN_DARK}"/>'''

def head():
    return f'''<circle cx="61" cy="90" r="7" fill="{SKIN}"/>
  <circle cx="139" cy="90" r="7" fill="{SKIN}"/>
  <circle cx="139" cy="97" r="2.4" fill="none" stroke="#cfcfcf" stroke-width="1.6"/>
  <ellipse cx="100" cy="86" rx="38" ry="40" fill="{SKIN}"/>'''

# ---- faces: eyes + brows + mouth per mood ----
def shades():
    return f'''<g>
    <rect x="68" y="78" width="28" height="18" rx="7" fill="{BLACK}"/>
    <rect x="104" y="78" width="28" height="18" rx="7" fill="{BLACK}"/>
    <rect x="94" y="82" width="12" height="4" rx="2" fill="{BLACK}"/>
    <rect x="73" y="81" width="9" height="3" rx="1.5" fill="#ffffff" opacity=".55"/>
    <rect x="109" y="81" width="9" height="3" rx="1.5" fill="#ffffff" opacity=".55"/>
  </g>'''

FACES = {
 # big grin + shades: the classic Malebo
 'hype': lambda: shades() + f'''
  <path d="M82 104 Q100 124 118 104 Z" fill="{WHITE}" stroke="{BLACK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M86 107 L114 107" stroke="#ddd" stroke-width="1.2"/>''',
 # round glasses, soft closed smile
 'calm': lambda: f'''
  <circle cx="83" cy="86" r="11" fill="none" stroke="{BLACK}" stroke-width="3"/>
  <circle cx="117" cy="86" r="11" fill="none" stroke="{BLACK}" stroke-width="3"/>
  <path d="M94 86 Q100 82 106 86" fill="none" stroke="{BLACK}" stroke-width="3"/>
  <path d="M78 87 Q83 83 88 87" fill="none" stroke="{BLACK}" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M112 87 Q117 83 122 87" fill="none" stroke="{BLACK}" stroke-width="2.6" stroke-linecap="round"/>
  <path d="M88 106 Q100 115 112 106" fill="none" stroke="{BLACK}" stroke-width="3" stroke-linecap="round"/>''',
 # one raised brow, flat unimpressed mouth
 'pressure': lambda: f'''
  <path d="M72 72 L92 75" stroke="{BLACK}" stroke-width="4" stroke-linecap="round"/>
  <path d="M108 70 Q118 64 128 70" fill="none" stroke="{BLACK}" stroke-width="4" stroke-linecap="round"/>
  <ellipse cx="83" cy="87" rx="5" ry="4" fill="{BLACK}"/>
  <ellipse cx="117" cy="86" rx="5" ry="5.5" fill="{BLACK}"/>
  <path d="M88 109 L112 107" stroke="{BLACK}" stroke-width="3.5" stroke-linecap="round"/>''',
 # narrowed eyes, sly toothy grin
 'chaos': lambda: f'''
  <path d="M72 76 L93 82" stroke="{BLACK}" stroke-width="4" stroke-linecap="round"/>
  <path d="M128 76 L107 82" stroke="{BLACK}" stroke-width="4" stroke-linecap="round"/>
  <path d="M75 88 Q83 84 91 88" fill="none" stroke="{BLACK}" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M109 88 Q117 84 125 88" fill="none" stroke="{BLACK}" stroke-width="3.5" stroke-linecap="round"/>
  <path d="M80 102 Q100 122 122 100 Q100 110 80 102 Z" fill="{WHITE}" stroke="{BLACK}" stroke-width="2.5" stroke-linejoin="round"/>
  <path d="M90 105 L91 111 M100 107 L100 114 M110 105 L109 111" stroke="{BLACK}" stroke-width="1.5"/>''',
}

BG = {'hype': '#f4b400', 'calm': '#3fbf5a', 'pressure': '#f26b1d', 'chaos': '#e3262d'}

def halo():
    cols = [BLACK, WHITE, RED, WHITE, GREEN]
    out = [f'<circle cx="100" cy="100" r="92" fill="none" stroke="#6b5a45" stroke-width="1.5"/>']
    n = 40
    for i in range(n):
        a = math.radians(i * 360 / n - 90)
        x = 100 + 92 * math.cos(a); y = 100 + 92 * math.sin(a)
        if i % 8 == 0:   # the Ngao shield every 8th position, rotated along the ring
            out.append(f'<g transform="translate({x:.1f} {y:.1f}) rotate({i*360/n:.1f})"><ellipse rx="5.5" ry="7.5" fill="{RED}" stroke="{BLACK}" stroke-width="1.6"/><rect x="-1.2" y="-7" width="2.4" height="14" fill="{WHITE}"/></g>')
        else:
            c = cols[i % 5]
            stroke = ' stroke="#444" stroke-width="1"' if c == BLACK else ''
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{c}"{stroke}/>')
    return '\n  '.join(out)

def character(mood, with_bg, with_halo=False):
    bg = halo() if with_halo else ''
    if with_bg:
        bg = f'<rect width="200" height="200" fill="{BG[mood]}"/>\n  <circle cx="100" cy="96" r="78" fill="#000" opacity=".12"/>'
    vb = '-8 -8 216 208' if with_halo else '0 0 200 200'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img">
  {bg}
  {body()}
  {necklace()}
  {head()}
  {locs()}
  {FACES[mood]()}
</svg>
'''

for mood in FACES:
    (OUT / f'malebo-{mood}.svg').write_text(character(mood, True), encoding='utf-8')
(OUT / 'malebo.svg').write_text(character('hype', False, True), encoding='utf-8')
print('written', sorted(p.name for p in OUT.iterdir()))
