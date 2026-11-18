import os
# Drawings for the Sand Table build guide. mm, true proportions unless noted.
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'guide'))
from diagrams import svg, R, L, P, T, C, dh, dv, lead, DEFS

def system():  # not to scale
    b = ''
    def box(x, y, w, h, t, s2='', c='blk'):
        r = R(x, y, w, h, c, 4) + T(x + w/2, y + (h/2 if not s2 else h/2 - 4) + 4, t, 'middle', 'm')
        if s2: r += T(x + w/2, y + h/2 + 12, s2, 'middle', 's')
        return r
    b += box(0, 60, 130, 60, 'Agent box', 'Raspberry Pi 5: the agent')
    b += box(230, 60, 150, 60, 'Mac Studio', 'the model + the meter, only')
    b += box(480, 60, 140, 60, 'Controller', 'Pico, no radio, in the tray')
    b += box(480, 170, 140, 44, 'Plate', 'DAC → amp → driver')
    b += box(0, 170, 130, 44, 'Network switch', 'powered by the key')
    b += box(0, 250, 130, 34, 'Router / internet')
    b += box(230, 170, 150, 44, 'Key', 'SEALED · ONLINE · ACT')
    b += L(130, 90, 230, 90, 'usb') + T(180, 82, 'one Ethernet cable', 'middle', 's') + T(180, 104, 'model requests only', 'middle', 's')
    b += L(380, 90, 480, 90, 'acw') + T(430, 82, 'one-way wire', 'middle', 's') + T(430, 104, 'receive wire cut', 'middle', 's')
    b += L(550, 120, 550, 170, 'dc') + L(65, 120, 65, 170, 'usb') + L(65, 214, 65, 250, 'usb')
    b += L(230, 192, 130, 192, 'sig') + T(180, 186, 'power', 'middle', 's') + L(305, 170, 305, 145, 'sig') + L(305, 145, 100, 145, 'sig') + L(100, 145, 100, 120, 'sig') + T(200, 140, 'ACT contact', 'middle', 's')
    b += T(310, 20, 'The agent can ask the model questions. It can\'t log in to the Mac, reconfigure the model, see the meter or reach the table.', 'middle', 's')
    b += T(310, 34, 'The Mac has no internet in normal use. The controller can\'t receive anything but numbers.', 'middle', 's')
    return svg((-10, 0, 640, 300), b, 'The three machines and how they connect')

def body_plan():  # plan of the body, front at the bottom
    b = R(0, 0, 600, 600, 'conc') + R(15, 15, 570, 570, 'air')
    b += R(-3, 50, 3, 500, 'btn') + R(600, 50, 3, 500, 'btn')
    b += R(286, 40, 6, 520, 'bp') + C(289, 250, 20, 'hole2')
    for (x, z) in ((60, 60), (540, 60), (60, 540), (540, 540)): b += C(x, z, 22, 'win')
    b += C(540, 60, 12, 'hole2')
    b += R(397, 203, 197, 197, 'psu') + T(495, 304, 'Mac Studio', 'middle', 'm') + T(495, 318, 'on four 15 mm feet', 'middle', 's')
    for (x, z) in ((420, 226), (571, 226), (420, 377), (571, 377)): b += C(x, z, 18, 'dot')
    b += R(110, 265, 93, 66, 'ctl') + T(156, 302, 'agent box', 'middle', 's')
    b += R(40, 60, 70, 50, 'inl') + T(75, 89, 'switch', 'middle', 's')
    b += R(330, 50, 180, 40, 'inl') + T(420, 74, 'power strip · 24 V supply', 'middle', 's')
    b += R(150, -4, 300, 19, 'zone') + T(300, -8, 'back hatch 260 × 110 opening', 'middle', 's')
    b += P('M203,298 L289,250 L397,300', 'usb') + T(289, 236, 'the one cable', 'middle', 's')
    b += T(300, 625, 'FRONT', 'middle', 'm') + T(-14, 300, 'air in', 'end', 's') + T(614, 300, 'air out', 'start', 's')
    b += dh(0, 600, -24, '600') + lead(289, 500, 640, 500, 'perforated brass divider in cast grooves') + lead(540, 60, 640, 40, 'hollow post: wire and tray power up')
    b += T(300, 645, 'plan, inside the body · walls 15 · vents 500 × 100 in both side walls', 'middle', 's')
    return svg((-90, -50, 1120, 720), DEFS + b, 'Plan of the body: two compartments, divider, vents and posts')

def section():  # front section, y down from the top of the glass
    H = 310
    def Y(h): return H - h
    b = R(40, Y(40), 520, 40, 'felt') + R(0, Y(190), 600, 150, 'conc') + R(15, Y(170), 570, 130, 'air')
    b += R(0, Y(40) - 2, 600, 4, 'bp')
    b += R(397, Y(40 + 2 + 15 + 95), 197, 95, 'psu') + T(495, Y(100), 'Mac Studio', 'middle', 's')
    b += R(420, Y(57), 12, 15, 'gasket') + R(560, Y(57), 12, 15, 'gasket')
    b += R(286, Y(170), 6, 128, 'bp') + R(110, Y(70), 93, 28, 'ctl') + T(156, Y(52), 'agent box', 'middle', 's')
    b += R(-3, Y(160), 3, 100, 'btn') + R(600, Y(160), 3, 100, 'btn')
    for x in (49, 529): b += R(x, Y(230), 22, 40, 'btn')
    b += R(40, Y(191), 520, 2, 'led')
    b += R(0, Y(240), 600, 10, 'frame') + R(0, Y(305), 18, 65, 'frame') + R(582, Y(305), 18, 65, 'frame')
    b += R(270, Y(270), 60, 30, 'ctl') + T(300, Y(250), 'driver', 'middle', 's')
    b += R(100, Y(276), 400, 2, 'lid') + R(100, Y(279), 400, 3, 'sand')
    b += R(12, Y(310), 576, 4, 'win')
    b += dv(625, Y(190), Y(40), '150') + dv(625, Y(230), Y(190), '40 gap') + dv(625, Y(310), Y(230), '80 tray') + dv(660, Y(310), Y(0), '310')
    b += lead(300, Y(278), 700, Y(285), 'brass plate, 35 above the tray floor; sand on it') + lead(400, Y(308), 700, Y(318), 'glass cover, 4 mm, in a rebate on felt')
    b += lead(60, Y(191), -20, Y(205), 'gap light on the body top', 'end') + lead(60, Y(210), -20, Y(225), 'brass post on a rubber isolator', 'end')
    b += lead(10, Y(110), -20, Y(110), 'vent', 'end') + lead(300, Y(20), -20, Y(20), 'felt plinth 520 × 520 × 40, set back', 'end') + lead(289, Y(150), 700, Y(150), 'divider')
    b += lead(300, Y(39), 700, Y(39), 'bottom plate, 6 mm aluminum or birch ply')
    return svg((-330, -20, 1430, 350), DEFS + b, 'Front section through the body, gap and tray')

def tray():  # tray plan, front at the bottom, plate size noted
    b = R(0, 0, 600, 600, 'frame') + R(18, 18, 564, 564, 'void') + R(9, 9, 582, 582, 'fade')
    b += R(100, 100, 400, 400, 'plate') + C(300, 300, 6.5) + C(300, 300, 60, 'fade')
    b += R(22, 40, 4, 520, 'led')
    b += R(60, 500, 60, 50, 'ctl') + T(90, 528, 'Pico', 'middle', 's') + R(140, 500, 70, 55, 'inl') + T(175, 530, 'DAC + amp', 'middle', 's')
    b += C(540, 540, 12, 'hole2')
    b += dh(0, 600, -14, '600 outside · 564 inside · 18 walls') + dh(100, 500, 90, 'plate: 400 (from the desk test)')
    b += lead(22, 300, -14, 300, 'raking light strip', 'end') + lead(9, 9, -14, 40, 'rebate 582 × 582 × 5 for the glass', 'end')
    b += lead(300, 270, 640, 200, 'driver under the plate centre, M6 stud') + lead(540, 540, 640, 560, 'cable from the hollow post')
    b += lead(500, 480, 640, 440, 'floor: a shallow dish (5 mm) catches sand that leaves the edges')
    b += T(300, 625, 'FRONT EDGE: counters · telltales · key', 'middle', 'm')
    return svg((-330, -40, 1350, 690), DEFS + b, 'Tray plan with the brass plate, driver, light strip and electronics')

def front_edge():  # front face of the tray, 600 x 80
    b = R(0, 0, 600, 70, 'frame')
    for x, t in ((70, 'TASKS'), (155, 'UNSETTLED')): b += R(x - 26, 22, 52, 26, 'blk') + T(x, 39, '0 0 0 0 0', 'middle', 'd') + T(x, 62, t, 'middle', 's')
    for i, t in enumerate(('working', 'tool call', 'web open', 'may act')): x = 330 + i * 34; b += R(x - 8, 30, 16, 6, 'led') + T(x, 52, t, 'middle', 's')
    b += C(500, 35, 26, 'win') + T(500, 62, 'key', 'middle', 's') + T(470, 18, 'SEALED', 'middle', 's') + T(500, 12, 'ONLINE', 'middle', 's') + T(530, 18, 'ACT', 'middle', 's')
    b += dh(0, 600, -10, '600') + T(300, 88, 'counters: DIN 48 × 24 cutouts · telltales: 3 mm LEDs behind small brass bezels · key: 22 mm hole', 'middle', 's')
    return svg((-20, -24, 640, 120), DEFS + b, 'Front edge of the tray: two counters, four telltales and the key')

def wire():  # the one-way cable
    b = R(0, 20, 120, 60, 'blk', 4) + T(60, 46, 'USB-serial', 'middle', 'm') + T(60, 62, '3.3 V cable', 'middle', 's')
    for i, (t, c, keep) in enumerate((('GND (black)', 'dc', True), ('TX (orange)', 'acw', True), ('RX (yellow)', 'usb', False))):
        y = 30 + i * 20; b += L(120, y, 210 if not keep else 360, y, c) + T(130, y - 3, t, 'start', 's')
        if not keep: b += L(205, y - 8, 215, y + 8, 'acw') + L(215, y - 8, 205, y + 8, 'acw') + T(220, y + 3, 'cut, shrink-wrapped, and the end cut off', 'start', 's')
    b += R(360, 20, 120, 60, 'blk', 4) + T(420, 46, 'Pico', 'middle', 'm') + T(420, 62, 'GP1 (RX) · GND', 'middle', 's')
    b += T(240, 100, 'Data can only leave the Mac. Leave GP0 (the Pico\'s TX) unconnected too.', 'middle', 's')
    return svg((-10, 0, 500, 112), b, 'The one-way wire: receive wire cut')

def controller():
    b = R(180, 20, 140, 260, 'blk', 6) + T(250, 40, 'Pico', 'middle', 'm')
    pins = [('GP1 ← one-way wire', 60, 'L'), ('GP20/21/22 → DAC (BCK, LRCK, DIN)', 90, 'R'), ('GP10 → TASKS counter (MOSFET)', 120, 'R'), ('GP11 → UNSETTLED counter (MOSFET)', 140, 'R'),
            ('GP12, GP13 → working, tool telltales', 165, 'R'), ('GP14 → gap light (MOSFET)', 190, 'R'), ('GP15 → raking light (MOSFET)', 210, 'R'), ('GP18 → heartbeat pilot LED', 230, 'R'),
            ('GP16 ← SETUP button', 120, 'L'), ('GP17 ← LIGHTS switch', 145, 'L'), ('VSYS ← 5 V from a 24 → 5 V buck', 200, 'L')]
    for t, y, s in pins:
        if s == 'R': b += L(320, y, 350, y, 'dc') + T(355, y + 3, t, 'start', 's')
        else: b += L(150, y, 180, y, 'dc') + T(145, y + 3, t, 'end', 's')
    b += T(250, 300, 'Counters, lights and amplifier run on 24 V; MOSFETs are logic-level (IRLZ44N or similar) with a flyback diode on each counter coil.', 'middle', 's')
    return svg((-20, 0, 640, 312), b, 'Controller wiring')

def desk():  # desk test, side view
    b = R(0, 150, 300, 8, 'frame') + T(150, 172, 'baking sheet catches the sand', 'middle', 's')
    b += R(110, 90, 80, 60, 'blk', 6) + T(150, 124, 'driver', 'middle', 's') + R(146, 74, 8, 16, 'bp') + R(30, 70, 240, 4, 'plate')
    for x in range(40, 262, 9): b += C(x, 67, 2.5, 'dot')
    b += R(330, 90, 90, 40, 'blk', 4) + T(375, 114, 'amplifier', 'middle', 's') + R(450, 90, 90, 40, 'blk', 4) + T(495, 108, 'laptop:', 'middle', 's') + T(495, 120, 'tone + noise', 'middle', 's')
    b += L(190, 120, 330, 110, 'dc') + L(420, 110, 450, 110, 'dc') + lead(240, 66, 330, 40, 'glass microbeads, a thin even layer') + lead(150, 80, 330, 60, 'plate bolted at its centre')
    return svg((-10, 20, 560, 165), DEFS + b, 'Desk test setup')

def mold():  # body mold, cast upside down
    b = R(-20, -20, 640, 190, 'mold') + R(0, 0, 600, 150, 'conc') + R(15, 20, 570, 130, 'core')
    b += R(0, 25, 15, 100, 'core2') + R(585, 25, 15, 100, 'core2') + C(540, 10, 14, 'insert')
    for x in (60, 540): b += R(x - 3, 0, 6, 14, 'insert')
    b += R(286, 20, 6, 130, 'void')
    b += T(300, 90, 'interior core: XPS, 570 × 570 × 130, taped, 2° draft', 'middle', 's') + T(300, 165, 'open face: the bottom; bottom plate screws on here', 'middle', 's')
    b += T(300, -28, 'MOLD FLOOR = the top of the body', 'middle', 'm') + lead(7, 75, -40, 75, 'vent blocks', 'end') + lead(60, 7, -40, 20, 'post inserts', 'end') + lead(289, 60, 660, 40, 'divider: slots formed by 6 mm strips on the core') + lead(540, 10, 660, 10, 'Ø14 tube for the post cable')
    return svg((-200, -50, 1250, 240), DEFS + b, 'Body mold, cast upside down')

ALL = dict(system=system, body_plan=body_plan, section=section, tray=tray, front_edge=front_edge, wire=wire, controller=controller, desk=desk, mold=mold)
