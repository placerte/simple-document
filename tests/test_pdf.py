from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

import pytest

from simdoc import Doc, SimDocError


def test_save_pdf_smoke(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    doc = Doc()
    doc.h1("Report")
    output = tmp_path / "report.pdf"

    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/pandoc")

    called: dict[str, object] = {}

    def fake_run(args: list[str], check: bool) -> subprocess.CompletedProcess[str]:
        called["args"] = args
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
    assert called["args"][0] == "pandoc"
    assert "-o" in called["args"]
    assert called["args"][-2:] == ["--pdf-engine=xelatex", "--metadata=author:simdoc"]


def test_save_pdf_missing_pandoc(monkeypatch: pytest.MonkeyPatch) -> None:
    doc = Doc()
    monkeypatch.setattr(shutil, "which", lambda name: None)

    with pytest.raises(SimDocError, match="pandoc executable not found"):
        doc.save_pdf("out.pdf")
