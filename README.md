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
