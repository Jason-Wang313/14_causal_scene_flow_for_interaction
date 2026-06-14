# Novelty Boundary Map

## Not Novel

- Estimating 3D scene flow from point clouds or RGB-D.
- Using self-supervised consistency, cost volumes, recurrent updates, rigid-motion priors, or coordinate MLP priors for scene flow.
- Using predicted visual motion for robot planning.
- Learning affordance flow for articulated objects.
- Training a better dynamics model or larger perception backbone.
- Adding uncertainty, active data collection, verification, or an LLM planner as the main contribution.

## Potentially Novel

- Treating robot-caused flow as a treatment effect: `C_a(s,x)=E[Delta x | do(a),s]-E[Delta x | do(noop),s]`.
- Making the planner optimize the caused component rather than the total future displacement.
- Showing a formal counterexample where total-flow planning provably chooses a passive distractor.
- Providing a full-scale synthetic stress suite in which increasing passive motion breaks total-flow ranking while causal effect flow remains accurate when the no-action baseline is calibrated.
- Demonstrating that endpoint error relative to total flow can be anti-aligned with interaction success.

## Boundary Conditions

- If passive dynamics are zero or identical across all candidate actions, total-flow and causal-flow rankings can coincide.
- If passive no-action flow is estimated poorly enough to exceed the action-effect margin, causal-flow planning can fail.
- If the no-action estimate leaks robot-caused effects, the residual can erase the action effect.
- If a prior method already computes an intervention-defined dense 3D do-difference field and plans on it directly, this paper's novelty collapses to exposition.
- The current evidence does not establish real-robot success or learned estimator quality.

## Formal Boundary

For candidate contacts `i`, let total score be `T_i=<P_i + E_i, g>` and causal score be `C_i=<E_i, g>`, where `P_i` is passive flow, `E_i` is robot-caused effect, and `g` is task progress direction. If some distractor `d` has `<P_d,g> + <E_d,g> > <P_c,g> + <E_c,g>` but `<E_c,g> > <E_d,g>` for the true controllable contact `c`, total-flow ranking selects `d` while causal-flow ranking selects `c`. This is the paper's core claim, not a claim about a particular neural architecture.
