# Submission Readiness Decision

Decision: ready under mechanism/counterexample scope after v3 full-scale hardening.

The paper is now a coherent full-scale mechanism submission. It identifies a concrete estimand mistake: dense total flow can rank passive motion as if it were controllable robot-caused motion. The v3 artifact expands the evidence from a 5-page one-distractor counterexample into a 25-page manuscript with seven synthetic experiment families, stronger baselines, negative controls, failure boundaries, generated tables, generated figures, and reproducibility material.

The paper is still not a real-robot systems result. It does not train a neural RGB-D no-action predictor, does not evaluate hardware, and does not prove that no-action counterfactuals are identifiable in every fast-changing scene.

Submission-safe claim:

Robots should plan interaction with a dense action-effect flow, defined by a state-conditioned action/no-action difference, because total scene flow is not invariant to passive exogenous motion and can select uncontrollable distractors.

Claims to avoid:

- Do not claim real-robot superiority.
- Do not claim learned no-op estimation is solved.
- Do not claim better scene-flow endpoint error.
- Do not claim the residual works without a calibrated no-action baseline.
- Do not claim the synthetic suite is a substitute for hardware validation.

Minimum next evidence for a systems paper:

- A trained no-action predictor on real or high-fidelity RGB-D scenes.
- Real or simulated manipulation with moving distractors, conveyors, camera motion, or human-induced passive motion.
- Contact-ranking labels that distinguish robot-caused motion from observed passive motion.
- Reporting of endpoint error, passive-flow error, residual-flow error, and planning rank metrics side by side.
