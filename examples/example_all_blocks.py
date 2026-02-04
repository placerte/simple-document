from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from simdoc import Doc  # type: ignore[import-not-found]


def build_document() -> Doc:
    doc = Doc()

    doc.h1("Simple Document - All Blocks Example")
    doc.hr()

    doc.h2("Headings")
    doc.h1("Level 1")
    doc.h2("Level 2")
    doc.h(2, "Heading via h(level, text) - Level is 2 here")
    doc.h3("Level 3")
    doc.h4("Level 4")
    doc.h5("Level 5")
    doc.h6("Level 6")
    doc.hr()

    doc.h2("Text")
    doc.p("Paragraphs preserve\ninternal newlines.")
    doc.p("Inline styling: this should be **bold** and this *italics* and this ***both***.")
    doc.hr()

    doc.h2("Lists")
    doc.h3("Unordered")
    doc.ul(["alpha", ["beta", "gamma"], "delta"])
    doc.h3("Ordered")
    doc.ol(["one", ["two", "three"], "four"])
    doc.hr()

    doc.h2("Code Blocks")
    doc.h3("Wack Example")
    doc.code("line1\n```\nline2", lang="bash")
    doc.h3("Python Hello World")
    code: str = """
    def main():
        print(\"Hello World!\")
    """
    doc.code(code, lang="python")
    doc.hr()

    doc.h2("Tables")
    doc.h3("Wack Example")
    doc.table(
        [
            {"b": "x|y", "a": "1\n2"},
            {"a": None, "b": "ok"},
        ],
        headers=["a", "b"],
        align=["left", "right"],
    )
    doc.h3("Simple Example")
    doc.table(
        rows=[
            [1,2],
            [3,4]
        ],
        headers=["a", "b"],
    )
    doc.hr()

    doc.h2("Horizontal Bar")
    doc.hr()

    return doc


def main() -> None:
    doc = build_document()
    _markdown = doc.to_markdown()
    output_path = Path(__file__).parent / "example_output.md"
    doc.save(output_path)


if __name__ == "__main__":
    main()
