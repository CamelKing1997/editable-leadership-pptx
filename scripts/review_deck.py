#!/usr/bin/env python3
"""Quick visual review wrapper for editable PPTX decks.

Default behavior is optimized for fast human review:
- render slides
- build montage/contact sheet
- skip overflow check
- skip font check
- skip tile generation

Use validate_deck.py for the full QA chain or pass the opt-in flags below
to enable deeper checks during review.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run a fast visual review for a deck. By default this renders slides and "
            "builds a montage, while skipping overflow, font, and tile checks."
        )
    )
    parser.add_argument("deck", help="Path to the editable .pptx deck")
    parser.add_argument("--output-dir", help="Directory for review artifacts")
    parser.add_argument("--width", type=int, help="Rendered review image width hint")
    parser.add_argument("--height", type=int, help="Rendered review image height hint")
    parser.add_argument(
        "--with-overflow",
        action="store_true",
        help="Include overflow/out-of-bounds check in this review run",
    )
    parser.add_argument(
        "--with-font-check",
        action="store_true",
        help="Include font inspection in this review run",
    )
    parser.add_argument(
        "--with-tiles",
        action="store_true",
        help="Generate local tiles for dense slide regions in this review run",
    )
    parser.add_argument(
        "--tile-slides",
        help="Slides to tile, e.g. 'all', '3', or '3,5-7' (implies --with-tiles)",
    )
    parser.add_argument("--tile-rows", type=int, help="Tile grid rows per slide")
    parser.add_argument("--tile-cols", type=int, help="Tile grid cols per slide")
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Run the same checks as validate_deck.py, but still without --strict unless you pass it through",
    )
    args, passthrough = parser.parse_known_args()

    here = Path(__file__).resolve().parent
    validate_path = here / "validate_deck.py"
    command = [sys.executable, str(validate_path), args.deck]

    if args.output_dir:
        command.extend(["--output-dir", args.output_dir])
    if args.width is not None:
        command.extend(["--width", str(args.width)])
    if args.height is not None:
        command.extend(["--height", str(args.height)])

    want_tiles = args.with_tiles or bool(args.tile_slides)

    if not args.deep:
        if not args.with_overflow:
            command.append("--skip-overflow")
        if not args.with_font_check:
            command.append("--skip-font-check")
        if not want_tiles:
            command.append("--skip-tiles")

    if want_tiles:
        if args.tile_slides:
            command.extend(["--tile-slides", args.tile_slides])
        if args.tile_rows is not None:
            command.extend(["--tile-rows", str(args.tile_rows)])
        if args.tile_cols is not None:
            command.extend(["--tile-cols", str(args.tile_cols)])

    command.extend(passthrough)
    return subprocess.run(command).returncode


if __name__ == "__main__":
    raise SystemExit(main())
