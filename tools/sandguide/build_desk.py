import sys, os, re, html
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
from sand_data import PARTS
import sand_diagrams as D
src = open(SP + 'guide/build_guide.py').read()
CSS = re.search(r"CSS=r'''(.*?)'''", src, re.S).group(1) + '''
svg .sand{fill:var(--dim)}
table.rec td{height:2.1em}table.rec td:first-child{white-space:nowrap}
.decide{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.4fr);gap:0;border:1px solid var(--line);border-radius:6px;overflow:hidden;background:var(--card)}
.decide div{padding:9px 12px;border-top:1px solid var(--line)}.decide div:nth-child(-n+2){border-top:0}.decide div:nth-child(odd){color:var(--dim);font-size:.9rem}
'''
def a(url, t): return f'<a href="{html.escape(url)}">{t}</a>'
desk = PARTS[0][1]
rows = ''.join(f'<tr><td>{html.escape(p)}</td><td>{html.escape(s)}</td><td class="n">{html.escape(q)}</td><td>{("<span class=ok>✓</span> " if v else "") + a(u, html.escape(w)) if u else html.escape(w)}</td><td class="n">{html.escape(c)}</td></tr>' for (p, s, q, c, w, u, v) in desk)
def rec(cols, n): return '<div class="tbl"><table class="rec"><thead><tr>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr></thead><tbody>' + ('<tr>' + '<td></td>' * len(cols) + '</tr>') * n + '</tbody></table></div>'
def recl(cols, labels): return '<div class="tbl"><table class="rec"><thead><tr>' + ''.join(f'<th>{c}</th>' for c in cols) + '</tr></thead><tbody>' + ''.join('<tr><td>' + l + '</td>' + '<td></td>' * (len(cols) - 1) + '</tr>' for l in labels) + '</tbody></table></div>'

body = f'''
<span class="eyebrow">The Sand Table · before anything is built</span>
<h1>Sand Table Desk Test</h1>
<p class="lede">One afternoon at a kitchen table, about $150–300 in parts. It answers the questions the whole design rests on, before any concrete, walnut or brass is ordered.</p>
<div class="facts"><div><b>3–4 hours</b><span>plus shopping</span></div><div><b>$150–300</b><span>less if you borrow a driver</span></div><div><b>2 plates</b><span>30 and 40 cm</span></div><div><b>5 answers</b><span>to bring back</span></div></div>

<h2>What it decides</h2>
<div class="decide">
<div>Plate size</div><div>30 or 40 cm (or between). Bigger plates have more figures, crowded closer together, and are harder to drive cleanly.</div>
<div>Driver</div><div>Which driver makes clean figures on brass at a sensible volume, and whether it fits under the plate (35 mm in the tray).</div>
<div>Frequencies and loudness</div><div>Which notes make clean figures, and how loud each is at 1 m. Sets the volume ceiling.</div>
<div>The blur</div><div>Whether adding noise to the drive visibly smears the figure from across a room. This is the core idea.</div>
<div>Sand loss</div><div>How much sand leaves the plate per verdict, so the tray's catch dish can be sized and top-ups planned.</div>
</div>

<h2>What you need</h2>
<div class="tbl"><table><thead><tr><th>Part</th><th>What to get</th><th>Qty</th><th>Where</th><th>Rough cost</th></tr></thead><tbody>{rows}
<tr><td>Laptop</td><td>With Audacity (free, works offline) to make the test tones, and a 3.5 mm to RCA cable to the amplifier.</td><td class="n">1</td><td>{a('https://www.audacityteam.org/download/', 'Audacity')}</td><td class="n">$0–10</td></tr>
<tr><td>Camera</td><td>A phone on a stand or a stack of books, pointing straight down at the plate.</td><td class="n">1</td><td></td><td class="n">$0</td></tr></tbody></table></div>
<p>A <span class="ok">✓</span> means the link was checked and points at the item or its maker's page. A physics department or a school science teacher may lend you a wave driver.</p>
<div class="warn"><b>Glass microbeads only.</b> Don't use fine silica sand, even for the test: some carries dust that's harmful to breathe. The beads are too coarse to breathe in, but keep the bag closed and out of reach of small children, and work over the baking sheet.</div>
<div class="warn"><b>Ears.</b> Brass plates can be piercing at high notes. Wear ear protection while sweeping, start with the amplifier turned all the way down, and take it off only for the loudness readings.</div>

<h2>Make the test sounds</h2>
<p>All in Audacity, before you start. Export each as a WAV file.</p>
<ol class="steps">
<li><b>Sweep:</b> Generate → Chirp. Sine, start 80 Hz, end 1,200 Hz, amplitude 0.8 both ends, interpolation <i>logarithmic</i>, duration 600 s (10 minutes). Save as <code>sweep.wav</code>.</li>
<li><b>Holding tones:</b> you'll make these during the test, once you know the good frequencies: Generate → Tone, sine, that frequency, amplitude 0.8, 10 s.</li>
<li><b>Noisy tones:</b> for your favourite frequency, make the tone on one track and pink noise (Generate → Noise, pink) on a second track, then set the noise track's gain so its amplitude is about 0.08, 0.24 and 0.48 (10%, 30% and 60% of the tone). Export each mix: <code>noise-10.wav</code>, <code>noise-30.wav</code>, <code>noise-60.wav</code>. This is close to what the controller does when the agent was unsettled.</li>
</ol>

<h2>Set up</h2>
<figure class="dg">{D.desk()}<figcaption>Side view. The plate is held only at its centre; its edges are free.</figcaption></figure>
<ol class="steps">
<li><b>Mount the 30 cm plate</b> on the driver through its centre hole, using the driver's own attachment (or an M6 bolt with a rubber washer under the plate and a nylon washer over it). The plate should sit level, edges free, over the baking sheet.</li>
<li><b>Connect:</b> laptop headphone out → amplifier input; amplifier speaker output → driver. Amplifier volume all the way down. Laptop volume about 75%.</li>
<li><b>Weigh</b> about 20 g of beads and write it down. Sprinkle them evenly through a tea strainer, just enough to grey the brass.</li>
<li><b>Camera</b> straight above the plate. Note the room's background level on the sound meter.</li>
</ol>

<h2>The tests</h2>
<h3>1 · Find the figures</h3>
<p>Play <code>sweep.wav</code>. Raise the amplifier slowly until the beads begin to dance. Each time a clean figure forms, pause, note the time in the sweep (it maps to a frequency; Audacity shows it if you click the same point in the sweep), take a photo, and resume. Expect 5–15 figures.</p>
{rec(['Plate', 'Frequency (Hz)', 'Photo #', 'Clean? (1–5)', 'Notes on the shape'], 10)}

<h3>2 · Loudness at each good figure</h3>
<p>For each figure you rated 4 or 5: play its holding tone, set the amplifier just high enough that the figure forms in about 3 seconds, and note the amplifier setting. Take your ear protection off, and read the level at 1 m.</p>
{rec(['Plate', 'Frequency (Hz)', 'Amp setting', 'Forms in (s)', 'dB at 1 m', 'Livable?'], 8)}
<div class="tip">Lower notes are usually quieter and kinder. A figure you'd happily hear several times a day is worth more than a beautiful one that makes you wince.</div>

<h3>3 · The blur</h3>
<p>On your favourite figure: let it form crisp with the plain tone, photograph it, then play each noisy version from a freshly scattered plate (tap the plate's edge to scatter, or play the 60% noise for a few seconds first). Photograph each. Then stand across the room.</p>
{recl(['Drive', 'Photo #', 'Readable from across the room?', 'How it sounds'], ['Plain tone', '10% noise', '30% noise', '60% noise'])}
<div class="check"><b>What you're looking for:</b> a clear, continuous change from crisp to smeared that someone who knows nothing about it can see from 3 m. If 10% already looks smeared, the controller can use a gentler scale. If 60% still looks crisp, the noise needs to be stronger (or the drive should also wander off the note).</div>

<h3>4 · Sand loss</h3>
<p>Weigh the plate's sand (brush it onto paper and weigh it, then sprinkle it back). Play a 3-second holding tone 20 times, letting it settle between each. Weigh again.</p>
{recl(['Plate', 'Start (g)', 'After 20 (g)', 'Lost per verdict (g)'], ['30 cm', '40 cm'])}

<h3>5 · Repeat on the 40 cm plate</h3>
<p>Tests 1–4 again. If you have a second driver to compare, run test 1 and 2 with it on the plate you prefer.</p>
{recl(['Driver', 'Height (mm)', 'Cleanest figure (Hz)', 'dB at 1 m', 'Notes'], ['Driver 1', 'Driver 2'])}

<h3>6 · Two quick extras</h3>
<ul>
<li><b>The ring-down:</b> stop the tone abruptly and listen. The brass should keep ringing for a moment, like a bell. Note how long.</li>
<li><b>The cover:</b> rest a sheet of glass (or a picture-frame glass) on four felt pads about 10 mm above the plate's edges and play a verdict. Does it buzz? If so, felt and weight fix it in the real tray.</li>
</ul>

<h2>Bring back</h2>
<div class="decide">
<div>Plate size</div><div>&nbsp;</div>
<div>Driver (and its height)</div><div>&nbsp;</div>
<div>Good frequencies</div><div>&nbsp;</div>
<div>Amp setting for a 3 s figure</div><div>&nbsp;</div>
<div>Loudest acceptable dB at 1 m</div><div>&nbsp;</div>
<div>Noise level that reads as "unsettled"</div><div>&nbsp;</div>
<div>Sand lost per verdict</div><div>&nbsp;</div>
</div>
<h3>Then</h3>
<ol>
<li>Set the plate size in <b>the-sand-table-model.html</b> and press <b>Cut files</b>.</li>
<li>Copy the amplifier setting into the build notes, and set the firmware's <code>MAX_DRIVE</code> low to start (0.3); raise it to match.</li>
<li>Keep the photos: they're the first honest pictures of the object, and the best thing to show reviewers.</li>
<li>Pour the beads back into their bag through a funnel. Wipe the plate with a dry cloth.</li>
</ol>
'''
page = f'''<title>Sand Table Desk Test</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>{CSS}</style>
<main class="wrap">{body}</main>'''
open(SP + 'sand-desk-test.html', 'w').write(page)
full = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">{page}</head><body></body></html>'
full = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Sand Table Desk Test</title><style>{CSS}</style></head><body><main class="wrap">{body}</main></body></html>'
open(SP + '../builds/the-sand-table/the-sand-table-desk-test.html', 'w').write(full)
print(len(page))
