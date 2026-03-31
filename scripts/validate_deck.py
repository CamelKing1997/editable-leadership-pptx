#!/usr/bin/env python3
"""Validate an editable PPTX deck with render-based QA artifacts and checks.

This wrapper uses the bundled review scripts vendored inside the
``editable-leadership-pptx`` skill so a deck can be reviewed with one command
instead of manually chaining render, montage, overflow, and font checks.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from PIL import Image


@dataclass
class CommandResult:
    ok: bool
    command: list[str]
    stdout: str
    stderr: str
    returncode: int


def _run(command: list[str]) -> CommandResult:
    proc = subprocess.run(command, capture_output=True, text=True)
    return CommandResult(
        ok=proc.returncode == 0,
        command=command,
        stdout=proc.stdout,
        stderr=proc.stderr,
        returncode=proc.returncode,
    )


def _bundled_review_scripts_dir() -> Path:
    return Path(__file__).resolve().parent / "slides"


def _ensure_review_script(name: str) -> Path:
    path = _bundled_review_scripts_dir() / name
    if not path.exists():
        raise FileNotFoundError(f"Required bundled review script not found: {path}")
    return path


def _parse_slide_range(spec: str, max_slide: int) -> list[int]:
    values: set[int] = set()
    for part in spec.split(","):
        item = part.strip()
        if not item:
            continue
        if "-" in item:
            start_s, end_s = item.split("-", 1)
            start = int(start_s)
            end = int(end_s)
            if start > end:
                start, end = end, start
            values.update(range(start, end + 1))
        else:
            values.add(int(item))
    return sorted(v for v in values if 1 <= v <= max_slide)


def _natural_slide_sort(paths: Iterable[Path]) -> list[Path]:
    def key(path: Path) -> list[object]:
        return [int(p) if p.isdigit() else p for p in re.split(r"(\d+)", path.name)]

    return sorted(paths, key=key)


def _collect_rendered_images(render_dir: Path) -> list[Path]:
    images = [p for p in render_dir.iterdir() if p.is_file() and p.suffix.lower() == ".png"]
    return _natural_slide_sort(images)


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _missing_modules(stderr: str) -> list[str]:
    return re.findall(r"ModuleNotFoundError: No module named '([^']+)'", stderr)


def _failure_hints(result: CommandResult) -> list[str]:
    hints: list[str] = []
    missing = _missing_modules(result.stderr)
    if missing:
        review_scripts_dir = _bundled_review_scripts_dir()
        hints.append(
            "Missing Python packages for this skill's bundled review scripts: "
            + ", ".join(sorted(set(missing)))
        )
        hints.append(
            f"Install the dependencies used by {review_scripts_dir} "
            "(for example pdf2image, Pillow, numpy, python-pptx) in the Python environment used to run this wrapper."
        )
    stderr_lower = result.stderr.lower()
    if "soffice" in stderr_lower or "libreoffice" in stderr_lower:
        hints.append("LibreOffice/soffice is required for PPTX-to-PDF rendering.")
    if "poppler" in stderr_lower or "pdfinfo" in stderr_lower:
        hints.append("Poppler tools are required for pdf2image-based rasterization.")
    return hints


def _create_tiles(image_path: Path, out_dir: Path, rows: int, cols: int) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    with Image.open(image_path) as img:
        width, height = img.size
        tile_w = math.ceil(width / cols)
        tile_h = math.ceil(height / rows)
        for r in range(rows):
            for c in range(cols):
                left = c * tile_w
                top = r * tile_h
                right = min(width, left + tile_w)
                bottom = min(height, top + tile_h)
                tile = img.crop((left, top, right, bottom))
                out_path = out_dir / f"tile_r{r}_c{c}.png"
                tile.save(out_path)
                outputs.append(out_path)
    return outputs


def _create_tiles_for_slides(
    rendered_images: list[Path],
    tiles_dir: Path,
    tile_rows: int,
    tile_cols: int,
    slide_spec: str,
) -> dict[str, list[str]]:
    selected: list[Path]
    if slide_spec == "all":
        selected = rendered_images
    else:
        slide_numbers = _parse_slide_range(slide_spec, len(rendered_images))
        selected = [rendered_images[i - 1] for i in slide_numbers]

    result: dict[str, list[str]] = {}
    for image_path in selected:
        slide_name = image_path.stem
        out_dir = tiles_dir / slide_name
        outputs = _create_tiles(image_path, out_dir, tile_rows, tile_cols)
        result[slide_name] = [str(p) for p in outputs]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run deck review and validation by chaining render, montage, overflow, font, and tile checks."
    )
    parser.add_argument("deck", help="Path to the editable .pptx deck")
    parser.add_argument(
        "--output-dir",
        help="Directory for review artifacts. Defaults to <deck-stem>__deck-review next to the deck.",
    )
    parser.add_argument("--width", type=int, default=1600, help="Rendered review image width hint")
    parser.add_argument("--height", type=int, default=900, help="Rendered review image height hint")
    parser.add_argument(
        "--tile-slides",
        default="all",
        help="Slides to tile, e.g. 'all', '3', or '3,5-7'. Default: all",
    )
    parser.add_argument("--tile-rows", type=int, default=3, help="Tile grid rows per slide")
    parser.add_argument("--tile-cols", type=int, default=3, help="Tile grid cols per slide")
    parser.add_argument("--skip-montage", action="store_true", help="Skip montage generation")
    parser.add_argument("--skip-overflow", action="store_true", help="Skip overflow/out-of-bounds check")
    parser.add_argument("--skip-font-check", action="store_true", help="Skip font check")
    parser.add_argument("--skip-tiles", action="store_true", help="Skip tile generation")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if overflow or font issues are detected",
    )
    args = parser.parse_args()

    deck_path = Path(args.deck).expanduser().resolve()
    if not deck_path.exists():
        raise FileNotFoundError(f"Deck not found: {deck_path}")

    output_dir = (
        Path(args.output_dir).expanduser().resolve()
        if args.output_dir
        else deck_path.with_name(f"{deck_path.stem}__deck-review")
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    render_dir = output_dir / "rendered"
    logs_dir = output_dir / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)

    render_script = _ensure_review_script("render_slides.py")
    render_cmd = [
        sys.executable,
        str(render_script),
        str(deck_path),
        "--output_dir",
        str(render_dir),
        "--width",
        str(args.width),
        "--height",
        str(args.height),
    ]
    render_result = _run(render_cmd)
    _write_text(logs_dir / "render_slides.stdout.txt", render_result.stdout)
    _write_text(logs_dir / "render_slides.stderr.txt", render_result.stderr)
    if not render_result.ok:
        failure_summary = {
            "deck": str(deck_path),
            "output_dir": str(output_dir),
            "failed_stage": "render_slides",
            "command": render_result.command,
            "returncode": render_result.returncode,
            "stdout": render_result.stdout,
            "stderr": render_result.stderr,
            "hints": _failure_hints(render_result),
            "log_dir": str(logs_dir),
        }
        (output_dir / "summary.json").write_text(
            json.dumps(failure_summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Render failed. See logs under {logs_dir}", file=sys.stderr)
        for hint in failure_summary["hints"]:
            print(f"- {hint}", file=sys.stderr)
        return render_result.returncode or 1

    rendered_images = _collect_rendered_images(render_dir)
    if not rendered_images:
        print(f"No rendered slide images found in {render_dir}", file=sys.stderr)
        return 1

    montage_path = output_dir / "montage.png"
    montage_result: CommandResult | None = None
    if not args.skip_montage:
        montage_script = _ensure_review_script("create_montage.py")
        montage_cmd = [
            sys.executable,
            str(montage_script),
            "--input_dir",
            str(render_dir),
            "--output_file",
            str(montage_path),
            "--label_mode",
            "number",
        ]
        montage_result = _run(montage_cmd)
        _write_text(logs_dir / "create_montage.stdout.txt", montage_result.stdout)
        _write_text(logs_dir / "create_montage.stderr.txt", montage_result.stderr)

    overflow_result: CommandResult | None = None
    overflow_ok = True
    if not args.skip_overflow:
        overflow_script = _ensure_review_script("slides_test.py")
        overflow_cmd = [
            sys.executable,
            str(overflow_script),
            str(deck_path),
            "--width",
            str(args.width),
            "--height",
            str(args.height),
        ]
        overflow_result = _run(overflow_cmd)
        overflow_ok = overflow_result.ok
        _write_text(logs_dir / "slides_test.stdout.txt", overflow_result.stdout)
        _write_text(logs_dir / "slides_test.stderr.txt", overflow_result.stderr)

    font_result: CommandResult | None = None
    font_ok = True
    font_payload: dict[str, object] | None = None
    if not args.skip_font_check:
        font_script = _ensure_review_script("detect_font.py")
        font_cmd = [sys.executable, str(font_script), str(deck_path), "--json"]
        font_result = _run(font_cmd)
        _write_text(logs_dir / "detect_font.stdout.json", font_result.stdout)
        _write_text(logs_dir / "detect_font.stderr.txt", font_result.stderr)
        if font_result.ok:
            try:
                font_payload = json.loads(font_result.stdout or "{}")
                missing = font_payload.get("font_missing_overall") or []
                substituted = font_payload.get("font_substituted_overall") or []
                font_ok = not missing and not substituted
            except json.JSONDecodeError:
                font_ok = False
        else:
            font_ok = False

    tiles_payload: dict[str, list[str]] = {}
    if not args.skip_tiles:
        tiles_payload = _create_tiles_for_slides(
            rendered_images=rendered_images,
            tiles_dir=output_dir / "tiles",
            tile_rows=args.tile_rows,
            tile_cols=args.tile_cols,
            slide_spec=args.tile_slides,
        )

    summary = {
        "deck": str(deck_path),
        "output_dir": str(output_dir),
        "rendered_slide_count": len(rendered_images),
        "rendered_dir": str(render_dir),
        "montage_path": str(montage_path) if montage_path.exists() else None,
        "overflow_ok": overflow_ok,
        "font_ok": font_ok,
        "tile_rows": None if args.skip_tiles else args.tile_rows,
        "tile_cols": None if args.skip_tiles else args.tile_cols,
        "tile_slides": None if args.skip_tiles else args.tile_slides,
        "tiles": tiles_payload,
        "log_dir": str(logs_dir),
    }
    if font_payload is not None:
        summary["font_report"] = font_payload
    if overflow_result is not None:
        summary["overflow_stdout"] = overflow_result.stdout.strip()
    if montage_result is not None and not montage_result.ok:
        summary["montage_stdout"] = montage_result.stdout.strip()
        summary["montage_stderr"] = montage_result.stderr.strip()

    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Deck review artifacts written to {output_dir}")
    print(f"Rendered slides: {render_dir}")
    if montage_path.exists():
        print(f"Montage: {montage_path}")
    if not args.skip_tiles:
        print(f"Tiles: {output_dir / 'tiles'}")
    if overflow_result is not None:
        print("Overflow check: " + ("PASS" if overflow_ok else "FAIL"))
    if font_result is not None:
        print("Font check: " + ("PASS" if font_ok else "ISSUES FOUND"))
    print(f"Summary: {summary_path}")

    if args.strict and (not overflow_ok or not font_ok):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
