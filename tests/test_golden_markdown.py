from __future__ import annotations

from pathlib import Path

from simdoc import Doc


def test_golden_basic() -> None:
    doc = Doc()
    doc.h1("Simple Document")
    doc.p("First line\nSecond line")
    doc.hr()
    doc.h2("Next")
    doc.p("Final paragraph.")

    expected = (Path(__file__).parent / "fixtures" / "golden" / "basic.md").read_text(
        encoding="utf-8"
    )
    assert doc.to_markdown() == expected
