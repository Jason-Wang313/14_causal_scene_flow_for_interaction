# Submission Readiness Decision

Decision: workshop-only / revise before main-conference submission.

The paper is coherent as a mechanism-and-counterexample paper. It identifies a real estimand mistake: dense total flow can rank passive motion as if it were controllable robot-caused motion.

The paper is not main-conference-ready as a systems result. It does not learn causal scene flow from RGB-D data, does not evaluate a real robot, and does not test whether a no-action predictor can be matched accurately in fast-changing scenes.

Minimum next evidence for a stronger submission:

- A learned no-action predictor trained separately from action-effect outcomes.
- A real or high-fidelity scene with moving distractors, conveyors, camera motion, or human-induced passive motion.
- Ranking-error metrics that measure whether the selected contact is moved by the robot rather than merely observed to move.
- Ablations separating passive-prediction error, action-effect leakage, and candidate-contact ambiguity.
