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

## Example script

Run the full example that exercises every block type:

```bash
uv run python examples/example_all_blocks.py
```

The script writes `examples/example_output.md`.
