# Writes the Sand Table's small-versions document (Tier 1: kitchen table, Tier 2: honest version)
# straight into builds/the-sand-table/. Print it with: node ../make-pdf.js <html> <pdf>
import sys, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SP = os.path.dirname(HERE) + '/'
OUT = os.path.join(SP, '..', 'builds', 'the-sand-table', 'the-sand-table-small-versions.html')
from sand_data import PARTS, G
src = open(SP + 'guide/build_guide.py').read()
CSS = re.search(r"CSS=r'''(.*?)'''", src, re.S).group(1) + '''
.decide{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:0;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:var(--card)}
.decide div{padding:9px 12px;border-top:1px solid var(--line)}.decide div:nth-child(-n+2){border-top:0}.decide div:nth-child(odd){color:var(--dim);font-size:.9rem}
.placard{border:2px solid var(--ink);border-radius:4px;padding:18px 22px;margin:14px 0;break-inside:avoid;font-family:Georgia,serif;max-width:34em}
.placard h4{margin:12px 0 2px;font-size:1.02rem}.placard h4:first-child{margin-top:0}.placard p{margin:0}
.placard .tier{font-family:inherit;font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:var(--dim)}
table.cmp td:first-child{color:var(--dim);white-space:nowrap}
h2{break-before:auto;margin-top:28px}h2.pg{break-before:page;margin-top:0}
ol.steps{counter-reset:st}
'''
def a(url, t): return f'<a href="{html.escape(url)}">{t}</a>'
def known(part):       # a row from the full build's parts list, with its checked link
    for _, items in PARTS:
        for row in items:
            if row[0] == part: return row
    raise KeyError(part)
def table(rows):
    out = ''
    for p, s, q, c, w, u, ok in rows:
        where = (('<span class=ok>✓</span> ' if ok else '') + a(u, html.escape(w))) if u else html.escape(w)
        out += f'<tr><td>{html.escape(p)}</td><td>{s}</td><td class="n">{html.escape(q)}</td><td>{where}</td><td class="n">{html.escape(c)}</td></tr>'
    return ('<div class="tbl"><table><thead><tr><th>Part</th><th>What to get</th><th>Qty</th><th>Where</th><th>Rough cost</th></tr></thead><tbody>'
            + out + '</tbody></table></div>')

beads, amp, pi, pico, dac, wire = (known(p) for p in ('Glass microbeads', 'Amplifier', 'Agent box', 'Controller', 'DAC', 'One-way wire'))
TIER1 = [
 ('Brass plate', 'C260 brass, 1 mm, a 30 cm square with a 6.5 mm centre hole, edges deburred.', '1', '$25–50', 'search', G('C260 brass sheet 1mm cut to size'), False),
 ('Driver, option A', 'A 6.5" woofer with a rod from the centre of its cone to the plate\'s centre hole: the method most home-made Chladni plates use.', '1', '$20–40', 'Instructables: Easy Chladni Plate', 'https://www.instructables.com/Easy-Chladni-Plate', True),
 ('Driver, option B', 'A small bass shaker (Dayton Audio TT25-8). Cheap, but rated for 20–80 Hz, below where most figures form: the desk test decides.', '1', '$25–30', 'Dayton Audio', 'https://www.daytonaudio.com/product/1104/tt25-8-puck-tactile-transducer-mini-bass-shaker', True),
 (amp[0], html.escape(amp[1]), amp[2], amp[3], amp[4], amp[5], amp[6]),
 ('USB sound adapter', 'Any small USB audio adapter with a headphone out. Used for the plate and nothing else.', '1', '$8–15', 'search', G('USB audio adapter headphone out'), False),
 ('Cable', '3.5 mm to RCA, from the adapter to the amplifier.', '1', '$5–10', 'search', G('3.5mm to RCA cable'), False),
 (beads[0], html.escape(beads[1]), '500 g', beads[3], beads[4], beads[5], beads[6]),
 ('Tray', 'A deep picture frame with its glass (a box frame), or a shallow wooden frame on a board, to catch the beads and keep dust off.', '1', '$10–30', 'craft or hardware store', '', False),
 ('Odds', 'M6 bolt with rubber and nylon washers, ear protection, a phone sound-meter app.', '', '$10–20', 'hardware store', '', False),
]
TIER2 = [
 (pi[0], 'Raspberry Pi 5 (4 GB is enough), its 27 W USB-C supply, a 32 GB microSD card.', '1', '$85–120', pi[4], pi[5], pi[6]),
 ('Network', 'A USB Ethernet adapter for your computer (most laptops have no Ethernet port) and a short Ethernet cable.', '1', '$15–30', 'search', G('USB C gigabit ethernet adapter'), False),
 (pico[0], html.escape(pico[1]), '1', pico[3], pico[4], pico[5], pico[6]),
 (dac[0], html.escape(dac[1]), '1', dac[3], dac[4], dac[5], dac[6]),
 (wire[0], html.escape(wire[1]), '1', wire[3], wire[4], wire[5], wire[6]),
 ('Counters', 'Two electromechanical counters, non-resettable, 24 V DC, 5 or 6 digits. One counts tasks, one counts unsettled tasks.', '2', '$10–25 each', 'search', G('electromagnetic counter 24V DC non-resettable 5 digit'), False),
 ('Board parts', 'Two logic-level MOSFETs (IRLZ44N or similar), two 1N4007 diodes, a 24 to 5 V buck module, perfboard, screw terminals.', '', '$10–20', 'search', G('IRLZ44N MOSFET 1N4007 diode kit'), False),
]

body = f'''
<span class="eyebrow">The Sand Table · smaller versions</span>
<h1>The Sand Table, Small Versions</h1>
<p class="lede">The desk test already holds the core of the object: a brass plate, a driver, an amplifier and beads, plus a computer that turns a number into a settled or smeared figure. Everything else in the full build exists to make it beautiful, permanent and hard to tamper with. These versions keep the core and say plainly what they give up.</p>
<div class="facts"><div><b>Tier 1</b><span>kitchen table, about $120–220</span></div><div><b>Tier 2</b><span>honest version, about $300–500</span></div><div><b>One afternoon</b><span>for Tier 1, in a workshop</span></div><div><b>Plus</b><span>a computer you already own</span></div></div>

<h2>What every version keeps</h2>
<ul>
<li><b>The figure:</b> crisp means settled, smeared means unsettled. The sound and the figure are the same vibration.</li>
<li><b>Measured, not reported:</b> the number comes from the model's own word probabilities, never from the agent describing itself.</li>
<li><b>The worst moment counts:</b> one torn step in a task can't hide inside a confident answer.</li>
<li><b>Settled isn't right:</b> the figure shows how the model behaved, not whether its work was correct. The log has a column to mark that.</li>
</ul>

<h2 class="pg">The three versions side by side</h2>
<div class="tbl"><table class="cmp"><thead><tr><th></th><th>Tier 1 · Kitchen table</th><th>Tier 2 · Honest version</th><th>Full build</th></tr></thead><tbody>
<tr><td>Parts</td><td>About $120–220</td><td>About $300–500</td><td>Several thousand, with the Mac</td></tr>
<tr><td>Computers</td><td>One you own runs everything</td><td>One you own for the model and meter; a Raspberry Pi for the agent</td><td>A Mac that does nothing else, and a Pi</td></tr>
<tr><td>Plays the plate</td><td>The computer, through a USB sound adapter</td><td>A Pico controller, down a one-way wire</td><td>The same controller</td></tr>
<tr><td>Agent can't reach the meter</td><td>A software promise</td><td>Physical: one cable, one port</td><td>Physical, on a dedicated machine</td></tr>
<tr><td>Loudness ceiling</td><td>Amplifier knob and a setting on the computer</td><td>Amplifier knob and the controller's firmware</td><td>The same</td></tr>
<tr><td>Long record</td><td>The log</td><td>The log and two counters</td><td>The same, in brass and walnut</td></tr>
<tr><td>Agent online or acting</td><td>However you set it up</td><td>Never: the Pi has no internet</td><td>Only by the key</td></tr>
<tr><td>Who it's for</td><td>Classrooms, workshops, conference booths</td><td>Makers, labs, a longer installation</td><td>A home, a gallery</td></tr>
</tbody></table></div>

<h2>Start with the desk test</h2>
<p>Both versions begin with the desk test (<b>the-sand-table-desk-test.pdf</b>): the same plate, amplifier and beads. It answers the question these versions depend on most: does your driver make clean figures, and does added noise visibly smear them? If you're choosing between the two cheap drivers below, test both.</p>

<h2 class="pg">Tier 1 · The kitchen table</h2>
<p>One computer runs the model, the meter and the agent. There's no controller: the meter plays each verdict to the plate itself, with the same sound the controller makes. Setup steps: <code>software/KITCHEN-TABLE-SETUP.txt</code>.</p>
{table(TIER1)}
<p>A <span class="ok">✓</span> means the link was checked. Everything else is a search, because the right listing changes from week to week.</p>
<ol class="steps">
<li><b>Set up the plate</b> as in the desk test, in its tray. Run the USB sound adapter into the amplifier, with the amplifier turned all the way down.</li>
<li><b>Install a model you run yourself</b> with llama.cpp. A small one that supports tool calls is enough. Most hosted AI services don't share word probabilities, so the table can't read them.</li>
<li><b>Choose your figure</b> with <code>python3 plate.py sweep</code>, or save the note your desk test found. Set the amplifier so a test verdict forms the figure in about 3 seconds.</li>
<li><b>Start the meter</b> in audio mode and point the agent at it, never at the model directly.</li>
<li><b>Give the agent a task.</b> When it finishes, the plate plays the verdict.</li>
</ol>
<div class="warn"><b>What Tier 1 gives up: isolation.</b> The agent, the model and the meter share one computer, so "the agent can't reach the meter" is a software promise, not a physical one. Anything on that computer could read the meter's numbers, call the model directly, or play sounds of its own. There are no counters, and the loudness ceiling is a setting on the computer plus the amplifier's knob. That's fine for a demo, as long as the placard says so.</div>

<h2 class="pg">Tier 2 · The honest version</h2>
<p>Everything in Tier 1, plus the parts that make the honesty claim physical: the agent lives on a Raspberry Pi whose only way to the meter is one cable, and the plate is played by a controller that listens down a one-way wire and can't talk back. Setup steps: <code>software/HONEST-VERSION-SETUP.txt</code>.</p>
{table(TIER2)}
<ol class="steps">
<li><b>Give the meter its own account</b> on your computer (macOS or Linux), owning the model and the meter. Your computer keeps its Wi-Fi and its everyday use.</li>
<li><b>Run one cable</b> from your computer to the Pi, and switch on the firewall that locks down only that cable: the agent can reach the meter's one port, and nothing else, in either direction.</li>
<li><b>Set up the Pi</b> with its Wi-Fi and Bluetooth off and the agent in an account without admin rights. It has no internet.</li>
<li><b>Build the controller</b> with the full build's firmware: the Pico, the sound board, two counters and the one-way wire. The light and telltale pins stay unconnected.</li>
<li><b>Check the separation</b> from the Pi: the meter answers; the model, SSH and the internet don't.</li>
</ol>
<div class="warn"><b>What Tier 2 gives up.</b> The meter shares a computer with your everyday life, so that computer's security is only as good as its settings. There's no key: the agent never goes online or acts in the world. No lights and no case. The isolation itself is real: the agent's only path is one cable, and the table can't talk back.</div>

<h2>Running it as a workshop</h2>
<ul>
<li><b>Do the desk test once beforehand,</b> with the exact plate and driver everyone will use, and write down the notes that make clean figures. Then nobody has to sweep: each table saves a known note with <code>plate.py save</code>.</li>
<li><b>Prepare the software in advance:</b> llama.cpp, a small model, and the software folder on each laptop. Downloads are the slowest part of the afternoon.</li>
<li><b>A rough afternoon:</b> 30 minutes for the plate and tray, 30 for the software, 15 to save the note and set the loudness, then the rest giving the agent easy and impossible tasks and watching the difference.</li>
<li><b>Safety:</b> glass microbeads only, never silica sand. Keep the bags closed and away from small children. Ear protection while setting the loudness. Start every amplifier turned all the way down.</li>
</ul>

<h2 class="pg">Placards</h2>
<p>Print the one for your version and put it beside the plate. Saying plainly what the object can't do is part of the object.</p>
<div class="placard"><span class="tier">Tier 1 · Kitchen table</span>
<h4>What you're seeing</h4><p>How settled an AI agent was at its shakiest moment in its last task. A crisp figure: settled. A smeared figure: unsettled.</p>
<h4>What it can't tell you</h4><p>Whether the work was right. Settled is not the same as correct.</p>
<h4>What this version gives up</h4><p>The agent, the model and the meter share one computer. That the agent can't reach the meter is a software promise here, not a physical one.</p></div>
<div class="placard"><span class="tier">Tier 2 · Honest version</span>
<h4>What you're seeing</h4><p>How settled an AI agent was at its shakiest moment in its last task. A crisp figure: settled. A smeared figure: unsettled.</p>
<h4>What it can't tell you</h4><p>Whether the work was right. Settled is not the same as correct.</p>
<h4>Why it can't be faked</h4><p>The agent runs on its own small computer and reaches the model only through the meter, over one cable. The table hears the result down a one-way wire and can't talk back.</p></div>
'''
page = (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<title>The Sand Table, Small Versions</title><style>{CSS}</style></head><body><main class="wrap">{body}</main></body></html>')
open(OUT, 'w').write(page)
print(len(page))
