# Living Light Wall: Flow and Grow Tiles (spec draft)

Grow food from waste heat, while monitoring the health of your systems in a way that's beautiful and natural. Flow tiles show whether heat is arriving; grow tiles show whether it's sustaining life, and give back food and oxygen. Nothing on the wall is a screen. Physics and biology do the showing.

## Two tiles, one sentence

Read together, the wall says: the heat is arriving, and it's sustaining life. Or it shows you which part isn't.

| Tile | The question | How it shows it | Honest by |
|---|---|---|---|
| Flow | Is waste heat arriving? | Light ripples through a clear channel of loop water; still light means no flow | Physics |
| Grow | Is it sustaining life? | A backlit spirulina culture beside its healthy reference band | Biology |

Flow tiles change within seconds and grow tiles over a few days, so a mismatch also tells you when. If the flow looks fine but the culture is yellowing, the loop was off recently.

## The flow tile

A clear, sealed channel that the loop water itself runs through, in a winding path behind glass, lit from behind by one point-like LED. The moving water bends the light, so patterns ripple across the tile and onto the floor in front of it.

- **Water flowing:** the light moves. Faster flow moves it faster.
- **Flow stopped:** the light goes still.
- **No sensors, no controller:** the real water draws the pattern.

**Build notes:** a channel a few millimetres deep in glass or acrylic rated for the loop's temperature, drip-free couplings, and a vent to clear trapped air. Sight glasses that show flow in pipes already exist; this is the same honesty in a form you'd want on a wall.

## The grow tile: slow record, and food

A thin, sealed glass panel of living spirulina, warmed by the loop and breathing the room's air. How well it has grown over the last few days shows whether the whole system is sustaining life. It can't tell you exactly what's wrong, only that something is; the flow tiles help narrow it down.

**How it's built**

- **Culture layer:** about 1 to 2 cm thick, so light reaches all of it.
- **Medium:** a standard alkaline spirulina growth medium. Spirulina likes very alkaline water, around 30 to 35 °C, which also discourages many contaminants.
- **Warmth:** a thin plate behind the culture carries loop water, so the culture lives at the loop's temperature.
- **Light:** a fixed backlight on a day and night cycle, the same in every tile, so differences between tiles come from the loop, not the lamp.
- **Mixing:** gentle air bubbling keeps the culture from settling and supplies carbon dioxide.
- **Reference band:** a printed healthy colour along the bottom edge.

**Harvest**

Every few days, drain part of the culture through a food-grade valve, strain it through fine mesh, rinse, and eat it fresh or dry it. Top up with fresh medium. A harvest also thins the tile, so it reads clearly again.

**Honest yield:** at home scale, a tile produces a small amount, more a garnish and a demonstration than a diet. A wall of them is a different story, and that's the long-term vision.

## The shared frame

Both tiles fit the same frame, so a wall can mix them in any arrangement and any tile can be swapped by hand.

- **Module:** about 30 × 30 cm, held in a frame rail with quick-release clips.
- **Services behind each tile:** low-voltage power, drip-free quick couplings to the loop for both tile types.
- **Access from the front:** a tile lifts out without tools. Grow tiles have their harvest valve and refill port on the front edge.
- **Drip safety:** a drip channel at the bottom of the frame, and the electrics kept above the water connections.
- **Arrangement:** for example, flow tiles in a band at eye level, with grow tiles above and below.

## Where the water goes

Three separate systems that never mix, all visible on the wall so anyone can see where the water goes.

| System | Comes from | Goes to | On the wall |
|---|---|---|---|
| Loop water | The building or habitat's thermal loop, or a home server's waste heat | Back to the loop. It only passes heat through a plate behind each tile | Copper supply and return pipes up the left side, with a branch to each row |
| Flow tiles | The loop itself | Back to the loop, after passing through a clear channel in the tile | A loop branch running through each flow tile |
| Culture medium | A fresh-medium reservoir: water plus nutrient salts | Harvest drains through a strainer. The algae become food; the spent medium is partly reused and the rest waters a planter, or goes to greywater or water recovery | Reservoir and refill line on the right, harvest trough along the bottom, strainer, then a line to a planter |
| Air | Room air, carrying people's exhaled CO₂ | Back to the room as oxygen-richer air through a filtered vent | An air line along the top, with a vent above the wall |

In a habitat, that closes the circle: waste heat warms the culture, the crew's CO₂ feeds it, and the culture returns oxygen and food, with the spent medium feeding plants. Nothing is terminal.

## Safety and honest limits

- **Colour isn't proof the food is safe.** Healthy blue-green means "worth testing," not "safe to eat." Some contaminating organisms that produce toxins can look similar. Start from a pure, food-grade starter culture, keep the panel sealed, and check under a microscope or with a toxin test kit before eating. Off colour or off smell: don't eat it.
- **Food-safe contact only.** Glass and food-grade seals wherever the culture touches. Flow tiles carry loop water only, never culture medium.
- **Selling it as food** would bring in food-safety regulation. Keep it personal and experimental until then.
- **Microgravity.** Flow tiles work without gravity, because their channel is full of water with no free surface. Grow tiles rely on bubbles rising, so a space version needs active mixing and gas separation. Test on a parabolic flight before claiming any of it.
- **Care.** Grow tiles need harvesting and refills every few days. They suit occupied homes and habitats, not unattended sites. And at home scale, grow tiles barely change a room's CO₂: they are not an air purifier.
- **Prior art.** Algae façades and spirulina life-support research already exist. What's new here is the combination: a readable record of a loop, and food, in one tile.

## Desk tests

**Flow tile:** run warm water from a small aquarium pump through a clear tube or flat channel, backlit by a small LED, and film the light on a wall. Stop the pump and check that the light goes still.

**Grow tile (about two weeks)**

1. Buy a food-grade spirulina starter kit with its medium.
2. Grow two cultures in flat glass vessels, each on a backlight with the same timer. Keep one at about 32 °C and one at about 38 °C, using aquarium heaters.
3. Photograph both every day at the same time beside a printed reference band.
4. After a week, harvest the healthy one: strain, rinse and weigh. Note the yield.
5. Check a sample under a cheap microscope before tasting.

**Prediction:** the 32 °C culture stays blue-green and dense, while the 38 °C one visibly yellows within days.

**What would prove it wrong:** no visible difference, or a difference too slow or subtle to read without instruments.

Built a version? [Send a build report](../../../../issues/new?template=build-report.md).
