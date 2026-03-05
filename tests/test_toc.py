from __future__ import annotations

from simdoc import Doc


def test_toc_basic_nested() -> None:
    doc = Doc()
    doc.h1("Title")
    doc.toc()
    doc.h2("Intro")
    doc.h3("Details")
    doc.h4("Deep")
    doc.h5("Skip")

    expected = (
        "# Title\n\n"
        "## Contents\n\n"
        "- [Intro](#intro)\n"
        "  - [Details](#details)\n"
        "    - [Deep](#deep)\n\n"
        "## Intro\n\n"
        "### Details\n\n"
        "#### Deep\n\n"
        "##### Skip\n"
    )
    assert doc.to_markdown() == expected


def test_toc_duplicate_headings() -> None:
    doc = Doc()
    doc.h2("Section")
    doc.h2("Section")
    doc.toc(title=None, levels=(2, 2))

    expected = (
        "## Section\n\n## Section\n\n- [Section](#section)\n- [Section](#section-1)\n"
    )
    assert doc.to_markdown() == expected


def test_toc_level_filtering() -> None:
    doc = Doc()
    doc.h1("Top")
    doc.h2("Mid")
    doc.h3("Low")
    doc.h4("Bottom")
    doc.toc(levels=(1, 3))

    expected = (
        "# Top\n\n"
        "## Mid\n\n"
        "### Low\n\n"
        "#### Bottom\n\n"
        "## Contents\n\n"
        "- [Top](#top)\n"
        "  - [Mid](#mid)\n"
        "    - [Low](#low)\n"
    )
    assert doc.to_markdown() == expected
