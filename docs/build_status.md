# Build Status

- Paper number: 14
- Slug: `causal_scene_flow_for_interaction`
- Required Downloads PDF: `C:/Users/wangz/Downloads/14.pdf`
- Desktop PDF: no new Desktop copy in v3
- Manuscript source: `paper/main.tex`
- Bibliography: `paper/references.bib`
- ICLR style files: `paper/iclr2026_conference.sty`, `paper/iclr2026_conference.bst`
- Build result: success
- Final Downloads PDF size: 389,425 bytes
- Final Downloads PDF pages: 25
- Final Downloads SHA256: `037834C37314E0671C7267ED778CFD34E84D444D6AB402AD742D92CAB42D5C56`
- Local `paper/main.pdf` after final copy: removed

## Commands

```powershell
python -m py_compile experiments\full_scale_causal_scene_flow.py experiments\causal_scene_flow_sim.py
python experiments\full_scale_causal_scene_flow.py
cd paper
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Verification

- `results/full_scale/progress.json` reports stage `complete`.
- `results/full_scale/metadata.json` records the v3 headline numbers.
- `pdfinfo C:/Users/wangz/Downloads/14.pdf` reports 25 pages and 389,425 bytes.
- `pdftotext C:/Users/wangz/Downloads/14.pdf -` contains the v3 manuscript marker and full-scale headline values.
- Downloads contains only one matching Paper 14 PDF: `14.pdf`.
- Final log scan found no unresolved citations, undefined references, LaTeX errors, fatal stops, missing files, or overfull boxes.
- Remaining benign warnings: underfull boxes from layout and MiKTeX update reminder.
