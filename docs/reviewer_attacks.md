# Reviewer Attacks

## Attack 1: This is just background subtraction.

Response: In the simplest case it resembles subtracting a no-action passive flow, but the estimand is intervention-defined: `do(action)` minus `do(noop)` conditioned on the same state. The v3 paper emphasizes this distinction for moving foreground objects, conveyors, ego-motion, and passive distractors where geometric background masks are not enough.

## Attack 2: The no-action baseline is unrealistic.

Response: This is the main limitation, not a hidden assumption. Family B shows the boundary: 50% passive under-subtraction drops residual success to 0.037, and 75% action-effect leakage yields 0.706 success. The paper claims the residual is the right planning variable when the no-action baseline is calibrated, not that such a baseline is always easy to obtain.

## Attack 3: The original evidence was a one-distractor toy.

Response: v3 replaces the narrow toy with seven synthetic families. Family A sweeps multi-distractor scenes, passive strength, noise, controllable contacts, and baselines. The main multi-distractor setting keeps total-flow success at 0.000 while causal-residual success is 1.000.

## Attack 4: A stronger action-conditioned baseline would solve it.

Response: The v3 action-conditioned total-flow baseline improves over total flow but does not close the gap: it reaches 0.614 success in the main setting versus 1.000 for the residual and oracle effect. This supports the claim that the optimized variable matters, not just conditioning.

## Attack 5: Spatial overlap or occlusion will break the residual.

Response: Family C tests overlap and occlusion directly. Full spatial overlap with no occlusion retains 0.999 success, while occlusion exposes degradation. The paper reports both the robustness and the hard boundary.

## Attack 6: Camera ego-motion and global passive fields are ignored.

Response: Family D adds translation, rotation, conveyor-like, gravity-like, and mixed global passive fields. The residual objective remains the correct estimand when the passive component is estimable; total-flow and global-compensation variants remain vulnerable to local passive distractors.

## Attack 7: Endpoint error is the proper perception metric.

Response: Family F shows this is false for interaction. A predictor can have low endpoint error relative to total flow and still rank a passive distractor, while a residual estimate can have worse total-flow endpoint error and correct planning rank.

## Attack 8: The learned no-op result is too weak.

Response: Correct. Family E is only a finite-sample proxy, intentionally scoped as a calibration stress rather than a neural RGB-D solution. The claims ledger marks learned no-op estimation as unsupported.

## Attack 9: The paper still lacks hardware.

Response: Correct. v3 is ready as a full-scale mechanism/counterexample paper. It should not be sold as a real-robot systems paper.

## Attack 10: The planner is simple.

Response: Yes, intentionally. The simple planner isolates the representational error: optimizing total observed motion can select uncontrollable motion. More complex MPC could use the same residual, but planner complexity is not the contribution.

## Numeric Stress Points

- Main v3 setting: total-flow success 0.000; causal-residual success 1.000.
- Total-flow passive-distractor rate: 1.000; causal-residual passive-distractor rate: 0.000.
- Action-conditioned total-flow baseline success: 0.614.
- 50% passive under-subtraction: residual success 0.037.
- 75% action-effect leakage: residual success 0.706.
- Full overlap with no occlusion: residual success 0.999.
