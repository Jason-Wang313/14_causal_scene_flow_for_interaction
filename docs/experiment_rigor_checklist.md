# Experiment Rigor Checklist

- Fixed seeds: yes. Original grid uses deterministic seeds; v3 full-scale runner uses master seed 14014.
- RAM-light execution: yes. The v3 runner writes summary CSVs, figures, tables, metadata, and progress JSON rather than storing full dense fields for every trial.
- Original outputs: `data/experiment_results.csv`, `data/experiment_summary.json`, `data/passive_misspecification_stress.csv`.
- V3 outputs: `results/full_scale/*.csv`, `results/full_scale/*.pdf`, `results/full_scale/*.png`, `results/full_scale/*.tex`, `results/full_scale/metadata.json`, and `results/full_scale/progress.json`.
- Baselines: total-flow planner, causal residual planner, attention/contact baseline, action-conditioned total-flow baseline, learned no-op proxy, passive-only and random-noop negative controls, and oracle effect planner.
- Stress axes: number of passive distractors, passive-confound strength, passive-estimation scale error, action-effect leakage, bias direction, spatial overlap, occlusion, ego/global passive fields, finite-sample no-op proxy quality, and endpoint-error/planning mismatch.
- Metrics: success, passive-distractor selection, caused progress, regret, endpoint error, ranking accuracy, calibration error, false controllability, missed controllable contact, and ablation deltas.
- Manuscript artifacts: generated v3 figures and LaTeX tables imported directly into `paper/main.tex`.
- Remaining evidence gap: no real robot, no high-fidelity simulator, and no trained RGB-D no-action predictor.
