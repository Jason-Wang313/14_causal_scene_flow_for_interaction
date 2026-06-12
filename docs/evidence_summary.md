# Evidence Summary

The experiment is a synthetic intervention test, not a real-robot claim. It isolates the exact failure mode targeted by the paper: passive motion aligned with the task goal can dominate total scene flow while being unaffected by the robot.

- Grid rows: 40
- Trials per row: 2000
- Total trials: 80000
- At passive-confound strength 0.0 and passive-estimation noise 0.10, total-flow success is 1.000; causal-flow success is 1.000.
- At passive-confound strength 2.0 and passive-estimation noise 0.10, total-flow success is 0.000; causal-flow success is 1.000.
- At that setting, the total-flow planner chooses the passive distractor 1.000 of trials; causal-flow chooses it 0.000.
- Causal advantage at confound 2.0/noise 0.10: 1.000.
- V2 misspecification stress at confound 2.0/noise 0.10: calibrated no-op residual success is 1.000; under-subtracting passive flow by 50% lowers residual success to 0.387; leaking 75% of the robot effect into the no-op estimate lowers success to 0.505; no subtraction has success 0.001.
- Plots generated: yes

Interpretation: the evidence supports the mechanistic claim that planning on total flow is not invariant to passive exogenous motion, while planning on a do-difference field is robust when the passive estimate is accurate enough. It does not support claims about real-robot performance, learned perception accuracy, or benchmark superiority.
The v2 stress makes the main boundary explicit: the no-action future must be calibrated and uncontaminated by the robot action, or the residual can collapse toward total-flow behavior or erase true action effects.
