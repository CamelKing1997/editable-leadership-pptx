# Executive PPTX Rules

## Intake Defaults

- Primary audience: leadership, business stakeholders, or decision makers
- Primary question: what changed, what improved, what is next
- Output: editable `.pptx` plus rebuildable authoring source
- Aspect ratio: 16:9 unless source material proves otherwise
- History: use only as setup; progress is the story
- Evidence should come from the active project repo, code, experiment outputs, model artifacts, or evaluation data whenever possible
- Work in a task-local build directory and publish to the final path only after validation

## Low-Token Intake Rules

- Infer from existing decks, templates, style guides, repo files, filenames, and recent reports before asking the user anything.
- Ask only for missing inputs that materially change the deck outcome.
- Keep clarification to one short round unless a blocker remains.
- If a previous approved deck exists, infer audience level, page count rhythm, visual system, and section cadence from it first.
- If no slide-count target is given, infer it from the reporting cadence and the amount of real delta; otherwise default to 10–15 slides.
- If a company template already locks visual language, skip exploratory style loops and move to production.

## Copy Rules

- Use short titles with a conclusion, not a topic label.
- Keep slide text sparse enough that the presenter does the talking.
- Large text blocks are prohibited. If a slide contains a paragraph, cut it into labels, captions, or remove it.
- Remove inflated language. Prefer precise claims over celebratory language.
- Rewrite technical terms into business language unless a technical proof page requires them.
- If a slide contains more than one dense paragraph, it is probably a document page, not a presentation page.

## Visual Rules

- Default to white pages with flat composition.
- Use thin rules, modest accent lines, and low-saturation colors.
- Avoid big filled rectangles, oversized rounded cards, glossy effects, and decorative gradients.
- Use dark branded backgrounds only on purpose, typically cover or closing.
- Keep generous margins and visible breathing room between content groups.
- Set fonts explicitly. Do not accept PowerPoint's default typography just because it is available.
- Reuse stable spacing values across the deck: title baseline, top margin, column gutter, caption gap, and footer offset.
- Treat image placement as a design choice:
  - crop when the image should own the frame
  - contain when preserving the full figure or paper diagram matters
- Top-align content areas that may grow so edits change height downward instead of shifting vertical rhythm unpredictably.
- For simple visuals, prefer clean native PowerPoint charts so the result stays editable and visually consistent with the rest of the deck.
- For custom diagrams or high-density charts, render them externally, then place them carefully with correct aspect ratio and clear surrounding whitespace.
- For premium visual quality, load [apple-keynote-aesthetic.md](apple-keynote-aesthetic.md) and review against its checklist before shipping.

## Editability Rules

- Editable `.pptx` output is mandatory.
- Keep titles, subtitles, captions, labels, and callouts as native text.
- Keep separators, simple timelines, and status markers as native shapes.
- Use native PowerPoint charts only when they are straightforward and stable.
- Use external PNG or SVG only for complex plots, saliency maps, architecture diagrams, or other visuals that are painful to maintain natively.
- Never flatten an entire slide into one image.
- Do not convert editable chart pages into screenshot-only pages just to avoid layout work.
- Always preserve the generator or update the existing source script instead of making manual-only deck edits.

## Evidence Extraction Rules

- Read the repo before drafting copy. Do not start from abstract slide titles alone.
- Prefer generating charts from:
  - evaluation CSV or JSON files
  - prediction outputs
  - training logs
  - model checkpoints and weight analysis
  - code structure or config comparisons
- If the needed view does not already exist, write a small analysis script and generate the chart.
- Prefer one strong chart from real data over three decorative callout boxes.
- External paper figures are allowed for architecture explanation, but local project evidence takes priority for claims about results or decisions.

## Screenshot Review Rules

- Export the whole deck to slide images after each serious layout pass.
- Build a montage or contact sheet for the full deck when global rhythm or consistency is in doubt.
- Review both:
  - full-slide screenshots for composition, hierarchy, and whitespace
  - local crops or tiles for dense regions, chart corners, architecture panels, and any page that was recently modified
- Use screenshot review to explicitly catch:
  - overlap between labels, titles, captions, and charts
  - clipping at shape, panel, or slide boundaries
  - off-canvas elements
  - image distortion from bad aspect-ratio placement
  - annotation boxes covering the data they explain
  - inconsistent comparison scales across before/after charts
  - template background failures or stray artifacts
  - sparse pages with large dead zones that signal weak balance
- If a defect is found, fix the generating source or the inserted asset, then re-export screenshots and recheck.

## Validation Rules

- Do not trust the PowerPoint editor view alone; validate from rendered slide images.
- If validation tools are missing, install them first using [environment-setup.md](environment-setup.md) instead of skipping QA.
- Run an overflow or out-of-bounds check when layouts are dense or close to slide edges.
- Check for missing or substituted fonts when typography or brand consistency matters.
- Normalize awkward source assets before use. If a diagram or figure arrives as SVG, EMF, WMF, HEIC, PDF, or another non-trivial format, rasterize or convert it intentionally before placement or review.
- Prefer SVG over PNG for diagrams when the selected authoring path supports it cleanly; otherwise use a high-resolution raster export.
- When using the JavaScript/PptxGenJS path, prefer this skill's vendored helper bundle for text measurement, crop/contain logic, code highlighting, LaTeX rendering, and overlap or boundary diagnostics.
- When generating or substantially editing a deck in PptxGenJS, include overlap and out-of-bounds checks in the authoring source and fix all unintentional warnings before delivery.
- If you bootstrap tooling into a task workspace, keep the copied wrappers and `scripts/slides/` subtree together so the local validation chain remains runnable without external dependencies.

Recommended local tools in this skill:

- `scripts/review_deck.py` for fast visual review during iteration
- `scripts/validate_deck.py`
- `scripts/review_deck.py --deep` when you want review-mode behavior plus the full bundled checks
- `scripts/slides/render_slides.py`
- `scripts/slides/create_montage.py`
- `scripts/slides/slides_test.py`
- `scripts/slides/detect_font.py`
- `scripts/slides/ensure_raster_image.py`

## Technical Evidence Rules

When a technical section is necessary, follow this order:

1. State the business reason for the page.
2. Show the evidence visually.
3. Add one short interpretation line.
4. Add citations if the architecture or method comes from a paper.

Do not include algorithm names by themselves. A leadership audience needs a reason, a picture, and a consequence.

## Default Slide Spine

Use this only as a starting point; cut or merge pages aggressively.

1. Cover
2. What this report covers
3. Last report issue recap, maximum one slide
4. Progress item 1 with before/after evidence
5. Progress item 2 with before/after evidence
6. Progress item 3 or remaining risk
7. Why the new method or model was introduced
8. Architecture or mechanism visual
9. Evidence chart
10. Quantitative result summary
11. Near-term next steps
12. Closing

## Review Order

Run reviews in this order and do not mix them:

1. Story review
   - Are we telling only the new progress?
   - Is each slide answering a leadership question?
2. Style review
   - Are there large blocks, noisy shapes, or over-saturated accents?
   - Does the deck feel restrained rather than decorative?
3. Chart review
   - Is the intended contrast obvious from a distance?
   - Are axes, labels, and annotations readable and not colliding?
4. Copy review
   - Is jargon translated?
   - Is the tone precise instead of grandiose?
5. Layout bug review
   - Any overflow, overlap, clipping, or template artifacts?

## Common Failure Modes

- Writing directly into the final deck path before validation
- Rebuilding the whole deck before the visual direction is locked when no reference exists
- Using the previous report as the main structure instead of the current delta
- Filling empty space with cards rather than deleting weak content
- Writing explanatory paragraphs because the needed chart was never generated
- Adding a technical page without real evidence from code, data, or models
- Missing a layout regression because only the editor preview was checked
- Shipping a deck with substituted fonts or distorted external assets
- Declaring the deck done without capturing screenshots of the whole deck and the risky local regions
- Trying to solve style and story problems by changing colors only
- Asking the user for information that could have been inferred from the existing deck, repo, or file layout
