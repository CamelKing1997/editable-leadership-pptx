---
name: editable-leadership-pptx
description: Use when creating or revising a leadership or executive progress deck as an editable 16:9 `.pptx` with repo-backed evidence, minimal text, restrained white-first visuals, and screenshot-based layout QA.
---

# Editable Leadership PPTX

## Overview

Create leadership decks as fully editable 16:9 `.pptx` files. Authoring implementation is flexible: use an existing repo generator, PptxGenJS, Python, or a mixed pipeline, but keep the delivered deck editable, reproducible, and visually strong.

Assume most decks in this workflow are grounded in a live project repo. Pull evidence from code, configs, experiments, model outputs, logs, metrics, and derived analysis before writing slide copy.

Load these references as needed:
- [references/executive-pptx-rules.md](references/executive-pptx-rules.md)
- [references/authoring-strategy.md](references/authoring-strategy.md)
- [references/pptxgenjs-helpers.md](references/pptxgenjs-helpers.md)
- [references/environment-setup.md](references/environment-setup.md)
- [references/apple-keynote-aesthetic.md](references/apple-keynote-aesthetic.md)

## Bundled Resources

All resources are vendored locally — this skill has **no runtime dependency on the external `slides` skill**.

### PptxGenJS Helpers (`assets/pptxgenjs_helpers/`)

Self-contained JS library (v1.2.0) for slide authoring:

| Module | Capabilities |
|--------|-------------|
| `text.js` | `autoFontSize`, `calcTextBox`, `calcTextBoxHeightSimple` — accurate text measurement via skia-canvas + fontkit |
| `layout.js` | `warnIfSlideHasOverlaps`, `warnIfSlideElementsOutOfBounds`, `alignSlideElements`, `distributeSlideElements` |
| `layout_builders.js` | `addImageTextCard`, `addCardRow`, `addThreeLevelTree` — composite layout helpers |
| `image.js` | `imageSizingCrop`, `imageSizingContain`, `getImageDimensions` — crop/contain/metadata |
| `code.js` | `codeToRuns` — syntax-highlighted code blocks via PrismJS |
| `latex.js` | `latexToSvgDataUri` — LaTeX → SVG via MathJax |
| `svg.js` | `svgToDataUri`, `sanitizeSvg` |
| `util.js` | `safeOuterShadow` |

JS dependencies: `pptxgenjs`, `skia-canvas`, `linebreak`, `fontkit`, `prismjs`, `mathjax-full`.

### Review & Validation Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `validate_deck.py` | `scripts/` | One-command QA: render + montage + overflow + font + tiles → `summary.json` |
| `review_deck.py` | `scripts/` | Fast visual review: render + montage by default, with optional overflow/font/tile checks |
| `render_slides.py` | `scripts/slides/` | PPTX/PDF → per-slide PNG |
| `create_montage.py` | `scripts/slides/` | Contact sheet from slide PNGs |
| `slides_test.py` | `scripts/slides/` | Overflow / out-of-bounds detection |
| `detect_font.py` | `scripts/slides/` | Missing vs. substituted font classification |
| `ensure_raster_image.py` | `scripts/slides/` | SVG/EMF/HEIC/PDF/EPS → PNG conversion |

### Bootstrap Script

`scripts/bootstrap_slides_tooling.py` copies helpers and/or the full local review stack from this skill's bundled resources into a task workspace:

```bash
python scripts/bootstrap_slides_tooling.py path/to/workspace --all
python scripts/bootstrap_slides_tooling.py path/to/workspace --with-helpers
python scripts/bootstrap_slides_tooling.py path/to/workspace --with-review-scripts
```

### System Requirements

Python: `pdf2image`, `Pillow`, `numpy`, `python-pptx`.
System tools: LibreOffice/`soffice`, Poppler. Optional: Inkscape, ImageMagick, Ghostscript, heif-convert.

If the environment is not ready yet, load [references/environment-setup.md](references/environment-setup.md) and follow the install and verification commands before running render-based QA.

## Low-Token Operating Mode

Optimize for speed and fewer clarification turns:

- Infer first from existing decks, templates, filenames, reports, repo structure, commit history, and generated assets before asking questions.
- Ask only for missing inputs that materially change the deck outcome.
- Keep clarification to one short round unless a blocker remains.
- If a prior approved deck or company template exists, preserve its geometry, theme rhythm, and page logic first, then improve.
- If the visual direction is already clear, skip exploratory loops and build directly.

## Workflow

1. Inspect the request and determine whether you are creating a new deck, revising an existing one, or replacing a weak HTML or screenshot-based deck with an editable `.pptx`.

2. **Intake confirmation (new deck only, infer first).** Before designing slides, infer as much as possible from the available materials. Ask the user only for missing items that materially change the deck. Use one short round of questions at most unless a blocker remains.
   - **Time range**: infer from the latest report, repo activity, filenames, or previous deck; ask only if still ambiguous
   - **Audience level**: default to leadership / business stakeholders; ask only if technical proof depth is unclear
   - **Must-include topics**: derive from repo evidence and current delta; ask only for hard constraints or politically mandatory topics
   - **Reference material**: infer from nearby decks, templates, style guides, or requested paths; ask for a file path only if no usable reference is present
   - **Expected length**: infer from the previous deck, the reporting cadence, and the amount of delta; default to 10–15 slides if not specified

   If any answer changes the defaults in step 6 (audience, aspect ratio, background style), carry those overrides forward.

3. Work in a task-local build directory. Do not overwrite the requested final deck path until rendering and validation pass.
4. Read the current source materials before designing slides:
   - previous deck
   - current report or notes
   - repo evidence
   - any existing PPT build script or generator
5. If revising an existing deck, render the current deck first so you can compare geometry, rhythm, and problem areas visually.
6. Lock the deck contract up front:
   - audience defaults to leadership or business stakeholders (override with intake answer if different)
   - output defaults to editable 16:9 `.pptx`
   - most slides default to white background and flat layout
   - cover and closing slides may use a darker branded background if deliberate and clean
7. Choose the authoring path that best preserves editability and visual quality. Do not force a language or library if another path will produce a stronger editable deck.
8. Extract only the delta since the last report. If historical callback is necessary, keep it to one setup slide.
9. Derive evidence before writing copy:
   - inspect project structure, experiment outputs, model artifacts, evaluation scripts, and metrics files
   - compute or regenerate key comparisons when the needed evidence is not already materialized
   - prefer charts and diagrams generated from repo-backed facts over prose summaries
10. Draft sample slides only when the visual direction or page structure is not yet locked:
    - if the deck is new and style is uncertain, draft up to three sample slides:
      - one business progress slide
      - one chart-heavy evidence slide
      - one technical explanation slide, only if technical proof is required
    - if an approved deck, template, or strong company visual language already exists, skip samples and move directly into full-deck production
11. Build or revise the deck:
    - set fonts explicitly
    - keep a stable spacing system across titles, captions, charts, and margins
    - keep titles, body copy, dividers, labels, timelines, and status text as native PowerPoint elements
    - top-align content boxes that may grow
    - place images intentionally: crop when the image should fill the frame, contain when preserving the full figure matters
    - prefer native PowerPoint charts for simple visuals that should remain editable
    - render only complex charts, saliency plots, and architecture diagrams as images or SVG when native objects would be weaker
    - when using PptxGenJS, load [references/pptxgenjs-helpers.md](references/pptxgenjs-helpers.md) and bootstrap the helper bundle into the task workspace if needed
    - if using PptxGenJS, use `autoFontSize`, `calcTextBox`, and related helpers instead of `fit` or `autoFit`
    - if using PptxGenJS, use bullet options instead of literal bullet glyphs
    - if using PptxGenJS, use `imageSizingCrop` or `imageSizingContain` for image placement
    - if using PptxGenJS, use `codeToRuns()` for syntax-highlighted code and `latexToSvgDataUri()` for equations when those elements are needed
    - if using PptxGenJS, include overlap and out-of-bounds diagnostics in the authoring source and resolve all unintentional warnings before delivery
12. Validate with real render output, not only the editor:
    - if required tools are missing, install them using [references/environment-setup.md](references/environment-setup.md) before continuing
    - use `scripts/review_deck.py` for fast visual iteration
    - use `scripts/validate_deck.py` for the full QA chain before delivery
    - export slides to PNG
    - build a montage or contact sheet for deck-level review
    - run an overflow or out-of-bounds check for dense decks
    - detect missing or substituted fonts when typography matters
    - normalize odd image formats before placement if source assets are SVG, EMF, HEIC, PDF, or similar
13. Review in this order:
    - story and page order
    - visual style
    - chart readability
    - wording and jargon level
    - screenshot-based layout QA: full-slide screenshots first, then local crops or tiles for dense areas
    - overflow, overlap, clipping, spacing, font, and asset issues
14. Deliver the `.pptx`, the authoring source, and any generated assets needed to rebuild the deck.

## Authoring Rules

- Editable output is mandatory. Do not rasterize full slides just to get the look right.
- Keep text, simple layout elements, separators, callouts, and straightforward charts editable whenever practical.
- Treat slide text as presentation support, not a document. Large paragraphs are prohibited.
- Default to evidence-first storytelling. Build charts, timelines, architecture visuals, and before/after comparisons from project files, code paths, experiment outputs, metrics, model checkpoints, logs, or derived analysis instead of filling space with prose.
- Use business language for leadership audiences. Translate jargon unless the page exists to prove a technical point.
- If you introduce a new model, algorithm, or architecture, include real evidence:
  - why the change was made
  - one concrete visual or chart
  - paper citations when external architecture is referenced
- Use charts to make the point obvious from a distance. Hidden labels, conflicting scales, decorative dual axes, or annotation collisions are defects.
- Screenshot review is mandatory. Do not trust code inspection alone for visual QA.
- Do not promote working files to the final destination until render, screenshot QA, overflow checks, and font checks have passed.

## Internalized Slides Capabilities

This skill internally carries the reusable `slides` capabilities needed for high-quality editable PPT authoring:

- vendored `pptxgenjs_helpers` for text measurement, layout helpers, crop/contain, SVG, LaTeX, code highlighting, and overlap diagnostics
- vendored review scripts for render, montage, overflow detection, font inspection, and asset rasterization
- local wrapper scripts for one-command deck review and workspace bootstrap

Always use these bundled resources instead of depending on the external `slides` skill.

## Apple-Keynote Aesthetic

When premium visual quality matters, load [references/apple-keynote-aesthetic.md](references/apple-keynote-aesthetic.md) and apply its rules before claiming a deck looks polished. Treat Apple-like quality as a strict review target, not a vague inspiration word.

## Recreate Or Edit Existing Slides

When revising or rebuilding from a reference deck or PDF:

- Render the source deck or reference PDF first so you can compare slide geometry visually.
- Match the original aspect ratio before rebuilding layout.
- Preserve editability where possible: text should stay text, and simple charts should stay native charts.
- If a reference slide uses raster artwork, use `scripts/slides/ensure_raster_image.py` to generate debug PNGs from vector or odd image formats before placing them.

## Screenshot QA

After every meaningful rebuild:

1. Export full-slide screenshots for the entire deck.
2. Build a contact sheet or review slides one by one for global balance.
3. For every dense chart page, architecture page, or page that previously failed review, generate local crops or tiles covering the top, middle, bottom, and crowded regions.
4. Use those images to check:
   - text or annotations covering charts
   - labels cut off by shape or canvas boundaries
   - nodes or arrows clipped at panel edges
   - objects extending off the slide
   - distorted aspect ratios after image placement
   - mismatched axis scales that weaken the intended comparison
   - visually empty dead zones caused by poor balance
   - template artifacts, ghost text, or broken background layers
   - card, caption, or title collisions after content updates
5. Fix the source layout and regenerate. Do not patch only in exported images.

Recommended command:

```bash
python scripts/validate_deck.py path/to/deck.pptx --strict
```

## Validation Commands

```bash
python scripts/bootstrap_slides_tooling.py path/to/workspace --all
python scripts/review_deck.py path/to/deck.pptx
python scripts/review_deck.py path/to/deck.pptx --deep
python scripts/validate_deck.py path/to/deck.pptx --strict
```

## Red Flags

- The deck repeats the prior report instead of showing new progress.
- A slide contains dense paragraphs or looks like speaker notes pasted into boxes.
- Visual weight comes from filled cards instead of typography, spacing, and evidence.
- A model name appears without a one-line business reason and a supporting visual.
- A chart was hand-waved instead of being generated from project, code, model, or experiment data.
- The `.pptx` exists but key text, shapes, or simple layout elements are no longer editable.
- Layout review was done from code or the PPT editor alone without full-slide screenshots and local crops.
- A chart needs explanation because the key contrast is not visually obvious.
- Fixes are attempted across story, style, copy, and layout in the same pass.
