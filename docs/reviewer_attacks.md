# Reviewer Attacks

## Attack 1: This is just background subtraction.

Response: In the simplest case it reduces to subtracting a no-action passive flow, but the definition is intervention-based. The baseline is `do(noop)` conditioned on the same state, not a geometric background mask. That matters for articulated objects, moving cameras, conveyors, and multi-object scenes where passive object motion is foreground but still not robot-caused.

## Attack 2: FlowBot3D already predicts motion for manipulation.

Response: FlowBot3D is a closest hostile prior because it uses flow-like articulation affordances. The boundary is that this paper distinguishes motion that would happen anyway from motion caused by the robot. FlowBot-style articulation flow makes motion useful for manipulation, but does not by itself define a no-action counterfactual effect field.

## Attack 3: Action-conditioned dynamics models already compare outcomes across actions.

Response: Many dynamics models can in principle represent this. The paper's claim is that the planner should optimize the action-effect component and that total predicted displacement is provably non-invariant under passive confounding. If a dynamics paper already subtracts the passive no-op dense 3D field and plans on the residual, it is the closest predecessor and should be cited as such.

## Attack 4: The evidence is synthetic and too easy.

Response: Correct. The result is a controlled counterexample designed to prove the broken assumption matters, not a benchmark claim. The final paper must not claim real-robot superiority.

## Attack 5: Estimating the passive future is hard.

Response: Also correct. The proposition includes a passive-estimation margin; the simulation sweeps passive-estimation noise. The mechanism is valuable only when the no-action baseline is more accurate than the action-effect margin.

## Attack 6: If passive flow is constant across actions, it cancels.

Response: It cancels for pure action selection over a fixed contact and fixed object. It does not cancel for contact discovery, object selection, moving distractors, waiting/intervention choices, or planners that score dense moving regions.

## Attack 7: Causal language is overkill.

Response: The causal framing prevents a common mistake: treating observed change as controllable affordance. The paper can be read without heavy causal machinery as no-op-differenced flow, but the do-operator clarifies the estimand.

## Attack 8: The planner is trivial.

Response: Yes. That is intentional: a trivial planner isolates the representational failure. More complex MPC can use the same field, but the contribution should not hide behind planner complexity.

## Attack 9: The literature sweep uses heuristic extraction.

Response: The sweep is broad and auditable, but not a substitute for a final manual related-work pass. The audit must mark this limitation.

## Attack 10: The title promises interaction but the experiment is point selection.

Response: The title is acceptable only if the paper clearly frames interaction as robot-caused physical change and avoids claiming full contact-rich manipulation experiments.

## Numeric Stress Point

At confound strength 2.0/noise 0.10, total-flow success is 0.000; causal-flow success is 1.000. This is a counterexample regime, not a representative benchmark average.
