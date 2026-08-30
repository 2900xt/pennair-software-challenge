"""Tests you can run yourself to verify the detector actually works.

    make test
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from pennair import ShapeDetector, classify, local_stddev

STATIC = Path(__file__).resolve().parents[1] / "PennAir 2024 App Static.png"

# Centres measured from the static image. The tolerance is generous enough to
# survive a harmless parameter tweak but tight enough to catch a real
# regression in localisation.
EXPECTED_CENTERS = [(112, 76), (279, 320), (553, 104), (691, 344), (839, 148)]
CENTER_TOL_PX = 6


@pytest.fixture(scope="module")
def static_frame() -> np.ndarray:
    if not STATIC.exists():
        pytest.skip(f"challenge image not present: {STATIC.name}")
    img = cv2.imread(str(STATIC))
    assert img is not None, "image present but unreadable"
    return img


# -- the core measure -----------------------------------------------------

def test_local_stddev_is_zero_on_a_flat_region():
    """A solid block has no internal variation -- this is the whole premise."""
    flat = np.full((80, 80), 128, np.uint8)
    assert local_stddev(flat, 9).max() == pytest.approx(0.0, abs=1e-3)


def test_local_stddev_is_large_on_texture():
    """Random texture must land far above any flat region."""
    rng = np.random.default_rng(0)
    noise = rng.integers(0, 256, (200, 200), dtype=np.uint8)
    assert np.median(local_stddev(noise, 9)) > 30


def test_gradient_still_reads_as_flat():
    """A smooth colour ramp is locally flat, which is why gradient-filled
    shapes (the hard video) survive the same threshold as solid ones."""
    ramp = np.tile(np.linspace(0, 255, 200, dtype=np.uint8), (200, 1))
    assert np.median(local_stddev(ramp, 9)) < 5


# -- detection on the real image ------------------------------------------

def test_finds_exactly_five_shapes(static_frame):
    assert len(ShapeDetector().detect(static_frame)) == 5


def test_centers_are_where_we_expect(static_frame):
    found = sorted(d.center for d in ShapeDetector().detect(static_frame))
    assert len(found) == len(EXPECTED_CENTERS)
    for got, want in zip(found, EXPECTED_CENTERS):
        assert np.hypot(got[0] - want[0], got[1] - want[1]) <= CENTER_TOL_PX, \
            f"center {got} too far from expected {want}"


def test_all_five_shape_types_are_named(static_frame):
    labels = {d.label for d in ShapeDetector().detect(static_frame)}
    assert {"triangle", "circle", "pentagon"} <= labels
    assert sum(d.label == "quadrilateral" for d in ShapeDetector().detect(static_frame)) == 2


def test_detect_is_pure(static_frame):
    """Part 2 needs a stateless per-frame function; prove there is no state."""
    det = ShapeDetector()
    a = det.detect(static_frame)
    b = det.detect(static_frame)
    assert [d.center for d in a] == [d.center for d in b]
    assert [d.area for d in a] == [d.area for d in b]


def test_contours_are_closed_and_nontrivial(static_frame):
    for d in ShapeDetector().detect(static_frame):
        assert len(d.contour) >= 4
        assert d.area > 0
        assert cv2.contourArea(cv2.convexHull(d.contour)) > 0


# -- false positives ------------------------------------------------------

def test_pure_texture_yields_no_shapes():
    """A frame of nothing but texture must produce nothing. This is the guard
    against the class of bug where background is reported as a shape."""
    rng = np.random.default_rng(1)
    noise = rng.integers(0, 256, (540, 960, 3), dtype=np.uint8)
    assert ShapeDetector().detect(noise) == []


# -- classification -------------------------------------------------------

@pytest.mark.parametrize("sides,expected", [(3, "triangle"), (5, "pentagon")])
def test_classify_regular_polygon(sides, expected):
    img = np.zeros((300, 300), np.uint8)
    ang = np.linspace(0, 2 * np.pi, sides, endpoint=False) - np.pi / 2
    pts = np.stack([150 + 110 * np.cos(ang), 150 + 110 * np.sin(ang)], 1).astype(np.int32)
    cv2.fillPoly(img, [pts], 255)
    c = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0]
    assert classify(c, cv2.contourArea(c)) == expected


def test_classify_circle():
    img = np.zeros((300, 300), np.uint8)
    cv2.circle(img, (150, 150), 110, 255, -1)
    c = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0][0]
    assert classify(c, cv2.contourArea(c)) == "circle"


# -- touching shapes ------------------------------------------------------
# Regression test for the bug where two shapes that touch were both dropped:
# stage 2 OR-ed every grown region into one bitmap, so a single pixel of
# contact fused them into one non-convex blob that failed the solidity gate.

def _synthetic_touching(gap: int) -> np.ndarray:
    """Two solid squares of different colours on a noisy background."""
    rng = np.random.default_rng(0)
    img = rng.integers(40, 210, (400, 600, 3), dtype=np.uint8)  # 'grass'
    img[150:250, 150:250] = (200, 40, 40)     # blue square
    x = 250 + gap
    img[150:250, x:x + 100] = (40, 220, 220)  # yellow square
    return img


@pytest.mark.parametrize("gap", [40, 1, 0])
def test_touching_shapes_are_reported_separately(gap):
    """Two shapes stay two detections even when they share an edge."""
    dets = ShapeDetector().detect(_synthetic_touching(gap))
    assert len(dets) == 2, f"gap={gap}: expected 2 shapes, got {len(dets)}"
    # ...and each keeps its own centre rather than a merged one.
    xs = sorted(d.center[0] for d in dets)
    assert xs[1] - xs[0] > 80, f"gap={gap}: centres collapsed together: {xs}"
