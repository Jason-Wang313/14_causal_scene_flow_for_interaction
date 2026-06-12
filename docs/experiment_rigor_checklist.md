# Experiment Rigor Checklist

- Fixed seeds: yes (`14000+` for grid rows, `14200+` for v2 stress rows).
- Raw grid output: `data/experiment_results.csv`.
- V2 stress output: `data/passive_misspecification_stress.csv`.
- Manuscript table artifact: `data/passive_misspecification_table.tex`.
- Main trials: 40 grid rows x 2,000 trials = 80,000 trials.
- V2 stress trials: 9 rows x 2,000 trials = 18,000 trials.
- Baselines: total-flow planner, calibrated residual planner, oracle effect planner, no-subtraction stress endpoint.
- Stress axes: passive-confound strength, passive-estimation noise, passive under/over-subtraction, action-effect leakage into no-action estimate.
- Main remaining gap: no learned perception, no hardware, no high-fidelity simulator, and no real passive/no-op data collection protocol.
