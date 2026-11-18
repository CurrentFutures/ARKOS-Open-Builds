# ARKOS Open Builds

Open source builds from the ARKOS Lab, the hardware division of Current Futures Group. You're welcome to use them and to send feedback.

ARKOS asks one question: **how do we live and work with technology when it's everywhere?** Each build is an experiment that tries an answer in a physical object.

## The two foundations

**Legibility by anyone.** A system's state should be readable by a person or a machine, without a manual and without trusting the system's own report.

**Dignity in design.** Respect for limited resources, for people and for organic materials. People and agents get equal standing.

[PRINCIPLES.md](PRINCIPLES.md) explains both. They're guidelines, not rules: each build applies at least one, and says which.

## Builds

| Build | What it is | Status |
|---|---|---|
| [Living Light Wall](builds/living-light-wall/) | Wall tiles that grow food from waste heat and show the health of the system that heats them | Concept and desk tests |
| [Living Indicator Tiles](builds/living-indicator-tiles/) | Backlit algae tiles that light a corridor and report on the habitat's thermal loop | Concept study |
| [The Lantern](builds/lantern/) | A silent home media server built as furniture, in glass and concrete | Build book complete |
| [The Sand Table](builds/sand-table/) | An agent's computer whose sand figure shows, from measurement, how settled it was | Designed; desk test next |
| [The Float](builds/the-float/) | A gaming PC as furniture, hovering above a walnut block | Designed, not yet built |

## How to read a build

Every build folder follows the same layout ([template](builds/_template/README.md)):

- `README.md`: what it is, which principles it applies, its status and what's known to be wrong with it
- `SPEC.md`: how it works and how to build it
- `render/`: concept renders, labelled as renders
- Desk tests: the cheapest experiment that could prove the idea wrong

**We label honestly.** A render is a render, a prediction is a prediction, and the spec says when something hasn't been tested.

## Use it, build it, tell us

- Build something from here? Open a [build report](../../issues/new?template=build-report.md). Failures are as useful as successes.
- Found a problem or a better way? Open an issue or a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Designs and docs: CC BY 4.0. Hardware: CERN-OHL-P-2.0. Code: MIT. See [LICENSE.md](LICENSE.md).
