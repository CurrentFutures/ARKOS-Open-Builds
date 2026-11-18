# Dimensioned drawings for the Lantern build guide. Units: mm, true proportions. Each returns an inline <svg>.
def svg(vb,body,label):
    x,y,w,h=vb
    return f'<svg viewBox="{x} {y} {w} {h}" role="img" aria-label="{label}"><title>{label}</title>{body}</svg>'
def R(x,y,w,h,c='part',rx=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" class="{c}"'+(f' rx="{rx}"' if rx else '')+'/>'
def L(x1,y1,x2,y2,c='thin'): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{c}"/>'
def P(d,c='part'): return f'<path d="{d}" class="{c}"/>'
def T(x,y,s,a='middle',c='s'): return f'<text x="{x}" y="{y}" text-anchor="{a}" class="{c}">{s}</text>'
def C(x,y,d,c='hole'): return f'<circle cx="{x}" cy="{y}" r="{d/2}" class="{c}"/>'
def arrow(x1,y1,x2,y2): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="dim" marker-start="url(#ar)" marker-end="url(#ar)"/>'
def dh(x1,x2,y,t): return arrow(x1,y,x2,y)+T((x1+x2)/2,y-3,t,c='d')
def dv(x,y1,y2,t,side=1): return arrow(x,y1,x,y2)+T(x+4*side,(y1+y2)/2+3,t,'start' if side>0 else 'end','d')
def lead(x1,y1,x2,y2,t,a='start'): return L(x1,y1,x2,y2,'ldr')+C(x1,y1,1.6,'dot')+T(x2+(2 if a=='start' else -2),y2+3,t,a)
DEFS='<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,1 L9,5 L0,9 z" class="arh"/></marker></defs>'

def pane():  # front view of a window pane, y down: bottom edge at y=220
    H=220;b=P('M0,0 H210 V220 H184 V69 Q184,66 181,66 H29 Q26,66 26,69 V220 H0 Z')
    b+=R(0,200,26,20,'band')+R(184,200,26,20,'band')+P('M0,180 H26 M184,180 H210','fade')
    for x in (12,198):
        for y in (H-13,H-207): b+=C(x,y,6)
    b+=dh(0,210,-10,'210')+dv(222,0,220,'220')+dh(26,184,58,'158')+dv(36,66,220,'154')
    b+=lead(198,207,232,236,'Ø6 × 4, 12 from the sides, 13 and 207 up')+lead(26,69,-6,100,'R3 inside corners','end')
    b+=lead(200,210,232,250,'20 clear band, fades in by 40')
    b+=T(105,140,'window panes 06–12','middle','m')+T(105,152,'solid panes: same outline, no notch','middle','s')
    return svg((-70,-22,400,284),DEFS+b,'Pane drawing, 210 by 220 millimetres, with the window notch, rod holes and clear band')

def stack():  # side view, front at the right
    b='';x=0
    for i in range(17):
        n=17-i;win=6<=n<=12
        b+=R(x,0,6,220,'pw' if win else 'ps')
        if i<16: b+=R(x+6,4,6,12,'ring')+R(x+6,204,6,12,'ring')
        if n in (1,9,17): b+=T(x+3,236,f'{n:02d}','middle','s')
        x+=12
    for y in (13,207): b+=L(-7,220-y,205,220-y,'rod')+R(-8,220-y-4,6,8,'nut',3)+R(200,220-y-4,6,8,'nut',3)
    b+=dh(0,198,-10,'198 = 17 panes × 6 + 16 gaps × 6')+T(0,252,'back','start','s')+T(198,252,'front','end','s')
    b+=lead(66,10,-20,-30,'clear ring Ø12 / Ø5.5, 6 thick','start')+lead(-5,207,-14,250,'acorn nut on a nylon washer','end')
    b+=T(99,110,'shaded: window panes 06–12','middle','m')
    return svg((-110,-44,330,306),DEFS+b,'Side view of the pane stack on four M5 rods with clear spacer rings')

def topplate():  # plan view, front at the bottom (y=200)
    b=R(0,0,210,200,'plate')
    for s in range(16):
        z=-90+12*s;y=100+z;b+=R(29,y-2,152,4,'slot')
    b+=C(105,48,30,'hole2')
    for x in (19,191): b+=R(x-6,8,12,178,'led')+C(x,14,6)
    for x in (12,198):
        for y in (7,193): b+=C(x,y,4.5)
        for y in (60,140): b+=C(x,y,5.5,'csk')
    b+=R(41,77,123,46,'pc')+T(105,104,'computer, on edge','middle','s')
    b+=dh(0,210,-10,'210')+dv(222,0,200,'200')+T(105,214,'FRONT','middle','m')
    b+=lead(105,33,240,20,'Ø30 grommet, 52 behind center')+lead(181,94,240,60,'16 slots 152 × 4 at 12 pitch, under the gaps')
    b+=lead(191,150,240,100,'LED strip on the plate, x = ±86')+lead(198,140,240,140,'Ø5.5 countersunk from the top: M5 into the base')+lead(198,193,240,180,'Ø4.5 countersunk from below: pane standoffs')
    b+=lead(19,14,-8,30,'strip wires down','end')
    return svg((-80,-22,540,248),DEFS+b,'Top plate plan view with slots, grommet, LED strips and holes')

def backplate():  # seen from behind, y down: plate top at y=0
    H=170;b=R(0,0,186,H,'plate')
    b+=R(0,0,186,34,'zone')+T(4,-4,'air space zone (above the vault lid)','start','s')
    for c in (140,145,150,155,160,165): b+=R(137,H-c-1.5,30,3,'slot')
    for (x,y) in ((9,9),(177,9),(9,161),(177,161)): b+=C(x,H-y,5.5)
    b+=R(42-23.25,H-153-13.75,46.5,27.5,'cut')+T(42,H-153+3,'inlet','middle','s')
    for x,t in ((89,'HDMI'),(118,'RJ45')): b+=C(x,H-153,24,'cut')+C(x-9.5,H-153-12,3.2)+C(x+9.5,H-153+12,3.2)+T(x,H-153+3,t,'middle','s')
    b+=C(71,H-80,25,'win')+C(150,H-42,20,'hole2')
    b+=dh(0,186,-16,'186')+dv(198,0,170,'170')
    b+=lead(71,H-80,-10,60,'Ø25 window: drive label','end')+lead(150,H-42,-10,150,'Ø20 vent plug (low inlet)','end')
    b+=lead(152,H-165,230,10,'6 air slots 30 × 3')+lead(177,H-161,230,30,'Ø5.5 × 4 thumbscrews, 9 in')
    b+=T(93,186,'2 mm aluminum · seen from behind · ports centred 17 below the top','middle','s')
    return svg((-150,-34,500,230),DEFS+b,'Back plate seen from behind: slots, ports, label window, vent plug and screw holes')

def section():  # side section through the middle, front at the right
    b=R(0,-10,200,10,'plate')+R(0,0,200,172,'conc')
    b+=R(0,0,166,41,'air')+R(0,41,166,5,'void')+R(-4,46,170,1,'gasket')+R(0,47,166,1,'lid')+R(0,48,166,109,'vault')
    b+=R(32,1,97,30,'psu')+T(80,20,'power supply 129 × 97 × 30','middle','s')
    b+=R(14,58,150,96,'sled')+T(89,110,'drive sled, slides out the back','middle','s')
    b+=R(-2.5,2,2,168,'bp')+R(10,172,180,10,'felt')
    b+=R(176,10,16,20,'btn')
    for y,t in ((0,'172'),): pass
    b+=dv(212,0,172,'172')+dv(-24,0,41,'41 air space',-1)+dv(-24,48,157,'vault, 109 + 15 floor',-1)
    b+=T(100,198,'section, side view · back at the left · front wall 32 · felt plinth 10','middle','s')
    b+=lead(150,47,240,60,'3 mm aluminum lid on a 7 mm cast ledge, neoprene gasket')+lead(184,20,240,20,'button, 19 mm, in a thin front web')
    b+=lead(-1,120,-30,180,'back plate, 2 mm, in its rebate','end')+lead(100,-5,240,-10,'top plate 8 mm')
    return svg((-175,-22,640,230),DEFS+b,'Side section of the base: air space, lid, vault, sled and back plate')

def front_section():  # front view section, y down from the top face
    b=R(0,0,210,172,'conc')+R(30,0,150,41,'air')+R(37,41,136,116,'vault')+R(30,41,7,1,'ledge')+R(173,41,7,1,'ledge')
    b+=dh(30,180,-6,'150')+dh(37,173,60,'136')+dh(0,210,-16,'210')+dv(222,0,172,'172')
    b+=T(105,24,'air space','middle','m')+T(105,110,'vault','middle','m')+T(105,182,'section, front view · floor 15','middle','s')
    return svg((-20,-30,270,220),DEFS+b,'Front section of the base: air space and vault widths')

def mold():  # cast upside down. y down = up in the mold
    b=R(-16,-16,242,204,'mold')+R(0,0,210,172,'conc')
    b+=R(30,0,150,41,'core')+R(37,41,136,116,'core2')
    b+=T(105,24,'air-space core, XPS 150 × 166 × 41','middle','s')+T(105,100,'vault core, XPS 136 × 166 × 116','middle','s')
    b+=T(105,166,'open face: trowel flat; this becomes the bottom','middle','s')
    for x in (12,198):
        b+=R(x-3,0,6,14,'insert')+L(x,-16,x,0,'bolt')
    b+=dh(0,210,-24,'210 inside')+lead(12,10,-30,60,'M5 insert, bolted through the mold floor','end')
    b+=T(105,-36,'MOLD FLOOR = the top face of the base','middle','m')
    return svg((-150,-50,400,246),DEFS+b,'Mold cross-section, cast upside down, with the two foam cores and inserts')

def airspace():  # plan of the air space, front at the bottom; x mirrored to the model's front view
    b=R(0,0,210,200,'conc')+R(30,0,150,166,'air')
    b+=R(40.5,71,129,97,'psu')+T(105,124,'power supply','middle','s')
    b+=C(105,48,30,'hole2')+T(105,52,'grommet','middle','s')
    b+=R(34,26,44,36,'ctl')+T(56,47,'light ctrl','middle','s')
    b+=R(133,0,46,30,'inl')+T(156,19,'inlet','middle','s')+R(96,0,26,20,'inl')+T(109,13,'HDMI','middle','s')+R(67,0,26,20,'inl')+T(80,13,'RJ45','middle','s')
    b+=R(159,168,30,26,'btn')+T(174,214,'button pocket','middle','s')+T(105,232,'FRONT','middle','m')+T(105,-6,'BACK','middle','m')
    b+=T(105,190,'front wall 32','middle','s')
    return svg((-20,-20,250,260),DEFS+b,'Plan of the air space under the top plate: power supply, controller, inlet and grommet')

def wiring():
    b=''
    def box(x,y,w,h,t,c='blk',s2=None):
        r=R(x,y,w,h,c,3)+T(x+w/2,y+h/2+(0 if s2 else 4),t,'middle','m')
        if s2: r+=T(x+w/2,y+h/2+13,s2,'middle','s')
        return r
    b+=box(0,120,110,46,'Inlet','mains','fuse + switch')+box(170,120,120,46,'12 V supply','mains','LRS-100-12')
    b+=L(110,136,170,136,'acw')+L(110,150,170,150,'acw')+T(140,130,'L','middle','s')+T(140,162,'N','middle','s')
    b+=L(55,120,55,60,'earth')+L(55,60,560,60,'earth')+L(230,60,230,120,'earth')
    for x,t in ((330,'top plate'),(430,'back plate'),(530,'vault lid')): b+=L(x,60,x,40,'earth')+T(x,34,t,'middle','s')
    b+=T(60,52,'earth (green/yellow)','start','s')
    ys=[(90,'Computer power','12 V barrel'),(150,'Drive adapter 1','12 V barrel'),(210,'Drive adapter 2','12 V barrel'),(270,'Light controller','12 V screw terminal')]
    b+=L(290,143,320,143,'dc')+L(320,90+23,320,270+23,'dc')
    for y,t,s2 in ys: b+=L(320,y+23,350,y+23,'dc')+box(350,y,130,46,t,'blk',s2)
    b+=box(540,250,110,30,'LED strips')+box(540,295,110,30,'Window LED')+L(480,293,510,293,'dc')+L(510,265,510,310,'dc')+L(510,265,540,265,'dc')+L(510,310,540,310,'dc')
    b+=box(540,205,110,30,'Button')+L(540,220,500,220,'sig')+L(500,220,500,285,'sig')+L(480,285,500,285,'sig')
    b+=L(480,163,540,140,'usb')+L(480,223,540,150,'usb')+box(540,120,110,46,'Computer USB','blk','to both drives')
    b+=T(160,250,'red: mains (inside the inlet','middle','s')+T(160,264,'and the enclosed supply only)','middle','s')+T(160,282,'black: 12 V · blue: data','middle','s')
    return svg((-10,20,670,320),b,'Wiring diagram: inlet, supply, 12 V loads, earth bonds and data')

def sled():  # view from behind the sled
    b=R(0,0,120,108,'frame')+R(4,4,112,100,'void')+R(57,0,6,108,'frame')
    for x in (23,71):
        b+=R(x,3,26,102,'drive')
        for y in (14,94):
            b+=L(4,y,23,y,'cord') if x==23 else L(97,y,116,y,'cord')
            b+=L(49,y,57,y,'cord') if x==23 else L(63,y,71,y,'cord')
    b+=R(0,108,120,3,'run')+C(36,60,14,'win')
    b+=dh(0,120,-8,'120')+dv(130,0,108,'108')+T(60,126,'two drives on edge, each hung on four loops of 3 mm shock cord; UHMW runners; 150 deep','middle','s')
    b+=lead(36,60,-10,40,'cut-out for the label window','end')+lead(60,50,150,30,'centre rail')
    return svg((-110,-22,300,160),DEFS+b,'Drive sled seen from behind')
ALL=dict(pane=pane,stack=stack,topplate=topplate,backplate=backplate,section=section,front_section=front_section,mold=mold,airspace=airspace,wiring=wiring,sled=sled)
