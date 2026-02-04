from __future__ import annotations

from typing import Sequence

from .._blocks import CodeBlock, Heading, Hr, ListBlock, Paragraph, TableBlock
from .._errors import SimDocError
from .._text import format_table_cell, normalize_newlines, select_code_fence


def render_markdown(blocks: Sequence[object]) -> str:
    parts: list[str] = []
    for block in blocks:
        parts.append(_render_block(block))
    if not parts:
        return "\n"
    return "\n\n".join(parts) + "\n"


def _render_block(block: object) -> str:
    if isinstance(block, Heading):
        return _render_heading(block)
    if isinstance(block, Paragraph):
        return block.text
    if isinstance(block, ListBlock):
        return _render_list(block)
    if isinstance(block, CodeBlock):
        return _render_code(block)
    if isinstance(block, TableBlock):
        return _render_table(block)
    if isinstance(block, Hr):
        return "---"
    raise SimDocError(f"unknown block type: {type(block)!r}")


def _render_heading(block: Heading) -> str:
    prefix = "#" * block.level
    return f"{prefix} {block.text}"


def _render_list(block: ListBlock) -> str:
    lines = _render_list_items(block.items, ordered=block.ordered, level=0)
    return "\n".join(lines)


def _render_list_items(items: Sequence[object], ordered: bool, level: int) -> list[str]:
    lines: list[str] = []
    indent = "  " * level
    marker = "1." if ordered else "-"
    for item in items:
        if isinstance(item, (list, tuple)):
            lines.extend(_render_list_items(item, ordered=ordered, level=level + 1))
            continue
        text = "" if item is None else str(item)
        text = normalize_newlines(text)
        if "\n" in text:
            continuation = "\n" + indent + "  "
            text = text.replace("\n", continuation)
        lines.append(f"{indent}{marker} {text}")
    return lines


def _render_code(block: CodeBlock) -> str:
    fence = select_code_fence(block.text)
    lang = block.lang or ""
    first_line = f"{fence}{lang}" if lang else fence
    closing_newline = "" if block.text.endswith("\n") else "\n"
    return f"{first_line}\n{block.text}{closing_newline}{fence}"


def _render_table(block: TableBlock) -> str:
    headers = list(block.headers)
    rows = [list(row) for row in block.rows]
    column_count = max(len(headers), max((len(row) for row in rows), default=0))
    if column_count == 0:
        raise SimDocError("table requires at least one column")

    headers = _pad_row(headers, column_count)
    rows = [_pad_row(row, column_count) for row in rows]
    align = _normalize_alignment(block.align, column_count)

    header_line = _format_row(headers)
    align_line = _format_alignment_row(align)
    row_lines = [_format_row(row) for row in rows]

    return "\n".join([header_line, align_line, *row_lines])


def _pad_row(row: Sequence[object], width: int) -> list[object]:
    padded = list(row)
    if len(padded) < width:
        padded.extend([""] * (width - len(padded)))
    return padded[:width]


def _normalize_alignment(align: Sequence[str] | None, width: int) -> list[str]:
    if align is None:
        return ["left"] * width
    normalized: list[str] = []
    for value in align:
        name = value.lower()
        if name in {"left", "l"}:
            normalized.append("left")
        elif name in {"center", "c"}:
            normalized.append("center")
        elif name in {"right", "r"}:
            normalized.append("right")
        else:
            raise SimDocError(f"invalid alignment value: {value!r}")
    if len(normalized) < width:
        normalized.extend(["left"] * (width - len(normalized)))
    return normalized[:width]


def _format_row(cells: Sequence[object]) -> str:
    rendered = [format_table_cell(cell) for cell in cells]
    return f"| {' | '.join(rendered)} |"


def _format_alignment_row(align: Sequence[str]) -> str:
    markers: list[str] = []
    for value in align:
        if value == "left":
            markers.append("---")
        elif value == "center":
            markers.append(":---:")
        elif value == "right":
            markers.append("---:")
        else:
            raise SimDocError(f"invalid alignment value: {value!r}")
    return f"| {' | '.join(markers)} |"
