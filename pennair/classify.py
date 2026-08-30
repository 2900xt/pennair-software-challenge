"""Naming a shape once its outline is already known.

This is deliberately downstream of detection. Searching an image for a
parametric template is enormously expensive (the parameter space is position x
scale x rotation x aspect, and each combination costs a full-image pass).
Fitting a model to an *already extracted* contour is not: it touches a few
hundred boundary points instead of two million pixels, and measures at well
under 1% of the cost of detection.

The challenge does not actually ask for classification -- only outlines,
centres and 3D position -- so this is a small extra.
"""

from __future__ import annotations

import cv2
import numpy as np

# approxPolyDP tolerance as a fraction of perimeter. 2% is the usual value:
# large enough to collapse the jitter left by pixel quantisation, small enough
# to keep genuine vertices.
_EPSILON_FRAC = 0.02

# A polygon with many vertices and near-perfect circularity is a circle. The
# threshold is generous because a rasterised circle's contour is slightly
# under-area compared to the ideal disk.
_CIRCULARITY_MIN = 0.90

_NAMES = {3: "triangle", 4: "quadrilateral", 5: "pentagon", 6: "hexagon", 7: "heptagon"}


def classify(contour: np.ndarray, area: float) -> str:
    """Return a human-readable name for a contour, e.g. "triangle"."""
    peri = cv2.arcLength(contour, True)
    if peri <= 0:
        return "unknown"
    n = len(cv2.approxPolyDP(contour, _EPSILON_FRAC * peri, True))

    _, radius = cv2.minEnclosingCircle(contour)
    circularity = area / (np.pi * radius * radius) if radius > 0 else 0.0

    # Check circle first: a rasterised circle approximates to 8-ish vertices,
    # so vertex count alone would call it an octagon.
    if circularity > _CIRCULARITY_MIN and n > 4:
        return "circle"
    return _NAMES.get(n, f"{n}-gon")
