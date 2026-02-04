from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Sequence


@dataclass(frozen=True)
class Heading:
    level: int
    text: str


@dataclass(frozen=True)
class Paragraph:
    text: str


@dataclass(frozen=True)
class ListBlock:
    ordered: bool
    items: Sequence[Any]


@dataclass(frozen=True)
class CodeBlock:
    text: str
    lang: str | None


@dataclass(frozen=True)
class TableBlock:
    headers: Sequence[str]
    rows: Sequence[Sequence[Any]]
    align: Sequence[str] | None


@dataclass(frozen=True)
class Hr:
    pass


Block = Heading | Paragraph | ListBlock | CodeBlock | TableBlock | Hr
