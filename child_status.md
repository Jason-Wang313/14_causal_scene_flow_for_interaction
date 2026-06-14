# Child Status

- Paper: 14, `causal_scene_flow_for_interaction`
- Stage: v3 full-scale hardening complete pending commit/push
- Workspace: `C:\Users\wangz\robotics_60_paper_batch\14_causal_scene_flow_for_interaction`
- Required final PDF path: `C:/Users/wangz/Downloads/14.pdf`
- GitHub repository: `https://github.com/Jason-Wang313/14_causal_scene_flow_for_interaction`

## Current Facts

- The old canonical artifact was a 5-page v2 synthetic counterexample; it was stale under the current 25-page internal standard.
- `docs/full_scale_execution_plan.md` was written before the v3 pass.
- `experiments/full_scale_causal_scene_flow.py` completed seven experiment families sequentially with deterministic seeds and RAM-light summary outputs.
- `results/full_scale/progress.json` reports stage `complete`.
- Seed-row summaries: Family A 350, Family B 360, Family C 600, Family D 192, Family E 216, Family F 96, Family G 96.
- Plot failures: 0.
- Headline v3 result: total-flow success 0.000 versus causal-residual success 1.000 in the multi-distractor passive-confound setting.
- Strongest failure boundary: 50% passive under-subtraction lowers residual success to 0.037; 75% action-effect leakage yields 0.706 success.
- Full spatial overlap with no occlusion retains 0.999 causal-residual success.
- The final manuscript compiled successfully to 25 pages and 389,425 bytes.
- The final verified PDF was copied to `C:/Users/wangz/Downloads/14.pdf`.
- Downloads `14.pdf` SHA256: `037834C37314E0671C7267ED778CFD34E84D444D6AB402AD742D92CAB42D5C56`.
- Local `paper/main.pdf` was removed after final copy.
- Final log scan found no unresolved citations, undefined references, LaTeX errors, fatal stops, missing files, or overfull boxes; only benign underfull warnings and the MiKTeX update reminder remain.

## Next

- Commit, push, and verify `HEAD` equals upstream before starting Paper 15.
