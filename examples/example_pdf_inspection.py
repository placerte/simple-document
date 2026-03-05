from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simdoc import Doc  # type: ignore[import-not-found]


def build_document() -> Doc:
    doc = Doc()

    doc.h1("SimDoc PDF Inspection")
    doc.p("This document exercises all block types for PDF inspection.")

    doc.toc(title="Contents", levels=(2, 4))

    doc.h2("Headings")
    doc.h3("Headings")
    doc.h4("Headings")
    doc.h5("Heading Level 5 (Not in TOC by default)")
    doc.hr()

    doc.h2("Paragraphs")
    doc.p("Paragraphs preserve\ninternal newlines.")
    doc.p("Inline styling: **bold**, *italics*, ***both***.")
    doc.hr()

    doc.h2("Lists")
    doc.h3("Unordered")
    doc.ul(["alpha", ["beta", "gamma"], "delta"])
    doc.h3("Ordered")
    doc.ol(["one", ["two", "three"], "four"])
    doc.hr()

    doc.h2("Code Blocks")
    doc.h3("Fence Escalation")
    doc.code("line1\n```\nline2", lang="bash")
    doc.h3("Python Example")
    code = """def main():
    print(\"Hello World!\")
"""
    doc.code(code, lang="python")
    doc.hr()

    doc.h2("Tables")
    doc.h3("Escaping + Alignment")
    doc.table(
        [
            {"b": "x|y", "a": "1\n2"},
            {"a": None, "b": "ok"},
        ],
        headers=["a", "b"],
        align=["left", "right"],
    )
    doc.h3("Simple Table")
    doc.table(
        rows=[[1, 2], [3, 4]],
        headers=["a", "b"],
    )
    doc.hr()

    doc.h2("Horizontal Rule")
    doc.hr()

    return doc


def main() -> None:
    doc = build_document()
    output_dir = Path(__file__).parent
    markdown_path = output_dir / "example_pdf_inspection.md"
    pdf_path = output_dir / "example_pdf_inspection.pdf"
    doc.save(markdown_path)
    doc.save_pdf(pdf_path, preset="default")


if __name__ == "__main__":
    main()
