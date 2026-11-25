import sys, os, re, base64, io, html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
SP = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
from sand_data import PARTS
import sand_diagrams as D
from PIL import Image

src = open(SP + 'guide/build_guide.py').read()
CSS = re.search(r"CSS=r'''(.*?)'''", src, re.S).group(1) + "\nsvg .sand{fill:var(--dim)}\nfigure.big svg{max-height:620px}figure.big svg .s{font-size:17px}figure.big svg .d{font-size:16px}figure.big svg .m{font-size:19px}\n"

def img(path, w=900, crop=None):
    im = Image.open(path).convert('RGB')
    if crop: im = im.crop(crop)
    im.thumbnail((w, w * 2)); b = io.BytesIO(); im.save(b, 'JPEG', quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def fig(svg, cap, cls=''): return f'<figure class="dg {cls}">{svg}<figcaption>{cap}</figcaption></figure>'
def a(url, t): return f'<a href="{html.escape(url)}">{t}</a>'
I = {'q': img(SP + 'shots/s-q.png', 900, (150, 60, 1050, 800)), 'set': img(SP + 'shots/s-top-settled.png', 520, (250, 40, 950, 780)),
     'unset': img(SP + 'shots/s-top-unsettled.png', 520, (250, 40, 950, 780)), 'xray': img(SP + 'shots/s-xray.png', 900, (100, 80, 1100, 820))}

rows = []
for grp, items in PARTS:
    rows.append(f'<tr class="g"><td colspan="5">{html.escape(grp)}</td></tr>')
    for (part, spec, qty, cost, srcn, url, v) in items:
        mark = '<span class="ok" title="link checked">✓</span> ' if v else ''
        link = (mark + a(url, html.escape(srcn))) if url else html.escape(srcn)
        rows.append(f'<tr><td>{html.escape(part)}</td><td>{html.escape(spec)}</td><td class="n">{html.escape(qty)}</td><td>{link}</td><td class="n">{html.escape(cost)}</td></tr>')
PTABLE = '<div class="tbl"><table><thead><tr><th>Part</th><th>What to ask for</th><th>Qty</th><th>Where</th><th>Rough cost</th></tr></thead><tbody>' + ''.join(rows) + '</tbody></table></div>'

S = []
S.append(f'''
<span class="eyebrow">Build guide · ARKOS · the agent and its honest face</span>
<h1>The Sand Table, step by step</h1>
<p class="lede">A low object of concrete, walnut and brass that shows, in sand, how settled an AI agent was when it finished its last task. A proof of concept, made to start a conversation about readable systems and how to live with them.</p>
<div class="hero"><img src="{I['q']}" alt="The Sand Table, three-quarter view"><img src="{I['xray']}" alt="The body seen through: two compartments, one cable between them"></div>
<div class="two"><figure class="dg"><img src="{I['set']}" alt="A crisp figure" style="width:100%;border-radius:4px"><figcaption>Settled: a crisp figure.</figcaption></figure><figure class="dg"><img src="{I['unset']}" alt="The same figure smeared" style="width:100%;border-radius:4px"><figcaption>Unsettled: the same figure, smeared.</figcaption></figure></div>
<div class="facts"><div><b>600 × 600 × 310</b><span>mm</span></div><div><b>about 35 kg</b><span>body 25, tray and glass 10</span></div><div><b>8–10 weeks</b><span>after a one-afternoon desk test</span></div><div><b>$1,300–3,000</b><span>plus the Mac</span></div></div>
<p>This guide goes with <b>the-sand-table-model.html</b> in the same folder. Set the plate size there from your desk test, then press its two buttons: <b>Cut files</b> (brass plate, glass, vents, divider, hatch, optional placard) and <b>Software</b> (the meter, the controller firmware, and the setup for the Mac and the agent box).</p>
<h3>Contents</h3>
<ol class="toc"><li>What it shows, and what it doesn't</li><li>Before you start</li><li>Parts</li><li>The desk test</li><li>Make the files</li><li>The three machines</li><li>Controller and sound</li><li>The tray</li><li>The body</li><li>Assembly</li><li>Choosing your figure</li><li>Tests</li><li>Living with it</li></ol>
''')

S.append(f'''
<h2>1 · What it shows, and what it doesn't</h2>
<p>When the agent finishes a task, the brass plate rings for a few seconds and the sand jumps into a figure. A crisp figure means the model was <b>settled</b>: at every decision in the task, its probability sat firmly on its choice. A smeared figure means it was <b>unsettled</b> at some point: torn between options, even if its words sounded sure.</p>
<ul>
<li><b>Settled is not the same as right.</b> A model can be confidently wrong. The figure shows how the model behaved, not whether its work was correct. A smeared figure is a good reason to check the work; a crisp one is not proof.</li>
<li><b>The shakiest moment counts.</b> The meter scores every decision (each tool call and the final answer) and the task takes its worst one, so one torn step can't hide inside a confident task.</li>
<li><b>Measured, not reported.</b> The number comes from the model's word probabilities, read by a small program that is arithmetic only. It never asks the agent how it did.</li>
<li><b>The agent can't reach it.</b> The agent runs on its own small computer. It can ask the model questions over one cable; it can't log in to the Mac, change how the model runs, see the meter, or reach the table, which listens on a one-way wire and has no radio.</li>
<li><b>The figure is the household's; clarity is everyone's.</b> At setup the plate shows every figure it can make and the household picks one. Sharp means settled and smeared means unsettled in every home, so a visitor can read any table without knowing which figure was chosen. The choice makes each table personal; it doesn't hide anything.</li>
<li><b>One event.</b> The tone is the brass plate itself ringing, so what you hear and what you see can't disagree.</li>
<li><b>The counters remember.</b> Two counters on the front edge only count up: every task, and every unsettled task. Each verdict replaces the last figure, but nothing replaces the count.</li>
<li><b>Calibration, later, by hand.</b> The meter logs every task with an empty column for a person to mark whether the work was right. After a few months, that log shows what a crisp figure is worth in your house.</li>
</ul>
''')

S.append('''
<h2>2 · Before you start</h2>
<div class="timeline"><div><b>Week 1</b>Desk test. Decide the plate size and driver.</div><div><b>Weeks 2–3</b>Order parts. Set up the Mac and agent box. Write files.</div><div><b>Weeks 3–5</b>Mold and cast the body. Woodworker makes the tray.</div><div><b>Weeks 5–6</b>Controller on the bench. Cure and seal the body.</div><div><b>Weeks 7–8</b>Fit out tray and body. Assemble.</div><div><b>Week 9</b>Choose the figure. Tests.</div></div>
<h3>Tools</h3>
<ul><li>Soldering iron, wire strippers, multimeter, heat-shrink.</li><li>Drill with metal bits; M5 and M6 taps; files.</li><li>A laptop with the Arduino IDE, and a USB cable for the Pico.</li><li>For the body: saw for melamine, clamps, bucket and paddle mixer, scale, level, gloves, eye protection, dust mask.</li><li>Ear protection and a phone sound-meter app for the plate tests.</li></ul>
<div class="warn"><b>Sand:</b> use the round glass microbeads only. Fine silica sand can carry dust that's harmful to breathe; don't use it, even for the test. Keep the bead bag closed and away from small children.</div>
<div class="warn"><b>Mains:</b> the only mains parts are factory-made: the Mac, the power strip, and the enclosed 24 V supply. Don't open them. Everything you wire yourself is 24 V or less.</div>
<div class="warn"><b>Wet concrete is caustic:</b> gloves and eye protection when mixing and casting.</div>
''')

S.append(f'''
<h2>3 · Parts</h2>
<p>Rough prices for November 2026. A <span class="ok">✓</span> means the link was checked for this guide and points at the item or its maker's page. Other links are a search or a home page: choose the exact item from the description. Buy the desk-test group first; much of the rest depends on it.</p>
{PTABLE}
''')

S.append(f'''
<h2>4 · The desk test</h2>
<p>An afternoon that answers the biggest unknowns before anything else is bought or built: which plate size and driver make clean figures, how loud they are, whether the blur reads, and how much sand leaves the plate.</p>
{fig(D.desk(), 'Desk test, side view.')}
<ol class="steps">
<li><b>Set up.</b> Bolt the 30 cm plate to the driver through its centre hole, over the baking sheet. Amplifier gain at minimum. Ear protection on. Sprinkle a thin, even layer of microbeads, just enough to grey the brass.</li>
<li><b>Sweep.</b> Play a slow sine sweep from 80 to 1,200 Hz (Audacity: Generate → Chirp, or any tone-generator app). Raise the gain until the sand starts to move. Every time a clean figure forms, write down the frequency and take a photo from above.</li>
<li><b>Loudness.</b> At each good frequency, set the drive just high enough to form the figure in about 3 seconds and read the level at 1 m. Low notes are usually quieter; note which figures stay under about 60 dB.</li>
<li><b>The blur.</b> On your favourite figure, play the tone with pink noise mixed in at three levels (10, 30, 60%). Photograph each. This is the core idea: can you see the difference from across the room?</li>
<li><b>Sand loss.</b> Weigh the sand on the plate, run 20 three-second verdicts, weigh what's left.</li>
<li><b>Repeat</b> on the 40 cm plate. If you have a second driver to try, try it.</li>
</ol>
<div class="check"><b>Bring back:</b> plate size and driver that gave the cleanest, quietest figures; the list of good frequencies; the amplifier gain setting; photos at each noise level; sand lost per 20 verdicts. Set the plate size in the model before making the cut files, and copy the gain setting into the firmware's MAX_DRIVE (start low).</div>
''')

S.append('''
<h2>5 · Make the files</h2>
<ol class="steps">
<li><b>Open the-sand-table-model.html.</b> It works offline. Try a few readings with the slider and the Settled and Unsettled buttons; watch the counters.</li>
<li><b>Set the plate size</b> from your desk test.</li>
<li><b>Press “Cut files”.</b> <code>sandtable-cut-files.zip</code>: the brass plate, glass cover, two vent panels, the divider, the back hatch plate, an optional placard to engrave, and <code>ORDER-SHEET.txt</code> with material and quantity for each.</li>
<li><b>Press “Software”.</b> <code>sandtable-software.zip</code>: <code>meter.py</code>, the controller firmware, the firewall and start-up files for the Mac, the helper for the agent box, and three setup sheets.</li>
</ol>
''')

S.append(f'''
<h2>6 · The three machines</h2>
{fig(D.system(), 'Not to scale. Three machines, three jobs. Blue: network. Red: the one-way wire.')}
<ol class="steps">
<li><b>Set up the Mac as the measurer.</b> Follow <code>MAC-SETUP.txt</code>: a standard account called <i>meter</i> that owns the model and the meter; no account for the agent; Wi-Fi, Bluetooth and every kind of sharing off; one cable to the agent box with a fixed address; llama.cpp installed with Homebrew; both programs started at boot as the meter's user; the firewall that lets the agent box reach the meter's port and nothing else.</li>
<li><b>Check the model gives word probabilities.</b> The setup sheet has a one-line test. If it fails, update llama.cpp before going further: without probabilities the meter has nothing to measure. (The meter asks for OpenAI-style <code>logprobs</code>, which llama-server supports in recent versions.) The meter also sets every sampling setting itself and takes only the conversation, the tools and a length limit from the agent, so the agent can't sharpen the probabilities it is measured by.</li>
<li><b>Set up the agent box.</b> Follow <code>AGENT-BOX-SETUP.txt</code>: Raspberry Pi OS Lite; Wi-Fi and Bluetooth switched off in its boot settings; the built-in Ethernet to the Mac and a USB Ethernet adapter to the key's network switch; the agent in its own account without admin rights, pointed at <code>http://10.77.0.1:8080/v1</code> with streaming off.</li>
<li><b>Make the one-way wire.</b>
{fig(D.wire(), 'Cut the receive wire, insulate both ends, and trim the far end so it can never be reconnected by accident.', 'sm')}
Open the USB-serial cable's sheath near the plug end; cut the RX (yellow on FTDI cables) wire; heat-shrink both ends. Connect TX to the Pico's GP1 and black to its ground. Leave the Pico's GP0 unconnected.</li>
<li><b>Check the separation</b> from the agent box: the meter answers; the model's own port, SSH and file sharing on the Mac all fail; with the key in SEALED the agent box can't reach the internet. The setup sheets list each command.</li>
</ol>
<div class="tip"><b>Honest limits, worth saying out loud.</b> SEALED is enforced by hardware: the switch loses power. ACT is enforced by the agent's software reading the key. Wi-Fi on the agent box is off in its settings, which the agent can't change without admin rights. The Mac's own security depends on its settings staying as set: check them after macOS updates.</div>
''')

S.append(f'''
<h2>7 · Controller and sound</h2>
{fig(D.controller(), 'Controller wiring.')}
<ol class="steps">
<li><b>Flash the controller.</b> Follow <code>CONTROLLER-SETUP.txt</code>: Arduino IDE with the Raspberry Pi Pico core, board “Raspberry Pi Pico” (not Pico W), open <code>sandtable-controller.ino</code>, set <code>MAX_DRIVE</code> low (0.3), upload.</li>
<li><b>Build the board on perfboard:</b> the Pico, the DAC, a 24→5 V buck module feeding the Pico's VSYS, five logic-level MOSFETs (two counters, gap light, raking light, spare) with a diode across each counter coil, screw terminals for everything that leaves the board.</li>
<li><b>Bench test with the desk-test plate.</b> Run the meter on the Mac with the one-way wire connected. Use the Pico's USB and the Serial Monitor: <code>f 312</code> holds a frequency, <code>test 95</code> and <code>test 30</code> play a settled and an unsettled verdict, <code>show</code> prints the settings. Each verdict clicks the TASKS counter; below 50 it also clicks UNSETTLED. Then run a real task from the agent box and watch the verdict arrive.</li>
<li><b>Set the loudness ceiling twice:</b> the amplifier's gain knob, and <code>MAX_DRIVE</code> in the firmware. Neither can be changed from the Mac or the agent box.</li>
</ol>
''')

S.append(f'''
<h2>8 · The tray</h2>
{fig(D.tray(), 'Tray plan (mm). Front edge at the bottom.', 'big')}
{fig(D.front_edge(), 'Front edge of the tray (mm).', 'sm')}
<ol class="steps">
<li><b>Have the tray made</b> (or make it): solid walnut sides 600 × 80 × 18 mm, mitred or finger-jointed, with a 12 mm floor let into a groove 10 mm up. A rebate 9 × 5 mm round the inside top edge carries the glass on felt. Rout the floor into a shallow dish, 5 mm deep at the edges, so sand that leaves the plate collects where it can be brushed back. Oil, don't lacquer: the brass and walnut should age together.</li>
<li><b>Cut the front edge:</b> two 48 × 24 mm windows for the counters, four 3 mm holes for the telltales, one 22 mm hole for the key, all from the drawing. Drill the 12 mm cable hole in the floor above the back-right post.</li>
<li><b>Fit the driver</b> under the plate's centre on a small hardwood block, so the plate sits 35 mm above the floor and level. Bolt the plate to it with the M6 stud, a rubber washer under and a nylon washer over.</li>
<li><b>Fit the electronics</b> on the floor beside the driver (back left): the controller board, DAC and amplifier on standoffs. Raking-light strip along the inside of the left wall, just above plate height, angled across the plate.</li>
<li><b>Fit the counters, telltales and key</b> from the front. The key's ONLINE and ACT contacts both switch the network switch's 5 V; ACT also connects the agent box's GPIO 17 to ground. The <i>web open</i> and <i>may act</i> telltales take their power from those same contacts, so they always show what the key is really doing.</li>
<li><b>Optional placard.</b> Engrave <code>placard-optional.svg</code> on a small brass plate and set it in the front corner of the tray floor: what you're seeing, what it can't tell you, and why it can't be faked, for when you're not there to explain.</li>
</ol>
''')

S.append(f'''
<h2>9 · The body</h2>
{fig(D.body_plan(), 'Plan inside the body (mm). Front at the bottom.', 'big')}
{fig(D.section(), 'Front section through the whole object (mm).', 'big')}
{fig(D.mold(), 'The body is cast upside down, so the top (where the posts and the gap light sit) comes off the smooth mold floor.', 'big')}
<ol class="steps">
<li><b>Build the mold.</b> Melamine, inside 600 × 600, 150 deep. Taped XPS core 570 × 570 × 130 with 2° of draft, leaving 15 mm walls and a 20 mm top. Glue on: two vent blocks 500 × 100 (one each side wall), a hatch block 260 × 110 on the back wall, and 6 mm strips down the core's front and back faces and across its middle to form the divider's grooves. Bolt stainless inserts through the mold floor for the four posts (60 mm in from each corner) and push a Ø14 tube up through the floor at the back-right post for the cable. Inserts round each opening for the vents (8) and hatch (4), and along the open face's inner edge for the bottom plate (8).</li>
<li><b>Cast.</b> GFRC face coat about 3 mm, then backer mix to 15 mm walls and 20 mm top, following the {a('https://www.smooth-on.com/tb/files/BUDDY_RHODES_GFRC_MIX_TB.pdf', 'Buddy Rhodes bulletin')}. Tap out the air. Cover and leave above 15 °C.</li>
<li><b>Demold</b> the next day, pull the core, keep it damp for 7 days, dry for a week, seal inside and out.</li>
<li><b>Fit out.</b> Brass vents over the side openings (M4 into the inserts). Divider slid into its grooves, with a rubber grommet in its one 20 mm hole. Hatch plate on the back with thumbscrews, power cord and internet cable through its two grommets. Gap-light strip in a shallow channel round the top edge under the tray's shadow. Felt plinth under the bottom plate.</li>
<li><b>Fill the compartments.</b> Left: the agent box, the network switch, and their supplies. Right: the Mac on four 15 mm rubber feet with clear space under it (it breathes in through its base), turned so its exhaust faces the right vent, with a short duct if needed; the power strip and the 24 V supply against the back wall. The one Ethernet cable crosses through the divider's grommet; nothing else does.</li>
</ol>
''')

S.append('''
<h2>10 · Assembly</h2>
<ol class="steps">
<li>Body on its plinth where it will live. Bottom plate on.</li>
<li>Run the post cable: from the Mac compartment (the one-way wire's two cores and the 24 V pair) and the left compartment (the switch's 5 V pair and the GPIO 17 pair) up through the Ø14 tube.</li>
<li>Screw the four posts into their inserts on rubber isolators, the hollow one at back right with the cable through it.</li>
<li>Lower the tray onto the posts, cable through its floor hole, and connect it to the controller board's terminals.</li>
<li>Sand on the plate, a thin even layer. Glass cover on its felt.</li>
<li>Power on. The gap light comes on when the meter's heartbeat arrives.</li>
</ol>
''')

S.append('''
<h2>11 · Choosing your figure</h2>
<p>Every plate has its own set of figures, depending on its exact size and thickness, so the choice is made on your plate, not from a menu. Allow about 20 minutes in a quiet room, with everyone who'll live with it.</p>
<ol class="steps">
<li>Lift the glass off. Press <b>SETUP</b> under the tray once. The plate slowly sweeps from low notes to high and shows every figure it can make, one after another.</li>
<li>When you see one you like, press <b>SETUP</b>. It searches back and forth just around that note.</li>
<li>Press <b>SETUP</b> again when the figure is crispest. The note is saved and the plate rings once. That's your figure.</li>
<li>Hold SETUP for 3 seconds at any time to cancel. You can choose again whenever you like.</li>
</ol>
<p>Sand never lands exactly the same way twice, so even with the same figure, no two verdicts look identical.</p>
''')

S.append('''
<h2>12 · Tests</h2>
<div class="tbl"><table><thead><tr><th>Test</th><th>How</th><th>Pass</th></tr></thead><tbody>
<tr><td>Separation</td><td>From the agent box: the meter's port; the model's port; SSH; file sharing.</td><td>Only the meter answers.</td></tr>
<tr><td>Key</td><td>SEALED, ONLINE, ACT; ping out and run act-allowed in each.</td><td>No internet in SEALED; act-allowed says yes only in ACT; telltales match.</td></tr>
<tr><td>Agent can't shape the reading</td><td>On any computer with Python, run <code>tools/sandguide/test_meter.py</code>.</td><td>It ends with OK: a request carrying the agent's own temperature, logit bias or grammar reaches the model exactly like a plain one, with the same verdict.</td></tr>
<tr><td>Probabilities hidden</td><td>Look at a reply on the agent box.</td><td>No logprobs in it.</td></tr>
<tr><td>Range</td><td>Ask the agent something trivial, then something it can't know.</td><td>The first comes out crisp; the second visibly smeared.</td></tr>
<tr><td>Counters</td><td>Ten tasks.</td><td>TASKS went up by ten; UNSETTLED by the number below 50.</td></tr>
<tr><td>Loudness</td><td>Sound meter at 1 m during a verdict.</td><td>At or below your desk-test level.</td></tr>
<tr><td>Heat</td><td>A long agent run with the hatch closed.</td><td>The Mac's own temperatures are normal; the vent air is warm, not hot.</td></tr>
<tr><td>Off</td><td>Shut the Mac down.</td><td>Within 20 s the gap goes dark except a heartbeat blink every 10 s.</td></tr>
</tbody></table></div>
''')

S.append('''
<h2>13 · Living with it</h2>
<ul>
<li><b>The counters</b> are the long record: over months, unsettled ÷ tasks is an honest picture of how the agent does in your house. They can't be reset; that's the point.</li>
<li><b>The log</b> is in the meter's home folder on the Mac (<code>sandtable-log.csv</code>). Now and then, mark in its last column whether tasks were actually right. That's the start of calibration. Also watch the <code>tool_calls</code> column: the fixed parts of a tool call are forced by its format, so if tool-heavy tasks come out crisper than they deserve, note it.</li>
<li><b>Updates</b> to the Mac follow step 9 of <code>MAC-SETUP.txt</code>: the agent box is unplugged before the firewall goes off, and plugged back in only after it's on again.</li>
<li><b>Sand:</b> brush what's in the dish back onto the plate every few weeks; top up from the bag.</li>
<li><b>Brass:</b> unlacquered, it darkens over a few years; the key, handled daily, stays bright. Wipe with a dry cloth only.</li>
<li><b>The key</b> stays in SEALED unless the agent needs the web; ACT only when you mean it.</li>
<li><b>Lights:</b> the LIGHTS switch under the tray turns them all off, the heartbeat blink included.</li>
</ul>
<h3>For reviewers</h3>
<ul><li>Is a sand figure a meaningful way to show how settled a model was? What would you read into it?</li><li>Where would you attack the separation: the Mac's settings, the agent box, the key?</li><li>Is “the worst decision in the task” the right summary, or would you weigh decisions differently?</li><li>If you've built Chladni plates: sizes, drivers, sands, and how loud?</li></ul>
''')

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Sand Table Build Guide</title><style>{CSS}</style></head><body><main class="wrap">{''.join(S)}</main></body></html>'''
open(SP + 'sand-build-guide.html', 'w').write(page)
print(len(page))
