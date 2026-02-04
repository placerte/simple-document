from __future__ import annotations

from pathlib import Path

from simdoc import Doc


def test_code_fence_escalation() -> None:
    doc = Doc()
    doc.code("line1\n```\nline2", lang="py")

    expected = (
        Path(__file__).parent / "fixtures" / "golden" / "code_fences.md"
    ).read_text(encoding="utf-8")
    assert doc.to_markdown() == expected
