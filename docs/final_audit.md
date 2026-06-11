# Final Audit

- Paper number: 14
- Slug: `causal_scene_flow_for_interaction`
- Title: `Causal Scene Flow for Interaction`
- Recovery owner: parent batch monitor after child timeout at publish/final-audit step
- Terminal assessment: recoverable child failure, parent-recovered to success

## Required Outputs

- Downloads PDF: `C:/Users/wangz/Downloads/14.pdf`
- Desktop PDF: `C:/Users/wangz/OneDrive/Desktop/14.pdf`
- PDF size: 206005 bytes
- PDF pages: 5
- Source repository folder: `C:/Users/wangz/robotics_60_paper_batch/14_causal_scene_flow_for_interaction`
- GitHub repository: `https://github.com/Jason-Wang313/14_causal_scene_flow_for_interaction`
- Initial commit: `1a7fbb7`

## Evidence Package

- Literature matrix: `docs/related_work_matrix.csv`
- Literature counts: `data/literature_counts.json`
- Novelty decision: `docs/novelty_decision.md`
- Hostile prior work: `docs/hostile_prior_work.md`
- Claims ledger: `docs/claims.md`
- Reviewer attacks: `docs/reviewer_attacks.md`
- Experiment script: `experiments/causal_scene_flow_sim.py`
- Experiment summary: `data/experiment_summary.json`
- Build status: `docs/build_status.md`

## Build Verification

`scripts/build_paper.py` completed successfully, copied the final manuscript to `C:/Users/wangz/Downloads/14.pdf`, and recorded successful LaTeX/BibTeX passes in `data/build_status.json`.

Remaining benign warnings:

- MiKTeX update reminder
- One overfull hbox under 1 pt

Final log scan found no unresolved references or citations.

## Desktop Verification

`scripts/copy_and_arrange_desktop_pdfs.ps1 -Numbers 14` copied `14.pdf` to the visible OneDrive Desktop and updated `DESKTOP_PDF_REPORT.md`. The report requests numeric order from `01.pdf` through `14.pdf` and lists no blockers.

## Parent Recovery Notes

The child produced the PDF and repository assets but exited with code 999 after a tool timeout before GitHub publishing and final audit. Parent recovery preserved the generated assets, published the repository, recorded GitHub status, updated the queue row to `SUCCESS`, and left the Paper 15 runner alive.
