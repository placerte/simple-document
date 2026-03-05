from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

import pytest

from simdoc import Doc, SimDocError
from simdoc import doc as doc_module


def test_save_pdf_smoke(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    doc = Doc()
    doc.h1("Report")
    output = tmp_path / "report.pdf"

    def fake_which(name: str) -> str | None:
        if name in {"pandoc", "xelatex"}:
            return f"/usr/bin/{name}"
        return None

    monkeypatch.setattr(shutil, "which", fake_which)

    called_args: list[str] | None = None

    def fake_run(
        args: list[str], check: bool, **_: object
    ) -> subprocess.CompletedProcess[str]:
        nonlocal called_args
        called_args = args
        output_index = args.index("-o") + 1
        Path(args[output_index]).write_bytes(b"%PDF-1.4\n")
        return subprocess.CompletedProcess(args, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    result = doc.save_pdf(
        output,
        preset="article",
        pandoc_args=["--metadata=author:simdoc"],
    )

    assert result == output
    assert output.exists()
    assert called_args is not None
    assert called_args[0] == "pandoc"
    assert "-o" in called_args
    assert called_args[-2:] == ["--pdf-engine=xelatex", "--metadata=author:simdoc"]


def test_save_pdf_missing_pandoc(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = Doc()
    monkeypatch.setattr(shutil, "which", lambda name: None)

    with pytest.raises(
        SimDocError,
        match="PDF rendering requires pandoc and a TeX distribution",
    ):
        doc.save_pdf("out.pdf")


def test_save_pdf_missing_xelatex(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = Doc()

    def fake_which(name: str) -> str | None:
        if name == "pandoc":
            return "/usr/bin/pandoc"
        return None

    monkeypatch.setattr(shutil, "which", fake_which)

    with pytest.raises(
        SimDocError,
        match="PDF rendering requires pandoc and a TeX distribution",
    ):
        doc.save_pdf("out.pdf")


def test_eisvogel_template_path_exists() -> None:
    template_path = Path(doc_module._get_eisvogel_template())
    assert template_path.exists()


def test_pandoc_args_include_eisvogel(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = Doc()
    output = tmp_path / "report.pdf"

    def fake_which(name: str) -> str | None:
        if name in {"pandoc", "xelatex"}:
            return f"/usr/bin/{name}"
        return None

    monkeypatch.setattr(shutil, "which", fake_which)

    captured_args: list[str] | None = None

    def fake_run(
        args: list[str], check: bool, **_: object
    ) -> subprocess.CompletedProcess[str]:
        nonlocal captured_args
        captured_args = args
        output_index = args.index("-o") + 1
        Path(args[output_index]).write_bytes(b"%PDF-1.4\n")
        return subprocess.CompletedProcess(args, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    doc.save_pdf(output)

    assert captured_args is not None
    args = captured_args
    assert "--template" in args
    template_index = args.index("--template") + 1
    assert Path(args[template_index]).exists()
    assert "--pdf-engine=xelatex" in args
    assert "--listings" in args


def test_pandoc_failure_reports_stderr(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = Doc()
    output = tmp_path / "report.pdf"

    def fake_which(name: str) -> str | None:
        if name in {"pandoc", "xelatex"}:
            return f"/usr/bin/{name}"
        return None

    monkeypatch.setattr(shutil, "which", fake_which)

    def fake_run(
        args: list[str], check: bool, **_: object
    ) -> subprocess.CompletedProcess[str]:
        raise subprocess.CalledProcessError(
            43,
            args,
            stderr="missing package: sourcesanspro.sty",
        )

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.raises(SimDocError, match="missing package: sourcesanspro"):
        doc.save_pdf(output, preset="article")


def test_eisvogel_fallback_to_plain_template(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    doc = Doc()
    output = tmp_path / "report.pdf"

    def fake_which(name: str) -> str | None:
        if name in {"pandoc", "xelatex"}:
            return f"/usr/bin/{name}"
        return None

    monkeypatch.setattr(shutil, "which", fake_which)

    calls: list[list[str]] = []

    def fake_run(
        args: list[str], check: bool, **_: object
    ) -> subprocess.CompletedProcess[str]:
        calls.append(args)
        if len(calls) == 1:
            raise subprocess.CalledProcessError(
                43,
                args,
                stderr="missing package: sourcesanspro.sty",
            )
        output_index = args.index("-o") + 1
        Path(args[output_index]).write_bytes(b"%PDF-1.4\n")
        return subprocess.CompletedProcess(args, 0)

    monkeypatch.setattr(subprocess, "run", fake_run)

    with pytest.warns(RuntimeWarning, match="falling back"):
        result = doc.save_pdf(output)

    assert result == output
    assert output.exists()
    assert len(calls) == 2
    assert "--template" in calls[0]
    assert "--template" not in calls[1]
    assert "--pdf-engine=xelatex" in calls[1]
