"""The "busyness" measure that the whole detector is built on.

The shapes we want are solid -- flat, single-colour interiors. Every background
in the challenge (grass, asphalt) is textured -- fine-grained, high-frequency
detail. So instead of asking "what colour is this pixel?", which breaks the
instant a shape is the same green as the grass and cannot generalise to an
unseen background, we ask "how much does the neighbourhood around this pixel
vary?".
"""

from __future__ import annotations

import cv2
import numpy as np


def local_stddev(gray: np.ndarray, ksize: int) -> np.ndarray:
    """Per-pixel standard deviation over a ksize x ksize window.

    The obvious implementation -- slide a window, call std() per pixel -- is
    far too slow. Instead use

        Var(X) = E[X^2] - E[X]^2

    where both expectations are box filters (local means). OpenCV's boxFilter
    uses a separable running sum, so its cost is O(1) per pixel *regardless of
    kernel size*: we can widen the window for free. Two filters plus some
    arithmetic, no Python-level loop.

    Args:
        gray: single-channel image.
        ksize: window side length, should be odd.

    Returns:
        float32 array, same shape as ``gray``.
    """
    f = gray.astype(np.float32)
    mean = cv2.boxFilter(f, ddepth=-1, ksize=(ksize, ksize), normalize=True)
    mean_sq = cv2.boxFilter(f * f, ddepth=-1, ksize=(ksize, ksize), normalize=True)
    # Clamp at 0: floating-point cancellation can push a perfectly flat region
    # very slightly negative, and sqrt of a negative is NaN.
    var = cv2.max(mean_sq - mean * mean, 0.0)
    return cv2.sqrt(var)
