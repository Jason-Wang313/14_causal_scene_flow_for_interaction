# Claims

| Claim | Status | Support | Limitations |
| --- | --- | --- | --- |
| Dense total scene flow can be a bad manipulation-planning objective under passive exogenous motion. | Supported in formal toy setting and synthetic stress test. | Inequality counterexample plus simulation. | Does not say all total-flow planners fail in all tasks. |
| Causal effect flow can be defined as an action/no-action do-difference field. | Definitional/formal. | SCM-style intervention definition in paper. | Requires a meaningful no-action baseline and state conditioning. |
| If passive-estimation error is below the effect margin, causal-flow ranking recovers the controllable contact in the toy setting. | Supported by proposition. | Formal margin argument. | Assumes candidate set contains the true contact and effects are pointwise comparable. |
| In the implemented stress test at confound strength 2.0 and passive-estimation noise 0.10, causal-flow success exceeds total-flow success by 1.000. | Supported by code. | `experiments/causal_scene_flow_sim.py`, 80000 trials. | Synthetic only; no real robot. |
| The causal-flow advantage depends on a calibrated, uncontaminated no-action estimate. | Supported by v2 stress. | At confound 2.0/noise 0.10, calibrated residual success is 1.000; 50% passive under-subtraction drops success to 0.387; 75% action-effect leakage drops success to 0.505. | This is still synthetic and does not validate any learned passive predictor. |
| Existing scene-flow and manipulation papers do not make total-flow prediction novel. | Supported by literature sweep. | 1200-row matrix and hostile prior set. | Metadata/abstract-level extraction, not exhaustive full-text review. |
| The proposed method will improve real manipulation systems. | Unsupported. | None in this run. | Marked as future work. |
| The proposed decomposition can be learned accurately from real RGB-D data. | Unsupported. | None in this run. | Requires future datasets or robot experiments. |

## Honest Claim Scope

The paper is ready as a mechanism-and-counterexample paper, not as a real-robot systems paper. Its strongest claim is conceptual and diagnostic: planning on total motion is not causally invariant to passive motion. The v2 stress narrows the claim further: the residual is useful only when the no-action counterfactual is matched closely enough to preserve action-effect margins.
