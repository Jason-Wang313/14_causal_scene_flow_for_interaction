# Claims

| Claim | Status | Support | Limitations |
| --- | --- | --- | --- |
| Dense total scene flow can be a bad manipulation-planning objective under passive exogenous motion. | Strongly supported in synthetic mechanism tests. | Formal counterexample, original 80,000-trial grid, and v3 multi-distractor family where total-flow success is 0.000 and passive-distractor selection is 1.000. | Does not imply every total-flow system fails in every manipulation task. |
| Causal effect flow can be defined as an action/no-action do-difference field. | Definitional/formal. | SCM-style definition and planner objective in `paper/main.tex`. | Requires a meaningful state-conditioned no-action baseline. |
| Planning on causal residual flow recovers the controllable contact when passive estimation preserves the action-effect margin. | Supported in synthetic grids and stress tests. | Causal-residual success is 1.000 in the main v3 multi-distractor setting and oracle-effect success is 1.000. | Fails when the no-action estimate is badly scaled, contaminated, or unidentifiable. |
| The advantage survives richer passive scenes beyond the original one-distractor toy. | Supported. | Seven v3 families under `results/full_scale/`, including 350 multi-distractor seed rows and 600 overlap seed rows. | Still synthetic and summary-level, not hardware. |
| The causal-flow advantage depends on a calibrated, uncontaminated no-action estimate. | Supported. | 50% passive under-subtraction lowers residual success to 0.037; 75% action-effect leakage yields 0.706 success; 100% leakage nearly collapses the residual. | Does not solve no-action estimation in real RGB-D data. |
| Endpoint error alone is insufficient for interaction perception. | Supported in synthetic metric-mismatch family. | Total-flow-like estimates can have low endpoint error and zero planning success; causal residuals can have higher total-flow endpoint error and perfect contact ranking. | Uses constructed estimators rather than real learned scene-flow models. |
| Learned no-op estimation is solved. | Unsupported. | None. | v3 includes only a finite-sample proxy, not a trained neural RGB-D predictor. |
| The proposed method improves real robot manipulation. | Unsupported. | None in this run. | The paper must remain scoped as a mechanism/counterexample paper until real or high-fidelity robot evidence exists. |

## Honest Claim Scope

The v3 paper is ready as a full-scale mechanism and counterexample submission. It argues that interaction planners should optimize robot-caused motion rather than total observed motion, and it backs that claim with broad synthetic stress evidence. It is not a real-robot systems paper, not a new scene-flow architecture paper, and not proof that a learned no-action counterfactual is available in every scene.
