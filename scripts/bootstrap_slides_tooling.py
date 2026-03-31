#!/usr/bin/env python3
"""Copy helper assets and review scripts from this skill's local bundle into a task workspace.

Resources are vendored inside this skill directory — no dependency on the
external ``slides`` skill at runtime.
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

# ── resource roots (relative to *this* script) ──────────────────────
_SKILL_DIR = Path(__file__).resolve().parent.parent
_LOCAL_HELPERS = _SKILL_DIR / "assets" / "pptxgenjs_helpers"
_LOCAL_WRAPPERS = _SKILL_DIR / "scripts"
_LOCAL_REVIEW_SCRIPTS = _LOCAL_WRAPPERS / "slides"


def _copy_file(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def _copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Copy helper assets and/or review scripts into a workspace."
    )
    parser.add_argument("workspace", help="Target workspace directory")
    parser.add_argument(
        "--with-helpers",
        action="store_true",
        help="Copy assets/pptxgenjs_helpers into the workspace",
    )
    parser.add_argument(
        "--with-review-scripts",
        action="store_true",
        help="Copy validate/review wrappers plus render/montage/overflow/font/raster scripts into the workspace",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Copy both helpers and review scripts",
    )
    args = parser.parse_args()

    if args.all:
        args.with_helpers = True
        args.with_review_scripts = True

    if not args.with_helpers and not args.with_review_scripts:
        parser.error("Select at least one of --with-helpers, --with-review-scripts, or --all")

    workspace = Path(args.workspace).expanduser().resolve()
    workspace.mkdir(parents=True, exist_ok=True)

    copied: list[Path] = []

    if args.with_helpers:
        if not _LOCAL_HELPERS.exists():
            raise FileNotFoundError(
                f"Local pptxgenjs_helpers not found at: {_LOCAL_HELPERS}\n"
                "Did you forget to vendor assets into this skill?"
            )
        dst = workspace / "assets" / "pptxgenjs_helpers"
        _copy_tree(_LOCAL_HELPERS, dst)
        copied.append(dst)

    if args.with_review_scripts:
        if not _LOCAL_REVIEW_SCRIPTS.exists():
            raise FileNotFoundError(
                f"Local review scripts not found at: {_LOCAL_REVIEW_SCRIPTS}\n"
                "Did you forget to vendor scripts/slides/ into this skill?"
            )
        wrapper_scripts = [
            "validate_deck.py",
            "review_deck.py",
        ]
        for name in wrapper_scripts:
            src = _LOCAL_WRAPPERS / name
            dst = workspace / "scripts" / name
            _copy_file(src, dst)
            copied.append(dst)

        scripts = [
            "render_slides.py",
            "create_montage.py",
            "slides_test.py",
            "detect_font.py",
            "ensure_raster_image.py",
        ]
        for name in scripts:
            src = _LOCAL_REVIEW_SCRIPTS / name
            dst = workspace / "scripts" / "slides" / name
            _copy_file(src, dst)
            copied.append(dst)

    print("Copied:")
    for path in copied:
        print(f"  {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
