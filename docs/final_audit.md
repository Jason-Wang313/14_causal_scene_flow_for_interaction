# Final Audit

- Paper number: 14
- Slug: `causal_scene_flow_for_interaction`
- Title: `Causal Scene Flow for Interaction`
- Terminal assessment: ready as a full-scale mechanism/counterexample paper under the stated claim scope
- Audit date: 2026-06-20

## Required Outputs

- Downloads PDF: `C:/Users/wangz/Downloads/14.pdf`
- PDF size: 389,425 bytes
- PDF pages: 25
- SHA256: `3CB0713C86F0DABBBCF325599FD36213A3D5C8A7AC3EE7BA17D102EC968C548B`
- VLA-style boxed-link audit: 64 link annotations on pages `[(1, 19), (2, 29), (4, 4), (5, 6), (7, 4), (8, 2)]`; colors green = 48, red = 16, cyan = 0; all borders `(0, 0, 1)`.
- Visual link audit: pages 1, 2, 4, 5, 7, and 8 rendered after export; green citation/URL boxes and red internal-reference boxes are crisp and aligned.
- Local build PDF after final copy: removed (`paper/main.pdf` does not exist)
- Desktop PDF: no new Desktop copy created during v3 hardening
- Source repository folder: `C:/Users/wangz/robotics_60_paper_batch/14_causal_scene_flow_for_interaction`
- GitHub repository: `https://github.com/Jason-Wang313/14_causal_scene_flow_for_interaction`

## Evidence Package

- Full-scale plan: `docs/full_scale_execution_plan.md`
- Full-scale runner: `experiments/full_scale_causal_scene_flow.py`
- Progress log: `results/full_scale/progress.json`
- Metadata: `results/full_scale/metadata.json`
- CSV summaries: `results/full_scale/family_*_summary.csv`
- Seed rows: `results/full_scale/family_*_seed.csv`
- Figures: `results/full_scale/figure_*.pdf` and `.png`
- Tables: `results/full_scale/table_*.tex`
- Experiment report: `docs/experiment_report.md`
- Claims ledger: `docs/claims.md`
- Readiness decision: `docs/submission_readiness_decision.md`

## Build Verification

- `python -m py_compile experiments\full_scale_causal_scene_flow.py experiments\causal_scene_flow_sim.py` passed.
- `python experiments\full_scale_causal_scene_flow.py` completed.
- `bibtex main`, `pdflatex`, and final `pdflatex` completed.
- Final local PDF before copy had 25 pages and 389,425 bytes.
- Copied PDF in Downloads has 25 pages and 389,425 bytes.
- `pdftotext` found the v3 manuscript marker and headline numbers in `C:/Users/wangz/Downloads/14.pdf`.
- Downloads contains only one matching Paper 14 PDF: `14.pdf`.
- Final log scan found no unresolved citations, undefined references, LaTeX errors, fatal stops, missing files, or overfull boxes.
- Remaining benign warnings: underfull boxes from layout and MiKTeX update reminder.

## Evidence Summary

- Seven v3 experiment families completed.
- Total v3 seed-row summaries: 1,910.
- Plot failures: 0.
- Main setting: total-flow success 0.000, causal-residual success 1.000.
- Main distractor rates: total-flow 1.000, causal-residual 0.000.
- Action-conditioned total-flow baseline success: 0.614.
- 50% passive under-subtraction: causal-residual success 0.037.
- 75% action-effect leakage: causal-residual success 0.706.
- Full spatial overlap with no occlusion: causal-residual success 0.999.

## Claim Boundary

The paper is submission-ready as a mechanism/counterexample paper. It does not claim real-robot superiority, learned no-op estimation, a new scene-flow architecture, or hardware validation.
