# Novelty Decision

## Chosen Thesis

Robots should plan manipulation actions using causal scene flow: a dense 3D treatment-effect field that subtracts the no-action passive future from the action future. The field answers, point by point, what motion the robot would cause rather than what motion it would merely observe.

## Central Mechanism

The central mechanism is do-differenced flow decomposition:

`C_a(s,x) = E[X_{t+1}(x)-X_t(x) | do(a), s] - E[X_{t+1}(x)-X_t(x) | do(noop), s]`.

A manipulation planner then scores contacts or actions with `C_a`, not with total predicted flow. This explicitly separates passive scene dynamics from robot-caused dynamics.

## Why This Direction Beats Alternatives

- It changes the variable being optimized, not just the model size, data source, benchmark, uncertainty wrapper, verifier, or planner.
- It directly attacks the hostile scene-flow prior work: they own dense motion, but not action treatment-effect flow.
- It directly attacks hostile manipulation prior work: they own action-conditioned behavior, but usually do not audit whether the predicted motion is caused by the robot or passive background dynamics.
- It is testable with a crisp counterexample and a runnable stress test.

## Rejected Directions

- A new 3D scene-flow architecture: too close to FlowNet3D/RAFT-3D/PointPWC/NSFP and a forbidden bigger-model move.
- A new benchmark only: useful, but insufficient without a central mechanism.
- A planner that adds uncertainty to flow: uncertainty does not identify causal effect.
- LLM or reinforcement-learning planning over scene flow: forbidden weak move and not necessary for the causal claim.

## Final Choice

Proceed with an ICLR-style paper titled `Causal Scene Flow for Interaction`, focused on causal effect-flow decomposition and its planning consequences.
