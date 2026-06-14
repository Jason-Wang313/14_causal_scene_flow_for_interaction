# Hostile Reviewer Response

The strongest criticism remains correct: causal scene flow only helps if the no-action future is a meaningful and calibrated counterfactual. The v3 paper now treats that as a central boundary condition and tests it directly rather than hiding it behind a clean counterexample.

At the main multi-distractor passive-confound setting, total-flow planning succeeds in 0.000 of trials and selects a passive distractor in 1.000. Causal-residual planning succeeds in 1.000 and selects a passive distractor in 0.000. The action-conditioned total-flow baseline reaches 0.614, which is stronger than raw total flow but still below the residual and oracle effect.

The boundary is sharp. Under-subtracting passive flow by 50% leaves enough passive motion in the residual that success falls to 0.037. Leaking 75% of the robot effect into the no-action estimate still leaves 0.706 success, but complete leakage nearly erases the advantage. Endpoint-error tests also show why total-flow accuracy is not enough: a predictor can be accurate about passive motion and still be wrong for interaction.

The correct final claim is therefore not that causal scene flow is solved, learned, or robot-validated. The claim is that total flow is the wrong estimand for interaction under passive confounding, and that a matched no-action residual is the correct planning variable when it can be estimated accurately enough.
