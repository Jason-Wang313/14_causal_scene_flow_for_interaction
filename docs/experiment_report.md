# Full-Scale Experiment Report

## Scope

- Seven experiment families: multi-distractor passive confounds, baseline misspecification, spatial overlap, ego/global passive fields, learned no-op proxy, endpoint-error mismatch, and ablations.
- Main headline setting uses 30 seeds; diagnostic grids use replicated summaries with vectorized trials.
- Outputs are under `results/full_scale/`.
- Total seed-row summaries: 1,910.
- Plot failures: 0.

## Key Findings

- Main setting: total-flow success 0.000, causal-residual success 1.000.
- Main distractor rates: total-flow 1.000, causal-residual 0.000.
- Action-conditioned total-flow baseline success: 0.614.
- 50% passive under-subtraction: causal-residual success 0.037.
- 75% action-effect leakage: causal-residual success 0.706.
- Full spatial overlap with no occlusion: causal-residual success 0.999.
- Endpoint-error mismatch family: low total-flow endpoint error can still produce wrong interaction ranking.

## Artifact Map

- CSV summaries: `results/full_scale/family_*_summary.csv`
- Seed rows: `results/full_scale/family_*_seed.csv`
- Figures: `results/full_scale/figure_*.pdf` and `.png`
- Tables: `results/full_scale/table_*.tex`
- Metadata: `results/full_scale/metadata.json`
- Progress: `results/full_scale/progress.json`

## Final Artifact

- Canonical PDF: `C:/Users/wangz/Downloads/14.pdf`
- Pages: 25
- Size: 389,425 bytes
- SHA256: `3CB0713C86F0DABBBCF325599FD36213A3D5C8A7AC3EE7BA17D102EC968C548B`
- VLA-style boxed-link inventory: 64 annotations on pages `[(1, 19), (2, 29), (4, 4), (5, 6), (7, 4), (8, 2)]`; green = 48, red = 16, cyan = 0; all borders `(0, 0, 1)`.
- Visual audit: rendered pages 1, 2, 4, 5, 7, and 8 after export and confirmed crisp, aligned link boxes.
