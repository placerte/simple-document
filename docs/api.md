# simdoc API Reference

Public APIs are exposed from `simdoc.__init__`.

## Public Surface

### Doc

Append-only document builder. All builder methods return `None`.

**Construction**

```python
from simdoc import Doc

doc = Doc()
```

**Block Builders**

- `h(level, text)`: Append an ATX heading with explicit level (1..6).
- `h1(text)` .. `h6(text)`: Append heading at a fixed level.
- `p(text)`: Append a paragraph; ignores empty/whitespace-only text.
- `ul(items)`: Append an unordered list. Nested lists via nested Python lists.
- `ol(items)`: Append an ordered list. Nested lists via nested Python lists.
- `code(text, lang=None)`: Append a fenced code block; uses a safe fence.
- `table(rows, headers=None, align=None)`: Append a table.
  - `rows` supports list-of-lists or list-of-dicts.
  - `headers` controls column order; defaults to sorted keys for dict rows.
  - `align` accepts `left|center|right` (or `l|c|r`) per column.
- `hr()`: Append a horizontal rule.
- `toc(title="Contents", levels=(2, 4))`: Append a Table of Contents block.
  - `levels` is a `(min, max)` tuple within 1..6.
  - `title=None` omits the TOC heading.

**Export**

- `to_markdown() -> str`: Render the document to deterministic Markdown.
- `save(path) -> Path`: Write Markdown to disk (UTF-8, `\n` newlines).
- `save_pdf(path, preset="default", pandoc_args=None) -> Path`: Render to PDF via Pandoc.
  - `preset="default"` uses the Eisvogel template + XeLaTeX.
  - `pandoc_args` are appended to the Pandoc command.
  - If Eisvogel fails, simdoc falls back to the Pandoc default template and emits a warning.

**Introspection**

- `len(doc)` or `doc.block_count`: Number of blocks.

### SimDocError

Base exception type for document and render issues.

## Deterministic Rendering Rules (Highlights)

- Exactly one blank line between top-level blocks.
- Exactly one trailing newline at document end.
- No automatic line wrapping.
- Tables are valid GFM with escaped pipes and `<br>` for internal newlines.
- Code fences auto-escalate to remain safe for content.

## Contact Points & Integrations

- **Filesystem output**: `save()` and `save_pdf()` write to disk, creating parent directories.
- **Pandoc**: `save_pdf()` requires `pandoc` on PATH.
- **TeX engine**: `save_pdf()` requires `xelatex` on PATH.
- **Eisvogel template**: Bundled in `simdoc.templates` and used by default.
- **Warnings**: If Eisvogel fails, a `RuntimeWarning` is emitted before falling back.
