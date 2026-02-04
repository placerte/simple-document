from __future__ import annotations

from os import PathLike
from pathlib import Path


def save_markdown(text: str, path: str | PathLike[str]) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8", newline="\n")
    return output_path
