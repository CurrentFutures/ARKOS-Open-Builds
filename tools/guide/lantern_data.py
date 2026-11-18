# One source for the Lantern's parts, used by the model page and the build guide.
# v = True: the link was checked for this guide. v = False: a search or a shop's home page; pick the exact item yourself.
G=lambda q:'https://www.google.com/search?q='+q.replace(' ','+')
PARTS=[
('Computer and storage',[
 ('Mini PC','MINIX NEO Z100-0dB: fanless Intel N100, 123 × 120 × 46 mm, runs on 12–19 V DC. Fits the window with room to spare.','1','$200–280','MINIX product page','https://www.minix.com.hk/products/z100-0db-fanless-n100-mini-pc',True),
 ('Hard drives','WD Red Plus 8 TB, model WD80EFPX: 5640 rpm, CMR. One holds the library, one the nightly copy. (The 12 TB WD120EFGX spins at 7200 rpm even though it reports 5400; too hot and loud for a sealed vault.)','2','$360–440','Western Digital','https://www.westerndigital.com/products/internal-drives/wd-red-plus-sata-3-5-hdd?sku=WD80EFPX',True),
 ('USB to SATA adapters','USB 3 to 3.5" SATA adapter cable with its own 12 V barrel input and UASP. You will test that each one lets the drive sleep and passes SMART (step 2).','2 (+1 spare)','$15–25 each','search','%s'%G('USB 3.0 to SATA adapter 3.5 inch 12V UASP'),False),
 ('Short USB cables','USB-A to the adapter\'s plug, right-angle, 30 cm, if the adapter cable is too long to coil neatly.','2','$10–15','search',G('right angle USB 3.0 cable 30cm'),False),
]),
('Glass',[
 ('Cast acrylic, cut','Clear cast acrylic, 6 mm (0.236"). Window panes ×8, solid panes ×12, spacer rings ×72, from the cut files the model makes. Cast only: extruded crazes.','one order','$250–400','SendCutSend acrylic','https://sendcutsend.com/materials/acrylic',True),
 ('…or a local laser shop','Same files and material. Ask them to anneal after cutting if they can.','','','Multicraft Plastics laser service','https://www.multicraftplastics.com/capabilities/laser-cnc.html',True),
 ('UV printing','Print the 17 pane files on the inward face: color only, no white ink, no varnish. One test pane first.','17 + test','$150–350','search: UV flatbed print shop',G('UV flatbed printing on acrylic near me'),False),
]),
('Metal and hardware',[
 ('Top plate','6061 aluminum, 8 mm (or 5/16" = 7.9 mm), from top-plate.dxf. Countersinks as noted in the order sheet.','1','$60–120','SendCutSend','https://sendcutsend.com',False),
 ('Back plate','5052 aluminum, 2 mm (0.080"), from back-plate.dxf. 2 mm is the thickest panel the HDMI feed-through takes.','1','$20–40','SendCutSend','https://sendcutsend.com',False),
 ('Vault lid','5052 aluminum, 3 mm (0.125"), from vault-lid.dxf.','1','$20–35','SendCutSend','https://sendcutsend.com',False),
 ('Rods','M5 stainless (A2) threaded rod, cut to 4 × 208 mm. The clear spacer rings hide the thread between panes.','1 m','$8–15','McMaster-Carr threaded rod',G('McMaster M5 stainless threaded rod'),False),
 ('Acorn nuts','M5 stainless acorn (cap) nuts.','8','$8–12','McMaster-Carr metric acorn nuts','https://www.mcmaster.com/products/metric-acorn-nuts/',True),
 ('Nylon washers','M5 nylon washers, between each acorn nut and the acrylic.','8','$3','search',G('M5 nylon washer'),False),
 ('Pane standoffs','Stainless round spacers 8 mm OD × 4 mm long for M4, with M4 × 10 stainless countersunk screws from under the plate.','4','$6–10','search',G('M4 stainless spacer 8mm OD 4mm long'),False),
 ('Cast-in inserts','M5 stainless threaded inserts made for casting into concrete (4 for the top plate, 4 for the back plate). Never zinc or aluminum.','8 (+2 spare)','$15–30','search',G('M5 stainless cast in threaded insert concrete'),False),
 ('Screws','M5 × 16 stainless countersunk (top plate). M5 stainless knurled thumbscrews, 10–12 mm thread (back plate).','4 + 4','$15–25','search',G('M5 stainless knurled thumb screw'),False),
 ('Sled','15 × 15 × 1.5 mm aluminum angle (about 1.5 m), 3 mm shock cord, 2 strips of 3 mm UHMW tape or strip for runners, small pull.','','$25–40','hardware store',G('15mm aluminium angle 1.5mm'),False),
 ('Felt and seals','Wool felt 10 mm for the plinth and 3 mm for the vault walls; closed-cell neoprene strip 3 × 10 mm; Ø16 and Ø30 rubber grommets.','','$30–45','search',G('wool felt sheet 3mm 10mm'),False),
 ('Heat pads','Soft silicone thermal gap pad, 3–5 mm, from each drive\'s top edge to the vault lid.','2','$10–20','search',G('soft thermal gap pad 5mm'),False),
 ('Peak-hold labels','Irreversible temperature labels, about 40–60 °C in 5 ° steps (Tempilabel or Thermax).','2 + spares','$15–30','Tempil labels at ToolUp','https://toolup.com/collections/tempil-temperature-indicating-labels',True),
 ('','','','','Thermax','https://spotsee.io/temperature/thermax',True),
 ('Vent plugs','Two short felt-filled plugs: Ø20 in the back plate (low inlet) and the lid (high outlet). Turned from acrylic rod or any Ø20 push-in plug.','2','$5–10','search',G('20mm push in hole plug'),False),
]),
('Concrete base',[
 ('GFRC mix','Buddy Rhodes GFRC blended mix with its fibers and polymer, about 12 kg made up. Follow its technical bulletin.','1 bag','$60–90','Sculpture Supply','https://sculpturesupply.com/products/concrete-gfrc-blended-mix',True),
 ('','','','','Technical bulletin (PDF)','https://www.smooth-on.com/tb/files/BUDDY_RHODES_GFRC_MIX_TB.pdf',True),
 ('Mold','Melamine board 16 mm, 2 mm acrylic or melamine shim for the back rebate, XPS foam for the cores, silicone caulk, release agent.','','$40–60','hardware store','',False),
 ('Sealer','Penetrating concrete sealer (matte).','1','$20–30','hardware store','',False),
]),
('Power, light and controls',[
 ('Power supply','Mean Well LRS-100-12: 12 V, 8.5 A, fanless, 129 × 97 × 30 mm. Runs the computer, drives and lights.','1','$25–35','OMC StepperOnline','https://www.omc-stepperonline.com/lrs-100-12-mean-well-100w-12vdc-8-5a-115-230vac-enclosed-switching-power-supply.html',True),
 ('Power inlet','Qualtek 719W-UEL3BB81: IEC C14 with fuse holder and switch. Panel cutout 46.5 × 27.5 mm. Fuse not included.','1','$10–15','Digi-Key','https://www.digikey.com/en/products/detail/qualtek/719W-UEL3BB81/23019207',True),
 ('Fuse','Slow-blow, the size the inlet takes (5 × 20 mm): T2A for 120 V, T1A for 230 V.','2','$3','search',G('5x20mm slow blow fuse T2A'),False),
 ('HDMI feed-through','Neutrik NAHDMI-W (D-size, panel up to 2 mm).','1','$20–30','Neutrik','https://neutrik.com/product/nahdmi-w',True),
 ('Ethernet feed-through','Neutrik NE8FDP (D-size RJ45).','1','$12–20','search: Neutrik NE8FDP',G('Neutrik NE8FDP'),False),
 ('Light controller','QuinLED An-Penta-Mini: 5-channel analog controller for one RGBCCT strip, runs WLED, 3 button inputs.','1','$35–50','QuinLED','https://quinled.info/quinled-an-penta-mini',True),
 ('LED strip','12 V FCOB 5-in-1 RGBCCT, CRI 90+, 2700–6500 K. 1 m is plenty (2 × 180 mm under the panes, 72 mm in the window).','1 m','$20–40','Super Lighting LED','https://www.superlightingled.com/12v-fcob-5in1-led-rgbw-tunable-white-light-strip-960-super-high-density-p-6906.html',True),
 ('Button','19 mm stainless momentary push button, flat face (anti-vandal style), normally open.','1','$8–15','search',G('19mm stainless momentary push button flat'),False),
 ('Window LED plug','Small 6-pin plug and socket so the window strip unplugs when the glass lifts off.','1','$5','search',G('6 pin JST SM connector pair'),False),
 ('DC pigtails','Barrel plugs to feed 12 V to the computer and the two drive adapters. Match each socket (check the plug on each supplied adapter).','3','$8','search',G('5.5x2.5 DC barrel pigtail'),False),
 ('Wire and earth','18 AWG mains-rated wire, 20 AWG for 12 V, green/yellow earth wire, ring terminals, star washers, lever connectors, heat-shrink.','','$15–25','electrical supply','',False),
 ('Cables out','Fabric-covered IEC C13 cord; right-angle HDMI and Ethernet cables (plugs pointing down).','3','$30–60','search',G('fabric braided IEC C13 cord'),False),
]),
]
