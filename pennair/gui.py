"""Part 2: a live viewer that runs the detector on a video stream.

The video really is treated as a stream, which is what the prompt asks for: one
frame is read, detected on, drawn and shown before the next one is read. Nothing
is buffered, nothing looks ahead, and no seeking is offered -- an aircraft does
not get to rewind. The detector is the *same* ``ShapeDetector`` the static-image
path uses, called with no changes at all; this module is only a window around it.

    python -m pennair video "PennAir 2024 App Dynamic.mp4"

Keys: space pause | n step | o outline on/off | m mask view | s snapshot | q quit
"""

from __future__ import annotations

import time
from pathlib import Path

import cv2
import numpy as np

from pennair.detector import ShapeDetector
from pennair.visualize import annotate

_WHITE = (255, 255, 255)
_GREEN = (120, 255, 120)
_FONT = cv2.FONT_HERSHEY_SIMPLEX

_HELP = "space pause | n step | o outline | m mask | s snapshot | q quit"


def _draw_hud(vis: np.ndarray, lines: list[str]) -> None:
    """Draw a translucent status panel in the top-left corner, in place.

    Viewer chrome only -- it is deliberately *not* part of ``annotate``, so the
    frames written by --save carry the detection overlay and nothing else.
    """
    h, w = vis.shape[:2]
    scale = max(0.45, 0.6 * w / 1400)
    thick = max(1, round(w / 1100))
    pad = int(12 * w / 1400) + 4

    sizes = [cv2.getTextSize(t, _FONT, scale, thick)[0] for t in lines]
    lh = max(s[1] for s in sizes) + int(10 * scale) + 6
    box_w = max(s[0] for s in sizes) + 2 * pad
    box_h = lh * len(lines) + pad

    # Blend rather than fill: the frame stays readable underneath the panel.
    roi = vis[0:min(box_h, h), 0:min(box_w, w)]
    cv2.addWeighted(roi, 0.35, np.zeros_like(roi), 0.65, 0, dst=roi)

    y = pad + sizes[0][1]
    for i, text in enumerate(lines):
        cv2.putText(vis, text, (pad, y), _FONT, scale,
                    _GREEN if i == 0 else _WHITE, thick, cv2.LINE_AA)
        y += lh


def _open(source: str | int) -> cv2.VideoCapture:
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise SystemExit(f"error: could not open video source {source!r}")
    return cap


def run(
    source: str | int,
    detector: ShapeDetector | None = None,
    display_width: int = 1280,
    loop: bool = False,
    save: Path | None = None,
    snapshot_dir: Path = Path("out"),
) -> int:
    """Play ``source`` through the detector in a window. Returns an exit code."""
    det = detector or ShapeDetector()
    cap = _open(source)

    src_fps = cap.get(cv2.CAP_PROP_FPS)
    if not (1.0 < src_fps < 240.0):      # webcams and some containers report 0
        src_fps = 30.0
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fw = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fh = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    title = f"PennAir - {source}"
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    # Show 1080p footage in a sensible window. The detector still runs at full
    # resolution; only the presentation is scaled, by the window manager.
    cv2.resizeWindow(title, display_width, max(1, round(display_width * fh / max(fw, 1))))

    writer = None
    if save is not None:
        save.parent.mkdir(parents=True, exist_ok=True)
        writer = cv2.VideoWriter(str(save), cv2.VideoWriter_fourcc(*"mp4v"),
                                 src_fps, (fw, fh))

    print(f"{source}: {fw}x{fh} @ {src_fps:.1f} fps"
          + (f", {total} frames" if total > 0 else "")
          + f"\n{_HELP}")

    period = 1.0 / src_fps
    next_due = time.perf_counter()
    idx = 0
    paused = False
    step = False
    show_outline = True
    show_mask = False
    detect_ms = 0.0      # exponential moving averages, so the readout is
    play_fps = src_fps   # legible instead of flickering every frame
    last_shown = time.perf_counter()
    frame = vis = None

    try:
        while True:
            if not paused or step:
                ok, frame = cap.read()
                if not ok:
                    if loop and total > 0:
                        cap.release()
                        cap = _open(source)
                        idx = 0
                        continue
                    break
                idx += 1

                t0 = time.perf_counter()
                # analyze returns both, so the mask view costs nothing extra --
                # the pipeline still runs exactly once per frame.
                dets, mask = det.analyze(frame)
                ms = (time.perf_counter() - t0) * 1000
                detect_ms = ms if idx == 1 else 0.9 * detect_ms + 0.1 * ms

                now = time.perf_counter()
                inst = 1.0 / max(now - last_shown, 1e-6)
                play_fps = inst if idx == 1 else 0.9 * play_fps + 0.1 * inst
                last_shown = now

                base = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) if show_mask else frame
                vis = annotate(base, dets) if show_outline else base.copy()
                if writer is not None:
                    # Record the clean annotated frame, without viewer chrome.
                    writer.write(annotate(frame, dets) if show_outline else frame)
                step = False

                counter = f"frame {idx}/{total}" if total > 0 else f"frame {idx}"
                _draw_hud(vis, [
                    f"{counter}    {len(dets)} shapes",
                    f"detect {detect_ms:5.1f} ms    {play_fps:4.1f} fps"
                    + ("    PAUSED" if paused else ""),
                    _HELP,
                ])
                cv2.imshow(title, vis)

            # Pace playback to the source frame rate. If detection is slower
            # than real time the wait floors at 1 ms and we simply run as fast
            # as we can -- frames are never dropped, since the prompt wants
            # every frame processed.
            next_due = max(next_due + period, time.perf_counter())
            wait = 30 if paused else max(1, int((next_due - time.perf_counter()) * 1000))
            key = cv2.waitKey(wait) & 0xFF

            if key in (ord("q"), 27):
                break
            if key == ord(" "):
                paused = not paused
                next_due = time.perf_counter()
            elif key == ord("n") and paused:
                step = True
            elif key == ord("o"):
                show_outline = not show_outline
            elif key == ord("m"):
                show_mask = not show_mask
            elif key == ord("s") and vis is not None:
                snapshot_dir.mkdir(parents=True, exist_ok=True)
                p = snapshot_dir / f"frame_{idx:05d}.png"
                cv2.imwrite(str(p), annotate(frame, dets) if show_outline else frame)
                print(f"wrote {p}")

            # The user closing the window is a quit, same as pressing q.
            if cv2.getWindowProperty(title, cv2.WND_PROP_VISIBLE) < 1:
                break
    except KeyboardInterrupt:
        pass  # Ctrl+C is a normal way to stop a viewer; fall through and tidy up
    finally:
        cap.release()
        if writer is not None:
            writer.release()
            print(f"wrote {save}")
        cv2.destroyAllWindows()

    print(f"stopped after {idx} frames  ({detect_ms:.1f} ms/frame detect, "
          f"{play_fps:.1f} fps displayed)")
    return 0
