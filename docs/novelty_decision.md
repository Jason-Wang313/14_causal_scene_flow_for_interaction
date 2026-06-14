# Novelty Decision

## Chosen Thesis

Robots should plan manipulation actions using causal scene flow: a dense 3D treatment-effect field that subtracts the no-action passive future from the action future. The field answers, point by point, what motion the robot would cause rather than what motion it would merely observe.

## Central Mechanism

The central mechanism is do-differenced flow decomposition:

`C_a(s,x) = E[X_{t+1}(x)-X_t(x) | do(a), s] - E[X_{t+1}(x)-X_t(x) | do(noop), s]`.

A manipulation planner then scores contacts or actions with `C_a`, not with total predicted flow. This explicitly separates passive scene dynamics from robot-caused dynamics.

## Why This Direction Beats Alternatives

- It changes the variable being optimized, not just the model size, data source, benchmark, uncertainty wrapper, verifier, or planner.
- It directly attacks scene-flow prior work: prior work owns dense motion prediction, but not intervention-defined robot-caused dense motion as the planning objective.
- It directly attacks manipulation prior work: action-conditioned prediction may model outcomes, but the paper audits whether the predicted motion is caused by the robot or by passive background dynamics.
- The v3 evidence now tests the mechanism across multi-distractor scenes, misspecification surfaces, overlap and occlusion, ego/global passive fields, learned no-op proxies, endpoint-error mismatch, and ablations.

## Rejected Directions

- A new 3D scene-flow architecture: too close to FlowNet3D, RAFT-3D, PointPWC, NSFP, and other established perception work.
- A new benchmark only: useful, but insufficient without a central mechanism.
- A planner that adds uncertainty to flow: uncertainty does not identify causal effect.
- LLM or reinforcement-learning planning over scene flow: unnecessary for the causal estimand claim.

## Final Choice

Proceed with `Causal Scene Flow for Interaction` as a mechanism/counterexample paper. The novelty is the planning estimand and its failure analysis, not a new RGB-D architecture or real-robot benchmark.
