# Paper 14 Full-Scale Execution Plan

Paper: Causal Scene Flow for Interaction
Repository: `14_causal_scene_flow_for_interaction`
Date: 2026-06-14

## Current Claim

Scene flow for robot interaction should estimate the motion caused by the robot action, not total motion in the scene. Causal scene flow is the dense action-effect field obtained by subtracting the no-action passive future from the action future. Planning on total scene flow can select passive distractors; planning on the action-effect residual can select controllable contacts when the no-action baseline is calibrated.

## Current State

- Current canonical PDF is 5 pages and stale under the current 25-page standard.
- Existing evidence is a synthetic passive-confound stress with 80,000 trials.
- Existing headline: at passive confound strength 2.0 and passive-estimation noise 0.10, total-flow planner success is 0.000 and causal-flow planner success is 1.000.
- Existing v2 misspecification stress: under-subtracting the passive field by 50% drops residual success to 0.387; leaking 75% of robot effect into the no-action estimate drops success to 0.505.
- Existing readiness decision is workshop / revise because the evidence is synthetic and does not include learned no-op predictors, high-fidelity robot scenes, or real robot data.

## Reviewer Attacks To Resolve

1. This is just subtracting background flow, not a new interaction representation.
2. The no-action baseline is unrealistic or unavailable in robot scenes.
3. The synthetic benchmark is too easy: one passive distractor and one controllable contact.
4. Total-flow baselines are intentionally weak; action-conditioned predictors or attention baselines may recover.
5. The causal residual will be brittle when passive and robot-caused flows overlap spatially.
6. The method may erase true robot effects if the no-action model is contaminated by action data.
7. Camera ego-motion, moving conveyors, gravity, and articulated objects require separate treatments.
8. The claim is dense but the evaluation is a scalar contact ranking.
9. No learned no-op estimator or finite-data calibration stress is included.
10. No high-fidelity or hardware scenes validate the estimand.

## Experimental Expansion

Create a RAM-light full-scale runner under `experiments/full_scale_causal_scene_flow.py`. Keep `experiments/causal_scene_flow_sim.py` as the v2 baseline or shared helper. Store outputs under `results/full_scale/`. Run families sequentially and update `results/full_scale/progress.json` after each family.

### Family A: Multi-Distractor Passive Confounds

Purpose: Replace the one-distractor counterexample with a broad scene generator.

Settings:
- Controllable contacts: 1, 2, 4.
- Passive distractors: 1, 3, 8, 16.
- Confound strengths: 0.0, 0.5, 1.0, 1.5, 2.0, 3.0.
- Passive noise: 0.00, 0.05, 0.10, 0.20.
- Seeds: at least 30 for the headline setting; smaller replicated diagnostic grids where needed.

Baselines:
- Total-flow planner.
- Causal residual planner.
- Noisy residual planner.
- Attention-to-contact planner.
- Action-conditioned total-flow planner.
- Oracle caused-flow planner.

Metrics:
- Success, passive-distractor selection rate, caused progress, regret to oracle, selected-contact controllability, and margin to second-best contact.

### Family B: Passive Baseline Misspecification

Purpose: Deepen v2 under-subtraction and leakage into a full calibration surface.

Settings:
- Passive scale error: -75%, -50%, -25%, 0%, +25%, +50%.
- Action-effect leakage into no-op estimate: 0%, 10%, 25%, 50%, 75%, 100%.
- Bias direction: task-aligned, task-opposed, random.
- Spatial smoothing and local leakage.

Metrics:
- Residual success, true-effect erasure rate, passive residual hallucination rate, distractor selection, and calibration error.

### Family C: Spatial Overlap And Occlusion

Purpose: Test the hard case where passive and robot-caused motion occupy nearby or overlapping points.

Settings:
- Spatial overlap fraction: 0.0, 0.25, 0.50, 0.75, 1.00.
- Occluded caused points: 0%, 25%, 50%.
- Passive points adjacent to controllable contact.

Metrics:
- Contact ranking accuracy, false controllability, missed controllable contact, flow endpoint error versus effect-ranking error.

### Family D: Ego-Motion And Global Passive Fields

Purpose: Show when camera or platform motion fools total flow and when residualization helps.

Settings:
- Global translation and rotation fields.
- Conveyor-like uniform passive fields.
- Gravity-like downward passive drift.
- Combination of ego-motion plus local passive distractors.

Metrics:
- Planner success, global-field subtraction error, residual alignment, and failure mode attribution.

### Family E: Learned No-Op Estimator Proxy

Purpose: Move beyond perfect analytic no-action subtraction without claiming real learning.

Estimator variants:
- Finite-sample linear no-op predictor.
- Ridge no-op predictor from scene features.
- Biased predictor trained with action-contaminated samples.
- Conservative residual with uncertainty buffer.

Metrics:
- No-op prediction error, residual ranking error, success, calibration, and sample complexity.

### Family F: Dense-Field Metrics Versus Planning Metrics

Purpose: Attack the common assumption that lower flow endpoint error implies better interaction planning.

Settings:
- Estimators with low total-flow endpoint error but wrong causal ranking.
- Estimators with higher endpoint error but correct effect ranking.
- Flow noise localized at passive distractors versus controllable contacts.

Metrics:
- Endpoint error, caused-flow ranking accuracy, selected-contact success, and correlation between perception metric and planning metric.

### Family G: Ablations And Negative Controls

Purpose: Separate the causal estimand from incidental scoring choices.

Ablations:
- Total flow only.
- Passive flow only.
- Residual with perfect no-op.
- Residual with scale error.
- Residual with action leakage.
- Residual with random no-op baseline.
- Residual plus contact prior.
- Oracle effect field.

Metrics:
- Success, distractor selection, caused progress, and regret.

## Figures And Tables

Required figures:
- Multi-distractor success and distractor-selection curves.
- Misspecification heatmap for scale error and effect leakage.
- Spatial-overlap stress curves.
- Ego-motion/global passive-field comparison.
- Learned no-op sample-complexity curve.
- Endpoint-error versus planning-success scatter.
- Ablation waterfall.

Required tables:
- Main multi-distractor comparison.
- Misspecification table.
- Spatial overlap table.
- Ego-motion table.
- Learned no-op estimator table.
- Perception-versus-planning table.
- Ablation table.
- Runtime/RAM-light table.
- Claim-to-evidence table.

## Manuscript Expansion

Target structure:
- Abstract with v3 full-scale numbers and honest boundary.
- Introduction framing scene flow as the wrong estimand for interaction when passive motion is confounded with controllable motion.
- Related work boundary against scene flow, affordance flow, action-conditioned prediction, visual foresight, and causal confusion.
- Formal definitions: total flow, passive flow, causal effect flow, contact ranking, no-action calibration, and ranking margin.
- Algorithms: total-flow planner, residual planner, learned no-op residual, contact-prior residual, and oracle effect planner.
- Experiment design across seven families.
- Results with generated figures and tables.
- Failure analysis: under-subtraction, over-subtraction, action leakage, spatial overlap, ego-motion, endpoint-error mismatch.
- Limitations: synthetic evidence, no real RGB-D learning, no high-fidelity simulator, no guarantee that no-op counterfactual exists or is identifiable in every scene.
- Appendices: proof details, parameter grids, pseudocode, artifact schema, baseline fairness, self-attacks, deployment roadmap, and final audit.

Page strategy:
- Minimum internal threshold is 25 pages.
- Length must come from real content: richer synthetic scenes, learned-estimator proxy, endpoint-error/planning mismatch, stronger baselines, negative controls, and detailed appendices.

## RAM-Light Execution Strategy

- Use vectorized NumPy generation for point clouds, contacts, passive fields, and residual scores.
- Store summary rows and selected diagnostic examples, not full dense fields for every trial.
- Run families sequentially with progress checkpoints.
- Keep dense field sizes modest but replicate settings across seeds.
- Generate tables and figures from CSV summaries.
- Use NumPy-only linear/ridge predictors for learned no-op proxy unless an existing dependency is already present.

## Documentation Updates

Update after the full-scale pass:
- `README.md`
- `child_status.md`
- `docs/claims.md`
- `docs/evidence_summary.md`
- `docs/experiment_rigor_checklist.md`
- `docs/reproducibility_checklist.md`
- `docs/reviewer_attacks.md`
- `docs/hostile_reviewer_response.md`
- `docs/submission_attack_log.md`
- `docs/submission_version_log.md`
- `docs/final_audit.md`
- `docs/submission_readiness_decision.md`

## Acceptance Checklist

Paper14 is not final until all are true:
- Full-scale runner completes and writes `results/full_scale/progress.json` with stage `complete`.
- Edited Python files pass `python -m py_compile`.
- Figures and tables are regenerated from v3 summaries.
- Manuscript compiles with `pdflatex`, `bibtex`, `pdflatex`, `pdflatex`.
- Final PDF has at least 25 pages.
- Claims match generated CSVs/tables.
- Limitations explicitly include synthetic evidence, no learned real RGB-D estimator, no hardware, no high-fidelity simulator, and no guarantee that a calibrated no-action counterfactual is always identifiable.
- Canonical PDF is copied to `C:/Users/wangz/Downloads/14.pdf` only after final verification.
- No new Desktop PDF copy is created.
- Local `paper/main.pdf` is removed after final copy.
- Commit is pushed.
- Worktree is clean and `HEAD` matches upstream before moving to Paper15.
