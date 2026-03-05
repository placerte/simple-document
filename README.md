# simple-document

Deterministic, append-only Markdown documents with a small, explicit Python API.

## Installation

```bash
uv add simdoc
```

Or with pip:

```bash
pip install simdoc
```

## Usage

```python
from simdoc import Doc

doc = Doc()
doc.h1("Simple Document")
doc.p("First line\nSecond line")
doc.ul(["alpha", ["beta", "gamma"], "delta"])
doc.code("print('hi')", lang="py")
doc.table([
    {"b": "x|y", "a": "1\n2"},
    {"a": None, "b": "ok"},
])
doc.hr()

markdown = doc.to_markdown()
doc.save("example.md")
```

## API Reference

See the full API and integration notes in `docs/api.md`.

## Example script

Run the full example that exercises every block type:

```bash
uv run python examples/example_all_blocks.py
```

The script writes `examples/example_output.md`.

## PDF Rendering

simdoc uses Pandoc + XeLaTeX with the Eisvogel LaTeX template.

### PDF Toolchain Setup

System requirements:

- pandoc
- a TeX distribution with xelatex

Recommended installations:

Linux:
  sudo apt install pandoc texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra

Windows:
  Install Pandoc + MiKTeX (enable automatic package installation)

macOS:
  brew install pandoc
  brew install --cask mactex

Template project:
https://github.com/Wandmalfarbe/pandoc-latex-template

Thanks to Pascal Wagler and contributors for the template.
