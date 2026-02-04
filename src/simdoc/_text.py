from __future__ import annotations


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def escape_pipes(text: str) -> str:
    return text.replace("|", "\\|")


def select_code_fence(text: str) -> str:
    longest = 0
    current = 0
    for ch in text:
        if ch == "`":
            current += 1
            if current > longest:
                longest = current
        else:
            current = 0
    fence_len = max(3, longest + 1)
    return "`" * fence_len


def format_table_cell(value: object) -> str:
    if value is None:
        return ""
    text = normalize_newlines(str(value))
    text = text.replace("\n", "<br>")
    return escape_pipes(text)
