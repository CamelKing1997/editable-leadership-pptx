# PptxGenJS Helpers

## When To Read This

Read this file when the chosen authoring path is JavaScript or PptxGenJS and you need helper API details, command examples for the bundled review scripts, or dependency notes for a deck-generation task.

## Helper Modules

- `autoFontSize(textOrRuns, fontFace, opts)`: Pick a font size that fits a fixed box.
- `calcTextBox(fontSizePt, opts)`: Estimate text-box geometry from font size and content.
- `calcTextBoxHeightSimple(fontSizePt, numLines, leading?, padding?)`: Quick text height estimate.
- `imageSizingCrop(pathOrData, x, y, w, h)`: Center-crop an image into a target box.
- `imageSizingContain(pathOrData, x, y, w, h)`: Fit an image fully inside a target box.
- `svgToDataUri(svgString)`: Convert an SVG string into an embeddable data URI.
- `latexToSvgDataUri(texString)`: Render LaTeX to SVG for crisp equations.
- `getImageDimensions(pathOrData)`: Read image width, height, type, and aspect ratio.
- `safeOuterShadow(...)`: Build a safe outer-shadow config for PowerPoint output.
- `codeToRuns(source, language)`: Convert source code into rich-text runs for `addText`.
- `warnIfSlideHasOverlaps(slide, pptx)`: Emit overlap warnings for diagnostics.
- `warnIfSlideElementsOutOfBounds(slide, pptx)`: Emit boundary warnings for diagnostics.
- `alignSlideElements(slide, indices, alignment)`: Align selected elements precisely.
- `distributeSlideElements(slide, indices, direction)`: Evenly space selected elements.
- `addImageTextCard(...)`, `addCardRow(...)`, `addThreeLevelTree(...)`: Composite layout builders for common presentation patterns.

## Dependency Notes

JavaScript helpers expect these packages when you use the corresponding features:

- Core authoring: `pptxgenjs`
- Text measurement: `skia-canvas`, `linebreak`, `fontkit`
- Syntax highlighting: `prismjs`
- LaTeX rendering: `mathjax-full`

Python review scripts expect these packages:

- `Pillow`
- `pdf2image`
- `python-pptx`
- `numpy`

System tools used by the review scripts:

- `soffice` / LibreOffice for PPTX to PDF conversion (auto-detected across Windows, macOS, and Linux)
- Poppler tools for PDF size and raster support used by `pdf2image`
- Font enumeration: `fc-list` (Linux), Windows registry (Windows), `system_profiler` (macOS) — auto-selected by `detect_font.py`
- Optional rasterization tools for `ensure_raster_image.py`: Inkscape, ImageMagick, Ghostscript, `heif-convert`, `JxrDecApp`

For concrete installation and verification commands, read [environment-setup.md](environment-setup.md).

## Bundled Script Notes

- `scripts/validate_deck.py`: One-command deck QA wrapper for render, montage, overflow, font, and tile review.
- `scripts/review_deck.py`: Lightweight wrapper around `validate_deck.py`.
- `scripts/slides/render_slides.py`: Convert a deck to PNGs for visual review and diffing.
- `scripts/slides/slides_test.py`: Add a gray border outside the original canvas, render, and check whether any content leaks into the border.
- `scripts/slides/create_montage.py`: Combine multiple rendered slide images into a single overview image.
- `scripts/slides/detect_font.py`: Distinguish between fonts that are missing entirely and fonts that are installed but substituted during rendering.
- `scripts/slides/ensure_raster_image.py`: Produce a PNG from common vector or unusual raster formats so you can inspect or place the asset easily.

## PptxGenJS Authoring Rules

- Default to `LAYOUT_WIDE` unless the source material clearly uses another aspect ratio.
- Set font families explicitly before measuring text.
- Use `autoFontSize`, `calcTextBox`, and related helpers to size text boxes. Do not use PptxGenJS `fit` or `autoFit`.
- Use bullet options, not literal `•` characters.
- Use `imageSizingCrop` or `imageSizingContain` instead of PptxGenJS built-in image sizing.
- Use `valign: "top"` for content boxes that may grow.
- Use `latexToSvgDataUri()` for equations and `codeToRuns()` for syntax-highlighted code blocks.
- Prefer native PowerPoint charts over rendered images when the chart is simple and likely to be edited later.
- For charts or diagrams that PptxGenJS cannot express well, render SVG externally and place the SVG in the slide.
- Include both `warnIfSlideHasOverlaps(slide, pptx)` and `warnIfSlideElementsOutOfBounds(slide, pptx)` in the submitted JavaScript whenever you generate or substantially edit slides.
- Fix all unintentional overlap and out-of-bounds warnings before delivery. If an overlap is intentional, leave a short code comment near the relevant element.

## Workspace Bootstrap

Use the bootstrap script from this skill to copy the helper bundle and local review stack into a task workspace:

```bash
python scripts/bootstrap_slides_tooling.py path/to/workspace --with-helpers
python scripts/bootstrap_slides_tooling.py path/to/workspace --with-review-scripts
python scripts/bootstrap_slides_tooling.py path/to/workspace --all
```
