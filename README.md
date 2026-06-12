# Causal Scene Flow for Interaction

Anonymous research-paper workspace for paper 14 in the robotics/embodied-intelligence batch.

## Contents

- `docs/related_work_matrix.csv` - 1000+ paper landscape matrix with skim/deep/hostile labels.
- `docs/literature_map.md` - field map and assumption inventory.
- `docs/hostile_prior_work.md` - closest prior-work pressure set.
- `docs/novelty_boundary_map.md` - what is and is not novel.
- `experiments/causal_scene_flow_sim.py` - runnable synthetic evidence for passive-vs-agent-caused flow separation.
- `paper/main.tex` - anonymous ICLR-style manuscript.

## Reproduce

```powershell
python scripts/literature_sweep.py
python experiments/causal_scene_flow_sim.py
python scripts/write_paper_assets.py
python scripts/build_paper.py
```

The final compiled paper is written to `C:/Users/wangz/Downloads/14.pdf`.

## Submission-Hardening v2

- Added vectorized regeneration for the 80,000-trial synthetic grid.
- Added passive-baseline misspecification stress in `data/passive_misspecification_stress.csv`.
- Calibrated no-op residual success is 1.000 at confound 2.0/noise 0.10.
- Under-subtracting the passive field by 50% lowers residual success to 0.387.
- Leaking 75% of the robot effect into the no-action estimate lowers residual success to 0.505.
- Decision remains workshop-only until tested with learned no-op predictors and real or high-fidelity robot scenes.
