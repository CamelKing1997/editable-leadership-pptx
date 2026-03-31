# Environment Setup

Read this file when the task needs deck rendering, screenshot QA, font checks, unusual asset conversion, or a JavaScript/PptxGenJS authoring stack that is not installed yet.

## Fast Path

Install only what the chosen workflow needs:

- Review and QA only: Python review dependencies + LibreOffice + Poppler
- JavaScript/PptxGenJS authoring: Node packages, plus the review stack if you also need screenshot QA
- Optional vector or odd-format asset handling: Inkscape and other raster helpers

## Python Review Stack

Use the Python environment that will run `scripts/validate_deck.py` and `scripts/slides/*.py`.

```bash
python -m pip install --upgrade pip
python -m pip install Pillow pdf2image python-pptx numpy
```

Verification:

```bash
python -c "import PIL, pdf2image, pptx, numpy; print('python review deps ok')"
```

## JavaScript / PptxGenJS Stack

Use this when the final deck is authored in JavaScript or PptxGenJS.

```bash
npm install pptxgenjs skia-canvas linebreak fontkit prismjs mathjax-full
```

Verification:

```bash
node -e "require('pptxgenjs'); require('skia-canvas'); require('linebreak'); require('fontkit'); require('prismjs'); require('mathjax-full'); console.log('js ppt deps ok')"
```

## System Tools by Platform

### Windows

```bash
winget install -e --id TheDocumentFoundation.LibreOffice
winget install -e --id oschwartz10612.Poppler
```

Optional:

```bash
winget install -e --id Inkscape.Inkscape
```

Verification:

```bash
where soffice
where pdfinfo
where pdftoppm
```

If `pdfinfo` or `pdftoppm` is still not found after installing Poppler, add the Poppler `bin` directory to `PATH`, then open a new terminal and re-run the checks.

### macOS

```bash
brew install --cask libreoffice
brew install poppler
```

Optional:

```bash
brew install --cask inkscape
brew install imagemagick ghostscript
```

Verification:

```bash
which soffice
which pdfinfo
which pdftoppm
```

If `soffice` is not found after installing LibreOffice, it lives at `/Applications/LibreOffice.app/Contents/MacOS/soffice`. Either add that directory to `PATH` or create a symlink:

```bash
ln -s /Applications/LibreOffice.app/Contents/MacOS/soffice /usr/local/bin/soffice
```

### Linux (Debian / Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y libreoffice-impress poppler-utils
```

Optional:

```bash
sudo apt-get install -y inkscape imagemagick ghostscript
```

Verification:

```bash
which soffice
which pdfinfo
which pdftoppm
```

## Font Detection Notes

The bundled `detect_font.py` script enumerates installed system fonts to classify requested font families as missing or substituted. It supports three backends, chosen automatically:

| Platform | Backend | Notes |
|----------|---------|-------|
| Linux | `fc-list` (fontconfig) | Available by default on most distros |
| macOS | `system_profiler SPFontsDataType` | Built-in, no extra install needed |
| Windows | Windows registry (`HKLM\...\Fonts`) | Built-in, no extra install needed |

If `fc-list` is available on any platform (e.g., via MSYS2 on Windows or Homebrew fontconfig on macOS), it takes priority. Otherwise the platform-native backend is used. If no backend produces results, font checks report all fonts as missing — install LibreOffice and the required presentation fonts, then retry.

## Typical Setup Recipes

### Recipe 1: Minimal review environment (Windows)

```bash
python -m pip install --upgrade pip
python -m pip install Pillow pdf2image python-pptx numpy
winget install -e --id TheDocumentFoundation.LibreOffice
winget install -e --id oschwartz10612.Poppler
```

Then verify:

```bash
python -c "import PIL, pdf2image, pptx, numpy; print('python review deps ok')"
where soffice
where pdfinfo
```

### Recipe 1b: Minimal review environment (macOS)

```bash
python -m pip install --upgrade pip
python -m pip install Pillow pdf2image python-pptx numpy
brew install --cask libreoffice
brew install poppler
```

Then verify:

```bash
python -c "import PIL, pdf2image, pptx, numpy; print('python review deps ok')"
which soffice || ls /Applications/LibreOffice.app/Contents/MacOS/soffice
which pdfinfo
```

### Recipe 2: Full editable leadership PPT environment (Windows)

```bash
python -m pip install --upgrade pip
python -m pip install Pillow pdf2image python-pptx numpy
npm install pptxgenjs skia-canvas linebreak fontkit prismjs mathjax-full
winget install -e --id TheDocumentFoundation.LibreOffice
winget install -e --id oschwartz10612.Poppler
winget install -e --id Inkscape.Inkscape
```

Then verify:

```bash
python -c "import PIL, pdf2image, pptx, numpy; print('python review deps ok')"
node -e "require('pptxgenjs'); require('skia-canvas'); require('linebreak'); require('fontkit'); require('prismjs'); require('mathjax-full'); console.log('js ppt deps ok')"
where soffice
where pdfinfo
```

### Recipe 2b: Full editable leadership PPT environment (macOS)

```bash
python -m pip install --upgrade pip
python -m pip install Pillow pdf2image python-pptx numpy
npm install pptxgenjs skia-canvas linebreak fontkit prismjs mathjax-full
brew install --cask libreoffice
brew install poppler
brew install --cask inkscape
```

Then verify:

```bash
python -c "import PIL, pdf2image, pptx, numpy; print('python review deps ok')"
node -e "require('pptxgenjs'); require('skia-canvas'); require('linebreak'); require('fontkit'); require('prismjs'); require('mathjax-full'); console.log('js ppt deps ok')"
which soffice || ls /Applications/LibreOffice.app/Contents/MacOS/soffice
which pdfinfo
```

## Troubleshooting

- `ModuleNotFoundError: No module named 'pdf2image'`
  Install the Python review stack in the same Python environment used to run the wrapper.
- `soffice` not found
  Install LibreOffice, reopen the terminal, and verify with `where soffice` (Windows) or `which soffice` (macOS/Linux). On macOS, the binary is at `/Applications/LibreOffice.app/Contents/MacOS/soffice` — you may need to add it to `PATH` or create a symlink.
- `pdfinfo` or `pdftoppm` not found
  Install Poppler and ensure its `bin` directory is on `PATH`.
- `Cannot find module 'skia-canvas'` or similar Node errors
  Run the JavaScript/PptxGenJS install command in the workspace where the deck authoring code executes.
- Font checks behave unexpectedly
  Re-run after LibreOffice is installed and the required presentation fonts are present on the machine. On Windows the script reads fonts from the registry; on macOS it uses `system_profiler`; on Linux it uses `fc-list`. If none of these produce results, font detection will conservatively report all fonts as missing.

## Rule Of Thumb

If the task needs only editable deck generation, you do not need to install every optional tool.

If the task needs screenshot QA, full-slide rendering, montage generation, or overflow and font validation, the Python review stack plus LibreOffice and Poppler are required.
