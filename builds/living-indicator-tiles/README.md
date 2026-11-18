# Living Indicator Tiles

A thin layer of algae, warmed by a habitat's thermal loop and lit from behind. The tiles light a corridor and report on the loop at the same time: how much light gets through shows how much is growing, and the colour shows how it's doing.

**Status:** Concept study. The colours are modelled, not measured.
**Principles applied:**
- Legibility by anyone: a person reads the colour against a printed reference band; an agent reads the same light with a simple sensor.
- Honesty: a living culture can't be quietly reconfigured, so it keeps a record nobody owns.

## Files

- [render/index.html](render/index.html): interactive tile study. Move the loop temperature and days since harvest to see where a tile settles.
- [concept-board.html](concept-board.html): the first concept board: a corridor render, mood, three directions (wall panels, floor path, lantern modules) and tile anatomy.

Open them in a browser.

## How it reads

- **Fixed backlight:** every tile gets the same light, so differences between tiles come from the loop, not the lamp. Known light in, measured light out.
- **Reference band:** people judge absolute colour badly but compare colours well, so each tile carries a printed healthy colour under the same light.
- **For agents:** transmission at 620 nm (phycocyanin) and 680 nm (chlorophyll).
- **When readings disagree:** if the thermal readings say the loop is fine but the tiles have gone yellow, the disagreement is itself the alarm.

## Desk test

See the grow-tile desk test in the [Living Light Wall spec](../living-light-wall/SPEC.md#desk-tests): two cultures at about 32 °C and 38 °C, photographed daily beside a reference band.

## Honest limits

- Colours are illustrative, modelled from how algal pigments absorb light. Real tiles need calibrating for species, layer thickness and backlight.
- Assumes a spirulina-like culture with an optimum around 30–35 °C.
- Tiles react over days, not seconds.

## Related

The [Living Light Wall](../living-light-wall/) grew out of this study and adds flow tiles, harvesting and food.
