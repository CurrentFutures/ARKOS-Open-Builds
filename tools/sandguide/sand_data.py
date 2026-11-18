G = lambda q: 'https://www.google.com/search?q=' + q.replace(' ', '+')
# (part, what to ask for, qty, cost, where, url, link checked)
PARTS = [
('Desk test (do this first)', [
 ('Brass sheet', 'C260 brass, 1 mm, two squares: 30 and 40 cm, each with a 6.5 mm centre hole, edges deburred.', '2', '$50–100', 'search', G('C260 brass sheet 1mm cut to size'), False),
 ('Wave driver', 'A mechanical wave driver with a post (PASCO WA-9855 or similar; schools and physics departments often lend them). The older PASCO SF-9324 is discontinued.', '1', '$0–250', 'PASCO Chladni kit manual (PDF)', 'https://cdn.pasco.com/product_document/Chladni-Plates-Kit-WA-9607-Manual.pdf', True),
 ('Amplifier', 'Small class-D board, 2 × 50 W (TPA3116 type), with a 24 V supply.', '1', '$25–45', 'search', G('TPA3116 amplifier board 24V'), False),
 ('Glass microbeads', 'Round glass beads about 100–200 micrometres (sold as glass-bead blasting media, around #10–#11; check the supplier\'s sieve range). 1 kg. No silica sand: fine silica dust is harmful to breathe.', '1 kg', '$15–30', 'McMaster-Carr blasting media', 'https://www.mcmaster.com/products/blasting-media/', True),
 ('Odds', 'Baking sheet, kitchen scale (0.1 g), ear protection, phone sound-meter app, M6 bolt and washers.', '', '$20–40', 'kitchen / hardware store', '', False),
]),
('The three machines', [
 ('Mac Studio', 'Runs the model and the meter only. Enough memory for the model you choose.', '1', '$2,000–5,000', 'Apple', 'https://www.apple.com/mac-studio/', False),
 ('Agent box', 'Raspberry Pi 5, 8 GB, with its 27 W USB-C supply and a 64 GB microSD (or an NVMe drive).', '1', '$110–160', 'Raspberry Pi', 'https://www.raspberrypi.com/products/raspberry-pi-5/', False),
 ('Agent box case', 'Flirc aluminum case for Pi 5: passive, silent. Check the GPIO header can be reached (reviews disagree); any passive case that leaves it open will do.', '1', '$20–30', 'PiShop', 'https://www.pishop.us/product/flirc-raspberry-pi-5-case/', True),
 ('USB Ethernet adapter', 'USB 3 gigabit Ethernet adapter, for the agent box\'s internet side.', '1', '$15–25', 'search', G('USB 3 gigabit ethernet adapter'), False),
 ('Network switch', 'Small unmanaged switch powered by a 5 V barrel plug. The key switches its power.', '1', '$15–25', 'search', G('5 port gigabit switch 5V DC'), False),
 ('One-way wire', 'USB to 3.3 V TTL serial cable (FTDI TTL-232R-3V3 or similar). You cut its receive wire.', '1', '$15–25', 'search', G('FTDI TTL-232R-3V3'), False),
 ('Model runtime', 'llama.cpp (free), installed with Homebrew.', '', '$0', 'llama.cpp', 'https://github.com/ggml-org/llama.cpp', False),
]),
('Controller and sound (in the tray)', [
 ('Controller', 'Raspberry Pi Pico (the plain one, not the Pico W: no radio), with headers.', '1 (+1 spare)', '$5–8', 'Raspberry Pi', 'https://www.raspberrypi.com/products/raspberry-pi-pico/', False),
 ('DAC', 'PCM5102A I2S DAC board.', '1', '$8–12', 'search', G('PCM5102A I2S DAC board'), False),
 ('Amplifier', 'The desk-test class-D board, with its gain turned down to the level you found.', '1', '(reuse)', '', '', False),
 ('Driver', 'Whatever passed the desk test, short enough to fit under the plate (35 mm).', '1', '$60–250', '', '', False),
 ('Counters', 'Kübler electromechanical totalizers, non-resettable, 24 V DC (W 16 or similar), panel cutout 48 × 24 mm.', '2', '$40–80 each', 'Kübler W 16', 'https://www.kuebler.com/us/products/evaluation/process-devices/product-finder/product-details/W16', True),
 ('Key switch', 'Three-position keyed selector switch, 22 mm, maintained (SEALED, ONLINE, ACT), two contact blocks.', '1', '$20–40', 'search', G('3 position key selector switch 22mm maintained'), False),
 ('Telltales', 'Four 3 mm LEDs (warm white or amber) with resistors, small brass bezels.', '4', '$5–10', 'search', G('3mm LED brass bezel'), False),
 ('MOSFETs and parts', 'Logic-level MOSFETs (IRLZ44N or similar) ×5, 1N4007 diodes ×2, 24→5 V buck module, two small push buttons (SETUP, LIGHTS switch), perfboard, screw terminals.', '', '$15–25', 'search', G('IRLZ44N logic level MOSFET'), False),
 ('Light strips', '24 V warm-white COB strip (2700 K): about 2 m for the gap light round the body top, 0.6 m for the raking light.', '3 m', '$15–30', 'search', G('24V COB LED strip 2700K'), False),
 ('Power', 'Mean Well LRS-75-24 (24 V, fanless) in the Mac compartment; small power strip.', '1', '$25–35', 'search', G('Mean Well LRS-75-24'), False),
 ('Post cable', '8-core cable, 0.5 mm², about 7 mm across, 1 m (up the hollow post).', '1 m', '$5–10', 'search', G('8 core cable 0.5mm2 LiYY'), False),
]),
('Tray and plate', [
 ('Brass plate', 'Cut from the plate file at the size your desk test chose, 1 mm C260, unlacquered.', '1', '$40–120', 'SendCutSend or a local laser shop', 'https://sendcutsend.com', False),
 ('Walnut', 'Solid walnut for the tray: 4 sides 600 × 80 × 18 and a 12 mm floor panel (or walnut-veneered birch ply). A woodworker can make it from the drawings.', '', '$150–700', 'woodworker / lumber yard', '', False),
 ('Glass cover', '4 mm low-iron glass, 576 × 576 mm, edges polished. Felt strip for the rebate.', '1', '$60–120', 'local glass shop', '', False),
 ('Placard (optional)', 'Brass plate 120 × 70 mm, engraved from placard-optional.svg.', '1', '$20–40', 'engraver / laser shop', '', False),
]),
('Body', [
 ('GFRC mix', 'Buddy Rhodes GFRC blended mix with its fibres and polymer; about 25 kg made up.', '2 bags', '$120–180', 'Sculpture Supply', 'https://sculpturesupply.com/products/concrete-gfrc-blended-mix', True),
 ('', '', '', '', 'Technical bulletin (PDF)', 'https://www.smooth-on.com/tb/files/BUDDY_RHODES_GFRC_MIX_TB.pdf', True),
 ('Mold', 'Melamine 16 mm, XPS foam for the core and the vent and hatch blocks, packing tape, silicone, release agent.', '', '$80–120', 'hardware store', '', False),
 ('Inserts', 'M5 and M6 stainless cast-in inserts (posts ×4, vents ×8, hatch ×4, bottom plate ×8).', '24', '$40–70', 'search', G('M5 stainless cast in threaded insert concrete'), False),
 ('Perforated brass', 'Perforated brass sheet, about 1 mm, ~3 mm round holes: two vents and the divider.', '1 sheet', '$60–120', 'search', G('perforated brass sheet 3mm holes'), False),
 ('Hatch and bottom', '1.5 mm brass hatch plate (from the file) with thumbscrews and two Ø25 grommets; 6 mm aluminum or birch-ply bottom plate.', '', '$40–80', 'laser shop / hardware', '', False),
 ('Posts', 'Four brass posts, 22 mm round, 40 mm long, M6 stud at each end; the back-right one with a 12 mm bore. Rubber isolators (sorbothane or similar washers).', '4', '$60–150', 'machine shop', '', False),
 ('Feet and felt', 'Four 15 mm rubber feet under the Mac; 40 mm felt-faced plinth 520 × 520.', '', '$20–40', 'hardware store', '', False),
]),
]
