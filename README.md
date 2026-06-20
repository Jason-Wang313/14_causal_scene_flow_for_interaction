# Causal Scene Flow for Interaction

Anonymous research-paper workspace for paper 14 in the robotics/embodied-intelligence batch.

## Contents

- `docs/related_work_matrix.csv` - 1200-row literature landscape matrix with skim/deep/hostile labels.
- `docs/full_scale_execution_plan.md` - pre-run v3 hardening plan and acceptance checklist.
- `docs/experiment_report.md` - concise report for the v3 full-scale experiment package.
- `experiments/causal_scene_flow_sim.py` - original passive-confound synthetic evidence.
- `experiments/full_scale_causal_scene_flow.py` - v3 full-scale synthetic experiment runner.
- `results/full_scale/` - v3 CSV summaries, figures, LaTeX tables, metadata, and progress log.
- `paper/main.tex` - anonymous ICLR-style manuscript source.

## Reproduce

Run from the repository root:

```powershell
python experiments\causal_scene_flow_sim.py
python experiments\full_scale_causal_scene_flow.py
cd paper
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The final verified paper is `C:/Users/wangz/Downloads/14.pdf` (25 pages, 389,425 bytes, SHA256 `3CB0713C86F0DABBBCF325599FD36213A3D5C8A7AC3EE7BA17D102EC968C548B`).

VLA-style boxed-link verification:

- Link annotations: 64 total on pages `[(1, 19), (2, 29), (4, 4), (5, 6), (7, 4), (8, 2)]`.
- Annotation colors: green = 48, red = 16, cyan = 0.
- Border widths: `(0, 0, 1)` for all link annotations.
- Visual audit: rendered pages 1, 2, 4, 5, 7, and 8; green citation/URL boxes and red internal-reference boxes are crisp and aligned.

## Submission-Hardening v3

- Replaced the 5-page v2 artifact with a 25-page full-scale mechanism paper.
- Added seven experiment families: multi-distractor passive confounds, passive/no-op misspecification, spatial overlap and occlusion, ego/global passive fields, learned no-op proxy, endpoint-error versus planning mismatch, and ablations.
- Wrote 1,910 seed-row summaries under `results/full_scale/` with deterministic seeds and no plot failures.
- Main multi-distractor setting: total-flow success 0.000 and passive-distractor rate 1.000; causal-residual success 1.000 and distractor rate 0.000; action-conditioned total-flow baseline success 0.614.
- Boundary stress: 50% passive under-subtraction lowers residual success to 0.037; 75% action-effect leakage retains 0.706 success; full spatial overlap with no occlusion retains 0.999 success.
- Submission decision: ready as a full-scale mechanism/counterexample paper, not as a real-robot systems or learned RGB-D benchmark claim.
