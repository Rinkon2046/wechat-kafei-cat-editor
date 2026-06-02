#!/usr/bin/env python3
"""Normalize a WeChat cover image to an exact 2.35:1 canvas."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps


DEFAULT_WIDTH = 1645
DEFAULT_HEIGHT = 700


def normalize_cover(input_path: Path, output_path: Path, width: int, height: int, mode: str) -> None:
    image = Image.open(input_path).convert("RGB")
    if mode == "crop":
        normalized = ImageOps.fit(image, (width, height), method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))
    else:
        image.thumbnail((width, height), Image.Resampling.LANCZOS)
        normalized = Image.new("RGB", (width, height), "white")
        normalized.paste(image, ((width - image.width) // 2, (height - image.height) // 2))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    normalized.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Pad or crop a cover image to exact 2.35:1 WeChat cover size.")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output PNG path")
    parser.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    parser.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    parser.add_argument("--mode", choices=["pad", "crop"], default="pad", help="pad with white margins or center-crop")
    args = parser.parse_args()

    ratio = args.width / args.height
    if abs(ratio - 2.35) > 0.01:
        raise ValueError(f"Output size must be close to 2.35:1, got {args.width}x{args.height}.")
    normalize_cover(Path(args.input), Path(args.output), args.width, args.height, args.mode)


if __name__ == "__main__":
    main()
