import re,sys
p='lantern-unit.html'; s=open(p).read()
def R(a,b,n=1):
    global s
    c=s.count(a)
    if c!=n: sys.exit(f'count {c} for: {a[:80]}')
    s=s.replace(a,b)
# 1. centre the pane stack (it sat 6 mm forward)
R("var z=-HALF+.7+i*1.2,zc=z+.3","var z=-HALF+.1+i*1.2,zc=z+.3")
R("zc=-9+1.2*i,win=Math.abs(zc)<4.2","zc=-9.6+1.2*i,win=Math.abs(zc)<4.2")
R("[[-9.3,-8.8],[9.3,-8.8],[-9.3,8.8],[9.3,8.8]]","[[-9.3,-9.3],[9.3,-9.3],[-9.3,9.3],[9.3,9.3]]")
# top plate slots exactly under the 16 gaps, and the grommet where the cables really drop
R("for(var s=0;s<NP-1;s++){var zz=(s+1)*(512/NP);sg.fillRect(70,zz-5,372,10);}",
  "for(var s=0;s<NP-1;s++){var zz=(1+1.2*s)/BD*512;sg.fillRect(58,zz-5,396,10);}")
R("sg.arc(256,330,16,0,7)","sg.arc(256,(HALF-5.2)/BD*512,36,0,7)")
# 2. closed back: plate 186 x 170, rebated flush, no cable channel (ports moved up into the air space)
R("var CHs=BTOP-PLH,HWs=BW-4.6,HHs=CHs-1.6-1.2,yc=PLH+1.6+HHs/2","var CHs=BTOP-PLH,HWs=BW-2.4,HHs=CHs-.2,yc=PLH+.2+HHs/2")
R("""  slab(ox0,ox1,oy1,BTOP,zb,ze,concM,.12);                                       // above the plate
  slab(ox0,cx0,PLH,oy0,zb,ze,concM,.12);slab(cx1,ox1,PLH,oy0,zb,ze,concM,.12);  // below the plate, either side of the channel
  slab(cx0,cx1,PLH,oy0,ze-.3,ze,concM);                                         // back of the cable channel (0.9 cm deep)
""","""  oy1=BTOP;
""")
# 3. hatch
R("var HW=BW-4.6,HH=CH-1.6-1.2;\nvar hp=box(HW,HH,.4,0,PLH+1.6+HH/2,-HALF+.25,","var HW=BW-2.4,HH=CH-.2;\nvar hp=box(HW,HH,.2,0,PLH+.2+HH/2,-HALF+.2,")
R("for(var l=0;l<7;l++)lg.fillRect(40,22+l*13,432,6);","for(var l=0;l<4;l++)lg.fillRect(377,30+l*18,83,9);")
R("var portY=PLH+3.9;","var portY=PLH+.2+15.3;")
R("cyl(1.25,.03,-5,PLH+8.2,","cyl(1.25,.03,2.2,PLH+8.2,")
R("box(1.9,.5,.02,-5,PLH+8.2,","box(1.9,.5,.02,2.2,PLH+8.2,")
R("brass,-5,PLH+8.2,-HALF-.05,hatch);","brass,2.2,PLH+8.2,-HALF-.05,hatch);")
R("cyl(.9,.25,-5,PLH+4.4,-HALF-.12,felt,'z',hatch,32);cyl(1.05,.06,-5,PLH+4.4,","cyl(.9,.25,-5.7,PLH+4.2,-HALF-.12,felt,'z',hatch,32);cyl(1.05,.06,-5.7,PLH+4.2,")
R("box(1.8,1.6,.25,-1.2,portY,-HALF-.1,black,hatch);box(1.9,1.0,.25,1.1,portY,-HALF-.1,black,hatch);box(2.6,2.0,.25,3.5,portY,-HALF-.1,black,hatch);",
  "box(2.6,3.1,.25,-2.5,portY,-HALF-.1,black,hatch);box(2.6,3.1,.25,.4,portY,-HALF-.1,black,hatch);box(5.0,3.1,.25,5.1,portY,-HALF-.1,black,hatch);")
R("box(.3,.7,.08,2.9,portY,-HALF-.26,aluDark,hatch);box(.3,.7,.08,3.5,portY+.35,-HALF-.26,aluDark,hatch);box(.3,.7,.08,4.1,portY,-HALF-.26,aluDark,hatch);",
  "box(.3,.7,.08,3.6,portY,-HALF-.26,aluDark,hatch);box(.3,.7,.08,4.2,portY+.35,-HALF-.26,aluDark,hatch);box(.3,.7,.08,4.8,portY,-HALF-.26,aluDark,hatch);box(1.2,1.6,.08,6.4,portY,-HALF-.26,new THREE.MeshStandardMaterial({color:0x2a1a1a,roughness:.5}),hatch);")
R("box(1.4,1.7,1.1,-1.2,portY-.45,","box(1.4,1.7,1.1,-2.5,portY-.45,")
R("box(1.6,1.5,1.0,1.1,portY-.5,-HALF-.7,plugM,hatch);box(2.2,2.0,1.3,3.5,portY-.55,","box(1.6,1.5,1.0,.4,portY-.5,-HALF-.7,plugM,hatch);box(2.2,2.0,1.3,3.6,portY-.55,")
R("[[-HW/2+1,PLH+2.6],[HW/2-1,PLH+2.6],[-HW/2+1,PLH+1.6+HH-1],[HW/2-1,PLH+1.6+HH-1]]","[[-HW/2+.9,PLH+1.1],[HW/2-.9,PLH+1.1],[-HW/2+.9,BTOP-.9],[HW/2-.9,BTOP-.9]]")
R("var c=new THREE.CatmullRomCurve3([[x,portY-1.4,zOut],[x,PLH+1.0,-HALF+.1],[x,PLH-.35,-HALF+.42],[x,r+.02,-HALF-1.2]",
  "var c=new THREE.CatmullRomCurve3([[x,portY-1.4,zOut],[x,portY-3.5,-HALF-.75],[x,PLH+1.2,-HALF-.6],[x,r+.02,-HALF-1.4]")
R("var cord=cable(3.5,.32,-HALF-.85,cordM,16);\ncable(1.1,.27,-HALF-.7,black,2);\ncable(-1.2,.24,","var cord=cable(3.6,.32,-HALF-.85,cordM,16);\ncable(.4,.27,-HALF-.7,black,2);\ncable(-2.5,.24,")
# 4. open shell: thick walls, ledge for the lid, 15 mm floor
R("rbox(BW,CH,3,.35,0,cy,HALF-1.5,concM,shell);                 // front wall","rbox(BW,CH,3.2,.35,0,cy,HALF-1.6,concM,shell);               // front wall, 32 mm")
R("rbox(2.2,CH,BD,.35,-BW/2+1.1,cy,0,concM,shell);              // left wall\nrbox(2.2,CH,BD,.35,BW/2-1.1,cy,0,concM,shell);               // right wall",
  "[-1,1].forEach(function(sd){rbox(3.7,13.1,BD,.35,sd*(BW/2-1.85),PLH+6.55,0,concM,shell);rbox(3.0,CH-13.1,BD,.35,sd*(BW/2-1.5),PLH+13.1+(CH-13.1)/2,0,concM,shell);}); // walls: 37 mm round the vault, 30 mm round the air space (the step is the lid ledge)")
R("rbox(BW,2,BD,.35,0,PLH+1,0,concM,shell);                     // floor","rbox(BW,1.5,BD,.35,0,PLH+.75,0,concM,shell);                 // floor, 15 mm")
R("rbox(BW,1.6,1.6,.3,0,PLH+.8,-HALF+.8,concM,shell);rbox(2.2,CH,1.6,.3,-BW/2+1.1,cy,-HALF+.8,concM,shell);rbox(2.2,CH,1.6,.3,BW/2-1.1,cy,-HALF+.8,concM,shell);","")
# inside
R("var vaultLid=box(BW-4.4,.5,BD-4,0,BTOP-3.6,-.4,alu,inside);","var vaultLid=box(14.8,.3,16.6,0,PLH+13.1+.35,-1.6,alu,inside);")
R("var feltLine=box(BW-4.6,BTOP-3.9-(PLH+2),BD-3.8,0,(PLH+2+BTOP-3.9)/2,-.6,","var feltLine=box(13.0,11.4,16.2,0,PLH+1.5+5.8,-1.6,")
R("var psu=box(13,1.5,4,0,BTOP-.75,-5.2,aluDark,inside);","var psu=box(12.9,3.0,9.7,0,BTOP-1.5,1.95,aluDark,inside);")
R("box(5,.16,3.2,5.5,BTOP-.3,3.5,","box(4.4,.16,3.6,-4.9,BTOP-.3,-5.6,")
R("box(1.2,.5,1,5.5,BTOP-.6,3.5,black,inside);","box(1.2,.5,1,-4.9,BTOP-.6,-5.6,black,inside);")
R("[[-5.6,-5.2],[5.6,-5.2]].forEach(function(p){box(.8,.2,4.6,p[0],BTOP-.1,p[1],alu,inside);});","")
# sled: 120 wide, on runners, clear of the front wall
R("function rail(x){box(.5,.5,15.4,x,PLH+2.3,-.6,alu,sled);box(.5,.5,15.4,x,BTOP-4.4,-.6,alu,sled);box(.5,BTOP-4.4-(PLH+2.3),.5,x,(PLH+2.3+BTOP-4.4)/2,7,alu,sled);box(.5,BTOP-4.4-(PLH+2.3),.5,x,(PLH+2.3+BTOP-4.4)/2,-8.2,alu,sled);}\nrail(-6.6);rail(6.6);\nbox(13.7,.5,.5,0,BTOP-4.4,-8.2,alu,sled);box(13.7,.5,.5,0,PLH+2.3,-8.2,alu,sled);\nbox(13.7,BTOP-4.4-(PLH+2.3)+.5,.3,0,(PLH+2.3+BTOP-4.4)/2,-8.4,",
  "var SB=PLH+2.0,ST=PLH+12.8;\nfunction rail(x){box(.5,.5,15,x,SB,-1.6,alu,sled);box(.5,.5,15,x,ST,-1.6,alu,sled);box(.5,ST-SB,.5,x,(SB+ST)/2,5.7,alu,sled);box(.5,ST-SB,.5,x,(SB+ST)/2,-8.9,alu,sled);}\nrail(-5.75);rail(5.75);\nbox(11.5,.5,.5,0,ST,-8.9,alu,sled);box(11.5,.5,.5,0,SB,-8.9,alu,sled);\n[-5.75,5.75].forEach(function(x){box(1.0,.25,15,x,SB-.37,-1.6,new THREE.MeshStandardMaterial({color:0xe8e6e0,roughness:.7}),sled);}); // UHMW runners\nbox(11.5,ST-SB+.5,.3,0,(SB+ST)/2,-9.1,")
R("cyl(.22,5,0,(PLH+2.3+BTOP-4.4)/2,-9.1,brass,'x',sled);box(.3,.3,.7,-2.3,(PLH+2.3+BTOP-4.4)/2,-8.75,brass,sled);box(.3,.3,.7,2.3,(PLH+2.3+BTOP-4.4)/2,-8.75,brass,sled);",
  "cyl(.2,4,0,SB+1.2,-9.55,brass,'x',sled);box(.3,.3,.4,-1.8,SB+1.2,-9.35,brass,sled);box(.3,.3,.4,1.8,SB+1.2,-9.35,brass,sled);")
R("[-2.2,2.2].forEach(function(x){var yc=(PLH+2.3+BTOP-4.4)/2;\n  box(2.6,10.2,14.7,x,yc,-.6,","[-2.2,2.2].forEach(function(x){var yc=(SB+ST)/2;\n  box(2.6,10.2,14.7,x,yc,-1.5,")
R("[[-6.6,yc+4.6,-7],[-6.6,yc+4.6,5.8],[-6.6,yc-4.6,-7],[-6.6,yc-4.6,5.8]].forEach(function(p){var dx=(x<0?-6.4:6.4)-x;",
  "[[0,yc+4.6,-8],[0,yc+4.6,4.8],[0,yc-4.6,-8],[0,yc-4.6,4.8]].forEach(function(p){var dx=(x<0?-5.5:5.5)-x;")
# 5. knob -> flush momentary button (works with stock WLED firmware)
R("var knob=cyl(1.15,1.3,BW/2-3.6,BTOP-3.6,HALF+.65,[knurlM,brass,brass],'z',U,48);",
  "var knob=cyl(1.25,.12,BW/2-3.6,BTOP-2.6,HALF+.06,brass,'z',U,48);cyl(.85,.22,BW/2-3.6,BTOP-2.6,HALF+.12,brass,'z',U,48);")
s=s.replace("cyl(.18,.05,BW/2-3.6,BTOP-2.8,HALF+1.31,","cyl(.06,.01,BW/2-3.6,BTOP-2.6,HALF+.24,")
s=s.replace("// brass dimmer knob, front, with a knurled edge","// light button, front: a flush 19 mm momentary switch")
open(p,'w').write(s); print('patched')
