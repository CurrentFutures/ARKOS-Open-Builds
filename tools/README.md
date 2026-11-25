# Tools

The scripts that make everything in `builds/`. Run them from this folder. They need Python 3 with Pillow; the PDF, reel and teaser scripts also need Node with Playwright (Chromium) and ffmpeg.

Everything runs offline: three.js 0.147 is in `vendor/`, and each page has it inlined.

## The Lantern

```bash
cp lantern-unit.before-tool.html lantern-unit.html
python3 patch_model.py
python3 guide/build_tool.py
python3 guide/build_guide.py
node make-pdf.js lantern-build-guide.html lantern-build-guide.pdf
```

- `lantern-unit.before-tool.html` is the model.
- `patch_model.py` applies the final geometry to it.
- `guide/build_tool.py` adds the cut-file and print-file exports (`guide/export.js`). It writes `lantern-tool.html`, the copy in `builds/the-lantern/`.
- `guide/build_guide.py` draws the diagrams (`guide/diagrams.py`) and writes the build guide from the parts list (`guide/lantern_data.py`) and the renders in `shots/`.

## The Sand Table

```bash
python3 sandguide/patch_sand.py
python3 sandguide/build_sand_guide.py
python3 sandguide/build_desk.py
python3 sandguide/test_meter.py
node make-pdf.js sand-build-guide.html sand-build-guide.pdf
```

- `patch_sand.py` adds the cut-file and software exports (`sandguide/sand-export.js`) to the model. It writes `sand-tool.html`, the copy in `builds/the-sand-table/`.
- `build_sand_guide.py` and `build_desk.py` write the build guide and the desk test. The desk test goes straight into `builds/the-sand-table/`.
- `test_meter.py` checks the meter in `builds/the-sand-table/software/` against a fake model server.

## The Lantern, glass block version

```bash
python3 lantern/build_glass_block.py
node make-pdf.js ../builds/the-lantern/the-lantern-glass-block-version.html ../builds/the-lantern/the-lantern-glass-block-version.pdf
```

The script draws the plan and section to scale and writes the guide straight into `builds/the-lantern/`.

## Reel and teaser

These need the Lantern and Sand Table steps above to have run first. They render on the CPU, which is slow: about 2 to 5 seconds per frame at 1080p.

```bash
python3 reel/prep.py
node reel/capture.js lantern
python3 teaser/prep.py
node teaser/teaser.js render
```

- `reel/prep.py` makes capture copies of the Float, Lantern and Sand Table models.
- `reel/capture.js <build>` renders the stills, clips and `.glb` files. `reel/tiles.js` and `reel/tiles-lab.js` capture the Tiles page.
- `teaser/teaser.js` renders the teaser shots as frame sequences. `teaser/compose.py` cuts them into the teaser with titles.

The videos and 3D files these scripts make aren't in the repository. Run the scripts to make them; they may be published on the Releases page later.
