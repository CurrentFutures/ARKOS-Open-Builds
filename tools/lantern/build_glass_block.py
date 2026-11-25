# Writes the Lantern's glass block version into builds/the-lantern/.
# Print it with: node ../make-pdf.js <html> <pdf>   (from tools/)
import os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); TOOLS = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(TOOLS, 'guide'))
from diagrams import svg, R, L, P, T, C, dh, dv, lead, DEFS
OUT = os.path.join(TOOLS, '..', 'builds', 'the-lantern', 'the-lantern-glass-block-version.html')
CSS = re.search(r"CSS=r'''(.*?)'''", open(os.path.join(TOOLS, 'guide', 'build_guide.py')).read(), re.S).group(1) + '''
h2{break-before:auto;margin-top:28px}h2.pg{break-before:page;margin-top:0}
ol.steps{counter-reset:st}
table.cmp td:first-child{color:var(--dim);white-space:nowrap}
svg .gb{fill:var(--glass);stroke:var(--part);stroke-width:1}
svg .airf{stroke:var(--dim);stroke-width:1.2;fill:none;stroke-dasharray:5 3}
figure.big svg text{font-size:12px}figure.big svg text.d{font-size:11px}
.tbl table.parts{break-inside:auto}.tbl table.parts tr{break-inside:avoid}
h2{break-after:avoid}
'''
B, TH, J = 197, 98, 2          # block face, block thickness, joint (mm)
OUTER = B + TH + J             # pinwheel: outside = face + thickness
VOID = B - TH                  # inside = face - thickness

def plan():   # from above: four blocks in a pinwheel around the open middle
    o, v0, v1 = OUTER, TH + J / 2, B + J / 2
    b = R(-12, -12, o + 24, o + 24, 'conc')
    b += R(0, 0, B, TH, 'gb') + R(B + J, 0, TH, B, 'gb') + R(TH + J, B + J, B, TH, 'gb') + R(0, TH + J, TH, B, 'gb')
    b += R(v0, v0, VOID - J, VOID - J, 'void') + R(v0 + 22, v0 + 33, 33, 18, 'pc')
    for x, y in ((v0 + 4, v0 + 4), (v1 - 8, v0 + 4), (v0 + 4, v1 - 8), (v1 - 8, v1 - 8)): b += R(x, y, 4, 4, 'led')
    b += dh(0, o, -24, f'about {o}') + dv(o + 26, v0, v1, f'{VOID}', 1)
    b += lead(B / 2, TH / 2, B / 2, -50, 'End block: its finished end faces out at the corner', 'middle')
    b += lead(v0 + 38, v0 + 42, o + 60, v0 + 20, 'Raspberry Pi, standing on its short end') + lead(v1 - 6, v1 - 6, o + 60, v1 + 20, 'LED strip in each inside corner')
    b += lead(-12, o + 6, -20, o + 30, 'concrete base, 320 square', 'end')
    return svg((-200, -80, o + 560, o + 130), DEFS + b, 'Plan view: four glass blocks in a pinwheel around a 99 millimetre square open middle, on a concrete base')

def section():   # side section through the middle, air rising through it. h = height above the floor.
    W, BH, FT, ox = 320, 50, 15, 12
    gy = FT + BH + 3; top = gy + B + 6; Y = lambda h: top - h        # svg y runs down
    def box(x, h0, w, hh, c): return R(x, Y(h0 + hh), w, hh, c)
    hx = (W - 88) / 2; b = ''
    for x in (20, W - 40): b += box(x, 0, 20, FT, 'felt')
    b += box(0, FT, hx, BH, 'conc') + box(hx + 88, FT, W - hx - 88, BH, 'conc')
    b += box(ox, FT + BH, TH, 3, 'felt') + box(ox + B + J, FT + BH, TH, 3, 'felt')
    b += box(ox, gy, TH, B, 'gb') + box(ox + B + J, gy, TH, B, 'gb') + box(ox, gy + B, OUTER, 6, 'frame')
    b += box(ox + TH, FT + BH, VOID, 2, 'plate') + box(W / 2 - 15, FT + BH + 2, 30, 95, 'pc') + T(W / 2, Y(FT + BH + 50), 'Pi', 'middle', 's')
    b += box(ox + TH + 3, gy + 10, 4, B - 20, 'led') + box(ox + B + J - 7, gy + 10, 4, B - 20, 'led')
    for sgn in (-1, 1):
        x0, x1 = W / 2 + sgn * 75, W / 2 + sgn * 25
        b += P(f'M{x0},{Y(7)} C{(x0 + x1) / 2},{Y(7)} {x1},{Y(10)} {x1},{Y(30)} L{x1},{Y(top + 25)}', 'airf')
    b += dv(-14, Y(FT + BH), Y(FT), '50', -1) + dv(-14, Y(gy + B), Y(gy), f'{B}', -1) + dv(W + 16, Y(top), Y(0), f'about {top}', 1)
    b += lead(W / 2 + 25, Y(top + 18), W / 2 + 70, Y(top + 32), 'warm air out of the open top')
    b += lead(W / 2 - 75, Y(7), -40, Y(-12), 'cool air in under the base', 'end')
    b += lead(hx + 4, Y(FT + 25), -40, Y(FT + 40), '88 square hole through the base', 'end')
    b += lead(ox + TH + 8, Y(FT + BH + 1), -40, Y(FT + BH + 30), 'perforated aluminium plate', 'end')
    b += lead(ox + 40, Y(FT + BH + 1.5), -40, Y(FT + BH + 70), '3 mm wool felt under each block', 'end')
    b += lead(ox + 30, Y(top - 3), -40, Y(top - 20), 'top frame, 100 square opening', 'end')
    b += lead(W - 30, Y(FT / 2), W + 50, Y(-14), '15 mm felt feet')
    return svg((-300, -60, W + 560, top + 110), DEFS + b, 'Section through the middle: felt feet, concrete base with a square hole, two glass blocks on felt, the Pi standing on a perforated plate, LED strips, top frame, and air rising through')

def a(url, t): return f'<a href="{html.escape(url)}">{t}</a>'
def G(q): return 'https://www.google.com/search?q=' + q.replace(' ', '+')
def table(rows):
    out = ''
    for p, s, q, c, w, u, ok in rows:
        where = (('<span class=ok>✓</span> ' if ok else '') + a(u, html.escape(w))) if u else html.escape(w)
        out += f'<tr><td>{html.escape(p)}</td><td>{s}</td><td class="n">{html.escape(q)}</td><td>{where}</td><td class="n">{html.escape(c)}</td></tr>'
    return ('<div class="tbl"><table class="parts"><thead><tr><th>Part</th><th>What to get</th><th>Qty</th><th>Where</th><th>Rough cost</th></tr></thead><tbody>'
            + out + '</tbody></table></div>')
HD = 'https://www.homedepot.com/p/'
PARTS = [
 ('Glass blocks', 'Seves Nubio 8 × 8 × 4 in, wave pattern, End blocks (one finished end each). Actual 7.75 × 7.75 × 3.88 in (197 × 197 × 98 mm).', '4', '$20 each', 'Home Depot: End block', HD + 'Seves-Nubio-4-in-Thick-Series-8-x-8-x-4-in-End-Wave-Pattern-Glass-Block-Actual-7-75-x-7-75-x-3-88-in-LRWEB8X8/300493429', True),
 ('…or cheaper', 'Standard 8 × 8 × 4 in wave blocks, $6.99. Their corner ends are rough (made for mortar): cover them, or like them raw. Also in blue.', '4', '$7 each', 'Home Depot: standard block', HD + 'Seves-Nubio-7-75-in-x-7-75-in-x-3-875-in-Wave-Pattern-Glass-Block-LRWN8X8/300388744', True),
 ('Computer', 'Raspberry Pi 5, 4 GB, with its official 27 W USB-C supply and a 32 GB microSD card.', '1', '$85–110', 'Raspberry Pi', 'https://www.raspberrypi.com/products/raspberry-pi-5/', False),
 ('Passive case', 'An aluminium case that is the heatsink: no fan. Stood on its short end it must fit inside 90 × 90 mm.', '1', '$15–30', 'search', G('Raspberry Pi 5 passive aluminium case fanless'), False),
 ('Storage', 'A small USB SSD for the library (1–2 TB), or none if the films already live on another computer in the house.', '1', '$0–150', 'search', G('portable USB SSD 2TB'), False),
 ('Cables', 'Micro-HDMI to HDMI (the Pi 5 has micro-HDMI), right-angle if you can; optional Ethernet.', '', '$10–20', 'search', G('micro HDMI to HDMI cable right angle 4K'), False),
 ('Light controller', 'A small ESP32 board made for WLED (free light software): colour, brightness and scenes from a phone.', '1', '$15–25', 'WLED', 'https://kno.wled.ge/', False),
 ('LED strip', '5 V RGBW addressable strip (SK6812), about 0.8 m: four 18 cm pieces, one in each inside corner. A 5 V 3 A supply.', '1', '$20–35', 'search', G('SK6812 RGBW 5V LED strip 60 per meter'), False),
 ('Concrete', 'About 12 kg made up, for a 320 × 320 × 50 mm base: GFRC mix as in the full Lantern, or a bagged countertop mix. Matte penetrating sealer.', '', '$40–80', 'search', G('concrete countertop mix bag'), False),
 ('Mold', 'Melamine board offcut, XPS foam for the square hole and the cable channel, silicone caulk, release agent.', '', '$20–35', 'hardware store', '', False),
 ('Felt and glue', '3 mm wool felt (under each block), four 15 mm felt feet, clear 100% silicone for the block joints.', '', '$20–30', 'hardware or craft store', '', False),
 ('Top frame and plate', 'Top frame: 6 mm walnut ply or 3 mm brass, 300 square with a 100 square opening. Pi plate: 2 mm perforated aluminium, 96 × 96.', '', '$20–50', 'laser shop or hardware store', '', False),
 ('Peak-hold label', 'Irreversible temperature label, 40–60 °C: records the hottest it ever got inside.', '1', '$15', 'search', G('irreversible temperature label 40-60 C'), False),
]

body = f'''
<span class="eyebrow">The Lantern · glass block version</span>
<h1>The Lantern, Glass Block Version</h1>
<p class="lede">An object for the home first, a media player second. Four glass blocks stand on a concrete base around an open middle; inside, a silent Raspberry Pi plays films to the TV, and light glows out through the rippled glass. Real glass, concrete and felt: nothing to peel, bubble or warp, and every part from a hardware store or a maker's shop.</p>
<div class="facts"><div><b>30 × 30 cm</b><span>about 27 cm tall</span></div><div><b>About $300–650</b><span>depending on blocks and storage</span></div><div><b>Silent</b><span>nothing in it moves</span></div><div><b>One weekend</b><span>plus a week for the concrete</span></div></div>

<h2>What it keeps, and what it changes</h2>
<div class="tbl"><table class="cmp"><thead><tr><th></th><th>The full Lantern</th><th>Glass block version</th></tr></thead><tbody>
<tr><td>Body</td><td>17 cut and printed acrylic panes on rods</td><td>Four glass blocks, bonded at their edges</td></tr>
<tr><td>Colour and texture</td><td>Printed tint, darker toward the centre</td><td>The wave pattern in the glass, and the light's own colour</td></tr>
<tr><td>Base</td><td>Cast concrete with a sealed drive vault</td><td>A plain cast concrete slab with a square hole for air and cables</td></tr>
<tr><td>Computer</td><td>MINIX fanless mini PC</td><td>Raspberry Pi 5 in a fanless case</td></tr>
<tr><td>Storage</td><td>Two 8 TB hard drives, mirrored</td><td>A small USB SSD, or the library kept elsewhere</td></tr>
<tr><td>Silence</td><td>Fanless computer; drives quieted in the vault</td><td>Nothing moves: no fan, no drives</td></tr>
<tr><td>Size</td><td>About 21 × 20 cm, 40 cm tall</td><td>About 30 × 30 cm, 27 cm tall</td></tr>
<tr><td>Rough cost</td><td>About $2,000 and up</td><td>About $300–650</td></tr>
</tbody></table></div>
<p><b>Principle it applies: dignity in design.</b> A computer treated as furniture: silent, made of honest materials, and easy to repair. The Pi lifts straight out through the top.</p>

<h2 class="pg">How it works</h2>
<figure class="dg big">{plan()}<figcaption>From above, to scale. Each block's end butts against the face of the next, a pinwheel, so the four leave a square open middle: the block's face minus its thickness, about {VOID} mm.</figcaption></figure>
<figure class="dg big">{section()}<figcaption>Through the middle, to scale. The tower is a chimney: cool air comes in under the base, through the hole, past the Pi, and out of the open top. The hollow blocks hold heat in, so the air path does the cooling.</figcaption></figure>
<ul>
<li><b>Light:</b> glass blocks are sealed and hollow, so the light can't go inside them. Four short LED strips stand in the inside corners and shine out through all four blocks, rippled by the wave pattern. Colour is chosen for the room, not to report anything.</li>
<li><b>Felt:</b> under each block it cushions glass on stone and keeps the joints even; the felt feet lift the base so air can get under it, and stop it scratching furniture.</li>
<li><b>Concrete:</b> weight that keeps a heavy glass tower steady, a hole for air and cables, and the stone that frames the glass.</li>
</ul>

<h2>Try the look first</h2>
<p>Before casting anything: stand the four blocks in the pinwheel on a table at night, put an LED strip or a phone's torch in the middle, and look. That's about $30–80, and the blocks go straight into the build if you like it.</p>

<h2>What you need</h2>
{table(PARTS)}
<p>A <span class="ok">✓</span> means the link was checked. Everything else is a search, because the right listing changes from week to week. Prices are from November 2026.</p>

<h2 class="pg">Make it</h2>
<ol class="steps">
<li><b>Make the mold.</b> A melamine box 320 × 320 mm inside, 50 mm deep. Glue an 88 mm square XPS block in the centre (the hole), and a 30 × 15 mm XPS strip from it to the back edge on the floor of the mold (the cable channel, under the base). Seal the seams with silicone; coat with release agent.</li>
<li><b>Cast the base.</b> Mix and pour, following the mix's instructions; vibrate out the bubbles by tapping the mold. Cover and keep it damp for a week. Unmold, dig out the foam, and seal it.</li>
<li><b>Set up the Pi.</b> Flash LibreELEC for the Raspberry Pi 5 onto the card ({a('https://libreelec.tv/downloads/', 'libreelec.tv')}), put the Pi in its passive case, and connect it to the TV to set up Kodi and the library.</li>
<li><b>Set up the light.</b> Install WLED on the light controller from a browser ({a('https://kno.wled.ge/', 'kno.wled.ge')}). Cut four 18 cm pieces of strip, wire them in a chain, and set WLED's current limit to suit the supply (2.5 A for a 3 A supply).</li>
<li><b>Seat the blocks.</b> Felt feet under the base. A strip of 3 mm felt where each block will stand. Stand the blocks in the pinwheel, End blocks with their finished ends at the corners. Check the middle is square, then run clear silicone down each vertical joint, inside and out. Leave a day.</li>
<li><b>Fit the inside.</b> Stick the LED strips in the four inside corners, facing out. Lay the perforated plate over the hole, stand the Pi on its short end on the plate, and run every cable down through the hole and out along the channel. The power supplies stay outside, so their heat does too.</li>
<li><b>Top frame.</b> Bed it on dabs of clear silicone across the block tops. The 100 mm opening stays open: that's where warm air leaves and where the Pi comes out for repair.</li>
</ol>

<h2 class="pg">Tests</h2>
<div class="tbl"><table><thead><tr><th>Test</th><th>How</th><th>Pass</th></tr></thead><tbody>
<tr><td>Heat</td><td>Stick the peak-hold label on the Pi's plate. Play a 2-hour 4K film with the light on. Check the Pi's temperature in LibreELEC's system information near the end.</td><td>The label stays below about 55 °C; the Pi stays below about 70 °C and never slows down.</td></tr>
<tr><td>Silence</td><td>In a quiet room, ear close to the open top, during a film.</td><td>Nothing to hear.</td></tr>
<tr><td>Steady</td><td>Push gently on the top frame from each side.</td><td>No rocking; the tower and base move as one.</td></tr>
<tr><td>Repair</td><td>Lift the Pi out through the top.</td><td>It comes out without taking anything apart.</td></tr>
</tbody></table></div>

<h2>Honest limits</h2>
<ul>
<li><b>Not built yet.</b> The heat figures are estimates; the test above is how to find out.</li>
<li><b>Video:</b> the Pi 5 plays 4K HEVC smoothly in hardware, but has no hardware decoding for AV1: 4K AV1 films stutter. Most libraries are HEVC; if yours is AV1, use the full Lantern's computer.</li>
<li><b>Heavy glass:</b> the tower is heavy and the blocks are brittle. Put it on something solid, away from where children climb.</li>
<li><b>Rough ends:</b> standard blocks have rough mortar ends; End blocks hide one per block, the top frame hides the top edges.</li>
</ul>
'''
page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>The Lantern, Glass Block Version</title><style>{CSS}</style></head><body><main class="wrap">{body}</main></body></html>')
open(OUT, 'w').write(page)
print(len(page))
