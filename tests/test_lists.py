from __future__ import annotations

from pathlib import Path

from simdoc import Doc


def test_list_rendering() -> None:
    doc = Doc()
    doc.ul(["alpha", ["beta", "gamma"], "delta"])
    doc.ol(["one", ["two", "three"]])

    expected = (Path(__file__).parent / "fixtures" / "golden" / "lists.md").read_text(
        encoding="utf-8"
    )
    assert doc.to_markdown() == expected
