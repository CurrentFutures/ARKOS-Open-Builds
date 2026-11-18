import re,sys,html,os
sys.path.insert(0,os.path.dirname(__file__))
from lantern_data import PARTS
SP=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
s=open(SP+'lantern-unit.html').read()
def R(a,b):
    global s
    if s.count(a)!=1: sys.exit('miss: '+a[:70])
    s=s.replace(a,b)
R("for(var l=0;l<4;l++)lg.fillRect(377,30+l*18,83,9);","for(var l=0;l<6;l++)lg.fillRect(377,10+l*15,83,9);")
R('<span class="eyebrow">Build 2 · the media lantern · unit only</span>','<span class="eyebrow">Build 2 · the media lantern · model and build files</span>')
R("Use the switches to light it, open the back and pull the drives, or see through the concrete.</p>",
  "Use the switches to light it, open the back and pull the drives, or see through the concrete. When it looks right, make the files: cut files for the shops, and print files for the glass in the colors you chose.</p>")
# file buttons
R('<div class="group" style="grid-column:1/-1"><div class="seg"><button type="button" id="resetAll">',
  '<div class="group" style="grid-column:1/-1"><span class="eyebrow">Make the files</span><div class="seg"><button type="button" id="mkCut">Cut files (DXF, for acrylic and aluminum)</button><button type="button" id="mkPrint">Print files for these colors (17 PNG)</button></div><output id="fileOut" style="font-family:var(--mono);font-size:.78rem;color:var(--dim)">The cut files never change. The print files use the glass and film colors and the band set above.</output></div>\n    <div class="group" style="grid-column:1/-1"><div class="seg"><button type="button" id="resetAll">')
# description list
a=s.index('  <ul class="parts">');b=s.index('</ul>',a)+5
s=s[:a]+'''  <ul class="parts">
    <li><b>Glass:</b> 17 panes of 6 mm cast acrylic, 210 × 220 mm, 6 mm gaps, open top. Each pane steps darker toward the center.</li>
    <li><b>Film:</b> a soft-edged square of color printed on each pane, growing toward the center, where it's just bigger than the window.</li>
    <li><b>Window:</b> notched out of the middle 7 panes, 158 × 154 mm, around the computer.</li>
    <li><b>Rods:</b> four M5 stainless rods with acorn nuts hold the panes as one block, on clear acrylic spacer rings.</li>
    <li><b>Computer:</b> MINIX Z100-0dB, fanless, 123 × 120 × 46 mm, standing on edge.</li>
    <li><b>Base:</b> cast GFRC concrete, 210 × 200 × 172 mm, on an inset felt plinth.</li>
    <li><b>Top:</b> 8 mm aluminum plate with air slots under the pane gaps, LED strips under the pane edges and a grommet for the computer's cables.</li>
    <li><b>Back:</b> 2 mm aluminum plate set flush in a cast rebate on four thumbscrews. Air slots, power inlet, HDMI and Ethernet across the top, where the air space is; a window onto the peak-hold label and a vent plug below.</li>
    <li><b>Cables:</b> right-angle plugs point down, so the three cables drop straight down the back.</li>
    <li><b>Vault:</b> two 3.5" drives standing in a sled on elastic cords, on plastic runners; it slides out the back.</li>
    <li><b>Power:</b> one 12 V supply in the air space under the top plate runs the computer, drives and lights. One cord.</li>
    <li><b>Button:</b> a flush steel button on the front: tap for on and off, double-tap for the next mode, hold for lamp.</li>
  </ul>'''+s[b:]
# build section: short parts table from the shared data, pointer to the guide
rows=[]
for grp,items in PARTS:
    rows.append(f'<tr class="g"><td colspan="4">{html.escape(grp)}</td></tr>')
    for (part,spec,qty,cost,src,url,v) in items:
        if not part: continue
        link=f'<a href="{html.escape(url)}" target="_blank" rel="noopener">{html.escape(src)}</a>' if url else html.escape(src)
        rows.append(f'<tr><td>{html.escape(part)}</td><td>{html.escape(spec)}</td><td>{link}</td><td class="p">{html.escape(cost)}</td></tr>')
a=s.index('  <section class="sec2" id="build">');b=s.index('</section>',a)+10
s=s[:a]+'''  <section class="sec2" id="build">
    <h2>Parts</h2>
    <p style="color:var(--dim)">Rough prices for November 2026. The build guide that comes with this model has every step, drawing and test; this is the shopping list.</p>
    <div class="tbl"><table><thead><tr><th>Part</th><th>What to ask for</th><th>Where</th><th>Rough cost</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table></div>
  </section>'''+s[b:]
js=open(SP+'guide/export.js').read()
R("loop();\n})();\n</script>",'loop();\n'+js+'})();\n</script>')
s=s.replace('<title>The Lantern Unit</title>','<title>The Lantern Model</title>')
open(SP+'lantern-unit.html','w').write(s)
# offline copy: inline three.js, drop the web fonts
t=s
for pth in ['build/three.min.js','examples/js/controls/OrbitControls.js','examples/js/environments/RoomEnvironment.js','examples/js/geometries/RoundedBoxGeometry.js']:
    tag=f'<script src="https://cdn.jsdelivr.net/npm/three@0.147.0/{pth}"></script>'
    code=open(SP+'vendor/package/'+pth).read().replace('</script','<\\/script')
    if t.count(tag)!=1: sys.exit('no tag '+pth)
    t=t.replace(tag,'<script>\n'+code+'\n</script>')
t=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n','',t)
open(SP+'lantern-tool.html','w').write(t)
print('ok',len(s),len(t))
