# Evidence Summary

The v3 evidence package is a synthetic intervention suite designed to isolate the paper's causal estimand claim: observed total motion is not the same as robot-caused motion. It does not claim real-robot performance.

## Original v2 Evidence

- Original grid rows: 40
- Trials per row: 2,000
- Total trials: 80,000
- At passive-confound strength 2.0 and passive-estimation noise 0.10, total-flow success is 0.000 and causal-flow success is 1.000.
- At that setting, total-flow chooses the passive distractor in 1.000 of trials and causal-flow chooses it in 0.000.

## Full-Scale v3 Evidence

- Seven experiment families completed under `results/full_scale/`.
- Total v3 seed-row summaries: 1,910.
- Plot failures: 0.
- Family A multi-distractor setting: total-flow success 0.000, causal-residual success 1.000, total-flow distractor selection 1.000, causal-residual distractor selection 0.000.
- Action-conditioned total-flow baseline success: 0.614.
- Family B misspecification: 50% passive under-subtraction lowers residual success to 0.037; 75% action-effect leakage yields 0.706 success.
- Family C overlap: full spatial overlap with no occlusion retains 0.999 success; full overlap with 50% occlusion remains substantially harder.
- Family E learned no-op proxy: finite-sample proxy settings approach calibrated residual behavior at modest sample counts, but this is not a neural or real RGB-D learning result.
- Family F metric mismatch: endpoint error relative to total flow can reward passive-motion prediction even when planning rank is wrong.
- Family G ablations: total flow, passive-only flow, attention-contact scoring, and random no-op residuals fail in the main passive-confound regime; perfect residual and oracle effect succeed.

## Interpretation

The evidence supports the mechanism claim that planning on total flow is not invariant to passive exogenous motion, while planning on a do-difference residual is the right estimand when the no-action baseline is calibrated enough to preserve action-effect margins. It does not support claims about real-robot performance, learned RGB-D estimator accuracy, or benchmark superiority over deployed manipulation systems.

## Final PDF

- Path: `C:/Users/wangz/Downloads/14.pdf`
- Pages: 25
- Size: 389,425 bytes
- SHA256: `3CB0713C86F0DABBBCF325599FD36213A3D5C8A7AC3EE7BA17D102EC968C548B`
- VLA-style boxed-link audit: 64 annotations on pages `[(1, 19), (2, 29), (4, 4), (5, 6), (7, 4), (8, 2)]`; green = 48, red = 16, cyan = 0; all borders `(0, 0, 1)`.
- Visual audit: rendered pages 1, 2, 4, 5, 7, and 8 after export; citation/URL and internal-reference boxes are crisp and aligned.
