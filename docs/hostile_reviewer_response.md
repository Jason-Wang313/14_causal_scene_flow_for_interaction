# Hostile Reviewer Response

The strongest version of the criticism is correct: causal scene flow only helps if the no-action future is a meaningful and calibrated counterfactual. The v2 paper now makes that dependency explicit rather than hiding it behind the clean counterexample.

At confound strength 2.0 and passive-estimation noise 0.10, calibrated residual planning succeeds in 1.000 of trials while total-flow planning succeeds in 0.000. But the v2 stress shows the failure boundary: 50% passive under-subtraction lowers residual success to 0.387, and 75% action-effect leakage into the no-action estimate lowers residual success to 0.505.

The revised claim is therefore not that causal scene flow is solved, learned, or robot-validated. The claim is that total flow is the wrong estimand for interaction under passive confounding, and that a matched no-action residual is the correct planning variable when it can be estimated accurately enough.
