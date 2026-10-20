"""
STAMP: one header + one footer, copied into every English page.

Why this exists
---------------
Plain HTML has no "include" (no way to say "put the header here").
So every page carries its own copy of the header and footer. Changing
a link by hand in 17 files is slow and easy to get wrong, so instead
we change it ONCE, in this file, and run:

    python tools/stamp.py

from the project folder. The script finds the old header and footer
in each page and swaps in the new ones. Brand-new pages can use the
placeholders {{HEADER}} and {{FOOTER}} instead.

This only runs on YOUR computer while you build. The finished site is
still plain HTML + CSS: no JavaScript in the browser.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
EN = ROOT / "en"

# The five tabs. SOS sits in the middle, red, always one tap away.
TABS = [
    ("today", "Today"),
    ("streak", "Progress"),
    ("panic", "SOS"),
    ("journal", "Journal"),
    ("profile", "Me"),
]

# Which tab lights up on pages that aren't tabs themselves.
ACTIVE = {
    "checkIn": "today", "celebrate": "today", "slip": "today", "pause": "today",
    "start": "today", "settings": "profile", "how-it-works": "profile",
    # concept pages (ideas for later) sit under "Me"
    "community": "profile", "league": "profile", "shop": "profile",
    "savings": "profile", "anasa": "profile", "habit": "profile",
}

# Bump these whenever a stylesheet changes, so browsers fetch the new one
# instead of showing an old copy from their cache.
CSS_VERSION = {"styles": 9, "bead": 4}

# Pages that are ideas for later, not part of the MVP.
CONCEPTS = {"community", "league", "shop", "savings", "anasa", "habit"}


def header(R, P, active):
    links = []
    for page, label in TABS:
        sos = ' class="tab-sos"' if page == "panic" else ""
        here = ' aria-current="page"' if page == active else ""
        links.append(f'          <a href="{P}{page}.html"{sos}{here}>{label}</a>')
    links = "\n".join(links)
    return f'''<header class="site-header">
      <div class="wrap header-inner">
        <a class="wordmark" href="{R}index.html">Bead <span>by Bead</span></a>
        <!-- Five tabs. SOS sits in the middle as a red button so it's
             always one tap away (class="tab-sos"). -->
        <nav class="tabbar" aria-label="Main">
{links}
        </nav>
        <div class="header-actions">
          <!-- Two numbers that come straight from the record: beads earned
               and the current streak. No coins, no XP. alt="" on the icons
               because the sr-only text says it in words. -->
          <ul class="stat-chips" aria-label="Your record (example)">
            <li><a class="chip-bead" href="{P}streak.html"><img class="icon" src="{R}../Images/icons/bead.svg" alt="" />24<span class="sr-only"> beads earned</span></a></li>
            <li><a class="chip-flame" href="{P}streak.html"><img class="icon" src="{R}../Images/icons/flame.svg" alt="" />5<span class="sr-only"> day streak</span></a></li>
          </ul>
        </div>
      </div>
    </header>'''


def footer(R, P):
    return f'''<footer class="site-footer">
      <div class="shuka" aria-hidden="true"></div>
      <div class="wrap footer-inner">
        <div>
          <img class="footer-mascot" src="{R}../Images/illustrated/malebo.svg" alt="" width="216" height="208" loading="lazy" />
          <p class="wordmark">Bead <span>by Bead</span></p>
          <p class="footer-motto">One day at a time. One bead at a time.</p>
        </div>
        <nav class="footer-col" aria-label="The app">
          <h2>The app</h2>
          <ul>
            <li><a href="{P}start.html">Make your plan</a></li>
            <li><a href="{P}today.html">Today</a></li>
            <li><a href="{P}checkIn.html">Evening check-in</a></li>
            <li><a href="{P}streak.html">Progress</a></li>
            <li><a href="{P}panic.html">SOS</a></li>
            <li><a href="{P}journal.html">Journal</a></li>
            <li><a href="{P}settings.html">Settings</a></li>
            <li><a href="{P}how-it-works.html">How it works</a></li>
          </ul>
        </nav>
        <nav class="footer-col" aria-label="Ideas for later">
          <h2>Ideas for later</h2>
          <ul>
            <li><a href="{P}community.html">Group &amp; partner</a></li>
            <li><a href="{P}league.html">League</a></li>
            <li><a href="{P}shop.html">Shop</a></li>
            <li><a href="{P}savings.html">Savings goals</a></li>
          </ul>
        </nav>
      </div>
      <div class="wrap footer-base">
        <p>For ages 18+. · Need to talk to someone? Call <a href="tel:1192">1192</a>, NACADA's free 24/7 helpline for alcohol and drugs.</p>
        <p>Bead by Bead is a prototype: nothing you type is saved, and every name, date and number is an example. · <a href="{R}../index.html">Kenyan voice (Kiswahili &amp; Sheng)</a></p>
      </div>
    </footer>'''


CONCEPT_NOTE = '''<p class="concept-note"><strong>Idea for later.</strong> This page is a design concept, not part of the first version. We'll only build it if testing shows people need it.</p>'''


def head_links(R):
    """Fonts, stylesheets and icon: the same on every English page."""
    return f'''<link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,800&family=Caveat:wght@600&family=Manrope:wght@400;600;800&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="{R}../CSS/styles.css?v={CSS_VERSION['styles']}" />
    <!-- The Bead by Bead look (cream paper, forest ink, flag colours).
         Loaded second so it wins over styles.css. -->
    <link rel="stylesheet" href="{R}../CSS/bead.css?v={CSS_VERSION['bead']}" />
    <link rel="icon" href="{R}../Images/icons/bead.svg" />
  </head>'''


def stamp(path):
    s = path.read_text(encoding="utf-8")
    at_root = path.parent == EN
    R, P = ("", "pages/") if at_root else ("../", "")
    active = path.stem if path.stem in dict(TABS) else ACTIVE.get(path.stem, "")

    # Everything from the first font link to </head> is replaced.
    s, n = re.subn(r'<link rel="preconnect" href="https://fonts.googleapis.com" />.*?</head>',
                   lambda _: head_links(R), s, count=1, flags=re.S)
    assert n == 1, f"no font links found in {path}"

    # The landing page has its own big header, so only its footer is stamped.
    if "landing-header" not in s:
        if "{{HEADER}}" in s:
            s = s.replace("{{HEADER}}", header(R, P, active))
        else:
            s, n = re.subn(r'<header class="site-header">.*?</header>',
                           lambda _: header(R, P, active), s, flags=re.S)
            assert n == 1, f"no header found in {path}"

    if "{{FOOTER}}" in s:
        s = s.replace("{{FOOTER}}", footer(R, P))
    else:
        s, n = re.subn(r'<footer class="site-footer">.*?</footer>',
                       lambda _: footer(R, P), s, flags=re.S)
        assert n == 1, f"no footer found in {path}"

    # Concept pages get a yellow note right at the top of <main>.
    if path.stem in CONCEPTS and "concept-note" not in s:
        s = s.replace('<main id="main">', '<main id="main">\n      ' + CONCEPT_NOTE, 1)

    path.write_text(s, encoding="utf-8")


if __name__ == "__main__":
    pages = [EN / "index.html", *sorted((EN / "pages").glob("*.html"))]
    for page in pages:
        stamp(page)
    print(f"Stamped {len(pages)} English pages.")
