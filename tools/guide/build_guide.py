import sys,os,base64,io,html
sys.path.insert(0,os.path.dirname(__file__))
from lantern_data import PARTS
import diagrams as D
from PIL import Image
SP=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
def img(path,w=1000,crop=None,q=82):
    im=Image.open(path).convert('RGB')
    if crop: im=im.crop(crop)
    im.thumbnail((w,w*2));b=io.BytesIO();im.save(b,'JPEG',quality=q)
    return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
def fig(svg,cap,cls=''): return f'<figure class="dg {cls}">{svg}<figcaption>{cap}</figcaption></figure>'
def a(url,t): return f'<a href="{html.escape(url)}">{t}</a>'
I={k:img(SP+'shots/t-%s.png'%k,900,(250,40,1000,800)) for k in ('34',)}
I['back']=img(SP+'shots/t-back.png',900,(200,0,1000,800));I['drives']=img(SP+'shots/t-drives.png',900,(200,0,1000,800))
I['p03']=img(SP+'shots/p03.png',310);I['p09']=img(SP+'shots/p09.png',310)

rows=[]
for grp,items in PARTS:
    rows.append(f'<tr class="g"><td colspan="5">{html.escape(grp)}</td></tr>')
    for (part,spec,qty,cost,src,url,v) in items:
        mark='<span class="ok" title="link checked">✓</span> ' if v else ''
        link=(mark+a(url,html.escape(src))) if url else html.escape(src)
        rows.append(f'<tr><td>{html.escape(part)}</td><td>{html.escape(spec)}</td><td class="n">{html.escape(qty)}</td><td>{link}</td><td class="n">{html.escape(cost)}</td></tr>')
PTABLE='<div class="tbl"><table><thead><tr><th>Part</th><th>What to ask for</th><th>Qty</th><th>Where</th><th>Rough cost</th></tr></thead><tbody>'+''.join(rows)+'</tbody></table></div>'

CSS=r'''
:root{--paper:#f6f2ea;--card:#fffdf8;--ink:#1f1b16;--dim:#5e564c;--line:#d9d1c3;--accent:#8a6a2c;--warn:#9a3b1f;--warnbg:#f8e9df;--tip:#eef1e7;
 --part:#1f1b16;--fillA:#e6e0d4;--fillB:#cfd8d6;--fillC:#c9bfae;--glass:#bfe3dc;--led:#e7b552;--mains:#b4442a;--earth:#2f7d3b;--dc:#1f1b16;--data:#2d5f9a;
 --display:Georgia,"Times New Roman",serif;--body:"Helvetica Neue",Arial,sans-serif;--mono:ui-monospace,Menlo,Consolas,monospace;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--paper:#171513;--card:#201d1a;--ink:#ece6dc;--dim:#a99f92;--line:#3a342d;--accent:#d8b36a;--warn:#f0a585;--warnbg:#3a231a;--tip:#232a20;
 --part:#ece6dc;--fillA:#2f2b26;--fillB:#2b3836;--fillC:#3d362d;--glass:#2c5a52;--led:#c99a3a;--mains:#e0755a;--earth:#69b878;--dc:#ece6dc;--data:#7fa9df;color-scheme:dark}}
:root[data-theme="dark"]{--paper:#171513;--card:#201d1a;--ink:#ece6dc;--dim:#a99f92;--line:#3a342d;--accent:#d8b36a;--warn:#f0a585;--warnbg:#3a231a;--tip:#232a20;
 --part:#ece6dc;--fillA:#2f2b26;--fillB:#2b3836;--fillC:#3d362d;--glass:#2c5a52;--led:#c99a3a;--mains:#e0755a;--earth:#69b878;--dc:#ece6dc;--data:#7fa9df;color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.55}
.wrap{max-width:900px;margin:0 auto;padding:40px max(16px,env(safe-area-inset-left,0px)) 80px}
h1{font-family:var(--display);font-weight:600;font-size:clamp(2.2rem,6vw,3.4rem);line-height:1.02;margin:6px 0 14px;text-wrap:balance}
h2{font-family:var(--display);font-weight:600;font-size:1.75rem;margin:56px 0 6px;padding-top:14px;border-top:2px solid var(--ink);text-wrap:balance}
h3{font-family:var(--display);font-weight:600;font-size:1.2rem;margin:30px 0 6px}
p,li{max-width:70ch}p{margin:8px 0}
.eyebrow{font-family:var(--mono);font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;color:var(--dim)}
.lede{font-size:1.1rem;color:var(--dim)}
a{color:var(--accent);text-underline-offset:3px;word-break:break-word}
code,kbd,.mono{font-family:var(--mono);font-size:.86em}
pre{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:10px 14px;overflow-x:auto;font-size:.82rem;line-height:1.45;max-width:100%}
.hero{display:grid;grid-template-columns:1.2fr 1fr;gap:16px;margin:20px 0}
.hero img{width:100%;border-radius:6px;display:block;background:#111}
.facts{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:6px;overflow:hidden;margin:18px 0}
.facts div{background:var(--card);padding:10px 12px}.facts b{display:block;font-family:var(--display);font-size:1.25rem;font-weight:600}.facts span{font-size:.8rem;color:var(--dim)}
main{counter-reset:st}ol.steps{list-style:none;padding:0;margin:0}
ol.steps>li{counter-increment:st;position:relative;padding:14px 0 14px 52px;border-top:1px solid var(--line);max-width:none}
ol.steps>li::before{content:counter(st);position:absolute;left:0;top:14px;width:36px;height:36px;border-radius:50%;border:1.5px solid var(--ink);display:grid;place-items:center;font-family:var(--display);font-weight:600}
ol.steps>li>b:first-child{font-family:var(--display);font-size:1.08rem}
ol.sub{margin:6px 0;padding-left:1.2em}ol.sub li{margin:4px 0}
.timeline{display:grid;grid-template-columns:repeat(6,1fr);gap:4px;margin:14px 0;font-size:.78rem}
.timeline div{background:var(--card);border:1px solid var(--line);border-radius:4px;padding:6px 8px}.timeline b{display:block;font-size:.85rem}
.warn,.tip,.check{border-radius:0 6px 6px 0;padding:10px 14px;margin:12px 0;font-size:.94rem;max-width:72ch}
.warn{background:var(--warnbg);border-left:4px solid var(--warn)}.warn b:first-child{color:var(--warn)}
.tip{background:var(--tip);border-left:4px solid var(--earth)}
.check{background:var(--card);border-left:4px solid var(--accent)}
.tbl{overflow-x:auto;border:1px solid var(--line);border-radius:6px;margin:12px 0;background:var(--card)}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{text-align:left;vertical-align:top;padding:7px 10px;border-top:1px solid var(--line)}
thead th{border-top:0;font-family:var(--mono);font-size:.68rem;letter-spacing:.1em;text-transform:uppercase;color:var(--dim);font-weight:500}
td.n{white-space:nowrap;font-variant-numeric:tabular-nums}
tr.g td{background:var(--paper);font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.ok{color:var(--earth);font-weight:700}
figure.dg{margin:16px 0;background:var(--card);border:1px solid var(--line);border-radius:6px;padding:12px}
figure.dg svg{width:100%;height:auto;display:block;max-height:440px}
figure.dg.sm svg{max-height:300px}
figcaption{font-size:.82rem;color:var(--dim);margin-top:6px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.photo{margin:14px 0}.photo img{width:100%;border-radius:6px;display:block;background:#111}
.toc{columns:2;gap:28px;padding-left:1.2em;font-size:.95rem}
svg .part,svg .plate{fill:var(--fillA);stroke:var(--part);stroke-width:1}
svg .conc{fill:var(--fillC);stroke:var(--part);stroke-width:1}
svg .hole,svg .csk{fill:var(--paper);stroke:var(--part);stroke-width:.8}svg .csk{stroke-dasharray:2 1}
svg .hole2,svg .win,svg .cut{fill:var(--paper);stroke:var(--part);stroke-width:.9}
svg .win{fill:var(--glass)}
svg .slot{fill:var(--paper);stroke:var(--part);stroke-width:.6}
svg .band{fill:var(--paper);stroke:none;opacity:.85}svg .fade{stroke:var(--dim);stroke-dasharray:3 2;fill:none;stroke-width:.6}
svg .ps{fill:var(--fillB);stroke:var(--part);stroke-width:.5}svg .pw{fill:var(--glass);stroke:var(--part);stroke-width:.5}
svg .ring{fill:var(--paper);stroke:var(--part);stroke-width:.5}
svg .rod{stroke:var(--part);stroke-width:1.6}svg .nut{fill:var(--fillC);stroke:var(--part);stroke-width:.7}
svg .led{fill:var(--led);opacity:.75;stroke:none}svg .pc{fill:none;stroke:var(--dim);stroke-dasharray:4 3}
svg .zone{fill:var(--glass);opacity:.35;stroke:none}
svg .air,svg .vault,svg .void{fill:var(--paper);stroke:var(--part);stroke-width:.8}
svg .gasket{fill:var(--ink)}svg .lid,svg .bp{fill:var(--fillB);stroke:var(--part);stroke-width:.6}
svg .psu,svg .ctl,svg .inl{fill:var(--fillB);stroke:var(--part);stroke-width:.8}svg .btn{fill:var(--led);stroke:var(--part);stroke-width:.6}
svg .sled{fill:none;stroke:var(--part);stroke-width:1;stroke-dasharray:5 3}svg .felt{fill:var(--ink);opacity:.75}
svg .mold{fill:var(--fillA);stroke:var(--part);stroke-width:1}svg .core,svg .core2{fill:var(--glass);stroke:var(--part);stroke-width:.8}
svg .insert{fill:var(--ink)}svg .bolt{stroke:var(--part);stroke-width:2}svg .ledge{fill:var(--ink)}
svg .frame{fill:var(--fillA);stroke:var(--part)}svg .drive{fill:var(--fillB);stroke:var(--part);stroke-width:.8}svg .cord{stroke:var(--ink);stroke-width:.8}svg .run{fill:var(--ink)}
svg .blk{fill:var(--card);stroke:var(--part);stroke-width:1}svg .mains{fill:var(--warnbg);stroke:var(--mains);stroke-width:1.4}
svg .acw{stroke:var(--mains);stroke-width:2}svg .earth{stroke:var(--earth);stroke-width:2}svg .dc{stroke:var(--dc);stroke-width:1.6}
svg .usb{stroke:var(--data);stroke-width:1.6;fill:none}svg .sig{stroke:var(--data);stroke-width:1.2;stroke-dasharray:4 2}
svg .thin{stroke:var(--part);stroke-width:.6}svg .dim{stroke:var(--dim);stroke-width:.6}svg .arh{fill:var(--dim)}
svg .ldr{stroke:var(--dim);stroke-width:.5}svg .dot{fill:var(--dim)}
svg text{fill:var(--ink);font-family:var(--body)}svg .s{font-size:7px;fill:var(--dim)}svg .d{font-size:7.5px;fill:var(--dim);font-family:var(--mono)}svg .m{font-size:8.5px;font-weight:600}
@media (max-width:700px){.hero,.two{grid-template-columns:1fr}.facts{grid-template-columns:1fr 1fr}.timeline{grid-template-columns:1fr 1fr 1fr}.toc{columns:1}}
@media print{:root{--paper:#fff;--card:#fff}body{font-size:10.5pt}.wrap{max-width:none;padding:0}h2{break-before:page;margin-top:0}figure,table,.warn,.tip,.check,ol.steps>li{break-inside:avoid}a{color:var(--ink)}}
'''

S=[]  # sections
S.append(f'''
<span class="eyebrow">Build guide · the media lantern</span>
<h1>The Lantern, step by step</h1>
<p class="lede">A media player and lamp for beside the TV: a cube of printed acrylic panes around a fanless computer, standing on a concrete base that hides two hard drives in a sealed, silent vault. One cord, one button.</p>
<div class="hero"><img src="{I['34']}" alt="The Lantern, three-quarter view, lit"><img src="{I['back']}" alt="The back: ports and air slots across the top, label window and vent plug below"></div>
<div class="facts"><div><b>210 × 200 × 410</b><span>mm, wide × deep × tall</span></div><div><b>about 15 kg</b><span>lift by the base</span></div><div><b>6 weeks</b><span>mostly waiting on shops</span></div><div><b>$1,500–2,600</b><span>with computer and drives</span></div></div>
<p>This guide goes with <b>lantern-tool.html</b>, the interactive model in the same folder. The model is the tool: choose the glass and film colors there, then press its two buttons to make the <b>cut files</b> (for the acrylic and aluminum shops) and the <b>print files</b> (for the glass printer). Every dimension in those files matches the drawings here.</p>
<h3>Contents</h3>
<ol class="toc"><li>Before you start</li><li>Parts and where to get them</li><li>The computer and drives</li><li>Make the files</li><li>Glass</li><li>Metal</li><li>Concrete base</li><li>Electronics</li><li>Software</li><li>Assembly</li><li>Tests</li><li>Living with it</li><li>Key dimensions</li></ol>
''')

S.append(f'''
<h2>1 · Before you start</h2>
<h3>How the six weeks run</h3>
<p>Buy the computer and drives first; everything else sizes from them. After that, glass, metal and concrete run at the same time.</p>
<div class="timeline"><div><b>Week 1</b>Computer, drives, electronics. Desk-test the drives. Make the files.</div><div><b>Weeks 2–3</b>Order acrylic and aluminum. Build the mold.</div><div><b>Week 3</b>Cast the base. Anneal panes. Test print.</div><div><b>Week 4</b>Print all panes. Base cures. Bench-test lights.</div><div><b>Week 5</b>Seal base. Fit electronics. Software.</div><div><b>Week 6</b>Assemble. Heat, noise and light tests.</div></div>
<h3>Tools</h3>
<ul>
<li>Drill (a drill press if you can borrow one), 3.3, 4.2 and 5.5 mm bits, M3 and M4 taps, a countersink bit, a deburring tool.</li>
<li>Hacksaw or metal cutting blade for rod and aluminum angle; a fine file.</li>
<li>Multimeter with a continuity beep and a low-ohms range.</li>
<li>Soldering iron, wire strippers, crimper for ring terminals, heat-shrink and a heat gun.</li>
<li>Kitchen oven with an accurate oven thermometer (for annealing).</li>
<li>For the mold and cast: table or track saw (or have the melamine cut at the store), clamps, a bucket and paddle mixer, a scale, a level, nitrile gloves, eye protection, a dust mask.</li>
<li>A cheap probe thermometer and a phone sound-meter app for the tests.</li>
<li>A laptop that can run a Linux live USB (Ubuntu is fine), for formatting and checking the drives.</li>
</ul>
<div class="warn"><b>Mains voltage.</b> The inlet and power supply carry mains. Do that wiring with the power cord unplugged, follow the supply's own terminal labels, and have a qualified electrician or experienced technician check the inlet wiring and the earth bonds before the first power-on. Everything past the supply is 12 V.</div>
<div class="warn"><b>Wet concrete is caustic.</b> Gloves and eye protection when mixing and casting; wash skin straight away. Cut and sand concrete wet or with a mask.</div>
''')

S.append(f'''
<h2>2 · Parts and where to get them</h2>
<p>Rough prices for November 2026; they change. A <span class="ok">✓</span> means the link was checked for this guide and points at the exact item. Other links are a search or the shop's home page: choose the exact item yourself, using the description.</p>
{PTABLE}
<p><b>Total, roughly:</b> computer and drives $560–720; everything else $1,000–1,900.</p>
''')

S.append(f'''
<h2>3 · The computer and drives</h2>
<ol class="steps">
<li><b>Buy the computer and check it fits.</b> The guide is drawn around the {a('https://www.minix.com.hk/products/z100-0db-fanless-n100-mini-pc','MINIX NEO Z100-0dB')}: 123 × 120 × 46 mm, fanless, 12–19 V input, with its own 12 V 3 A adapter. The window in the panes is 158 wide × 154 tall and 78 deep, and needs 13 mm of air at each side and 24 mm above.
<div class="tbl"><table><thead><tr><th>Check</th><th>Need</th><th>Z100-0dB on edge</th></tr></thead><tbody>
<tr><td>Width + 2 × 13 mm</td><td>≤ 158</td><td class="n">123 + 26 = 149 ✓</td></tr>
<tr><td>Height + 24 mm</td><td>≤ 154</td><td class="n">120 + 24 = 144 ✓</td></tr>
<tr><td>Thickness</td><td>≤ 78</td><td class="n">46 ✓</td></tr>
<tr><td>Input voltage</td><td>12 V</td><td class="n">12–19 V ✓</td></tr></tbody></table></div>
If you use a different computer, run the same four checks before ordering anything else. A box that needs 19 V only adds a 12-to-19 V step-up converter in the air space.</li>
<li><b>Measure the real thing.</b> When it arrives, measure all three sides with calipers and write them down. Note where the ports are: it stands on edge with its ports facing back, so the cables drop straight to the grommet. Look at the plug on its power adapter and buy a barrel pigtail that matches it.</li>
<li><b>Buy the drives.</b> Two {a('https://www.westerndigital.com/products/internal-drives/wd-red-plus-sata-3-5-hdd?sku=WD80EFPX','WD Red Plus 8 TB (WD80EFPX)')}, 5640 rpm. Slower drives make less heat and less noise, and the vault is sealed.
<div class="warn"><b>Watch the model number.</b> The 12 TB WD Red Plus (WD120EFGX) spins at 7200 rpm even though it reports itself as 5400-class (Western Digital's own datasheet footnote says so). Check the spindle speed on the datasheet of any drive you consider, not the retailer listing. If you need more than 8 TB, take the vault heat test in section 11 especially seriously.</div></li>
<li><b>Desk-test the drive adapters.</b> USB-to-SATA bridges differ in two ways that matter here: whether the drive can sleep, and whether you can read its health (SMART). Test each adapter before building it in, on a laptop booted from an Ubuntu live USB:
<pre>sudo apt install smartmontools hdparm
lsblk                                   # find the drive, e.g. /dev/sdb
sudo smartctl -d sat -a /dev/sdb        # must print model, serial and a temperature
sudo hdparm -y /dev/sdb                 # put it to sleep now
sudo hdparm -C /dev/sdb                 # should say "standby"
sudo hdparm -S 120 /dev/sdb             # sleep after 10 minutes idle</pre>
If <code>hdparm</code> can't put it to sleep, try <code>sudo sdparm --command=stop /dev/sdb</code>. People on the {a('https://forum.libreelec.tv/thread/8909-how-can-i-make-external-usb-disks-suspend-when-unused','LibreELEC forum')} report this varies by bridge chip. Return any adapter that fails either test.</li>
<li><b>Format the drives</b> while you're there: <code>sudo mkfs.ext4 -L LIBRARY /dev/sdb1</code> on the first and <code>-L COPY</code> on the second (make one partition first with <code>sudo parted /dev/sdb mklabel gpt mkpart primary ext4 0% 100%</code>). Write LIBRARY and COPY on the drives' labels in marker.</li>
<li><b>Order the electronics now,</b> so you can measure them before the metal is cut: power supply, inlet, both Neutrik feed-throughs, light controller, strip, button. When the inlet and feed-throughs arrive, hold each against the back-plate drawing in step 18 and confirm the cutouts.</li>
</ol>
''')

S.append(f'''
<h2>4 · Make the files</h2>
<ol class="steps">
<li><b>Open lantern-tool.html</b> in Chrome, Edge, Firefox or Safari. It works with no internet connection. Drag to turn it, and try the light modes.</li>
<li><b>Choose the glass.</b> Under “Glass and film”: the glass color (the tint, which steps darker toward the center), the film color (the soft square), film squares on or off, and the clear band on or off. The defaults are near-black glass, a pale teal film and the clear band on.</li>
<li><b>Press “Cut files”.</b> You get <code>lantern-cut-files.zip</code>: <code>pane-window.dxf</code>, <code>pane-solid.dxf</code>, <code>spacer-ring.dxf</code>, <code>top-plate.dxf</code>, <code>back-plate.dxf</code>, <code>vault-lid.dxf</code> and <code>ORDER-SHEET.txt</code> with the material, thickness, quantity and notes for each. All are in millimetres at true size, outlines only. These never change.</li>
<li><b>Press “Print files for these colors”.</b> You get <code>lantern-print-files.zip</code>: 17 PNG files, one per pane, 210 × 220 mm at 150 dpi with the true size stored in the file, and <code>PRINT-NOTES.txt</code>. Pane 01 is the front. The transparency in each file is how much ink goes down.
<div class="two"><figure class="dg"><img src="{I['p03']}" alt="Print file for pane 03" style="width:100%;border-radius:4px"><figcaption>pane-03-solid.png, shown on white.</figcaption></figure><figure class="dg"><img src="{I['p09']}" alt="Print file for pane 09" style="width:100%;border-radius:4px"><figcaption>pane-09-window.png: the notch is empty because it's cut away.</figcaption></figure></div>
Change the colors and press it again as often as you like; only the print files change.</li>
</ol>
''')

S.append(f'''
<h2>5 · Glass</h2>
{fig(D.pane(),'Pane drawing (mm). Window panes 06–12 have the notch; the other ten are plain rectangles with the same four holes. The three-millimetre inside corners stop cracks starting at the notch.')}
<ol class="steps">
<li><b>Order the acrylic.</b> Upload the three acrylic DXF files to {a('https://sendcutsend.com/materials/acrylic','SendCutSend')} (they cut cast acrylic only, which is what you want), or take them to a local laser shop. Choose clear, 6 mm (0.236"). Quantities: <b>8</b> window panes, <b>12</b> solid panes, <b>72</b> spacer rings. That's three spares of each pane type and eight spare rings. Check that the preview shows the pane at 210 × 220 mm before you pay.</li>
<li><b>Check them in.</b> Lay each pane on a towel, film on. Measure one of each type with calipers. Measure the thickness of five panes and five rings and write down the average: your stack length is 17 × pane + 16 × ring. Number each pane on its protective film with a marker, 01 to 17, window panes as 06–12.</li>
<li><b>Anneal them.</b> Laser cutting leaves stress at the edges, which later shows up as fine cracks (crazing), especially near cleaners or heat. {a('https://www.acrylite.co/resources/knowledge-base/article/what-is-annealing-and-what-are-the-procedures-for-annealing-acrylic-sheet','ACRYLITE’s procedure')} for sheet up to 6 mm is 80 °C for 2 hours.
<ol class="sub"><li>Peel the protective film first; heated film can stick. Wear cotton gloves from now on.</li><li>Check your oven with an oven thermometer; many run 10–15 ° hot. Never go above 85 °C.</li><li>Stand the panes on edge in a rack (a board with saw cuts 12 mm apart works), or lay them flat on a clean baking sheet with paper between them. Don't stack them directly.</li><li>Heat to 80 °C, hold 2 hours, then switch off and leave the door closed until the oven is at room temperature.</li><li>Do the rings the same way, in a tray.</li></ol></li>
<li><b>Print one test pane.</b> Take a spare solid pane and <code>pane-05-solid.png</code> to a sign shop with a UV flatbed printer. Ask for: color only, no white underlayer, no varnish, printed at 100% size on one face. In a dark room, stand it on the LED strip (lit warm white and then your color) and look through it from a metre away. Too dark? Lower the glass color's brightness in the tool and remake the print files. Too faint? Raise it.</li>
<li><b>Print all 17.</b> Give the shop the 17 files and <code>PRINT-NOTES.txt</code>. Each pane is printed on its <b>inward</b> face: panes 01–08 on the face toward the back, 10–17 on the face toward the front, 09 on either. The ink is then protected inside the block and the outer faces stay glossy. Ask them to keep your numbering.</li>
<li><b>Assemble the stack.</b>
{fig(D.stack(),'Side view (mm). Pane, ring, pane: 12 mm pitch. Rods are M5 stainless, 208 mm long.')}
<ol class="sub"><li>Cut four M5 rods to 208 mm. Square the ends with a file and run an M5 nut on and off each end to clean the thread.</li><li>Make a jig: a scrap board with four 5 mm holes in the rod pattern (186 × 194 mm apart, centres). Stand the rods in it.</li><li>Put a nylon washer and an acorn nut on the bottom of each rod first, then slide on pane 17, a ring on each rod, pane 16, rings, and so on to pane 01. Window panes go on with the notch toward the jig board.</li><li>Every pane's printed face points toward the middle of the stack, pane 09. Check each one as it goes on.</li><li>Nylon washer and acorn nut on top. Tighten finger-tight, then one more eighth of a turn. Acrylic grows about seven times more than glass with heat; clamping it hard will crack it at the holes.</li><li>Measure the stack: about 198 mm. Lift it off the jig by the rods, never by one pane.</li></ol></li>
</ol>
<div class="tip"><b>Cleaning acrylic:</b> water with a drop of dish soap, and a microfiber cloth. Never alcohol, ammonia (window cleaner) or paper towels.</div>
''')

S.append(f'''
<h2>6 · Metal</h2>
{fig(D.topplate(),'Top plate, plan (mm). Front edge at the bottom.')}{fig(D.backplate(),'Back plate seen from behind (mm).')}
<ol class="steps">
<li><b>Order the plates.</b> Upload <code>top-plate.dxf</code>, <code>back-plate.dxf</code> and <code>vault-lid.dxf</code> to {a('https://sendcutsend.com','SendCutSend')} or a local waterjet or laser shop. Materials: top plate 6061 aluminum 8 mm (5/16" is fine); back plate 5052 aluminum 2 mm (0.080"); vault lid 5052 aluminum 3 mm (0.125"). Add the countersinks listed in the order sheet if the shop offers them; otherwise do them yourself (step 20).</li>
<li><b>Check the back plate before ordering.</b> The power inlet cutout is 46.5 × 27.5 mm, from the Digi-Key listing and Qualtek's drawing for the 719W family. The HDMI and Ethernet holes are standard Neutrik D-size: a 24 mm hole with two 3.2 mm holes on a diagonal. Hold the parts you bought against a 1:1 printout of the drawing and confirm both. The {a('https://neutrik.com/product/nahdmi-w','NAHDMI-W')} takes a panel up to 2 mm, which is why the back plate is 2 mm.</li>
<li><b>Order the hardware.</b> M5 stainless rod, {a('https://www.mcmaster.com/products/metric-acorn-nuts/','acorn nuts')}, nylon washers, the four pane standoffs, eight stainless cast-in inserts, screws and thumbscrews. The inserts must be in your hands before you build the mold.</li>
<li><b>Finish the plates.</b> Deburr every edge and hole. Countersink the top plate: the four 5.5 mm holes at 60 and 140 mm from the front edge from the <b>top</b>, so M5 flat heads sit flush; the four 4.5 mm corner holes from the <b>bottom</b>, for the M4 screws that hold the pane standoffs. Then brush the top face and the back plate's outside face: a fine non-woven pad (grey or maroon), long straight strokes in one direction, with a little water and dish soap.</li>
<li><b>Drill the parts' own holes.</b> These come from the real parts, so they aren't in the files:
<ol class="sub"><li>Power supply: set it on the underside of the top plate where the air-space plan shows (front edge 3 mm behind the front wall line, centered left to right). Mark its mounting holes through the supply's base, drill 2.5 mm, 6 mm deep, and tap M3. Don't go through the plate.</li><li>Light controller: the same way, at the back left (seen from the front), under the air slots.</li><li>Power inlet: its two flange screw holes, from the part, drilled 3.2 mm.</li><li>Earth points: one 3.3 mm hole tapped M4 in the underside of the top plate near the back, one in the back plate's inside face near the inlet, and the 4.2 mm hole already in the vault lid.</li></ol></li>
<li><b>Build the drive sled.</b>
{fig(D.sled(),'Drive sled seen from behind (mm).','sm')}
<ol class="sub"><li>Cut 15 × 15 mm aluminum angle: four rails of 150 mm, four cross pieces of 120 mm (top and bottom, front and back) and two uprights of 108 mm for a centre rail. Join them with M3 screws and nuts, or pop rivets.</li><li>Drill 3 mm holes in the side rails and the centre rail, level with the drives' side screw holes.</li><li>Screw a small M3 eye into each of the drive's four side holes. Tie each eye to the nearest rail with a short loop of 3 mm shock cord, so the drive floats about 20 mm from the rails and touches no metal.</li><li>Face the sled's back with 3 mm felt, and cut a 30 mm hole in the felt where the label window will be (opposite the left drive's end, seen from behind).</li><li>Stick UHMW strips along the two bottom rails as runners, and fit a small pull to the back.</li></ol></li>
</ol>
''')

S.append(f'''
<h2>7 · Concrete base</h2>
{fig(D.front_section(),'Front section (mm). The vault is narrower than the air space, which leaves a 7 mm ledge each side for the lid.','sm')}{fig(D.section(),'Side section (mm). Back at the left.')}
{fig(D.mold(),'The base is cast upside down, so the top face (where the plate sits) comes off the smooth melamine floor. Both foam cores lift out through the top once it has cured.')}
<ol class="steps">
<li><b>Build the mold.</b> Inside dimensions 210 × 200 mm, 172 deep, from 16 mm melamine. Floor about 260 × 250; walls screwed on from outside so they come off. Seal every inside joint with a thin bead of silicone, wiped to a small cove.
<ol class="sub"><li><b>Back rebate:</b> on the inside of the back wall, glue a 2 mm shim 189 × 171.5 mm, centered left to right and touching the floor (which is the top of the base). It forms the pocket the back plate sits in, with 1.5 mm of shadow gap round it.</li><li><b>Air-space core:</b> XPS foam, 150 wide × 166 deep × 41 tall, wrapped in packing tape for release, with 1–2° of draft on the sides (narrower at the open face). It sits on the mold floor, centered left to right, against the back shim.</li><li><b>Vault core:</b> XPS foam, 136 wide × 166 deep × 116 tall, taped, drafted; it sits on top of the air-space core, also against the back. That leaves a 15 mm floor at the open face.</li><li><b>Button pocket:</b> a foam block 30 × 26 × 36 mm glued to the front of the air-space core, 36 mm from the right side (seen from the front), so the front wall there is only 6 mm thick; and a 19 mm rod (a wooden dowel wrapped in tape) through the mold's front wall into it, 26 mm below the top face.</li><li><b>Inserts:</b> bolt four stainless inserts to the mold floor through holes drilled at the top plate's fixing positions (12 mm in from each side, 60 and 140 mm from the front), and four to the back wall at the back plate's thumbscrew positions. Coat the bolt threads with release so they come out.</li><li>Spray or wipe release agent on everything, not on the insert faces.</li></ol></li>
<li><b>Mix and cast.</b> Follow the {a('https://www.smooth-on.com/tb/files/BUDDY_RHODES_GFRC_MIX_TB.pdf','Buddy Rhodes GFRC technical bulletin')} for water, polymer and fiber amounts. The usual sequence:
<ol class="sub"><li>Face coat: a thin mix without fiber, sprayed or brushed about 3 mm thick on every mold surface. This is the finish you will see.</li><li>When the face coat is no longer glossy but still soft, pack the backer mix (with fiber) in layers, pressing it into the corners and around the inserts. Build the walls to full thickness and finish with the 15 mm floor.</li><li>Tap the mold walls with a rubber mallet all round to release air. Trowel the open face flat; check with a level.</li><li>Cover with plastic and leave it somewhere above 15 °C.</li></ol></li>
<li><b>Demold.</b> Next day (or when the bulletin says), unbolt the inserts, take off the walls, turn it the right way up and lift both cores out through the top. If a core sticks, break up the foam and pick it out. Keep the base wrapped and damp for 7 days.</li>
<li><b>Seal and finish.</b> Let it dry for a week. Fill any small voids with a slurry of the face mix. Apply the penetrating sealer to all faces, inside and out. Glue a 10 mm felt plinth, 180 × 170 mm, to the bottom, centered: it lifts the base 10 mm and makes the shadow line. Line the vault walls (not the lid ledge) with 3 mm felt.</li>
</ol>
<div class="warn"><b>No aluminum in wet concrete.</b> Fresh concrete eats aluminum and zinc. Only the stainless inserts go into the mold; the aluminum plates go on after the base has cured and been sealed.</div>
''')

S.append(f'''
<h2>8 · Electronics</h2>
{fig(D.wiring(),'Wiring. Everything right of the supply is 12 V.')}
<ol class="steps">
<li><b>Bench-wire everything first,</b> on a wooden board, before anything goes in the base. Lengths: about 25 cm for every 12 V lead, so there's slack to lift the top plate.
<ol class="sub"><li>Power inlet to supply: line (brown or black) and neutral (blue or white) from the inlet's switched terminals to the supply's L and N, with crimped, insulated spade or ring terminals. Earth from the inlet's earth tab to the supply's earth terminal.</li><li>Earth bonds: from the supply's earth terminal, one green/yellow wire each to the top plate, back plate and vault lid, with a ring terminal and a star washer under the screw head so it bites through to bare metal.</li><li>12 V: from the supply's +V and −V to a pair of lever connectors, then out to the computer pigtail, the two drive-adapter pigtails, and the light controller's power terminals.</li><li>Check the polarity of every barrel pigtail with the multimeter before you plug anything in: center is positive on almost all of them, but check.</li></ol></li>
<li><b>Set up the light controller.</b> Flash it from {a('https://install.quinled.info','install.quinled.info')} with Chrome or Edge on a computer, over USB. Join it to your Wi-Fi (2.4 GHz only), then open its page in a browser.
<ol class="sub"><li><b>LED Preferences:</b> one analog strip, type RGBCCT (5 channels), on the board's 5 outputs. Keep the max current at the strip's rating.</li><li>Wire the strip to the outputs as labelled (R, G, B, WW, CW, +12 V common). Cut the strip only at the marked cut points: two lengths of 180 mm for under the panes, and 72 mm for inside the window, joined to its run through the 6-pin plug.</li><li><b>Presets:</b> save 1 <i>Lamp</i> (warm white, 2700 K, full), 2 <i>Evening</i> (dim amber), 3 <i>Color</i> (your color), 4 <i>Asleep</i> (Breathe effect, slow, low). See the {a('https://quinled.info/quinled-an-penta-mini','An-Penta-Mini page')} for its button terminal: three button inputs, each pulled high, triggered by shorting to ground.</li><li><b>Button:</b> wire the 19 mm push button between the first button input and ground. In WLED, under Config → Time &amp; Macros → Button actions, give button 0: short press = on/off, double press = next preset, long press = preset 1 (Lamp).</li></ol></li>
<li><b>Test on the bench.</b> Plug in the cord with everything on the board. The computer boots; both drives spin up and show in its file manager; the strips light; the button does all three things. Leave it running for an hour and feel the supply: warm, not hot.</li>
<li><b>Fit it into the air space.</b>
{fig(D.airspace(),'Air space under the top plate, plan (mm). The supply hangs from the plate; the controller sits under the air slots.','sm')}
<ol class="sub"><li>Screw the supply and controller to the underside of the top plate (M3 into the holes you tapped).</li><li>Stick the LED strips on the top face of the plate, 86 mm each side of center, front to back, and take their wires down through the 6 mm holes. The aluminum plate is their heat sink.</li><li>Screw the four pane standoffs on from below with M4 flat heads.</li><li>Fit the Ø30 rubber grommet. Mount the inlet and the two Neutrik feed-throughs in the back plate.</li></ol></li>
</ol>
''')

S.append(f'''
<h2>9 · Software</h2>
<ol class="steps">
<li><b>Install LibreELEC.</b> It's a small system that boots straight into Kodi. Download the Generic x86-64 image from the {a('https://wiki.libreelec.tv/hardware/intel-x86-64-generic','LibreELEC Intel/AMD page')} (the Generic image, not Generic-Legacy, for HDR), write it to a USB stick with the LibreELEC USB-SD Creator, boot the computer from it and install to its internal drive.</li>
<li><b>Set up Kodi.</b> Settings → System → Display: 3840 × 2160, “Adjust display refresh rate” on start/stop. Settings → Player → Videos: allow HDR passthrough if your TV supports it. Add the LIBRARY drive (it mounts at <code>/var/media/LIBRARY</code>) as a Movies or TV source.</li>
<li><b>Turn on SSH and cron.</b> LibreELEC settings → Services: SSH on (set a password), Cron on. Install the <i>Network Tools</i> add-on from the LibreELEC repository, which brings <code>rsync</code>.</li>
<li><b>Make the drives sleep.</b> SSH in (<code>ssh root@lantern.local</code>, or its IP address) and create <code>/storage/.config/autostart.sh</code>:
<pre>#!/bin/sh
( sleep 60
  for d in /dev/sd?; do hdparm -S 120 $d; done ) &amp;</pre>
Then <code>chmod +x /storage/.config/autostart.sh</code> and reboot. If your adapter needed <code>sdparm</code> in step 4, use the command that worked there.</li>
<li><b>Nightly copy.</b> Find the add-on's rsync with <code>find /storage/.kodi/addons -name rsync</code>, then <code>crontab -e</code> and add one line (with your path):
<pre>30 3 * * * /storage/.kodi/addons/virtual.network-tools/bin/rsync -a /var/media/LIBRARY/ /var/media/COPY/</pre>
There's no <code>--delete</code> on purpose: if something is deleted from the library by mistake, the copy still has it. Tidy the copy by hand a few times a year.</li>
<li><b>Check it's working</b> the next morning: <code>ls /var/media/COPY</code>, and <code>hdparm -C /dev/sda /dev/sdb</code> should say <i>standby</i> when nothing is playing.</li>
</ol>
''')

S.append(f'''
<h2>10 · Assembly</h2>
<div class="photo"><img src="{I['drives']}" alt="The back opened with the drive sled pulled out"></div>
<ol class="steps">
<li><b>Base on its plinth,</b> on a towel on the bench. Vault felt in place.</li>
<li><b>Drives in.</b> Plug the adapters onto the drives, slide the sled in until it touches the front wall, and lay the two USB leads and the two 12 V leads up through the vault lid's Ø16 grommet.</li>
<li><b>Heat pads and lid.</b> Stick a gap pad on each drive's top edge. Run neoprene strip round the lid ledge and across the back edge of the opening. Lay the lid on: it should press lightly on both pads. Fit the earth wire to it and the high vent plug (closed).</li>
<li><b>Peak-hold labels.</b> One on the end of the left drive (seen from behind) where the window will look at it, one on the underside of the lid. Write the date next to each.</li>
<li><b>Top plate.</b> Connect the 12 V leads to the drive adapters' pigtails and the USB leads up through the plate grommet. Lower the plate on with its electronics hanging underneath, and screw it down with the four M5 flat heads into the cast inserts.</li>
<li><b>Back plate.</b> Connect the inlet, HDMI and Ethernet inside, then the earth wire. Set the plate into its rebate and do up the four thumbscrews evenly. It should press the neoprene against the vault's back edge.</li>
<li><b>Computer.</b> Stand it on edge, centered on the plate, ports to the back. Connect power, HDMI, Ethernet and the two drive USB leads through the grommet. Plug in the window LED.</li>
<li><b>Glass.</b> Lift the block by the rods, lower it straight down over the computer onto the four standoffs, and plug the window LED into its socket as it goes down.</li>
<li><b>Cables out.</b> Right-angle HDMI and Ethernet plugs pointing down, the fabric cord into the inlet. All three drop straight down the back.</li>
</ol>
''')

S.append(f'''
<h2>11 · Tests</h2>
<p>Do these before you put it beside the TV for good. Write the results on a card and keep it in the box.</p>
<div class="tbl"><table><thead><tr><th>Test</th><th>How</th><th>Pass</th></tr></thead><tbody>
<tr><td>Earth bonds</td><td>Unplugged. Multimeter on low ohms between the inlet's earth pin and each plate and the lid.</td><td>Under 0.5 Ω each. Then have it checked by someone qualified.</td></tr>
<tr><td>First power-on</td><td>Plug in, switch on at the inlet.</td><td>Computer boots, drives spin up, light comes on, no smell, no buzz.</td></tr>
<tr><td>Glass heat</td><td>Play 4K HDR video for 2 hours. Probe thermometer against the inside of the top of the window.</td><td>Under 50 °C.</td></tr>
<tr><td>Vault heat (the one that matters)</td><td>Warm the room to about 30 °C (a summer day). Over a few days, run the full nightly copy and a long self-test on each drive back to back. Read the drives' temperatures over SSH with <code>smartctl -d sat -A /dev/sda</code> if your build has it, or move the drives to the laptop after.</td><td>Drives stay under 50 °C. Labels show no step past 50 °C. If they do: open both vent plugs and repeat.</td></tr>
<tr><td>Sleep</td><td>Leave it idle for 15 minutes.</td><td><code>hdparm -C</code> says standby for both.</td></tr>
<tr><td>Noise</td><td>Quiet room, phone sound meter at 1 m, during the nightly copy.</td><td>You can't pick it out from the room at 1 m.</td></tr>
<tr><td>Light</td><td>Tap, double-tap and hold the button. Try each mode from the WLED page.</td><td>Every mode works; the window LED lights.</td></tr>
<tr><td>Lift-off</td><td>Lift the glass off and put it back.</td><td>It comes off clean and the window LED reconnects.</td></tr>
</tbody></table></div>
''')

S.append(f'''
<h2>12 · Living with it</h2>
<ul>
<li><b>Once a year:</b> read the peak-hold labels through the back window. Dust the top plate's slots with a soft brush (lift the glass off). Check <code>smartctl</code> on both drives.</li>
<li><b>Glass:</b> dust with a soft brush or blow it out; wash only with soapy water and microfiber.</li>
<li><b>Fuse:</b> if it goes dark and nothing responds, check the fuse drawer in the inlet. A blown fuse means find out why before replacing it.</li>
<li><b>A drive fails:</b> unplug, undo the four thumbscrews, slide the sled out. Swap the dead drive, format it (step 5), and copy back from the other.</li>
<li><b>Moving it:</b> lift the glass block off first and carry it separately, by the rods.</li>
</ul>
<h3>If something's wrong</h3>
<div class="tbl"><table><thead><tr><th>What you see</th><th>Likely cause</th></tr></thead><tbody>
<tr><td>Drives never sleep</td><td>The adapter ignores the sleep command, or something keeps reading them (Kodi library scan on a timer). Try <code>sdparm</code>; turn off scheduled scans.</td></tr>
<tr><td>A drive vanishes at random</td><td>12 V lead or barrel plug loose; or the adapter's UAS mode. Reseat; try a different adapter.</td></tr>
<tr><td>Light flickers</td><td>Loose strip connection at the window plug, or the controller's max current set too low.</td></tr>
<tr><td>Fine cracks near the rod holes</td><td>Nuts too tight, or a cleaner with alcohol. Loosen to finger-tight; replace the pane with a spare.</td></tr>
</tbody></table></div>
''')

S.append(f'''
<h2>13 · Key dimensions</h2>
<div class="tbl"><table><tbody>
<tr><td>Base</td><td>210 × 200 × 172 mm concrete, on a 10 mm felt plinth</td></tr>
<tr><td>Vault</td><td>136 wide × 166 deep × 116 tall; floor 15</td></tr>
<tr><td>Air space</td><td>150 wide × 166 deep × 41 tall; front wall 32</td></tr>
<tr><td>Top plate</td><td>210 × 200 × 8 mm, 6061</td></tr>
<tr><td>Back plate</td><td>186 × 170 × 2 mm, 5052, in a 2 mm rebate</td></tr>
<tr><td>Vault lid</td><td>148 × 166 × 3 mm, 5052</td></tr>
<tr><td>Panes</td><td>17 × 210 × 220 × 6 mm cast acrylic, 12 mm pitch, stack 198 mm</td></tr>
<tr><td>Window</td><td>158 × 154 mm, panes 06–12 (78 mm deep)</td></tr>
<tr><td>Rods</td><td>4 × M5 × 208 mm, at 12 mm from each side, 13 and 207 mm up</td></tr>
<tr><td>Panes above the plate</td><td>4 mm, on standoffs</td></tr>
<tr><td>Whole object</td><td>210 × 200 × about 414 mm tall, about 15 kg</td></tr>
</tbody></table></div>
<h3>Rules that can't change</h3>
<ul>
<li>Window clearance at least 13 mm round the computer's sides and 24 mm above.</li>
<li>Pane pitch 12 mm; an odd number of panes, so one sits at the darkest center.</li>
<li>Cast acrylic, annealed after cutting. Rod holes 6 mm for 5 mm rods; nuts never tight.</li>
<li>Print on the inward faces; keep the 20 mm clear band.</li>
<li>The vault stays sealed from the air space. Under 50 °C, for life.</li>
<li>All mains stays inside the inlet and the enclosed supply. Every metal plate is earthed.</li>
<li>Nothing aluminum or zinc in wet concrete.</li>
</ul>
''')

page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Lantern Build Guide</title><style>{CSS}</style></head><body><main class="wrap">{''.join(S)}</main></body></html>'''
open(SP+'lantern-build-guide.html','w').write(page)
print(len(page))
