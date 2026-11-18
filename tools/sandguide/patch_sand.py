import os
import sys,re
SP=os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
s=open(SP+'sand-object.before-tool.html').read()
def R(a,b):
    global s
    if s.count(a)!=1: sys.exit('miss %d: %s'%(s.count(a),a[:90]))
    s=s.replace(a,b)
# ---- header
R("crisp if the agent was sure, blurred if it guessed.","crisp if the agent was settled, smeared if it was unsettled.")
R("The figure stays until the next task.</p>","The figure stays until the next task. When it looks right, make the files: cut files for the shops, and the software for the three machines.</p>")
# ---- controls
R('<div class="seg"><button type="button" id="runSure" class="act">Agent was sure</button><button type="button" id="runUnsure" class="act">Agent was guessing</button></div>',
  '<div class="slider"><label for="settle">How settled</label><input id="settle" type="range" min="0" max="100" step="1" value="94"><output id="settleO" for="settle">94</output></div>'
  '<div class="seg"><button type="button" id="runNow" class="act">Finish a task at this reading</button><button type="button" id="runSure" class="act">Settled</button><button type="button" id="runUnsure" class="act">Unsettled</button></div>')
R('<div class="group"><span class="eyebrow">Plate</span>',
  '<div class="group"><span class="eyebrow">Your figure (chosen at setup)</span>'
  '<div class="seg" data-k="fig"><button type="button" data-v="0" aria-pressed="false">A</button><button type="button" data-v="1" aria-pressed="false">B</button><button type="button" data-v="2" aria-pressed="true">C</button><button type="button" data-v="3" aria-pressed="false">D</button><button type="button" data-v="4" aria-pressed="false">E</button><button type="button" data-v="5" aria-pressed="false">F</button></div></div>\n'
  '    <div class="group"><span class="eyebrow">Plate size (from the desk test)</span>'
  '<div class="seg" data-k="psize"><button type="button" data-v="30" aria-pressed="false">30 cm</button><button type="button" data-v="35" aria-pressed="false">35</button><button type="button" data-v="40" aria-pressed="true">40</button><button type="button" data-v="45" aria-pressed="false">45</button><button type="button" data-v="50" aria-pressed="false">50</button></div></div>\n'
  '    <div class="group"><span class="eyebrow">Plate</span>')
R('<div class="seg"><button type="button" id="resetAll">Reset everything</button></div></div>',
  '<div class="seg"><button type="button" id="resetAll">Reset everything</button></div></div>\n'
  '    <div class="group" style="grid-column:1/-1"><span class="eyebrow">Make the files</span><div class="seg"><button type="button" id="mkCut">Cut files (plate at this size, glass, vents, divider)</button><button type="button" id="mkSoft">Software (meter, controller, Mac and agent box)</button></div><output id="fileOut" style="font-family:var(--mono);font-size:.78rem;color:var(--dim)">The cut files use the plate size set above. The figure itself is chosen on the real plate, at setup.</output></div>')
# ---- description list
a=s.index('  <ul class="parts">');b=s.index('</ul>',a)+5
s=s[:a]+'''  <ul class="parts">
    <li><b>Size:</b> about 60 × 60 cm and 31 cm tall. An object for the floor or a sideboard, not a table.</li>
    <li><b>Body:</b> glass-fiber reinforced concrete with two compartments behind a perforated brass divider: the agent's small computer on the left, the Mac Studio (the model and the meter) on the right, raised on feet. One cable crosses between them, through one hole.</li>
    <li><b>Brass vents on opposite sides:</b> air in on the left, out on the right, straight across both compartments.</li>
    <li><b>Gap:</b> 4 cm on four brass posts with rubber isolators. The back-right post is hollow: the one-way wire and the tray's low-voltage power go up it.</li>
    <li><b>Sand tray:</b> walnut, with a square brass plate on a driver at its center, edges free, sized by the desk test. Glass microbeads, 100–200 micrometres. A lift-off glass cover.</li>
    <li><b>The figure:</b> one figure, chosen by the household at setup from the ones its own plate can make. Clarity is the reading everywhere: crisp is settled, smeared is unsettled.</li>
    <li><b>The tone is the plate:</b> no speaker. Unsettled makes it grainy. It rings down like a bell.</li>
    <li><b>Front edge:</b> the key (SEALED, ONLINE, ACT), four telltales (working, tool call, web open, may act) and two counters that only count up: tasks, and unsettled tasks.</li>
    <li><b>Gap light:</b> steady when on, breathing when resting, a heartbeat blink when off. It can be switched off.</li>
    <li><b>Honesty:</b> the agent lives on its own computer and can't reach the model's runtime, the meter or the table. The meter is arithmetic. One wire, one direction, a controller with no radio.</li>
  </ul>'''+s[b:]
# ---- notes
R("sure:'The last task ended with the agent sure of itself: the figure came out crisp, thin clean lines with bare metal between them.',unsure:'The last task ended with the agent guessing: the same figure, but smeared and scattered. You can see the doubt from across the room.',",
  "settled:'The last task ended settled: the figure came out crisp, thin clean lines with bare metal between them. Settled is not the same as right.',unsettled:'The last task had an unsettled moment: the same figure, smeared and scattered. Worth checking its work.',")
R("xray:' The body is shown see-through: the Mac Studio against the right wall with its duct to the right vent, the radio-free controller, the power strip, and the one-way wire running up the hollow back-right post.'",
  "xray:' The body is shown see-through: on the left, the agent\\'s small computer and the switch the key powers; behind the brass divider on the right, the Mac Studio on its feet. One blue cable crosses between them. The red one-way wire runs from the Mac up the hollow back-right post to the radio-free controller in the tray.'")
# ---- inside the body: two compartments
R("rbox(19.7,9.5,19.7,1.4,W/2-13.5,5.3+4.75,0,","[[-1,-1],[1,-1],[-1,1],[1,1]].forEach(function(p){cyl(.9,1.5,W/2-13.5+p[0]*7.5,5.3+.75,p[1]*7.5,rubber,inside);});\nrbox(19.7,9.5,19.7,1.4,W/2-13.5,6.8+4.75,0,")
R("box(8,1,6,-16,5,12,new THREE.MeshStandardMaterial({color:0x1d4a2c,roughness:.6}),inside);          // controller (no radio)",
  "box(.25,12.8,50,-1,5.3+6.4,0,perfM,inside);                                                          // brass divider\nrbox(9.3,2.8,6.6,.4,-14,5.3+1.4,4,new THREE.MeshStandardMaterial({color:0x8d9196,metalness:.8,roughness:.35}),inside); // agent box (Pi 5, passive case)\nbox(7,2.2,5,-20,5.3+1.1,-17,new THREE.MeshStandardMaterial({color:0x2a2b2d,roughness:.6}),inside); // network switch the key powers\nvar netM=new THREE.MeshBasicMaterial({color:0x3f7fd6});")
R("box(18,3,4,-12,5.6,-18,new THREE.MeshStandardMaterial({color:0xe8e6e1,roughness:.6}),inside);     // power strip",
  "box(18,3,4,10,5.3+1.5,-20,new THREE.MeshStandardMaterial({color:0xe8e6e1,roughness:.6}),inside);     // power strip")
R("tube([[-16,6,12],[-8,7,0],[6,7,-16],[20,8,-23],[24,BT+2,-24]],.18,wireM,inside);",
  "tube([[-9.3,6.8,4],[-4,8,4],[-1,9,4],[3,9,4],[8,9.5,4]],.22,netM,inside);                        // the one cable: agent box to Mac\ntube([[-14,6.8,.7],[-17,6.5,-10],[-20,6.5,-14.5]],.2,netM,inside);tube([[-20,6.5,-19.5],[-21,6.5,-25],[-21,6.5,-31]],.2,netM,inside); // agent box to the switch, switch out the back\ntube([[16,7,-9.8],[20,7.5,-18],[23,9,-23],[24,BT+2,-24]],.18,wireM,inside);")
# ---- figure choice, plate size, counters
R("var MODE=[2,5];","var FIGS=[[1,2],[2,3],[2,5],[1,4],[3,4],[3,5]],MODE=FIGS[2],PSIZE=40,PL0;")
R("var plate=box(PL,.15,PL,0,PY,0,plateM,top);","var plate=box(PL,.15,PL,0,PY,0,plateM,top);PL0=PL;")
R("var tells=[];",
  "var cnt=[0,0],cntCv=[],cntT=[];[['TASKS',-17],['UNSETTLED',-8.5]].forEach(function(c,i){var cv=cnv(256,128);cntCv.push(cv);var tx=new THREE.CanvasTexture(cv);tx.encoding=THREE.sRGBEncoding;cntT.push(tx);box(6.4,3.2,.25,c[1],TT+TH/2+.3,W/2+.1,[keyBrass,keyBrass,keyBrass,keyBrass,new THREE.MeshStandardMaterial({map:tx,roughness:.5}),keyBrass],top);});\n"
  "function drawCounters(){['TASKS','UNSETTLED'].forEach(function(lb,i){var g=cntCv[i].getContext('2d');g.fillStyle='#b8925a';g.fillRect(0,0,256,128);g.fillStyle='#111';g.fillRect(18,14,220,64);var d=('00000'+cnt[i]).slice(-5);g.font='bold 50px ui-monospace,Menlo,monospace';g.textAlign='center';for(var k=0;k<5;k++){g.fillStyle='#1d1d1d';g.fillRect(22+k*43.5,18,38,56);g.fillStyle='#f2efe8';g.fillText(d[k],41+k*43.5,64);}g.fillStyle='#2a1f10';g.font='600 26px Georgia,serif';g.fillText(lb,128,112);cntT[i].needsUpdate=true;});}\n"
  "var trayParts=new THREE.Group();top.add(trayParts);trayParts.visible=false;\nbox(5.1,.4,2.1,-18,TT+TF+.6,-16,new THREE.MeshStandardMaterial({color:0x1d4a2c,roughness:.6}),trayParts);   // controller: a Pico, no radio\nbox(6,1.6,5,-10,TT+TF+1.2,-17,new THREE.MeshStandardMaterial({color:0x2a2b2d,roughness:.6}),trayParts);   // DAC and amplifier\ntube([[24,TT+.6,-24],[10,TT+1.3,-22],[-15,TT+1.3,-17]],.18,wireM,trayParts);\nvar tells=[];")
# ---- verdicts: continuous reading
R("function run(unsure){last=unsure?'unsure':'sure';seed=Math.random()*100;anim={t0:performance.now(),unsure:unsure};tone(unsure);note();}",
  "var READ=94;function blurOf(r){return Math.min(1,Math.max(0,(1-r/100)*1.45-.04));}\n"
  "function run(r){READ=r;document.getElementById('settle').value=r;document.getElementById('settleO').textContent=r;last=r>=50?'settled':'unsettled';seed=Math.random()*100;anim={t0:performance.now(),b:blurOf(r)};tone(blurOf(r));cnt[0]++;if(r<50)cnt[1]++;drawCounters();note();}")
R("document.getElementById('runSure').addEventListener('click',function(){run(false);});",
  "document.getElementById('runSure').addEventListener('click',function(){run(94);});document.getElementById('runNow').addEventListener('click',function(){run(+document.getElementById('settle').value);});\n"
  "document.getElementById('settle').addEventListener('input',function(e){document.getElementById('settleO').textContent=e.target.value;});")
R("document.getElementById('runUnsure').addEventListener('click',function(){run(true);});","document.getElementById('runUnsure').addEventListener('click',function(){run(30);});")
R("blur=tb;","blur=anim.b;")
R("var tb=anim.unsure?1:0;","")
# tone scales with blur
R("function tone(unsure){","function tone(u){var unsure=u>.08;")
R("ng.gain.linearRampToValueAtTime(.35,t+.15);ng.gain.setValueAtTime(.35,t+1.5);","ng.gain.linearRampToValueAtTime(.38*u,t+.15);ng.gain.setValueAtTime(.38*u,t+1.5);")
R("paintSand(anim?order:1,last==='unsure'?1:0,seed);","paintSand(anim?order:1,blurOf(READ),seed);")
# segmented controls for fig and psize
R("if(k==='view'){setView(v);return;}",
  "if(k==='view'){setView(v);return;}if(k==='fig'){MODE=FIGS[+v];paintSand(1,blurOf(READ),seed);return;}if(k==='psize'){setPlate(+v);return;}")
R("function resetAll(){","function setPlate(cm){PSIZE=cm;var f=cm/PL0;plate.scale.set(f,1,f);sand.scale.set(f,f,1);edgeDrv.position.z=(PL0-cm)/2;}\nfunction resetAll(){MODE=FIGS[2];setPressed('fig','2');setPressed('psize','40');setPlate(40);cnt=[0,0];drawCounters();READ=94;document.getElementById('settle').value=94;document.getElementById('settleO').textContent=94;")
R("last='sure';order=1;blur=0;anim=null;seed=3.7;","last='settled';order=1;blur=0;anim=null;seed=3.7;")
# x-ray also shows the tray's parts
R("inside.visible=x;","inside.visible=x;trayParts.visible=x;")
# telltales: working, tool call, web open, may act
R("tells.forEach(function(m,i){var c=m.material.color;if(i===0){c.setRGB(1,.75,.4).multiplyScalar(.25+.25*Math.max(0,Math.sin(t*2.2)));}else if(i===1){c.setRGB(.4,.8,.5).multiplyScalar(.5);}else c.setRGB(0,0,0);});",
  "var wk=anim?1:0,tl=anim&&(now-anim.t0)<900?1:0;tells.forEach(function(m,i){var c=m.material.color;if(i===0)c.setRGB(1,.75,.4).multiplyScalar(wk*.8);else if(i===1)c.setRGB(.5,.7,1).multiplyScalar(tl*.9);else if(i===2)c.setRGB(.4,.8,.5).multiplyScalar(.5);else c.setRGB(0,0,0);});")
js=open(SP+'sandguide/sand-export.js').read()
R("loop();\n})();\n</script>","loop();\n"+js+"})();\n</script>")
s=s.replace('<title>','<title>',1)
open(SP+'sand-object.html','w').write(s)
# offline copy
t=s
for pth in ['build/three.min.js','examples/js/controls/OrbitControls.js','examples/js/environments/RoomEnvironment.js','examples/js/geometries/RoundedBoxGeometry.js']:
    tag=f'<script src="https://cdn.jsdelivr.net/npm/three@0.147.0/{pth}"></script>'
    if t.count(tag)!=1: sys.exit('no tag '+pth)
    t=t.replace(tag,'<script>\n'+open(SP+'vendor/package/'+pth).read().replace('</script','<\\/script')+'\n</script>')
t=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n?','',t)
open(SP+'sand-tool.html','w').write(t)
print('ok',len(s),len(t),re.search(r'<title>[^<]*',s).group(0))
