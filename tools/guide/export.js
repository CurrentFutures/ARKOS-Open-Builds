// ---------- build files: cut files (DXF, mm) and print files (PNG, true size at 150 dpi) ----------
(function(){
var CRCT=(function(){var t=[],c;for(var n=0;n<256;n++){c=n;for(var k=0;k<8;k++)c=c&1?0xEDB88320^(c>>>1):c>>>1;t[n]=c>>>0;}return t;})();
function crc(u){var c=0xFFFFFFFF;for(var i=0;i<u.length;i++)c=CRCT[(c^u[i])&255]^(c>>>8);return (c^0xFFFFFFFF)>>>0;}
var enc=new TextEncoder(),DT=new Date(),DD=((DT.getFullYear()-1980)<<9)|((DT.getMonth()+1)<<5)|DT.getDate();
function zip(files){var parts=[],cd=[],off=0;
  files.forEach(function(f){var nm=enc.encode(f.name),d=f.data,c=crc(d),h=new DataView(new ArrayBuffer(30));
    h.setUint32(0,0x04034b50,true);h.setUint16(4,20,true);h.setUint16(6,0x0800,true);h.setUint16(12,DD,true);h.setUint32(14,c,true);h.setUint32(18,d.length,true);h.setUint32(22,d.length,true);h.setUint16(26,nm.length,true);
    parts.push(new Uint8Array(h.buffer),nm,d);
    var e=new DataView(new ArrayBuffer(46));e.setUint32(0,0x02014b50,true);e.setUint16(4,20,true);e.setUint16(6,20,true);e.setUint16(8,0x0800,true);e.setUint16(14,DD,true);e.setUint32(16,c,true);e.setUint32(20,d.length,true);e.setUint32(24,d.length,true);e.setUint16(28,nm.length,true);e.setUint32(42,off,true);
    cd.push(new Uint8Array(e.buffer),nm);off+=30+nm.length+d.length;});
  var cdl=cd.reduce(function(a,b){return a+b.length;},0),end=new DataView(new ArrayBuffer(22));
  end.setUint32(0,0x06054b50,true);end.setUint16(8,files.length,true);end.setUint16(10,files.length,true);end.setUint32(12,cdl,true);end.setUint32(16,off,true);
  return new Blob(parts.concat(cd,[new Uint8Array(end.buffer)]),{type:'application/zip'});}
function fx(n){return String(Math.round(n*1000)/1000);}
function DXF(){var o=[];return{
  poly:function(pts,bul){o.push('0','POLYLINE','8','CUT','66','1','10','0','20','0','30','0','70','1');pts.forEach(function(p,i){o.push('0','VERTEX','8','CUT','10',fx(p[0]),'20',fx(p[1]),'30','0');if(bul&&bul[i])o.push('42',String(bul[i]));});o.push('0','SEQEND','8','CUT');return this;},
  rect:function(x,y,w,h){return this.poly([[x,y],[x+w,y],[x+w,y+h],[x,y+h]]);},
  circ:function(x,y,d){o.push('0','CIRCLE','8','CUT','10',fx(x),'20',fx(y),'30','0','40',fx(d/2));return this;},
  bytes:function(){return enc.encode(['0','SECTION','2','HEADER','9','$ACADVER','1','AC1009','9','$INSUNITS','70','4','0','ENDSEC','0','SECTION','2','ENTITIES'].concat(o,['0','ENDSEC','0','EOF']).join('\r\n')+'\r\n');}};}
var Q=-0.41421356; // bulge for a 90 degree arc turning right
function rodHoles(d){[[12,13],[198,13],[12,207],[198,207]].forEach(function(p){d.circ(p[0],p[1],6);});return d;}
function cutFiles(){var F=[];
  F.push({name:'pane-window.dxf',data:rodHoles(DXF().poly([[0,0],[26,0],[26,151],[29,154],[181,154],[184,151],[184,0],[210,0],[210,220],[0,220]],[0,0,Q,0,Q,0,0,0,0,0])).bytes()});
  F.push({name:'pane-solid.dxf',data:rodHoles(DXF().rect(0,0,210,220)).bytes()});
  F.push({name:'spacer-ring.dxf',data:DXF().circ(6,6,12).circ(6,6,5.5).bytes()});
  var t=DXF().rect(0,0,210,200);for(var s=0;s<16;s++){var y=100-(-90+12*s);t.rect(29,y-2,152,4);}
  t.circ(105,152,30);[[12,7],[198,7],[12,193],[198,193]].forEach(function(p){t.circ(p[0],p[1],4.5);});
  [[12,60],[198,60],[12,140],[198,140]].forEach(function(p){t.circ(p[0],p[1],5.5);});t.circ(19,186,6).circ(191,186,6);
  F.push({name:'top-plate.dxf',data:t.bytes()});
  var b=DXF().rect(0,0,186,170);[[9,9],[177,9],[9,161],[177,161]].forEach(function(p){b.circ(p[0],p[1],5.5);});
  b.rect(42-23.25,153-13.75,46.5,27.5);[89,118].forEach(function(x){b.circ(x,153,24).circ(x-9.5,153+12,3.2).circ(x+9.5,153-12,3.2);});
  [140,145,150,155,160,165].forEach(function(c){b.rect(137,c-1.5,30,3);});b.circ(71,80,25).circ(150,42,20);
  F.push({name:'back-plate.dxf',data:b.bytes()});
  F.push({name:'vault-lid.dxf',data:DXF().rect(0,0,148,166).circ(74,119,16).circ(124,140,20).circ(10,156,4.2).bytes()});
  F.push({name:'ORDER-SHEET.txt',data:enc.encode(ORDER)});return F;}
var ORDER=['THE LANTERN: CUT FILES','All files are in millimetres, drawn at true size, cut layer only. Check the scale on import: the pane is 210 x 220 mm.','',
 'CLEAR CAST ACRYLIC, 6 mm (0.236"), cast only, not extruded',
 '  pane-window.dxf   x 8   (7 + 1 spare)   window notch has 3 mm inside corner radii, keep them',
 '  pane-solid.dxf    x 12  (10 + 2 spare)',
 '  spacer-ring.dxf   x 72  (64 + 8 spare)  12 mm OD, 5.5 mm hole',
 '  Leave the protective film on. Anneal after cutting: 80 C for 2 hours, then cool slowly in the oven.','',
 '6061 ALUMINUM, 8 mm (or 5/16" = 7.9 mm)',
 '  top-plate.dxf     x 1   front edge is y = 0',
 '    4 x 5.5 mm holes at y = 60 and 140: countersink 90 deg from the TOP for M5 flat heads',
 '    4 x 4.5 mm holes near the corners: countersink 90 deg from the BOTTOM for M4 flat heads (they hold the pane standoffs)','',
 '5052 ALUMINUM, 2 mm (0.080")',
 '  back-plate.dxf    x 1   drawn as seen from behind (outside face up)',
 '    Before ordering: check the IEC inlet cutout (46.5 x 27.5 mm) and the two Neutrik D-size cutouts (24 mm hole, 3.2 mm holes on a 19 x 24 mm diagonal) against the parts\' own drawings.',
 '    The inlet\'s two screw holes are not in the file: drill them from the part itself.','',
 '5052 ALUMINUM, 3 mm (0.125")',
 '  vault-lid.dxf     x 1   front edge is y = 0','',
 'FINISH: brush all aluminum by hand with a fine non-woven pad, in one direction, after cutting.'].join('\r\n');
var DPMM=150/25.4;
function paneCanvas(i){var W=Math.round(210*DPMM),H=Math.round(220*DPMM),c=document.createElement('canvas');c.width=W;c.height=H;
  var g=c.getContext('2d'),gc=new THREE.Color(S.glass),fc=new THREE.Color(S.film),d=stepD(i),v=Math.pow(.9,d);
  var col='rgba('+Math.round(gc.r*255*v)+','+Math.round(gc.g*255*v)+','+Math.round(gc.b*255*v)+',',ta=(.05+(1-v)*.26).toFixed(3);
  if(S.band==='on'){var bd=20*DPMM,fd=40*DPMM,lg=g.createLinearGradient(0,H,0,H-fd);lg.addColorStop(0,col+'0)');lg.addColorStop(bd/fd,col+'0)');lg.addColorStop(1,col+ta+')');g.fillStyle=lg;g.fillRect(0,H-fd,W,fd);g.fillStyle=col+ta+')';g.fillRect(0,0,W,H-fd);}
  else{g.fillStyle=col+ta+')';g.fillRect(0,0,W,H);}
  if(S.filmOn){var sz=(65+d*15.5)*DPMM,cx=W/2,cy=H-79*DPMM,sig=(5+d*.6)*.82*DPMM;
    g.save();g.shadowColor='rgba('+Math.round(fc.r*255)+','+Math.round(fc.g*255)+','+Math.round(fc.b*255)+','+(.34+d*.03).toFixed(2)+')';g.shadowBlur=sig*2;g.shadowOffsetX=W*3;g.fillStyle='#000';g.fillRect(cx-sz/2-W*3,cy-sz/2,sz,sz);g.restore();}
  if(Math.abs(-9.6+1.2*i)<4.2)g.clearRect(26*DPMM,H-154*DPMM,158*DPMM,154*DPMM);
  return c;}
function withDpi(u){var o=new Uint8Array(u.length+21),ph=new Uint8Array(21),dv=new DataView(ph.buffer),ppm=Math.round(DPMM*1000);
  dv.setUint32(0,9);ph.set(enc.encode('pHYs'),4);dv.setUint32(8,ppm);dv.setUint32(12,ppm);ph[16]=1;dv.setUint32(17,crc(ph.subarray(4,17)));
  o.set(u.subarray(0,33),0);o.set(ph,33);o.set(u.subarray(33),54);return o;}
function toBytes(c){return new Promise(function(res){c.toBlob(function(b){b.arrayBuffer().then(function(a){res(withDpi(new Uint8Array(a)));});},'image/png');});}
function printFiles(){var jobs=[],names=[];
  for(var i=0;i<NP;i++){var n=NP-i,win=Math.abs(-9.6+1.2*i)<4.2;names.push('pane-'+(n<10?'0':'')+n+'-'+(win?'window':'solid')+'.png');jobs.push(toBytes(paneCanvas(i)));}
  return Promise.all(jobs).then(function(datas){var F=datas.map(function(d,k){return{name:names[k],data:d};});
    var txt=['THE LANTERN: PRINT FILES','17 files, one per pane, true size (210 x 220 mm at 150 dpi). Pane 01 is the front pane, 17 the back.',
     'Settings: glass '+S.glass+', film '+(S.filmOn?S.film:'off')+', clear band '+(S.band==='on'?'on':'off')+'.','',
     'Print on the INWARD face of each pane: panes 01-08 on the face toward the back, 10-17 on the face toward the front, 09 on either face.',
     'Color only: no white ink, no gloss or varnish layer. The transparency in each file is the ink density; do not flatten it onto white.',
     'Window panes: the notch area is empty in the file, it is cut away.','Print one test pane first and look at it over the LED strip in a dark room before printing the rest.'].join('\r\n');
    F.push({name:'PRINT-NOTES.txt',data:enc.encode(txt)});return F;});}
function save(blob,name){var a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;document.body.appendChild(a);a.click();setTimeout(function(){URL.revokeObjectURL(a.href);a.remove();},3000);}
var out=document.getElementById('fileOut');
document.getElementById('mkCut').addEventListener('click',function(){save(zip(cutFiles()),'lantern-cut-files.zip');out.textContent='Saved lantern-cut-files.zip: 6 DXF files and the order sheet.';});
document.getElementById('mkPrint').addEventListener('click',function(){out.textContent='Making 17 print files…';printFiles().then(function(F){save(zip(F),'lantern-print-files.zip');out.textContent='Saved lantern-print-files.zip: 17 pane files for glass '+S.glass+(S.filmOn?' and film '+S.film:'')+', plus print notes.';});});
window.LANTERN_FILES={cutFiles:cutFiles,printFiles:printFiles,zip:zip};
})();
