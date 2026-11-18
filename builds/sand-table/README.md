# The Sand Table

An AI agent's computer in a concrete body, with a tray of sand floating above it on brass posts. When a task ends, the brass plate rings and the sand jumps into a figure: crisp if the agent was settled, smeared if it was unsettled. The figure stays until the next task.

**Status:** Designed; desk test next.
**Principles applied:**
- Legibility by anyone: the sound and the figure are the same vibration of the same plate, so they can't disagree.
- Honesty: the reading comes from the model's internals, never from the agent's own account of itself.

## Files

- [model.html](model.html): **the latest design.** Interactive 3D model with the household's figure, plate size and settled/unsettled readings, plus buttons that make the cut files and the software for all three machines (meter, controller, Mac and agent box).
- [desk-test.html](desk-test.html): the bench test that sets the plate, driver, volume and blur before anything is built.
- [build-book.html](build-book.html): the full build book (principle, parts list, build steps, risks, questions for reviewers). Written before the agent moved onto its own small computer, so where it differs, the model is current.
- [WATER-VERSION.md](WATER-VERSION.md): a variant with water in a glass tray, projecting the pattern onto the ceiling.

Open the HTML files in a browser. The figures are idealised drawings, not simulations.

## How it works now

- **Two compartments.** The agent lives on its own small computer (a Raspberry Pi 5). The Mac Studio holds the model and the meter. One cable crosses between them.
- **The meter is arithmetic.** It reads how spread the model's word choices were, not the agent's account of itself.
- **One wire, one direction.** The numbers go up a hollow brass post to a controller with no radio, which drives the plate at the household's figure.
- **The household's figure** is chosen at setup from the figures its own plate can make. Clarity is the reading everywhere: crisp is settled, smeared is unsettled.
- **Front edge:** a key (sealed, online, act), four telltales, and two counters that only count up: tasks, and unsettled tasks.

## Honest limits

- The figure can be wrong, because it shows what was measured, and the model can be confidently wrong.
- Loudness is the biggest livability question.
- Whether the blur reads clearly is untested.

## Feedback wanted

The build book ends with questions for reviewers. Answer any of them in a [build report](../../../../issues/new?template=build-report.md) or an issue.
