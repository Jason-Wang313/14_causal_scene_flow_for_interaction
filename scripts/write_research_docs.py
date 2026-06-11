"""Write research-decision documents from the literature matrix and evidence."""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"
MATRIX = DOCS / "related_work_matrix.csv"
SUMMARY = DATA / "experiment_summary.json"


HIDDEN_ASSUMPTIONS = [
    "Scene flow is an exogenous perception target rather than an action-conditioned causal variable.",
    "All observed motion is equally useful for manipulation planning.",
    "Passive motion can be treated as nuisance noise after training a sufficiently good predictor.",
    "The robot-caused component can be learned from passive video statistics.",
    "A dense correspondence field is enough to infer what the robot can change.",
    "The same flow representation should serve passive prediction and control.",
    "Background, camera, and environmental motion are either known or ignorable.",
    "Rigid or smooth motion priors survive contact-rich manipulation.",
    "Object identity and part identity remain fixed across intervention.",
    "Short-horizon displacement is a reliable proxy for task progress.",
    "Action labels alone bind observed motion to the robot's actual effect.",
    "No-action futures are either static or irrelevant.",
    "Planner rollouts can tolerate exogenous motion mixed into controllable motion.",
    "Flow evaluation can be action-agnostic without damaging downstream planning.",
    "Multi-object causal chains are rare enough to ignore.",
    "The sensor sees the contact geometry that created the flow.",
    "Passive articulated motion and robot-induced articulation are equivalent affordance evidence.",
    "Simulation covers the passive/caused mixture encountered in real scenes.",
    "Moving points are better action targets than still points.",
    "A stronger backbone can absorb causal confounding without changing the objective.",
    "Uncertainty estimates repair causal attribution mistakes.",
    "Active data collection alone resolves the distinction between do-caused and merely observed motion.",
]


PAPER_DIRECTIONS = [
    (
        "Causal effect flow for manipulation planning",
        "Estimate a dense treatment-effect field C_a(x)=E[Delta x | do(a),s]-E[Delta x | do(noop),s] and plan over C_a rather than total scene flow.",
        "Changes the central mechanism from correspondence estimation to action-causal attribution; directly breaks the all-observed-motion assumption.",
    ),
    (
        "No-action world models as robot affordance baselines",
        "Train a passive dynamics model and treat action affordance as residual controllable progress.",
        "Strong but easier to dismiss as background subtraction unless tied to intervention semantics.",
    ),
    (
        "Contact-gated scene flow",
        "Predict which flow vectors can be mediated by feasible robot contact geometry.",
        "Useful, but can collapse into combining contact prediction with existing flow.",
    ),
    (
        "Counterfactual scene-flow benchmark",
        "Evaluate flow models by their ability to predict action differences under matched passive futures.",
        "Valuable infrastructure, but benchmark-only is a forbidden weak move without a new mechanism.",
    ),
    (
        "Multi-object causal-chain flow",
        "Track direct and indirect robot effects through object-object contacts.",
        "Ambitious but harder to support with evidence in this run.",
    ),
    (
        "Exogenous-motion-aware MPC",
        "Augment a planner with an explicit passive dynamics term and an action-effect term.",
        "A planning formulation follows naturally from the chosen direction, not the standalone novelty.",
    ),
]


def read_rows() -> list[dict[str, str]]:
    with MATRIX.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def truncate(text: str, limit: int = 92) -> str:
    text = " ".join((text or "").split())
    if len(text) <= limit:
        return text
    return text[: limit - 3] + "..."


def write(path: str, text: str) -> None:
    (DOCS / path).write_text(text.strip() + "\n", encoding="utf-8")


def literature_map(rows: list[dict[str, str]]) -> None:
    theme_counts = Counter(r["primary_theme"] for r in rows)
    top_titles = rows[:20]
    lines = [
        "# Literature Map",
        "",
        "## Field Box",
        "",
        "The field box is 3D perception for robotics, narrowed to dense motion representations that influence manipulation, planning, and physical interaction. The sweep covers scene flow and optical flow, point-cloud motion, robot manipulation, contact and interaction dynamics, object-centric models, causal/counterfactual learning, and action-conditioned world models.",
        "",
        "## Coverage",
        "",
        f"- Landscape sweep: {len(rows)} papers in `docs/related_work_matrix.csv`.",
        f"- Serious skim set: {sum(1 for r in rows if r['serious_skim'] == 'yes')} papers.",
        f"- Deep-read pressure set: {sum(1 for r in rows if r['deep_read'] == 'yes')} papers.",
        f"- Hostile prior-work set: {sum(1 for r in rows if r['hostile_prior'] == 'yes')} papers.",
        "- Data source: OpenAlex metadata/abstracts plus manually seeded anchor papers; extraction fields are heuristic and auditable in the CSV.",
        "",
        "## Topic Clusters",
        "",
    ]
    for theme, count in theme_counts.most_common():
        lines.append(f"- `{theme}`: {count} entries.")
    lines += [
        "",
        "## Twenty-Two Hidden Assumptions That May Be False",
        "",
    ]
    for idx, assumption in enumerate(HIDDEN_ASSUMPTIONS, start=1):
        lines.append(f"{idx}. {assumption}")
    lines += [
        "",
        "## Directions Generated By Breaking The Assumptions",
        "",
    ]
    for name, mechanism, reason in PAPER_DIRECTIONS:
        lines.append(f"- **{name}.** Mechanism: {mechanism} Why it matters: {reason}")
    lines += [
        "",
        "## Highest-Pressure Papers At The Boundary",
        "",
        "| Rank | Paper | Theme | Mechanism | What remains open |",
        "| ---: | --- | --- | --- | --- |",
    ]
    for row in top_titles:
        lines.append(
            "| {rank} | {title} ({year}) | {theme} | {mech} | {open} |".format(
                rank=row["landscape_rank"],
                title=truncate(row["title"], 70),
                year=row["year"],
                theme=row["primary_theme"],
                mech=truncate(row["actual_mechanism_introduced"], 70),
                open=truncate(row["what_it_leaves_open"], 90),
            )
        )
    lines += [
        "",
        "## Readout",
        "",
        "The strongest direction is not a larger scene-flow estimator. It is a change in what the flow variable means for a robot: from total observed displacement to an intervention-defined effect field. This is the one move that survives the hostile set because scene-flow papers own dense correspondence, manipulation papers own action-conditioned behavior, and causal papers own intervention semantics, but their overlap rarely defines a dense 3D treatment-effect field that a planner can directly optimize.",
    ]
    write("literature_map.md", "\n".join(lines))


def hostile_prior_work(rows: list[dict[str, str]]) -> None:
    hostile = [r for r in rows if r["hostile_prior"] == "yes"][:100]
    lines = [
        "# Hostile Prior Work",
        "",
        "This file records the 100-paper hostile set used to pressure-test novelty. The full extraction fields are in `docs/related_work_matrix.csv`; this view keeps the closest threats readable.",
        "",
        "| # | Paper | Problem claimed | Mechanism | Hidden assumption | Leaves open |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for row in hostile:
        lines.append(
            "| {rank} | {title} ({year}) | {problem} | {mech} | {assumption} | {open} |".format(
                rank=row["landscape_rank"],
                title=truncate(row["title"], 62),
                year=row["year"],
                problem=truncate(row["problem_claimed"], 72),
                mech=truncate(row["actual_mechanism_introduced"], 72),
                assumption=truncate(row["hidden_assumptions"], 72),
                open=truncate(row["what_it_leaves_open"], 82),
            )
        )
    lines += [
        "",
        "## Closest Threats",
        "",
        "- Scene-flow methods such as FlowNet3D, PointPWC-Net, RAFT-3D, NSFP, and Scene Flow Fields make dense 3D motion estimation non-novel by itself.",
        "- FlowBot3D and related articulation-flow manipulation papers make action-oriented flow for manipulation non-novel if the claim is only that motion vectors can guide contact selection.",
        "- Visual foresight, video-prediction planning, Transporter Networks, and learned manipulation dynamics make action-conditioned prediction non-novel by itself.",
        "- Causal representation and causal-confusion work make intervention language non-novel by itself.",
        "",
        "## Surviving Gap",
        "",
        "The gap is the dense, action-indexed causal effect field: a planner asks which future 3D motion would disappear under a no-action counterfactual, not which motion is visible or predictable. Existing work often estimates total motion, action outcomes, or causal variables separately; the proposed paper makes their difference the planning primitive.",
    ]
    write("hostile_prior_work.md", "\n".join(lines))


def novelty_boundary(rows: list[dict[str, str]]) -> None:
    lines = [
        "# Novelty Boundary Map",
        "",
        "## Not Novel",
        "",
        "- Estimating 3D scene flow from point clouds or RGB-D.",
        "- Using self-supervised consistency, cost volumes, recurrent updates, rigid-motion priors, or coordinate MLP priors for scene flow.",
        "- Using predicted visual motion for robot planning.",
        "- Learning affordance flow for articulated objects.",
        "- Training a better dynamics model or larger perception backbone.",
        "- Adding uncertainty, active data collection, verification, or an LLM planner as the main contribution.",
        "",
        "## Potentially Novel",
        "",
        "- Treating robot-caused flow as a treatment effect: `C_a(s,x)=E[Delta x | do(a),s]-E[Delta x | do(noop),s]`.",
        "- Making the planner optimize the caused component rather than the total future displacement.",
        "- Showing a formal counterexample where total-flow planning provably chooses a passive distractor.",
        "- Providing a runnable stress test in which increasing passive motion breaks total-flow ranking while causal effect flow remains accurate when the no-action baseline is accurate.",
        "",
        "## Boundary Conditions",
        "",
        "- If passive dynamics are zero or identical across all candidate actions, total-flow and causal-flow rankings can coincide.",
        "- If passive no-action flow is estimated poorly enough to exceed the action-effect margin, causal-flow planning can fail.",
        "- If a prior method already computes an intervention-defined dense 3D do-difference field and plans on it directly, this paper's novelty collapses to exposition.",
        "- The current evidence does not establish real-robot success or learned estimator quality.",
        "",
        "## Formal Boundary",
        "",
        "For candidate contacts `i`, let total score be `T_i=<P_i + E_i, g>` and causal score be `C_i=<E_i, g>`, where `P_i` is passive flow, `E_i` is robot-caused effect, and `g` is task progress direction. If some distractor `d` has `<P_d,g> + <E_d,g> > <P_c,g> + <E_c,g>` but `<E_c,g> > <E_d,g>` for the true controllable contact `c`, total-flow ranking selects `d` while causal-flow ranking selects `c`. This is the paper's core claim, not a claim about a particular neural architecture.",
    ]
    write("novelty_boundary_map.md", "\n".join(lines))


def novelty_decision() -> None:
    lines = [
        "# Novelty Decision",
        "",
        "## Chosen Thesis",
        "",
        "Robots should plan manipulation actions using causal scene flow: a dense 3D treatment-effect field that subtracts the no-action passive future from the action future. The field answers, point by point, what motion the robot would cause rather than what motion it would merely observe.",
        "",
        "## Central Mechanism",
        "",
        "The central mechanism is do-differenced flow decomposition:",
        "",
        "`C_a(s,x) = E[X_{t+1}(x)-X_t(x) | do(a), s] - E[X_{t+1}(x)-X_t(x) | do(noop), s]`.",
        "",
        "A manipulation planner then scores contacts or actions with `C_a`, not with total predicted flow. This explicitly separates passive scene dynamics from robot-caused dynamics.",
        "",
        "## Why This Direction Beats Alternatives",
        "",
        "- It changes the variable being optimized, not just the model size, data source, benchmark, uncertainty wrapper, verifier, or planner.",
        "- It directly attacks the hostile scene-flow prior work: they own dense motion, but not action treatment-effect flow.",
        "- It directly attacks hostile manipulation prior work: they own action-conditioned behavior, but usually do not audit whether the predicted motion is caused by the robot or passive background dynamics.",
        "- It is testable with a crisp counterexample and a runnable stress test.",
        "",
        "## Rejected Directions",
        "",
        "- A new 3D scene-flow architecture: too close to FlowNet3D/RAFT-3D/PointPWC/NSFP and a forbidden bigger-model move.",
        "- A new benchmark only: useful, but insufficient without a central mechanism.",
        "- A planner that adds uncertainty to flow: uncertainty does not identify causal effect.",
        "- LLM or reinforcement-learning planning over scene flow: forbidden weak move and not necessary for the causal claim.",
        "",
        "## Final Choice",
        "",
        "Proceed with an ICLR-style paper titled `Causal Scene Flow for Interaction`, focused on causal effect-flow decomposition and its planning consequences.",
    ]
    write("novelty_decision.md", "\n".join(lines))


def claims(summary: dict[str, float]) -> None:
    lines = [
        "# Claims",
        "",
        "| Claim | Status | Support | Limitations |",
        "| --- | --- | --- | --- |",
        "| Dense total scene flow can be a bad manipulation-planning objective under passive exogenous motion. | Supported in formal toy setting and synthetic stress test. | Inequality counterexample plus simulation. | Does not say all total-flow planners fail in all tasks. |",
        "| Causal effect flow can be defined as an action/no-action do-difference field. | Definitional/formal. | SCM-style intervention definition in paper. | Requires a meaningful no-action baseline and state conditioning. |",
        "| If passive-estimation error is below the effect margin, causal-flow ranking recovers the controllable contact in the toy setting. | Supported by proposition. | Formal margin argument. | Assumes candidate set contains the true contact and effects are pointwise comparable. |",
        f"| In the implemented stress test at confound strength 2.0 and passive-estimation noise 0.10, causal-flow success exceeds total-flow success by {summary['causal_advantage_at_confound_2_noise_0p10']:.3f}. | Supported by code. | `experiments/causal_scene_flow_sim.py`, {summary['total_trials']} trials. | Synthetic only; no real robot. |",
        "| Existing scene-flow and manipulation papers do not make total-flow prediction novel. | Supported by literature sweep. | 1200-row matrix and hostile prior set. | Metadata/abstract-level extraction, not exhaustive full-text review. |",
        "| The proposed method will improve real manipulation systems. | Unsupported. | None in this run. | Marked as future work. |",
        "| The proposed decomposition can be learned accurately from real RGB-D data. | Unsupported. | None in this run. | Requires future datasets or robot experiments. |",
        "",
        "## Honest Claim Scope",
        "",
        "The paper is ready as a mechanism-and-counterexample paper, not as a real-robot systems paper. Its strongest claim is conceptual and diagnostic: planning on total motion is not causally invariant to passive motion.",
    ]
    write("claims.md", "\n".join(lines))


def reviewer_attacks(summary: dict[str, float]) -> None:
    lines = [
        "# Reviewer Attacks",
        "",
        "## Attack 1: This is just background subtraction.",
        "",
        "Response: In the simplest case it reduces to subtracting a no-action passive flow, but the definition is intervention-based. The baseline is `do(noop)` conditioned on the same state, not a geometric background mask. That matters for articulated objects, moving cameras, conveyors, and multi-object scenes where passive object motion is foreground but still not robot-caused.",
        "",
        "## Attack 2: FlowBot3D already predicts motion for manipulation.",
        "",
        "Response: FlowBot3D is a closest hostile prior because it uses flow-like articulation affordances. The boundary is that this paper distinguishes motion that would happen anyway from motion caused by the robot. FlowBot-style articulation flow makes motion useful for manipulation, but does not by itself define a no-action counterfactual effect field.",
        "",
        "## Attack 3: Action-conditioned dynamics models already compare outcomes across actions.",
        "",
        "Response: Many dynamics models can in principle represent this. The paper's claim is that the planner should optimize the action-effect component and that total predicted displacement is provably non-invariant under passive confounding. If a dynamics paper already subtracts the passive no-op dense 3D field and plans on the residual, it is the closest predecessor and should be cited as such.",
        "",
        "## Attack 4: The evidence is synthetic and too easy.",
        "",
        "Response: Correct. The result is a controlled counterexample designed to prove the broken assumption matters, not a benchmark claim. The final paper must not claim real-robot superiority.",
        "",
        "## Attack 5: Estimating the passive future is hard.",
        "",
        "Response: Also correct. The proposition includes a passive-estimation margin; the simulation sweeps passive-estimation noise. The mechanism is valuable only when the no-action baseline is more accurate than the action-effect margin.",
        "",
        "## Attack 6: If passive flow is constant across actions, it cancels.",
        "",
        "Response: It cancels for pure action selection over a fixed contact and fixed object. It does not cancel for contact discovery, object selection, moving distractors, waiting/intervention choices, or planners that score dense moving regions.",
        "",
        "## Attack 7: Causal language is overkill.",
        "",
        "Response: The causal framing prevents a common mistake: treating observed change as controllable affordance. The paper can be read without heavy causal machinery as no-op-differenced flow, but the do-operator clarifies the estimand.",
        "",
        "## Attack 8: The planner is trivial.",
        "",
        "Response: Yes. That is intentional: a trivial planner isolates the representational failure. More complex MPC can use the same field, but the contribution should not hide behind planner complexity.",
        "",
        "## Attack 9: The literature sweep uses heuristic extraction.",
        "",
        "Response: The sweep is broad and auditable, but not a substitute for a final manual related-work pass. The audit must mark this limitation.",
        "",
        "## Attack 10: The title promises interaction but the experiment is point selection.",
        "",
        "Response: The title is acceptable only if the paper clearly frames interaction as robot-caused physical change and avoids claiming full contact-rich manipulation experiments.",
        "",
        "## Numeric Stress Point",
        "",
        f"At confound strength 2.0/noise 0.10, total-flow success is {summary['at_confound_2_noise_0p10_total_success']:.3f}; causal-flow success is {summary['at_confound_2_noise_0p10_causal_success']:.3f}. This is a counterexample regime, not a representative benchmark average.",
    ]
    write("reviewer_attacks.md", "\n".join(lines))


def main() -> int:
    rows = read_rows()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    literature_map(rows)
    hostile_prior_work(rows)
    novelty_boundary(rows)
    novelty_decision()
    claims(summary)
    reviewer_attacks(summary)
    print("wrote research docs", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
