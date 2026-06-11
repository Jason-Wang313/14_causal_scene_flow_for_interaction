"""Build the ICLR paper with direct pdflatex/bibtex passes."""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
DATA = ROOT / "data"
TARGET = Path("C:/Users/wangz/Downloads/14.pdf")
STATUS = DATA / "build_status.json"


COMMANDS = [
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ["bibtex", "main"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
]


def run_command(cmd: list[str]) -> dict[str, object]:
    print("running: " + " ".join(cmd), flush=True)
    try:
        proc = subprocess.run(
            cmd,
            cwd=PAPER,
            text=True,
            capture_output=True,
            timeout=300,
        )
        return {
            "command": cmd,
            "returncode": proc.returncode,
            "stdout_tail": proc.stdout[-4000:],
            "stderr_tail": proc.stderr[-4000:],
        }
    except Exception as exc:
        return {"command": cmd, "returncode": -999, "error": str(exc)}


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    results = []
    success = True
    for cmd in COMMANDS:
        result = run_command(cmd)
        results.append(result)
        if int(result.get("returncode", 1)) != 0:
            success = False
            break
    pdf = PAPER / "main.pdf"
    copied = False
    if success and pdf.exists():
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(pdf, TARGET)
        copied = True
        pdf.unlink()
    status = {
        "success": success and copied,
        "copied_to": str(TARGET) if copied else "",
        "commands": results,
    }
    STATUS.write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps({"success": status["success"], "copied_to": status["copied_to"]}, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
