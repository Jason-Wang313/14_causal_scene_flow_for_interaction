# Build Status

- Paper number: 14
- Slug: `causal_scene_flow_for_interaction`
- Required Downloads PDF: `C:/Users/wangz/Downloads/14.pdf`
- Desktop PDF: historical parent-recovery copy only; v2 hardening created no new Desktop copy
- Build wrapper: `scripts/build_paper.py`
- Manuscript source: `paper/main.tex`
- Bibliography: `paper/references.bib`
- ICLR style files: `paper/iclr2026_conference.sty`, `paper/iclr2026_conference.bst`
- Build result: success
- Final PDF size: 210277 bytes
- Final PDF pages: 5
- Final LaTeX warnings: one tiny overfull hbox and MiKTeX update reminder; no unresolved references or citations in the final log check.

## Commands

- `python scripts/literature_sweep.py`
- `python experiments/causal_scene_flow_sim.py`
- `python scripts/write_research_docs.py`
- `python scripts/fetch_iclr_template.py`
- `python scripts/write_paper_assets.py`
- `python scripts/build_paper.py`

## Verification

- `C:/Users/wangz/Downloads/14.pdf` exists and is 210277 bytes.
- No new Desktop PDF copy was created during v2 hardening.
- `data/build_status.json` records successful `pdflatex`, `bibtex`, `pdflatex`, `pdflatex` passes.
- `docs/related_work_matrix.csv` contains 1200 literature rows, including 300 serious-skim, 225 deep-read, and 100 hostile-prior labels.
