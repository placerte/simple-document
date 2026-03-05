# Release 0.2.0

## Title
simdoc 0.2.0

## Summary
This minor release adds Table of Contents support, upgrades PDF rendering with Eisvogel + listings, and publishes full API/toolchain documentation.

## Highlights
- Explicit TOC block with GitHub-style slug generation and deterministic rendering.
- PDF export via Pandoc + XeLaTeX with Eisvogel template and listings styling (fallback to default template on failure).
- New API reference and PDF toolchain setup guidance.

## Changes
### Added
- `Doc.toc()` block builder for Table of Contents rendering.
- Two-pass Markdown rendering to generate deterministic TOC slugs.
- `Doc.save_pdf()` for Pandoc-based PDF export with presets.
- Bundled Eisvogel template for high-quality PDF output.
- Fallback to Pandoc default template when Eisvogel fails (with warning).
- New API reference: `docs/api.md`.

### Updated
- PDF toolchain guidance in README, including platform install commands.
- Eisvogel preset now enables `--listings` for code block styling.

### Fixed
- Improved error messages for PDF rendering failures with actionable hints and Pandoc stderr.

## Compatibility
- No breaking API changes in the public surface.
- PDF export requires `pandoc` and `xelatex` on PATH.

## Migration
None required.

## Release Notes (GitHub)
**Summary**
- Added Table of Contents blocks with deterministic GitHub-style slugs.
- Upgraded PDF rendering with bundled Eisvogel template and listings styling.
- Documented full public API and PDF toolchain requirements.

**Testing**
- `uv run pytest tests/test_pdf.py -q`
- `uv run pytest`
