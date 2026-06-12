# Reproducibility Checklist

Run from the repository root:

```powershell
python experiments\causal_scene_flow_sim.py
```

Expected artifacts:

- `data/experiment_results.csv`
- `data/experiment_summary.json`
- `data/passive_misspecification_stress.csv`
- `data/passive_misspecification_table.tex`
- `figures/passive_confounding_success.pdf`
- `figures/passive_confounding_success.png`
- `figures/example_scene_flow_decomposition.pdf`
- `figures/example_scene_flow_decomposition.png`
- `docs/evidence_summary.md`

The script uses deterministic seeds and a NumPy vectorized path when NumPy is installed. A scalar fallback remains in the code path, but the vectorized path is the validated local configuration.
