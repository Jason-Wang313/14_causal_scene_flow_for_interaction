# Evidence Summary

The experiment is a synthetic intervention test, not a real-robot claim. It isolates the exact failure mode targeted by the paper: passive motion aligned with the task goal can dominate total scene flow while being unaffected by the robot.

- Grid rows: 40
- Trials per row: 2000
- Total trials: 80000
- At passive-confound strength 0.0 and passive-estimation noise 0.10, total-flow success is 1.000; causal-flow success is 1.000.
- At passive-confound strength 2.0 and passive-estimation noise 0.10, total-flow success is 0.000; causal-flow success is 1.000.
- At that setting, the total-flow planner chooses the passive distractor 1.000 of trials; causal-flow chooses it 0.000.
- Causal advantage at confound 2.0/noise 0.10: 1.000.
- Plots generated: yes

Interpretation: the evidence supports the mechanistic claim that planning on total flow is not invariant to passive exogenous motion, while planning on a do-difference field is robust when the passive estimate is accurate enough. It does not support claims about real-robot performance, learned perception accuracy, or benchmark superiority.
