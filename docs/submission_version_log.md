# Submission Version Log

## v1

- Generated initial synthetic counterexample paper and ICLR-style PDF.
- Published initial GitHub repository.
- Canonical PDF: `C:/Users/wangz/Downloads/14.pdf` (206,005 bytes at parent recovery).

## v2

Checked: 2026-06-12

- Added passive-baseline misspecification stress CSV and LaTeX table.
- Added v2 manuscript marker, abstract boundary, stress table, and limitations language.
- Added deterministic vectorized regeneration for the original 80,000-trial grid.
- Decision: workshop-only / revise before main-conference submission.

## v3

Checked: 2026-06-14

- Wrote a paper-specific full-scale execution plan before substantive edits.
- Added `experiments/full_scale_causal_scene_flow.py`.
- Generated seven full-scale experiment families under `results/full_scale/`.
- Imported generated v3 tables and figures into the manuscript.
- Expanded the manuscript to 25 pages with new experiments, proofs, baseline analysis, failure boundaries, reproducibility details, and appendices.
- Main result: total-flow success 0.000 versus causal-residual success 1.000 in the multi-distractor passive-confound setting.
- Boundary result: 50% passive under-subtraction lowers success to 0.037; 75% action-effect leakage yields 0.706.
- Decision: ready as a full-scale mechanism/counterexample paper under the stated claim scope.
