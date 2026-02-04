# AGENTS.md
# Guidance for coding agents working in this repo.

## Scope and repo status

- This repository is currently a design/spec repository.
- The only substantive guidance is in `docs/handoff_260203_1.md` and `docs/llm-persona.md`.
- There is no `src/` or `tests/` directory yet, and no build or lint config files.
- Follow the specs exactly; do not invent behavior beyond the locked decisions.

## Cursor/Copilot rules

- No Cursor rules found in `.cursor/rules/` or `.cursorrules`.
- No Copilot rules found in `.github/copilot-instructions.md`.

## Build, lint, and test commands

There is no configured tooling yet (no `pyproject.toml`, `pytest.ini`, etc.).
When implementation lands, prefer the `uv` workflow and `pytest` for tests.

### Expected/placeholder commands (use once config exists)

- Install deps: `uv sync`
- Run app/build (if added later): `uv run python -m simdoc` (placeholder)
- Lint (if ruff is added): `uv run ruff check src tests`
- Format (if ruff/black is added): `uv run ruff format src tests`
- Type-check (if mypy is added): `uv run mypy src`

### Tests

- Run all tests (pytest expected): `uv run pytest`
- Run a single file: `uv run pytest tests/test_tables.py`
- Run a single test by name: `uv run pytest -k test_render_table`
- Run a single test node: `uv run pytest tests/test_tables.py::test_render_table`

Note: Update this section when real commands/configs land.

## Code style and architecture guidelines

### Language and tooling

- Python only.
- Favor a minimal dependency footprint.
- Use `uv` for packaging and execution once added.

### Design constraints from the spec

- Document is append-only; no insert/reorder in v0.
- Public API is explicit convenience methods on the document object.
- Output is deterministic; spacing and newlines are strictly controlled.
- No implicit line wrapping; renderer is canonical authority.
- Markdown is the only export in v0.

### Module boundaries (from spec)

- Public API is exported from `simdoc/__init__.py` only.
- Internal modules are private and subject to change.
- Rendering logic lives in a dedicated renderer module.
- Blocks are private record types; no public block classes in v0.

### Imports

- Order: standard library, third-party, local.
- Keep imports explicit; avoid wildcard imports.
- Avoid dynamic imports and reflection.

### Formatting and layout

- Keep code readable and straightforward.
- Prefer explicit loops and clear control flow over clever expressions.
- Avoid dense comprehensions that reduce clarity.
- Keep functions small and single-purpose.
- Use blank lines to separate logical sections.

### Types

- Type hints are preferred for public APIs.
- Use simple, explicit types; avoid complex generics unless necessary.
- Prefer `Path` or `PathLike` for file paths when I/O is involved.

### Naming

- Public API names should match the spec: `Doc`, `h1..h6`, `h`, `p`, `ul`, `ol`,
  `code`, `table`, `hr`, `to_markdown`, `save`.
- Private modules and types should be prefixed or placed in private modules.
- Use descriptive names; avoid abbreviations unless standard.

### Error handling

- Use a single custom base exception for document/render issues (per spec).
- I/O should raise standard Python exceptions.
- Prefer early validation where it is cheap and deterministic.

### Determinism requirements (critical)

- Exactly one blank line between top-level blocks.
- Exactly one trailing newline at document end.
- Normalize newlines to `\n` internally.
- No automatic line wrapping.
- Markdown rendering is the canonical, deterministic output.

### Markdown-specific behavior

- Headings are ATX only, levels 1..6.
- Unordered lists use `-`, ordered lists use `1.` for all items.
- Code fences must be safe; auto-escalate fence length deterministically.
- Table rendering must be valid GFM; escape pipes and convert newlines to `<br>`.
- For list-of-dicts tables: headers order is deterministic (sorted if not provided).

### Testing conventions (expected)

- Golden-file tests should compare output to `tests/fixtures/golden/*.md`.
- Unit tests should cover fence escalation, table escaping, list rendering, spacing.
- Keep tests deterministic and focused on renderer invariants.

## Contribution notes for agents

- Do not add new behavior beyond the locked spec without explicit instruction.
- Avoid introducing frameworks or heavy abstractions.
- Keep changes minimal, readable, and aligned with the spec.
- Update this file if tooling or structure changes.
