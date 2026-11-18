# House Build: Design

*Date: 2026-11-15 · Status: draft for approval*
*Companion render: https://claude.ai/artifact/9QYBKKpKmL3eyzpPGQm1CJ (see "Differences from the render" at the end)*

## 1. Intent

A gaming and modding PC (heavily modded Skyrim SE + Creation Kit) that lives in the owner's downstairs as a piece of furniture, not as gamer hardware. It's part of a wider redo of that space: walnut, warm lamp light, fluted glass, tactile hardware and one strong accent color. It is the owner's **first PC build**. Learning by doing it is a goal, not a side effect.

There is a separate, parked concept (Build 1, "Aperture", a sculptural concrete/resin/light object). It is **out of scope** here.

**Governing principle (owner's words): "every choice deliberate."** Each element must justify itself by **airflow**, **touch**, or a **named reference**. Anything that can't is removed.

## 2. Goals

1. Hardware target: Ryzen 7 9800X3D, RTX 5080 16 GB, 32 GB DDR5, 2 TB+ NVMe, bought as a **prebuilt on Black Friday (Nov 27, 2026)** for its parts.
2. The owner moves those parts into a chosen case themselves (the learning goal).
3. It reads as walnut furniture with brass hardware that **ages unlacquered**.
4. The PC sits **on the right-hand wing of a fixed-height L desk**, to the owner's right, glass side facing them, "so I can look into it". The fluted side glass is at seated eye level; the toggle and rays are at hand height.
5. Its state and effort are readable at a glance without touching it (see §6.6).
6. It stays calm in a room where people watch TV: soft warm light and no RGB color cycling.

## 3. Non-goals

- Overclocking, custom liquid loops.
- Build 1 / Aperture concrete-and-resin work.
- Any RGB color effect. The only colors of light are warm white and amber.

## 4. Anti-goals (it fails if…)

- It looks like a "gamer PC": rainbow light, visible LED dots, logos.
- Any decorative element hurts cooling or noise noticeably.
- Any element exists only because it looked nice in a render.
- A mains cord or mains device is modified.

## 5. Constraints

- **Budget:** $4,000–6,000 total including monitor, keyboard and mouse. Mods are expected to cost about $500–800 in phase 1 and $200–450 in phase 2 (estimates).
- **Timing:** prebuilt bought Nov 27; build weekend in December; phase 2 in January.
- **Skill:** first build. Fabrication goes to services or a makerspace. Electronics are limited to low-voltage wiring and a small microcontroller.
- **Safety:** mains cords stay stock and certified. All mods are low voltage. Conductive mesh and mirror film stay away from circuit boards and pins.
- **Environment:** a living room with a TV, so it needs to be quiet and low-glare.

## 6. Decisions

### 6.1 Approach (chosen)
**B: buy a prebuilt for its parts and transplant them into a chosen case.**
- *Considered A:* keep the prebuilt's case. Rejected: the case is unknown until it arrives, the front can't be changed, and the owner learns less.
- *Considered C:* full DIY at retail. Rejected: about $450–700 more for the graphics card and memory at 2026 shortage prices, with no design gain.
- **Prebuilt requirements:** a mainstream builder using standard ATX parts, a **modular power supply**, and warranty terms that tolerate a case swap. No proprietary (Dell/HP-style) boards.

### 6.2 Case
**Fractal Design North XL, walnut front, glass side** (~$190–200). Chosen for its walnut-slat front, simple removable glass side, standard layout and power supply at the bottom.
- **Open:** tinted or clear glass variant. Pick it to suit the side treatment in §6.4.

### 6.3 Material rules
| Material | Means | Where |
|---|---|---|
| **Walnut** | furniture | base, front slats, top slats |
| **Brass, unlacquered** | what hand and eye follow; ages with touch | toggle, inlay line, mesh under slats, screws, standoffs |
| **Orange** | carries electricity | wall cord, power box, power cables inside (only power cables) |
| **Light** | reports the PC | the cord shows state, the rays show effort, the interior shows the parts |

No nickel, no chrome, and no orange used decoratively.

### 6.4 Case treatments
- **Front:** the stock walnut slats, with **woven brass mesh** behind them, replacing the stock mesh or laid over it. Open weave, ≥60% open area.
- **Top:** a **walnut slat cap over brass mesh**, matching the front's slat rhythm, raised 10–15 mm on brass standoffs above the stock top so exhaust flows between the slats. *(Replaces the earlier two-tone orange louvers, which broke the orange rule.)*
- **Left side (faces the owner): fully fluted.** One calm reeded surface with a light bronze tint, top to bottom (the owner's choice over a clear/fluted split). From the chair you see glowing forms and the orange power cables as smeared stripes, not hardware. With the inside dimmed, it reads as a bronze reflection of the room.
  - **Phase 1:** reeded film over a light bronze tint film, covering the whole glass.
  - **Phase 2:** a reeded acrylic insert (about 9 mm reeds) covering the whole glass area, mounted on brass standoffs just inside the existing glass. The phase 1 film comes off and the stock glass stays.
  - Because the inside is seen as soft light and shape, **neat cable runs matter less than light placement**. The interior strips are aimed to make the parts read as clear forms through the flutes.
- **Inside:**
  - Bronze mirror vinyl strips on the exposed tray area, kept off circuit boards. Phase 2 adds an angled ridged backer.
  - All component lighting **off**: motherboard LEDs off, memory lighting off.
  - Prebuilt RGB fans replaced with plain dark fans with no LEDs.
- **Interior light:** **dim-to-warm LED strips** (about 2700–3000 K at full, about 1800 K amber when dimmed) **around the inner edges of the case**, as a frame of light: the top edges, the bottom edges on the glass side and front, and the vertical edges at the front and back. About 3–4 m total, roughly 30–40 W at full. Each strip is hidden in a channel aimed across the components.
- **Power cables:** orange. Either **Lian Li Strimer Plus V2** extensions set to steady orange, or unlit orange sleeved extensions. *(Owner preference: open; see §9.)*

### 6.5 Base (walnut, flush)
- **Footprint:** the same as the case, so case and base read as one cabinet. **Height:** about 9 cm. It holds the ray fan (~8 cm), the air chamber and the controller board.
- **Construction:** a **laser-cut walnut-plywood kit** with interlocking edges, glued up by the owner. Cut by Ponoko (confirm walnut stock) or at a local makerspace. Every cut edge comes out dark brown or charred; design around that look.
- **Air:** it feeds only the power supply's bottom intake. That needs about 140 cm² of net opening.
  - **The back** (facing the wall): fully perforated, 6 mm holes on a 9 mm grid.
  - **Both sides:** the same holes, densest at the back and fading to solid wood by mid-depth, like the copper-to-glass brick wall reference.
  - **The front:** solid walnut except for the switch and rays.
  - A fine dust filter sits behind all intake holes.
  - The top of the base has an opening under the case's power supply vent.
- **Brass inlay line with a lit seam:** a flat brass strip, about 1.5 × 6 mm, set flush in a channel made by a slot through the outer ply layer. Directly beneath it, a 1.5 mm laser-cut slot is backlit from inside the base. It reads as a brass line that glows from below. **Its path wraps the base:** from the toggle, around the front-left corner, along the full left side, around the back-left corner, and along the back to the cord exit. There it ends in a **brass ring around the cord grommet**. Corners are mitered or bent. The walnut is sealed before sanding so brass dust doesn't stain it.
- **Cord exit:** on the **back face**, on the line, **directly below the power supply's power inlet**. The exact position is set once the prebuilt's power supply is known. The cord runs down behind the desk to the power box.
- **Cable path:** the switch and lighting wires run from the base into the case through the power supply vent area or a small grommet.

### 6.6 Touchpoints and indicators
- **Toggle:** a **raw-brass latching bat toggle**, e.g. Del City's all-brass SPST, on the front of the base at the front-left (nearest the owner's right hand and the glass side).
  - It does **not** connect directly to the motherboard. The controller reads it and sends a ~0.2 s pulse to the motherboard's power-switch header through an **optocoupler**.
  - **Up** = on. **Down** = sleep or shut down, following the Windows power-button setting.
  - If the PC turns itself off, the controller notices, so the next flip works normally.
- **Ray indicator:** 12 rays fanned around the toggle. Each ray = **50 W** of system power draw (12 × 50 = 600 W, just above the realistic peak).
  - Made as a **dead-front**: microscopic holes (about 0.3 mm) laser-drilled in thin walnut veneer over a light-diffusing backer, with 12 warm LEDs behind. Invisible when unlit.
  - It eases between values over about 2 s, with no flicker.
  - Built as a drop-in module in a pocket the base reserves from day one.
- **State light: the lit seam under the brass line** (on: faint steady glow; asleep: slow breathing, about a 6 s cycle and ~5% peak; off: dark). The seam runs along the left side facing the owner, so the state is visible from the chair.
- **Lit cord:** a translucent orange sleeve over a stock cord, with a side-glow fiber inside, lit from inside the base at the cord exit. It follows the seam's state. It runs behind the desk, so it's seen mostly from the room, not the chair. The desk is fixed, so the fiber is laid once and never flexes.
  - **On:** faint steady glow. **Asleep:** slow breathing (about 6 s cycle, ~5% peak). **Off:** dark.
  - The interior light follows the same states: on at the set brightness, asleep breathing in amber, off.
- **Controller:** one small microcontroller board in the base.
  - It runs the toggle logic, the ray LEDs, the lit seam, the cord light and the interior-light dimming (through a transistor switch for the 12 V strip).
  - **It needs power while the PC sleeps:** a USB-C charger plugged into the power box powers it, not the PC.
  - The power-draw number comes from a small program on the PC that reads the CPU and graphics card power sensors and sends it over USB.

### 6.7 Power
- **Power box:** Conway Electric Extō, **Pumpkin Orange**, about $70. Orange body, cotton-covered black/orange cord, UL listed, 12 ft, 1560 W rating. Ships in 2–3 weeks.
- **Surge protector:** hidden between wall and box. The Extō has no surge protection.
- **Box to PC:** a short orange C13 cord (no cloth-covered C13 cord was found; plastic orange it is), with the lit sleeve over it per §6.6.

## 7. Phasing

| Phase 1: December build weekend | Phase 2: January |
|---|---|
| Transplant parts into the North XL | Dead-front ray module |
| Brass mesh front; slat cap over brass mesh on top | Real reeded acrylic panel |
| Reeded + bronze film over the whole side glass | Angled mirror backer |
| Plain dark fans; all component LEDs off | Code polish: smoothing, sleep breathing |
| Dim-to-warm interior strip + dimmer | |
| Orange power-cable extensions; mirror strips | |
| Laser-cut base with brass inlay, holes, filter, and an empty pocket for the ray module | |
| Brass toggle + controller + optocoupler (toggle logic only) | |
| Lit seam + lit cord (steady on/off) | |
| Power box, surge protector, cords | |

## 7a. Who does what (my call, from the conversation)
- **Owner:** the parts transplant, film and mesh, base glue-up and inlay, and the low-voltage wiring, following a step-by-step guide. Use pre-soldered or screw-terminal boards and plug-in connectors where possible, so soldering is optional.
- **Claude:** the controller firmware, the PC-side power-reading program, the wiring diagram, the laser cut files, and the prebuilt shortlist.

## 7b. Monitor and peripherals
In scope and inside the total budget. Monitor: 27" 1440p high refresh (an OLED like the ASUS PG27AQDP, ~$799, or a cheaper QD-OLED ~$485). Keyboard and mouse are needed. Their look gets decided separately; the material rules are a guide, not a requirement. Reserve about $1,100–1,300. With a prebuilt at about $3,000–3,350 (Nov 2026 deals), that leaves the mod budget in §5 intact.

## 8. Left to the builder
- The exact prebuilt from a shortlist meeting §6.1.
- Fan and mesh specifics within the open-area rule.
- The controller board model, LED parts and wiring details.
- The laser file layout, joinery and kerf compensation, once the case is in hand and measured.
- The slat count and spacing on the top cap: match the front's rhythm.
- Clearance: keep the back of the base at least 10 cm from any wall so the back intake breathes.

## 9. Open with the owner
1. **How strict "no logos" is.** It affects which prebuilt or graphics card qualifies. *Default: a soft preference; favor plain cards when the price is close.*
2. **Orange power cables lit (Strimer) or unlit.** *Default: unlit, since light should only report the PC.*
3. **Tinted or clear glass** North XL variant. *Default: clear, so the bronze film alone sets the tint.*

## 10. Desk requirements (the desk is a separate purchase)
- Fixed height, L-shaped, PC on the right-hand wing near the corner. The owner dislikes industrial standing-desk frames.
- At least 60–65 cm deep where the PC sits; carries 20–25 kg.
- Base back at least 10 cm from the wall.
- A path for the lit cord from the desk edge down to the outlet that avoids the walkway at the room entrance.

## Differences from the render
The render predates several decisions:
- It shows orange two-tone louvers. Now: walnut slats over brass.
- It shows a nickel switch. Now: brass latching toggle.
- Its interior light is warm amber only. Now: dim-to-warm.

## 11. Revisions after the close-up renders (Nov 15, later)
These override earlier sections where they conflict.
- **Light color is gold, not orange.** All indicator and accent light is gold: the rays, the seam under the brass line, the fan and pump rings (if used). Interior strips are dim-to-warm, about 2200 K gold to 2800 K soft white.
- **Motherboard: Gigabyte X870E AERO X3D Dark Wood (in).** From the product photo, its wood is two vertical strips along the board's rear edge. It also has a brushed champagne-to-bronze VRM heatsink and copper accent dots. Under path B it replaces the prebuilt's board during the transplant, which adds a retail Windows license (~$139). Price ~$450–540.
- **Gold accents (in), kept to two or three, brushed or matte over mirror gold:**
  - Cooler Master MasterLiquid Atmos II Pro Gold: gold mesh pump cover, no lighting (~$199.99). It needs to fit the case's top radiator mount; check before buying.
  - PrimoChill gold aluminum graphics card support bracket.
  - Optional: G.Skill Trident Z5 Royal **Neo** gold memory (the AMD version).
- **Scored mirror strips: gold/amber mirror film** instead of bronze.
- **Power cables inside: amber** (default; orange, cream and black were compared in the close-up). Orange now marks power only outside the case: the cord and the Extō.
- **Still open:**
  - Graphics card: Aorus RTX 5080 Infinity Wood (~$1,873–1,900) or ASUS ROG Astral RTX 5080 Dhahab CORE gold (~$1,899). Wanting either card makes full DIY (path C) about as cheap as path B.
  - Memory: 2×16 GB, 4×8 GB, 2×32 GB or 4×16 GB, in dark or gold.
- Close-up render: https://claude.ai/artifact/EfDpe1dekWnbuGb4foMizL
