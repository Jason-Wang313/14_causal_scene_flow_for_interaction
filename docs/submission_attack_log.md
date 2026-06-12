# Submission Attack Log

Checked: 2026-06-12 23:46:59 +01:00

## Hostile Round 1: This is just a perfect no-op subtraction toy

Result: Recoverable.

Action: Added passive-baseline misspecification stress at the same confound 2.0/noise 0.10 setting used by the main counterexample. The calibrated residual planner succeeds in 1.000 of trials, but 50% passive under-subtraction drops success to 0.387 and 75% action-effect leakage into the no-action estimate drops success to 0.505.

## Hostile Round 2: The paper overpromises learned robot performance

Result: Claim narrowed.

Action: The abstract, results, claims ledger, reviewer attacks, and limitations now say this is a mechanism-and-counterexample paper, not a learned RGB-D or real-robot system.

## Hostile Round 3: Runtime and reproducibility are fragile

Result: Recoverable.

Action: Added a vectorized deterministic path for the 80,000-trial grid. The experiment now regenerates the full grid and v2 stress table in about 19 seconds on the local machine.
