# AGENTS.md

Guidance for coding agents working in this repository.

## What this repo is

This is Taha Rawjani's submission for the **PennAir (Penn Aerial Robotics) 2024
software application challenge**. The full challenge prompt is transcribed
verbatim in [`application.txt`](application.txt) — read it before doing anything
substantive, since it defines the scope, the deliverables, and the grading
rubric.

Short version: build a computer-vision pipeline that detects solid shapes on a
grassy background, traces their outlines, and marks their centers. Then extend
it to streamed video, then to arbitrary backgrounds, then to 3D pose using a
given camera intrinsic matrix, then optionally wrap the whole thing in ROS 2.

The submission is graded on accuracy, efficiency (real-time video), robustness
across backgrounds, code quality, and innovation.

## Current state

Parts 1 and 2 are complete and the project is a working Python package. Run
`make help` for the task list; `make setup` then `make demo` reproduces the
Part 1 result, and `make video` opens the Part 2 live viewer. See `README.md`
for the algorithm explanation and known issues.

```
pennair/texture.py     local standard deviation -- the "busyness" measure
pennair/detector.py    ShapeDetector: two-stage texture -> colour pipeline
pennair/classify.py    contour -> shape name
pennair/visualize.py   annotation + stage contact sheet
pennair/gui.py         live video viewer -- streams frames through the detector
pennair/cli.py         `python -m pennair image <path> [--stages]`
                       `python -m pennair video <path|camera> [--save P] [--loop]`
tests/                 12 tests, `make test`
```

Also present: `pyproject.toml` (package + deps), `Makefile` (setup/demo/test),
`.latexmkrc` (LaTeX report config; `main.tex` still does not exist).

The three challenge media files ARE present in the working directory. The two
`.mp4`s are gitignored (50 MB and 97 MB); the static PNG is committed because
the demo and tests need it.

Parts 3-6 are not started. Part 2 needed no detector restructuring:
`ShapeDetector.detect` was already pure and stateless, so `gui.py` is a
read-one-frame / detect / draw / show loop. The detector's public surface is now
`segment` (labels + rects), `detect`, `mask`, and `analyze` (detections + mask
from one pipeline run, which is what the viewer uses so its mask view is free).

The touching-shapes defect is FIXED. The cause was not the solidity gate: stage
2 already grew each shape from its own seed correctly, then OR-ed every region
into one binary mask, so a single pixel of contact fused two shapes into one
non-convex blob that the gate then rejected in pairs. Stage 2 now emits an int32
label image (one id per shape) and contours are traced per label; `mask()` is a
human-facing view only. The gate also moved 0.90 -> 0.80, since a partially
occluded shape is legitimately non-convex. Result: 2.77 -> 4.69 detections per
frame on the dynamic video, no new false positives, ~3-5 ms/frame slower
(~25 ms, still 30.4 fps end to end). Pinned by regression tests with squares
40/1/0 px apart.

Two known defects remain, documented in the README: one static false positive on
the hard video at (1900, 871) -- note it is the 6th detection in a video with
only 5 shapes, so do not treat "6 detections" as success there; and frame-edge
shapes are not filtered.

## Conventions to follow

- **Language:** Python with OpenCV (`cv2`) and NumPy is the expected stack — the
  prompt recommends OpenCV explicitly. Don't introduce a heavier framework
  (PyTorch, a detection model, etc.) unless asked; the challenge rewards a
  clean classical-CV solution.
- **Streaming discipline:** Part 2 explicitly requires processing video *one
  frame at a time*, as a stream. Never load a whole video into memory or do a
  multi-pass algorithm over frames. A per-frame `process(frame) -> detections`
  function that the static-image path also calls is the right shape.
- **Shared core:** Parts 1–4 are the same detector applied to different inputs.
  Factor the detection logic into one module, and keep the image runner, video
  runner, and ROS node as thin wrappers over it.
- **Efficiency matters:** it's a graded criterion. Prefer cheap operations,
  avoid redundant color-space conversions and per-frame reallocations, and note
  optimizations made — the deliverables ask for a written report on exactly this.
- **Comments:** the prompt asks for code that is "well-(enough)-documented" with
  comments explaining key steps and logic. Comment the *why* of CV parameter
  choices (thresholds, kernel sizes, morphology ordering), not the *what*.

## Known task-specific details

- Camera intrinsic matrix for Part 4:
  `K = [[2564.3186869, 0, 0], [0, 2569.70273111, 0], [0, 0, 1]]`
- The circle in the scene has a **radius of 10 inches**; that's the scale
  reference for recovering depth. Assume a flat surface.
- ROS 2 target: Ubuntu 24.04 / ROS 2 Jazzy (Humble and Lyrical also acceptable).
  Part 5 needs three things: a video-publisher node, a detection node, and a
  launch file.

## Deliverables checklist

A complete submission needs, per the prompt:

- [ ] Source code for the algorithm
- [ ] Processed static image (outlines traced, centers marked) + brief writeup
- [ ] Screen recording of the processed video + brief performance report
- [ ] Processed hard/background-agnostic video + writeup on the modifications
- [ ] `README.md` with run instructions, ideally with the videos embedded
- [ ] Public GitHub repo

Note that `README.md` does not exist yet and is a required deliverable.

## Building the report

If/when a LaTeX report is added:

```bash
latexmk main.tex
```

Output lands in `build/main.pdf` (both are gitignored). `.latexmkrc` sets
`-halt-on-error`, so a failed build stops at the first error.

## Things not to do

- Don't commit large media files (input videos, screen recordings) without
  checking with Taha first — they'll bloat the repo. The `.gitignore` currently
  has no media rules.
- Don't invent results. If the input assets aren't present, the algorithm can't
  be validated; report that instead of writing a README that claims it works.
- Don't restructure into a ROS package until Parts 1–3 actually run standalone.
