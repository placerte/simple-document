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


@dataclass(frozen=True)
class TocBlock:
    title: str | None
    levels: tuple[int, int]


Block = Heading | Paragraph | ListBlock | CodeBlock | TableBlock | Hr | TocBlock
