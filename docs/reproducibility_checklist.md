# Reproducibility Checklist

Run from the repository root:

```powershell
python -m py_compile experiments\full_scale_causal_scene_flow.py experiments\causal_scene_flow_sim.py
python experiments\causal_scene_flow_sim.py
python experiments\full_scale_causal_scene_flow.py
```

Then build from `paper/`:

```powershell
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

Expected v3 artifacts:

- `results/full_scale/family_a_multidistractor_seed.csv`
- `results/full_scale/family_b_misspecification_seed.csv`
- `results/full_scale/family_c_overlap_seed.csv`
- `results/full_scale/family_d_egomotion_seed.csv`
- `results/full_scale/family_e_learned_noop_seed.csv`
- `results/full_scale/family_f_metric_mismatch_seed.csv`
- `results/full_scale/family_g_ablation_seed.csv`
- `results/full_scale/figure_*.pdf`
- `results/full_scale/table_*.tex`
- `results/full_scale/metadata.json`
- `results/full_scale/progress.json`
- `docs/experiment_report.md`

Expected verification:

- `progress.json` has stage `complete`.
- `metadata.json` headline has total-flow success 0.0, causal-residual success 1.0, 50% passive under-subtraction success about 0.037, and 75% leakage success about 0.706.
- Final manuscript builds to 25 pages.
- Log scan has no unresolved citations, undefined references, LaTeX errors, fatal stops, missing files, or overfull boxes.

## Final Export Verification

- Canonical PDF: `C:/Users/wangz/Downloads/14.pdf`
- Pages: 25
- Size: 389,425 bytes
- SHA256: `3CB0713C86F0DABBBCF325599FD36213A3D5C8A7AC3EE7BA17D102EC968C548B`
- VLA-style boxed-link inventory: 64 annotations on pages `[(1, 19), (2, 29), (4, 4), (5, 6), (7, 4), (8, 2)]`; green = 48, red = 16, cyan = 0; all borders `(0, 0, 1)`.
- Visual render audit: pages 1, 2, 4, 5, 7, and 8 checked after export.
- Local build artifact: `paper/main.pdf` removed after export.
