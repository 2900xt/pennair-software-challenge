# PennAir 2024 Software Challenge — Shape Detection

Detects solid shapes on a textured background, traces their outlines, and marks
their centres. Pure classical computer vision: OpenCV and NumPy, no training,
no model weights, no GPU.

Challenge prompt: [`application.txt`](application.txt).

## Quickstart

```bash
make setup     # create .venv and install (run once)
make demo      # Part 1: detect shapes in the static image
```

`make demo` prints the detections and writes `out/static_detected.png`:

```
PennAir 2024 App Static.png: 960x540  5 shapes  10.2 ms/frame
  1. pentagon       center=  (691, 344)  area=    8795 px^2
  2. quadrilateral  center=  (839, 148)  area=    5608 px^2
  3. triangle       center=  (279, 320)  area=    5604 px^2
  4. circle         center=  (553, 104)  area=    5110 px^2
  5. quadrilateral  center=   (112, 76)  area=    3570 px^2
```

Part 2 is a live viewer — it opens a window and annotates the video as it plays:

```bash
make video       # the dynamic video
make video-hard  # the hard video (Part 3 background)
```

| key | |
|-----|---|
| `space` | pause / resume |
| `n` | step one frame (while paused) |
| `o` | outlines on / off, to compare against the raw frame |
| `m` | show the binary mask the detector is working from |
| `s` | save the current frame to `out/` |
| `q` or `esc` | quit |

The video is genuinely streamed, as the prompt requires: one frame is read,
detected on, drawn and shown before the next is read. There is no buffering, no
lookahead, and deliberately no seek bar. Playback is paced to the source frame
rate; if detection ever fell behind, frames would still all be processed, just
slower — none are dropped.

To record the annotated video instead of only watching it:

```bash
.venv/bin/python -m pennair video "PennAir 2024 App Dynamic.mp4" --save out/dynamic.mp4
```

`--save` writes the clean annotated frames, without the on-screen status panel.
Any video file works, and so does a bare camera index (`... video 0`) for a live
feed.

Other targets:

```bash
make stages    # same, plus a contact sheet showing every pipeline stage
make test      # run the test suite (12 tests)
make help      # list all targets
make clean     # delete generated output
```

To see *how* it works, run `make stages` and open
`out/static_detected_stages.png` — it shows the image at each step of the
pipeline, which is the fastest way to understand or debug the algorithm.

## How it works

**In one sentence: backgrounds look *busy*, shapes look *smooth*.**

The obvious approach is colour — "grass is green, filter out green." That fails
immediately, because the static image has a **bright green trapezoid sitting on
green grass**. Any green filter either keeps the grass or deletes the trapezoid.
And Part 3 supplies a background you have never seen, so colour cannot
generalise anyway.

What *is* true of every case: the shapes are solid, so their interiors are flat,
while grass and asphalt are full of fine detail. So for each pixel we look at a
small window around it and measure how much the brightness varies inside it.
Near-zero variation means we are inside a shape.

The pipeline is two stages, because neither signal alone is enough:

| stage | signal | good at | bad at |
|-------|--------|---------|--------|
| 1 | texture | finding *where* shapes are, on any background | exact edges — the measuring window straddles the boundary, so the result is shrunk by ~half a window |
| 2 | colour | exact, pixel-accurate edges | knowing where to look, and which colour to look for |

Stage 1 localises. Stage 2 then works in a small box around each blob, learns
*that shape's own colour* from the pixels stage 1 found, and grows out to the
true boundary. Because the reference colour is learned per shape per frame,
nothing is hardcoded — which is what keeps this background-agnostic and makes
gradient-filled shapes work with the same code.

Two decisions worth knowing about, both driven by measurement rather than taste:

- **The threshold is `0.5 × median(std-dev)`, not Otsu.** Otsu assumes two
  comparably sized classes, but shapes are only ~5% of the pixels, so it splits
  the *background* in half and the mask fills with speckle. Across the static
  image and both videos, Otsu labelled 61%, 75% and 98% of some frames "flat";
  the median rule stayed within a 2.3–5.9% band on every one.
- **Stage 1's shrunken mask is *not* fixed by dilating it.** Dilating by a disk
  restores the right area while rounding every convex corner off — it visibly
  truncated the triangle's apex. Stage 2 exists to avoid that.

### Keeping touching shapes apart

Stage 2 grows each shape outward from its own seed, using a colour reference
learned from that seed alone. That part was always right. The bug was what
happened next: every grown region was OR-ed into one binary mask, and
`findContours` cannot tell two shapes from one. Two shapes that ended up a
single pixel apart fused into one non-convex blob, which then failed the
solidity check — so *both* were thrown away.

The fix is to never flatten them. Stage 2 now emits an `int32` label image, one
id per shape, and contours are traced per label inside that shape's own
rectangle. Touching shapes stay two shapes no matter how close they get, and
the binary `mask()` is now only a view for humans.

The gate itself was also too strict at 0.90. A partially occluded shape is
legitimately non-convex — the one underneath has a bite taken out of it.
Unobstructed shapes measure 0.95+, occluded ones tail down to ~0.80, and no
spurious region scores above 0.75, so the gate moved to 0.80.

Together: **2.77 → 4.69 shapes detected per frame** on the dynamic video, with
zero false positives introduced. `tests/test_detector.py` pins this with two
squares placed 40, 1 and 0 pixels apart.

## Layout

```
pennair/
  texture.py     the "busyness" measure (local standard deviation)
  detector.py    ShapeDetector — the two-stage pipeline, frame in / shapes out
  classify.py    names a shape (triangle, circle, …) from its contour
  visualize.py   drawing detections, and the stage contact sheet
  gui.py         the live video viewer (Part 2)
  cli.py         command line entry point
tests/           run with `make test`
out/             generated output (gitignored; regenerate with `make demo`)
```

Library use:

```python
from pennair import ShapeDetector, annotate

det = ShapeDetector()
detections = det.detect(frame)       # -> [Detection(contour, center, area, label)]
vis = annotate(frame, detections)
```

## Status

| Part | | Notes |
|------|---|-------|
| 1 — static image | done | 5/5 shapes, accurate outlines and centres |
| 2 — video stream | done | ~30 fps on 1080p input; all 5 shapes in 75.8% of frames |
| 3 — background agnostic | mostly works | all 5 shapes in 69.4% of hard-video frames; one false positive |
| 4 — 3D position | not started | |
| 5 — ROS 2 | not started | |
| 6 — extras | partial | shape classification; touching/overlapping shapes now separate correctly |

**Video performance.** Measured over the dynamic video: 25–28 ms/frame of
detection, displayed at 29–30 fps against a 30.3 fps source, so the viewer holds
real time against the 33 ms budget — with less headroom than before, because
finding more shapes means more per-shape work. Adding `--save` costs the
encode and drops it to ~28.6 fps. Keeping shapes separately labelled (below)
costs ~3–5 ms/frame over the old merged-bitmap version — paid for by going from
2.77 to 4.69 shapes detected per frame.

**Performance.** 27 ms/frame at 1080p, single-threaded CPU, against a 33 ms
budget for 30 fps. The main cost saver is running stage 1 on a 960-wide copy —
a 39-pixel window at 1080p is the same physical window as 19 pixels at 540p, so
nothing is lost, and that pass went from 22.1 ms to 4.0 ms.

## Known issues

- **One persistent false positive on the hard video**, at (1900, 871): a patch
  of asphalt that is genuinely smooth enough to pass the flatness test. The hard
  video's background is completely static (frame-to-frame difference is
  0.000–0.005), so the same patch triggers on every frame — it accounts for the
  6th detection in a video that only contains 5 shapes.
- **Detection is good but not perfect across the video.** Sampling every 30th
  frame, all five shapes are found in 75.8% of dynamic-video frames (mean 4.69
  detections) and 69.4% of hard-video frames. The residue is shapes that are
  heavily occluded or partly off-frame.
- Detections whose shape runs off the edge of the frame have an unreliable
  centroid and area, and are currently not filtered.
- An occluded shape is classified by its *visible* outline, so a triangle with a
  circle over one corner is reported as a quadrilateral. The outline and centre
  are correct; only the name is wrong.

## Notes

- The challenge videos (`*.mp4`) are gitignored — they are 50 MB and 97 MB.
  The static PNG is committed since the demo and tests need it.
- Submission deliverables (processed image/video) should be copied out of
  `out/` into a committed `results/` directory when they are final.
