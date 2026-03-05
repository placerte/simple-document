from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from importlib import resources
from os import PathLike
from pathlib import Path
import shutil
import subprocess
import tempfile
import warnings
from typing import Any

from ._blocks import CodeBlock, Heading, Hr, ListBlock, Paragraph, TableBlock, TocBlock
from ._errors import SimDocError
from ._io import save_markdown
from ._render.markdown import render_markdown
from ._text import normalize_newlines


class Doc:
    """Append-only document builder."""

    def __init__(self) -> None:
        self._blocks: list[
            Heading | Paragraph | ListBlock | CodeBlock | TableBlock | Hr | TocBlock
        ] = []

    def __len__(self) -> int:
        return len(self._blocks)

    @property
    def block_count(self) -> int:
        return len(self._blocks)

    def __repr__(self) -> str:
        return f"Doc(blocks={len(self._blocks)})"

    def h(self, level: int, text: object) -> None:
        if level not in {1, 2, 3, 4, 5, 6}:
            raise SimDocError("heading level must be between 1 and 6")
        value = "" if text is None else str(text)
        value = normalize_newlines(value).replace("\n", " ")
        self._blocks.append(Heading(level=level, text=value))

    def h1(self, text: object) -> None:
        self.h(1, text)

    def h2(self, text: object) -> None:
        self.h(2, text)

    def h3(self, text: object) -> None:
        self.h(3, text)

    def h4(self, text: object) -> None:
        self.h(4, text)

    def h5(self, text: object) -> None:
        self.h(5, text)

    def h6(self, text: object) -> None:
        self.h(6, text)

    def p(self, text: object) -> None:
        value = "" if text is None else str(text)
        value = normalize_newlines(value)
        if value.strip() == "":
            return None
        self._blocks.append(Paragraph(text=value))

    def ul(self, items: Iterable[Any]) -> None:
        self._append_list(False, items)

    def ol(self, items: Iterable[Any]) -> None:
        self._append_list(True, items)

    def _append_list(self, ordered: bool, items: Iterable[Any]) -> None:
        if items is None:
            raise SimDocError("list items cannot be None")
        self._blocks.append(ListBlock(ordered=ordered, items=list(items)))

    def code(self, text: object, lang: object | None = None) -> None:
        value = "" if text is None else str(text)
        value = normalize_newlines(value)
        language = None if lang is None else str(lang)
        self._blocks.append(CodeBlock(text=value, lang=language))

    def table(
        self,
        rows: Iterable[Sequence[Any]] | Iterable[Mapping[str, Any]],
        headers: Iterable[object] | None = None,
        align: Iterable[object] | None = None,
    ) -> None:
        if rows is None:
            raise SimDocError("table rows cannot be None")

        rows_list = list(rows)
        headers_list = (
            ["" if h is None else str(h) for h in headers] if headers else None
        )
        align_list = [str(a) for a in align] if align else None

        if rows_list and isinstance(rows_list[0], Mapping):
            dict_rows: list[Mapping[str, Any]] = []
            for row in rows_list:
                if not isinstance(row, Mapping):
                    raise SimDocError("mixed table row types are not supported")
                dict_rows.append(row)
            if headers_list is None:
                keys: set[str] = set()
                for row in dict_rows:
                    keys.update(row.keys())
                headers_list = sorted(keys)
            rows_values = [
                [row.get(header) for header in headers_list] for row in dict_rows
            ]
        else:
            rows_values = []
            for row in rows_list:
                if isinstance(row, Mapping):
                    raise SimDocError("mixed table row types are not supported")
                if not isinstance(row, Sequence) or isinstance(row, (str, bytes)):
                    raise SimDocError("table rows must be sequences")
                rows_values.append(list(row))
            if headers_list is None:
                max_cols = max((len(row) for row in rows_values), default=0)
                headers_list = [""] * max_cols

        if headers_list is None:
            headers_list = []

        self._blocks.append(
            TableBlock(headers=headers_list, rows=rows_values, align=align_list)
        )

    def hr(self) -> None:
        self._blocks.append(Hr())

    def toc(
        self,
        title: str | None = "Contents",
        levels: tuple[int, int] = (2, 4),
    ) -> None:
        if levels is None:
            raise SimDocError("toc levels must be a (min, max) tuple")
        try:
            min_level, max_level = levels
        except (TypeError, ValueError):
            raise SimDocError("toc levels must be a (min, max) tuple") from None
        try:
            valid_range = 1 <= min_level <= max_level <= 6
        except TypeError:
            raise SimDocError("toc levels must be within 1..6") from None
        if not valid_range:
            raise SimDocError("toc levels must be within 1..6")
        self._blocks.append(TocBlock(title=title, levels=(min_level, max_level)))

    def to_markdown(self) -> str:
        return render_markdown(self._blocks)

    def save(self, path: str | PathLike[str]) -> Any:
        text = self.to_markdown()
        return save_markdown(text, path)

    def save_pdf(
        self,
        path: str | PathLike[str],
        *,
        preset: str | None = "default",
        pandoc_args: list[str] | None = None,
    ) -> Path:
        if shutil.which("pandoc") is None or shutil.which("xelatex") is None:
            raise SimDocError(
                "PDF rendering requires pandoc and a TeX distribution (xelatex).\n"
                "See README: PDF Toolchain Setup."
            )

        output_path = Path(path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        markdown = self.to_markdown()

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_path = Path(tmpdir) / "simdoc_temp.md"
            temp_path.write_text(markdown, encoding="utf-8", newline="\n")
            preset_args = _resolve_preset_args(preset)
            args = ["pandoc", str(temp_path), "-o", str(output_path)]
            args.extend(preset_args)
            if pandoc_args:
                args.extend(pandoc_args)
            try:
                subprocess.run(args, check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as exc:
                if _should_fallback_to_plain(preset):
                    warnings.warn(
                        "Eisvogel template failed; falling back to Pandoc default template.",
                        RuntimeWarning,
                    )
                    fallback_args = ["pandoc", str(temp_path), "-o", str(output_path)]
                    fallback_args.append("--pdf-engine=xelatex")
                    if pandoc_args:
                        fallback_args.extend(pandoc_args)
                    try:
                        subprocess.run(
                            fallback_args, check=True, capture_output=True, text=True
                        )
                    except subprocess.CalledProcessError as fallback_exc:
                        raise SimDocError(
                            _format_pandoc_error(fallback_exc.stderr)
                        ) from None
                else:
                    raise SimDocError(_format_pandoc_error(exc.stderr)) from None

        return output_path


def _resolve_preset_args(preset: str | None) -> list[str]:
    if preset == "default":
        preset = "eisvogel"
    if preset is None:
        return []

    if preset == "eisvogel":
        return [
            "--template",
            _get_eisvogel_template(),
            "--pdf-engine=xelatex",
            "--listings",
        ]

    if preset == "article":
        return ["--pdf-engine=xelatex"]

    raise SimDocError(f"unknown pdf preset: {preset!r}")


def _get_eisvogel_template() -> str:
    path = resources.files("simdoc.templates") / "eisvogel.latex"
    return str(path)


def _should_fallback_to_plain(preset: str | None) -> bool:
    return preset in {"default", "eisvogel"}


def _format_pandoc_error(stderr: str | None) -> str:
    output = (stderr or "").strip()
    if output == "":
        output = "<no stderr output>"
    return (
        "PDF rendering failed.\n\n"
        "Ensure the following are installed:\n\n"
        "Linux:\n"
        "  sudo apt install texlive-xetex texlive-latex-extra texlive-fonts-recommended texlive-fonts-extra\n\n"
        "Windows:\n"
        "  Install MiKTeX and enable automatic package installation.\n\n"
        "macOS:\n"
        "  Install MacTeX.\n\n"
        "Original pandoc error output:\n"
        f"{output}"
    )
