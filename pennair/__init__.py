"""Solid-shape detection for the PennAir 2024 software challenge.

Public API::

    from pennair import ShapeDetector, annotate

    det = ShapeDetector()
    detections = det.detect(frame)      # pure function of one frame
    vis = annotate(frame, detections)
"""

from pennair.detector import Detection, ShapeDetector
from pennair.texture import local_stddev
from pennair.classify import classify
from pennair.visualize import annotate, stage_panel

__version__ = "0.1.0"

__all__ = [
    "Detection",
    "ShapeDetector",
    "local_stddev",
    "classify",
    "annotate",
    "stage_panel",
]
