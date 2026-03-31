# editable-leadership-pptx | Codex PPT Skill for Editable PowerPoint and Presentation Decks

Community-maintained Codex PPT skill, PowerPoint skill, and presentation skill for creating or revising editable `16:9 .pptx`, PowerPoint decks, and presentation decks for executive and leadership reporting.

中文说明: [README.md](./README.md)

## What This Repository Is

`editable-leadership-pptx` is a specialized skill built for leadership-facing presentation workflows. It builds on top of the Codex `slides` skill workflow and packages the relevant helper utilities and review scripts into a self-contained repository.

This repository is not an official OpenAI repository, not an official Codex release artifact, and should not be presented as endorsed or certified by OpenAI.

## Relationship to the Codex `slides` Skill

- This repository is derived from and built on the Codex `slides` skill workflow
- It bundles vendored and/or adapted local resources under `assets/pptxgenjs_helpers/` and `scripts/slides/`
- Upstream copyright notices retained in source files should remain intact
- See [NOTICE](./NOTICE) and [LICENSE.txt](./LICENSE.txt) for attribution and license context

The goal of this repository is not to replace the original `slides` capability, but to tailor it for executive deck authoring with stronger defaults for storytelling, evidence, and screenshot-based QA.

## Main Capabilities

- Editable `16:9 .pptx` output
- Executive-friendly white-first visual defaults
- Evidence-first deck authoring for project status, experiments, and evaluations
- Screenshot-based QA instead of editor-only review
- Local tooling for bootstrap, rendering, montage generation, overflow checks, and font checks
- A Codex workflow for people who need a PPT skill, PowerPoint skill, or presentation skill that still outputs editable files

## Repository Layout

```text
editable-leadership-pptx/
├─ SKILL.md
├─ README.md
├─ README.en.md
├─ NOTICE
├─ LICENSE.txt
├─ agents/
├─ references/
├─ scripts/
└─ assets/
```

## Installation

Clone the repository into your Codex skills directory using your own repository URL:

```bash
git clone <repository-url> ~/.codex/skills/editable-leadership-pptx
```

Windows example:

```powershell
git clone <repository-url> $env:USERPROFILE\.codex\skills\editable-leadership-pptx
```

## Usage

```text
Use $editable-leadership-pptx to build or revise this deck as an editable 16:9 .pptx.
```

## Development And Validation

```bash
python scripts/bootstrap_slides_tooling.py path/to/workspace --all
python scripts/review_deck.py path/to/deck.pptx
python scripts/review_deck.py path/to/deck.pptx --deep
python scripts/validate_deck.py path/to/deck.pptx --strict
```

This README intentionally avoids machine-specific paths, usernames, and private local environment assumptions.

## Open Source And Attribution Notes

- This repository contains both original project content and vendored or adapted resources derived from the Codex `slides` skill workflow
- Source files that retain upstream copyright notices such as `Copyright (c) OpenAI` should continue to preserve those notices
- `LICENSE.txt` includes the Apache License 2.0 text needed for applicable vendored resources
- The names `Codex`, `OpenAI`, and `slides` are used descriptively only, to explain origin or compatibility, and do not imply affiliation, sponsorship, or endorsement

If you plan to redistribute this repository or integrate it into an internal template system, run your own legal and open source compliance review.

## Search Keywords

If you are searching GitHub or web search engines for PPT-related skills, these keywords are included to improve discoverability:

- PPT skill
- ppt skill
- PowerPoint skill
- presentation skill
- slides skill
- editable pptx
- PowerPoint presentation generator
- executive presentation
- leadership deck
- Codex skill for PPT
- Codex PowerPoint skill
- AI PPT workflow
