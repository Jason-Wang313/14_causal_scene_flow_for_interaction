"""Fetch the latest official ICLR template used for this paper run."""

from __future__ import annotations

import json
import shutil
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PAPER = ROOT / "paper"
ZIP_PATH = DATA / "iclr2026.zip"
EXTRACT = DATA / "iclr2026_template"
SOURCE_URL = "https://github.com/ICLR/Master-Template/raw/master/iclr2026.zip"


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    PAPER.mkdir(parents=True, exist_ok=True)
    try:
        print(f"downloading {SOURCE_URL}", flush=True)
        req = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "paper14-template-fetch/1.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            ZIP_PATH.write_bytes(resp.read())
        if EXTRACT.exists():
            shutil.rmtree(EXTRACT)
        EXTRACT.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(ZIP_PATH) as zf:
            zf.extractall(EXTRACT)
        copied = []
        for name in [
            "iclr2026_conference.sty",
            "iclr2026_conference.bst",
            "math_commands.tex",
            "fancyhdr.sty",
            "natbib.sty",
        ]:
            matches = list(EXTRACT.rglob(name))
            if matches:
                shutil.copy2(matches[0], PAPER / name)
                copied.append(name)
        manifest = {
            "source_url": SOURCE_URL,
            "zip_path": str(ZIP_PATH),
            "extracted_to": str(EXTRACT),
            "copied": copied,
            "status": "ok" if "iclr2026_conference.sty" in copied else "missing_style",
        }
        (DATA / "iclr_template_source.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(json.dumps(manifest, indent=2), flush=True)
    except Exception as exc:
        manifest = {"source_url": SOURCE_URL, "status": "failed", "error": str(exc)}
        (DATA / "iclr_template_source.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        print(json.dumps(manifest, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
