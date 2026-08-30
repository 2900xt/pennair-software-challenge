"""The detector itself: frame in, list of shapes out.

Two-stage design
----------------
Texture tells us *where* the shapes are, robustly, but not exactly where their
edges are. Colour then tells us exactly where the edges are, but only because
stage 1 already told us which pixels to learn a colour from. Each stage does
the job the other is bad at::

    stage 1  texture  ->  reliable localisation, boundary shrunk by ~k/2
    stage 2  colour   ->  pixel-accurate boundary, reference learned per shape

No colour is ever hardcoded, which is what keeps this background-agnostic
(Part 3) and tolerant of colour gradients inside a shape.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np

from pennair.classify import classify
from pennair.texture import local_stddev


@dataclass
class Detection:
    """One detected shape."""

    contour: np.ndarray       # (N, 1, 2) int32 -- outline in pixel coordinates
    center: tuple[int, int]   # centroid (x, y) in pixels
    area: float               # filled area, px^2
    label: str = "unknown"    # e.g. "triangle"; see pennair.classify


class ShapeDetector:
    """Detects solid shapes on a textured background.

    ``detect`` is a pure function of the frame it is handed -- no state carries
    between calls. That is deliberate: Part 2 requires the video to be treated
    as a stream, one frame at a time, with no lookahead.
    """

    def __init__(
        self,
        texture_ksize: int | None = None,
        flat_frac: float = 0.5,
        min_area_frac: float = 2e-4,
        max_area_frac: float = 0.30,
        min_solidity: float = 0.80,
        refine: bool = True,
        proc_width: int = 960,
    ):
        # Window size for the busyness measure, and a genuine trade-off. Too
        # small and the window fits inside a single blade of grass, which then
        # reads as flat (measured on the static image: at k=5 the 1st
        # percentile of grass std-dev is 0.0, indistinguishable from a shape
        # interior). Too large and the window straddles shape boundaries, so
        # interiors stop reading as flat (interior p99 goes 0.0 -> 20.6 -> 51.5
        # at k=21/31/41). Measured sweet spot is ~2% of frame width.
        self.texture_ksize = texture_ksize
        # Threshold as a fraction of the frame's median std-dev. The background
        # is by construction most of the frame, so the median *is* an estimate
        # of the background's texture level; half of it means "flat relative to
        # whatever this background happens to be".
        #
        # This replaced Otsu, which fails badly here. Otsu maximises
        # between-class variance assuming two comparably sized classes, but the
        # shapes are only ~5% of pixels, so it splits the *background* in half
        # instead. Measured across the static image and both videos, Otsu called
        # 61%, 75% and 98% of some frames "flat"; this rule stayed within a
        # 2.3-5.9% band on every one of them.
        self.flat_frac = flat_frac
        # Area gates as a fraction of frame area, so they are resolution
        # independent. The lower gate kills speckle; the upper gate stops a
        # large genuinely-flat background region (sky, asphalt) being reported.
        self.min_area_frac = min_area_frac
        self.max_area_frac = max_area_frac
        # Solidity = contour area / convex hull area. Every target shape is
        # convex, so this is ~1.0 for an unobstructed shape and much lower for
        # a ragged background blob.
        #
        # 0.80, not ~1.0, because a *partially occluded* shape is legitimately
        # non-convex: the one underneath has a bite taken out of it. Measured
        # over both videos, unobstructed shapes sit at 0.95+, occluded ones tail
        # down to ~0.80, and no spurious region appears anywhere above 0.75 --
        # so this clears the tail with margin. Worth 3.89 -> 4.69 shapes/frame
        # on the dynamic video for zero false positives.
        #
        # This gate used to discard touching shapes *in pairs*, but that was
        # really a bug in stage 2 (see _snap_to_colour), not in the gate.
        self.min_solidity = min_solidity
        self.refine = refine
        # Stage 1 only has to answer *where* the shapes are; stage 2 does the
        # precise work at full resolution. So the texture pass runs on a
        # downscaled copy: at 1080p the window is k=39, the same physical window
        # as k=19 at 540p, so nothing is lost -- but the pass costs ~4x less.
        # Measured: 22.1 ms -> 4.0 ms per 1080p frame.
        self.proc_width = proc_width

        self._se5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    # -- parameters -------------------------------------------------------

    def kernel_size(self, width: int) -> int:
        """Texture window size for an image of the given width."""
        if self.texture_ksize is not None:
            return self.texture_ksize
        k = int(round(width * 0.02))
        return max(5, k | 1)  # force odd, floor at 5

    # -- stage 1: texture -------------------------------------------------

    def texture_map(self, frame: np.ndarray) -> tuple[np.ndarray, int]:
        """Return (std-dev map, kernel size) at the internal working scale.

        Exposed so the debug visualisation can show exactly what the detector
        sees, rather than recomputing it slightly differently.
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        w = frame.shape[1]
        if w > self.proc_width:
            scale = self.proc_width / w
            # INTER_AREA averages the pixels it discards, so it does not alias
            # the very texture we are about to measure. INTER_LINEAR would.
            gray = cv2.resize(gray, None, fx=scale, fy=scale,
                              interpolation=cv2.INTER_AREA)
        k = self.kernel_size(gray.shape[1])
        return local_stddev(gray, k), k

    def seed_mask(self, frame: np.ndarray) -> np.ndarray:
        """Stage 1. Frame -> binary mask, 255 where 'flat, therefore shape'.

        The result is *inset*: because the busyness window straddles the shape
        boundary, the outer ~k/2 pixels of every shape read as busy and get
        dropped. Stage 2 puts the boundary back. Do not "fix" it here by
        dilating -- dilating by a disk of radius r rounds every convex corner by
        r, which restores the area but destroys the geometry (measured: it
        visibly truncates the triangle's apex).

        Returned at full frame resolution regardless of the internal downscale.
        """
        h, w = frame.shape[:2]
        sd, _ = self.texture_map(frame)

        # Split point from this frame's own texture level, so changing the
        # background moves the threshold with it. The median is taken on a
        # strided sample: np.median sorts, and a quarter of the pixels estimates
        # it far more precisely than this threshold needs. Clamped so a
        # pathological frame cannot drive it somewhere absurd.
        thr = min(max(float(np.median(sd[::2, ::2])) * self.flat_frac, 3.0), 40.0)
        _, flat = cv2.threshold(sd, thr, 255, cv2.THRESH_BINARY_INV)
        flat = flat.astype(np.uint8)

        # OPEN first (erode then dilate) removes isolated flat specks where a
        # patch of background happened to be uniform; CLOSE then seals pinholes
        # inside a shape. Order matters: CLOSE first would fuse neighbouring
        # specks into blobs large enough to clear the area gate.
        flat = cv2.morphologyEx(flat, cv2.MORPH_OPEN, self._se5)
        flat = cv2.morphologyEx(flat, cv2.MORPH_CLOSE, self._se5)

        if flat.shape[:2] != (h, w):
            # Nearest: the seed is only a coarse locator, and this keeps it
            # strictly binary with no threshold-after-interpolation step.
            flat = cv2.resize(flat, (w, h), interpolation=cv2.INTER_NEAREST)
        return flat

    # -- stage 2: colour --------------------------------------------------

    def _snap_to_colour(
        self, frame: np.ndarray, seed: np.ndarray
    ) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
        """Stage 2. Recover each shape's true boundary using its own colour.

        For every seed blob we work in a small ROI and ask a question that is
        only answerable *because* stage 1 ran first: "what colour is this
        particular shape?". Pixels near that colour, connected to the seed, are
        the shape. The reference is learned per shape per frame, so no colour is
        ever assumed -- a red shape and a green shape on green grass go through
        identical code.

        Returns an int32 label image (0 = background, 1..N = one id per shape)
        and each shape's ROI rectangle, so the caller can extract contours
        without rescanning the whole frame per shape.
        """
        h, w = frame.shape[:2]
        # CIELAB because Euclidean distance in it approximates perceived colour
        # difference, so a single tolerance behaves sensibly across all hues. In
        # BGR the same numeric distance means very different things per colour.
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.int16)

        pad = self.kernel_size(w) // 2 + 6  # must exceed the stage-1 inset
        min_seed_px = self.min_area_frac * h * w * 0.5

        n, labels = cv2.connectedComponents(seed)
        # int32 label image, not a binary mask. Writing every shape into one
        # bitmap was the old bug: two shapes that end up a single pixel apart
        # fuse into one non-convex blob at the findContours step, and the
        # solidity gate then throws away *both*. Each shape keeps its own id,
        # so touching neighbours stay two shapes no matter how close they get.
        out = np.zeros((h, w), np.int32)
        next_id = 0
        rects: list[tuple[int, int, int, int]] = []
        for i in range(1, n):
            comp = (labels == i).astype(np.uint8) * 255
            if int(comp.sum()) // 255 < min_seed_px:
                continue

            x, y, bw, bh = cv2.boundingRect(comp)
            x0, y0 = max(x - pad, 0), max(y - pad, 0)
            x1, y1 = min(x + bw + pad, w), min(y + bh + pad, h)
            roi_lab, roi_seed = lab[y0:y1, x0:x1], comp[y0:y1, x0:x1]

            # Median, not mean: robust to the few boundary pixels the seed may
            # have caught, which are blends of shape and background. Sampled to
            # ~4k pixels, since a median over every pixel of a large shape costs
            # a big sort to buy precision we do not use.
            inside = roi_lab[roi_seed > 0]
            if len(inside) > 4096:
                inside = inside[:: len(inside) // 4096]
            ref = np.median(inside, axis=0).astype(np.float32)

            # Squared distance in float32, no sqrt: we only compare against a
            # threshold and squaring is monotonic, so the comparison is
            # identical. float64 here was the single largest cost in this loop.
            d = roi_lab.astype(np.float32) - ref
            dist2 = np.einsum("ijk,ijk->ij", d, d)

            # Tolerance scaled by the shape's own colour spread, so a
            # gradient-filled shape automatically gets a wider gate than a flat
            # one -- this handles the "colour gradients" extra credit, and the
            # strongly gradient-filled shapes in the hard video. The floor keeps
            # a perfectly uniform shape from getting a zero-width gate that its
            # own anti-aliased edge would fail. Squared space: (2*p95)^2 = 4*p95^2.
            p95_2 = float(np.percentile(dist2[roi_seed > 0], 95))
            tol2 = max(p95_2 * 4.0, 18.0 * 18.0)
            _, keep = cv2.threshold(dist2, tol2, 255, cv2.THRESH_BINARY_INV)
            keep = cv2.morphologyEx(keep.astype(np.uint8), cv2.MORPH_CLOSE, self._se5)

            # A background pixel can coincidentally match the shape's colour, so
            # keep only the component(s) actually touching the seed.
            _, klab = cv2.connectedComponents(keep)
            ids = np.unique(klab[roi_seed > 0])
            ids = ids[ids > 0]
            if len(ids) == 0:
                continue
            # Almost always exactly one component; the equality test is much
            # cheaper than the general np.isin.
            sel = (klab == ids[0]) if len(ids) == 1 else np.isin(klab, ids)

            next_id += 1
            roi_out = out[y0:y1, x0:x1]
            # First claim wins on a contested pixel. Genuinely contested pixels
            # are rare -- measured at 0 on the frames where shapes touch, since
            # the colour gate stops each fill at the other shape's edge -- and
            # arbitrating them properly would cost more than it buys.
            np.copyto(roi_out, next_id, where=sel & (roi_out == 0))
            rects.append((x0, y0, x1, y1))
        return out, rects

    # -- public -----------------------------------------------------------

    def segment(self, frame: np.ndarray) -> tuple[np.ndarray, list[tuple[int, int, int, int]]]:
        """Frame -> (int32 label image, per-shape ROI rectangles)."""
        seed = self.seed_mask(frame)
        if self.refine:
            return self._snap_to_colour(frame, seed)
        # Unrefined: the seed's own components are the shapes. Stats give the
        # same rectangles the refined path returns, in one pass.
        n, labels, stats, _ = cv2.connectedComponentsWithStats(seed)
        rects = [(stats[i, cv2.CC_STAT_LEFT], stats[i, cv2.CC_STAT_TOP],
                  stats[i, cv2.CC_STAT_LEFT] + stats[i, cv2.CC_STAT_WIDTH],
                  stats[i, cv2.CC_STAT_TOP] + stats[i, cv2.CC_STAT_HEIGHT])
                 for i in range(1, n)]
        return labels, rects

    def mask(self, frame: np.ndarray) -> np.ndarray:
        """Full two-stage binary mask of the shapes in ``frame``.

        Only a view for humans -- the detector itself works from the label
        image, because flattening to binary is what merges touching shapes.
        """
        return (self.segment(frame)[0] > 0).astype(np.uint8) * 255

    def analyze(self, frame: np.ndarray) -> tuple[list[Detection], np.ndarray]:
        """Detections plus the binary mask they came from, in one pipeline run.

        For callers that want to display the mask as well as the detections
        (the live viewer), so they do not pay for the pipeline twice.
        """
        labels, rects = self.segment(frame)
        return self._detections(labels, rects), (labels > 0).astype(np.uint8) * 255

    def detect(self, frame: np.ndarray) -> list[Detection]:
        """Frame -> detected shapes, largest first. Pure; no cross-frame state."""
        return self._detections(*self.segment(frame))

    # -- contour extraction and gating ------------------------------------

    def _detections(self, labels: np.ndarray, rects) -> list[Detection]:
        h, w = labels.shape[:2]
        frame_area = float(h * w)

        out: list[Detection] = []
        for i, (x0, y0, x1, y1) in enumerate(rects, start=1):
            # One shape at a time, inside its own rectangle. Scanning the whole
            # frame per label would cost O(shapes x pixels); the ROI is the same
            # one stage 2 already worked in, so this is a few percent of that.
            sub = (labels[y0:y1, x0:x1] == i).astype(np.uint8)

            # RETR_EXTERNAL: outer boundaries only, not holes within shapes.
            # CHAIN_APPROX_SIMPLE collapses straight runs to their endpoints, a
            # big memory win on these polygons that loses nothing. offset puts
            # the contour back into full-frame coordinates.
            contours, _ = cv2.findContours(sub, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE, offset=(x0, y0))
            if not contours:
                continue
            # One label is one shape; if the colour fill left a stray fragment,
            # the shape is the largest piece.
            c = max(contours, key=cv2.contourArea)

            area = cv2.contourArea(c)
            if not (self.min_area_frac * frame_area <= area <= self.max_area_frac * frame_area):
                continue

            hull_area = cv2.contourArea(cv2.convexHull(c))
            if hull_area <= 0 or area / hull_area < self.min_solidity:
                continue

            # Centroid from image moments: (m10/m00, m01/m00) is the
            # area-weighted mean position, the true centre of mass of the filled
            # shape -- not the centre of its bounding box, which would be wrong
            # for the triangle and the trapezoid.
            mom = cv2.moments(c)
            if mom["m00"] == 0:
                continue
            cx = int(round(mom["m10"] / mom["m00"]))
            cy = int(round(mom["m01"] / mom["m00"]))

            out.append(Detection(contour=c, center=(cx, cy), area=area,
                                 label=classify(c, area)))

        # Largest first: stable, deterministic ordering for anything downstream.
        out.sort(key=lambda d: d.area, reverse=True)
        return out
