# The Sand Table

An AI agent's computer in a concrete body, with a tray of sand floating above it on brass posts. When a task ends, the brass plate rings and the sand jumps into a figure: crisp if the agent was sure, blurred if it was guessing. The figure stays until the next task.

**Status:** Build book complete; desk test next.
**Principles applied:**
- Legibility by anyone: the sound and the figure are the same vibration of the same plate, so they can't disagree.
- Honesty: the reading comes from the model's internals, never from the agent's own account of itself.

## Files

- [build-book.html](build-book.html): interactive 3D model, how it works, parts list with rough costs (November 2026), build steps, risks, questions for reviewers, and the desk test. Download it and open it in a browser. The figure in the model is an idealised drawing, not a simulation.

## In short

- A meter program, separate from the agent, reads how spread the model's word choices were (uncertainty), how much it did (effort) and which tools it used.
- The numbers leave over a one-way wire to a controller with no radio. Which figure and pitch mean what is generated per house and never seen by the agent.
- The controller drives the plate at one of its resonances. More uncertainty adds noise to the drive, which smears the figure and makes the tone grainy.

## Desk test

An afternoon and about $150–300: brass plates in two sizes on a wave driver. Find the clean figures, measure the loudness, and add noise at three levels to see whether the blur reads. Full steps are in the build book.

## Honest limits

- The figure can be wrong, because it shows what was measured, and the model can be confidently wrong.
- Loudness is the biggest livability question.
- Whether the blur reads clearly is untested.
- The meter software is custom work.

## Feedback wanted

The build book ends with questions for reviewers. Answer any of them in a [build report](../../../../issues/new?template=build-report.md) or an issue.
