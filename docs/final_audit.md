# Final Audit

- Paper number: 14
- Slug: `causal_scene_flow_for_interaction`
- Title: `Causal Scene Flow for Interaction`
- Recovery owner: parent batch monitor after child timeout at publish/final-audit step
- Terminal assessment: workshop-only after v2 submission hardening

## Required Outputs

- Downloads PDF: `C:/Users/wangz/Downloads/14.pdf`
- Desktop PDF: historical parent-recovery copy at `C:/Users/wangz/OneDrive/Desktop/14.pdf`; no new Desktop copy created during v2 hardening
- PDF size: 210,277 bytes
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

Historical parent recovery ran `scripts/copy_and_arrange_desktop_pdfs.ps1 -Numbers 14` and copied `14.pdf` to the visible OneDrive Desktop. The v2 hardening pass did not create or update any Desktop PDF copy.

## Parent Recovery Notes

The child produced the PDF and repository assets but exited with code 999 after a tool timeout before GitHub publishing and final audit. Parent recovery preserved the generated assets, published the repository, recorded GitHub status, updated the queue row to `SUCCESS`, and left the Paper 15 runner alive.

## Submission-Hardening v2

Checked: 2026-06-12 23:49:37 +01:00

- Added passive-baseline misspecification stress tests and a manuscript table.
- Main v1 counterexample retained: at confound strength 2.0/noise 0.10, total-flow success is 0.000 and calibrated causal residual success is 1.000.
- V2 boundary: 50% passive under-subtraction lowers residual success to 0.387 and raises residual distractor selection to 0.613.
- V2 boundary: 75% action-effect leakage into the no-action estimate lowers residual success to 0.505.
- Reproducibility improved by vectorizing the 80,000-trial grid while preserving deterministic fixed seeds.
- Canonical v2 PDF: `C:/Users/wangz/Downloads/14.pdf` (210,277 bytes).
- Terminal decision: workshop-only / revise before main-conference submission.
- Reason: the mechanism is crisp and runnable, but evidence remains synthetic and assumes a meaningful, calibrated no-action counterfactual; no learned RGB-D estimator, real robot, or high-fidelity interaction benchmark is evaluated.
