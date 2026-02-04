from __future__ import annotations

from pathlib import Path

from simdoc import Doc


def test_table_escaping_and_order() -> None:
    doc = Doc()
    doc.table(
        [
            {"b": "x|y", "a": "1\n2"},
            {"a": None, "b": "ok"},
        ]
    )

    expected = (Path(__file__).parent / "fixtures" / "golden" / "tables.md").read_text(
        encoding="utf-8"
    )
    assert doc.to_markdown() == expected
