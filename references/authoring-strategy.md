# Authoring Strategy

## Core Principle

Choose the authoring path that produces the strongest editable `.pptx`, not the path that happens to be familiar.

Chart generation and deck authoring do not need to use the same toolchain.

## Tool Selection

### Use an existing repo generator

Use when:
- the repo already has a mature deck generator
- the existing output is close to the desired visual level
- modifying the current pipeline is faster than rewriting the deck system

### Use PptxGenJS or another JS PPT generator

Use when:
- the deck needs polished structured layout and strong native PowerPoint editability
- you want tighter control over spacing, alignment, and repeatable page patterns
- the project does not already depend on a competing generator

Recommended support:
- read [pptxgenjs-helpers.md](pptxgenjs-helpers.md)
- bootstrap the local helper bundle and review scripts into the workspace:

```bash
python scripts/bootstrap_slides_tooling.py path/to/workspace --all
```

Additional guidance for the PptxGenJS path:
- prefer PptxGenJS over `python-pptx` when both are viable and you need stronger layout control, richer helper support, or better editability for structured decks
- deliver both the `.pptx` and the authoring `.js` when JavaScript is the chosen generation path
- use the vendored helper bundle from this skill instead of reimplementing text measurement, layout warnings, crop/contain logic, code highlighting, or LaTeX rendering

### Use Python-based PPT generation

Use when:
- the repo already has a Python generator
- analysis and chart generation are tightly coupled to Python code
- the deck mainly needs controlled layout rather than highly custom native charts
- do not choose a fresh Python path from scratch if an existing repo generator or a PptxGenJS flow would reduce authoring risk and review churn

### Use a mixed pipeline

Use when:
- evidence extraction and chart generation are easiest in Python or notebooks
- final deck assembly is stronger in another authoring stack
- you need custom plots plus a highly editable final PPT

Typical split:
- analysis scripts generate charts, diagrams, metrics tables, and citations
- deck authoring tool composes the editable `.pptx`

## Hard Constraints

- Do not choose a toolchain that forces the final deck to become screenshot-only.
- Do not flatten whole slides to preserve a visual effect.
- Prefer native text, shapes, and simple charts in the final deck.
- External rendered assets are acceptable for complex diagrams, saliency plots, or paper-style figures, but they should support the deck rather than replace it.
- Keep the workflow self-contained inside this skill's vendored assets, scripts, and references. Do not depend on the external `slides` skill at authoring or validation time.

## Decision Rule

If two options are viable, choose the one that better satisfies all of these at once:

1. Editable final `.pptx`
2. Strong white-first leadership visual quality
3. Reliable evidence extraction from repo, code, experiments, and models
4. Rebuildable source workflow
5. Fast screenshot-based review and correction

Default decision order:

1. Reuse an existing mature repo generator
2. Use PptxGenJS or another JS generator for new structured decks
3. Use a mixed pipeline when analysis and authoring naturally split
4. Use Python generation only when an existing Python generator or tight analysis coupling makes it the lower-risk option
