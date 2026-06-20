# Submission Attack Log

Checked: 2026-06-20

## Hostile Round 1: This is just a perfect no-op subtraction toy

Result: Addressed for mechanism-scope submission.

Action: Added seven v3 experiment families. The suite includes multi-distractor scenes, passive scale and leakage surfaces, spatial overlap and occlusion, ego/global passive fields, a learned no-op proxy, endpoint-error mismatch, and ablations.

## Hostile Round 2: The paper overpromises learned robot performance

Result: Claim narrowed and made explicit.

Action: The claims ledger, readiness decision, manuscript limitations, and reviewer response all state that this is a full-scale mechanism/counterexample paper, not a real-robot system or learned RGB-D benchmark result.

## Hostile Round 3: Runtime and reproducibility are fragile

Result: Addressed.

Action: The v3 runner uses deterministic seeds, sequential family execution, compact CSV summaries, progress JSON, metadata JSON, and regenerated LaTeX tables/figures under `results/full_scale/`.

## Hostile Round 4: Stronger baselines might close the gap

Result: Partially addressed.

Action: Added attention/contact scoring, action-conditioned total-flow, learned no-op proxy, passive-only negative control, random no-op residual, and oracle effect. In the main setting, action-conditioned total flow reaches 0.614 success while causal residual and oracle effect reach 1.000.

## Hostile Round 5: Endpoint error is enough

Result: Addressed as a conceptual attack.

Action: Family F constructs low-endpoint-error but wrong-ranking and higher-endpoint-error but correct-ranking estimators. The manuscript now argues that interaction perception must report effect-ranking metrics, not only total-flow endpoint error.

## Hostile Round 6: PDF link styling may silently drift from the VLA role model

Result: Incorporated.

Action: Added explicit `\hypersetup` policy in `paper/main.tex`, rebuilt the final PDF, and verified 64 boxed link annotations: green = 48, red = 16, cyan = 0, all with border `(0, 0, 1)`. Rendered affected pages 1, 2, 4, 5, 7, and 8 and confirmed the boxes are visually crisp and aligned.
