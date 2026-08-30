"""Drawing detections, and a debug view of the pipeline's intermediate stages."""

from __future__ import annotations

import cv2
import numpy as np

from pennair.detector import Detection, ShapeDetector

_RED = (0, 0, 255)
_WHITE = (255, 255, 255)
_FONT = cv2.FONT_HERSHEY_SIMPLEX


def annotate(frame: np.ndarray, dets: list[Detection], show_label: bool = True) -> np.ndarray:
    """Draw outlines, centre markers and labels onto a copy of ``frame``."""
    vis = frame.copy()
    # Line thickness scaled to resolution, so a 1080p frame downscaled for
    # viewing still shows a visible outline.
    t = max(1, round(frame.shape[1] / 640))
    cv2.drawContours(vis, [d.contour for d in dets], -1, _RED, t)

    h, w = frame.shape[:2]
    scale = w / 1400
    font_scale = max(0.55, 0.8 * scale)
    for d in dets:
        cx, cy = d.center
        cv2.drawMarker(vis, (cx, cy), _RED, cv2.MARKER_CROSS, int(26 * scale), t)

        text = f"{d.label} ({cx}, {cy})" if show_label else f"({cx}, {cy})"
        (tw, th), _ = cv2.getTextSize(text, _FONT, font_scale, t)
        # Prefer up-and-right of the centre, but keep the whole label on screen:
        # flip to the left if it would overflow, and clamp vertically.
        ox = cx + int(16 * scale)
        if ox + tw > w - 4:
            ox = max(4, cx - int(16 * scale) - tw)
        oy = min(max(cy - int(14 * scale), th + 4), h - 4)

        # White halo under red text, so it stays readable on any background.
        cv2.putText(vis, text, (ox, oy), _FONT, font_scale, _WHITE, t + 3, cv2.LINE_AA)
        cv2.putText(vis, text, (ox, oy), _FONT, font_scale, _RED, t, cv2.LINE_AA)
    return vis


def _label_tile(img: np.ndarray, text: str) -> np.ndarray:
    tile = img.copy()
    h = max(28, img.shape[0] // 18)
    cv2.rectangle(tile, (0, 0), (img.shape[1], h), (0, 0, 0), -1)
    cv2.putText(tile, text, (10, int(h * 0.72)), _FONT,
                h / 42, _WHITE, max(1, h // 18), cv2.LINE_AA)
    return tile


def stage_panel(frame: np.ndarray, det: ShapeDetector) -> np.ndarray:
    """A 2x3 contact sheet of the pipeline, for understanding and debugging.

    Reads the detector's real intermediates rather than recomputing them, so
    what you see is what the detector actually used.
    """
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    sd, k = det.texture_map(frame)
    seed = det.seed_mask(frame)
    refined = det.mask(frame)
    final = annotate(frame, det.detect(frame))

    # Stretch the std-dev map to full range so it is actually visible, and
    # scale it back up to frame size (it is computed at the working scale).
    sd_vis = cv2.applyColorMap(
        cv2.normalize(sd, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
        cv2.COLORMAP_INFERNO,
    )
    if sd_vis.shape[:2] != (h, w):
        sd_vis = cv2.resize(sd_vis, (w, h), interpolation=cv2.INTER_NEAREST)

    def bgr(x: np.ndarray) -> np.ndarray:
        return x if x.ndim == 3 else cv2.cvtColor(x, cv2.COLOR_GRAY2BGR)

    tiles = [
        _label_tile(frame, "1. input"),
        _label_tile(bgr(gray), "2. grayscale"),
        _label_tile(sd_vis, f"3. local std-dev (k={k}) - dark = flat = shape"),
        _label_tile(bgr(seed), "4. threshold + morphology (seed, inset)"),
        _label_tile(bgr(refined), "5. colour snap (true edges)"),
        _label_tile(final, "6. contours + centers"),
    ]
    return np.vstack([np.hstack(tiles[0:3]), np.hstack(tiles[3:6])])
