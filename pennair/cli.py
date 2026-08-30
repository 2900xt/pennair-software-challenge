"""Command line entry point.

    pennair image "PennAir 2024 App Static.png" --stages
    pennair video "PennAir 2024 App Dynamic.mp4"

Both subcommands are thin wrappers over the same detector. The video runner
holds exactly one frame at a time: read, detect, draw, show, discard.
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import cv2

from pennair import gui
from pennair.detector import ShapeDetector
from pennair.visualize import annotate, stage_panel


def _cmd_image(args: argparse.Namespace) -> int:
    frame = cv2.imread(str(args.image))
    if frame is None:
        print(f"error: could not read {args.image}", file=sys.stderr)
        return 1

    det = ShapeDetector()
    # Warm-up call: the first invocation pays one-off import and allocation
    # costs, which would otherwise be reported as the algorithm's runtime.
    det.detect(frame)

    t0 = time.perf_counter()
    dets = det.detect(frame)
    ms = (time.perf_counter() - t0) * 1000

    args.out.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(args.out), annotate(frame, dets))

    print(f"{args.image.name}: {frame.shape[1]}x{frame.shape[0]}  "
          f"{len(dets)} shapes  {ms:.1f} ms/frame")
    for i, d in enumerate(dets, 1):
        print(f"  {i}. {d.label:<14} center={str(d.center):>12}  "
              f"area={d.area:8.0f} px^2")
    print(f"wrote {args.out}")

    if args.stages:
        p = args.out.with_name(args.out.stem + "_stages.png")
        cv2.imwrite(str(p), stage_panel(frame, det))
        print(f"wrote {p}")
    return 0


def _cmd_video(args: argparse.Namespace) -> int:
    # A bare number means a camera index, so the same runner can be pointed at
    # a live feed -- the closest thing here to the aircraft's actual input.
    source = int(args.source) if str(args.source).isdigit() else str(args.source)
    return gui.run(source, display_width=args.width, loop=args.loop, save=args.save)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="pennair",
                                 description="Solid-shape detection on textured backgrounds.")
    sub = ap.add_subparsers(dest="command", required=True)

    p_img = sub.add_parser("image", help="detect shapes in a still image (Part 1)")
    p_img.add_argument("image", type=Path, help="input image")
    p_img.add_argument("-o", "--out", type=Path, default=Path("out/static_detected.png"),
                       help="output path (default: out/static_detected.png)")
    p_img.add_argument("--stages", action="store_true",
                       help="also write a contact sheet of the pipeline stages")
    p_img.set_defaults(func=_cmd_image)

    p_vid = sub.add_parser("video", help="live viewer over a video stream (Part 2)")
    p_vid.add_argument("source", help="video file, or a camera index like 0")
    p_vid.add_argument("--width", type=int, default=1280,
                       help="window width in pixels (default: 1280)")
    p_vid.add_argument("--loop", action="store_true", help="replay when the video ends")
    p_vid.add_argument("--save", type=Path, default=None,
                       help="also write the annotated video to this path")
    p_vid.set_defaults(func=_cmd_video)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
