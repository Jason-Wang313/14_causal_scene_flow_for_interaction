"""Synthetic evidence for causal scene flow in manipulation planning.

The experiment models a tabletop point cloud with candidate contact points. A
subset of points has passive motion (for example, a conveyor, moving camera, or
externally actuated distractor) that is independent of the robot. One contact
point has a robot-caused effect aligned with the task goal. A total-flow planner
ranks candidate contacts by observed/predicted total flow; a causal-flow planner
ranks by an estimated do-difference field: total flow minus passive no-action
flow.
"""

from __future__ import annotations

import csv
import json
import math
import random
from pathlib import Path

try:
    import numpy as np
except Exception:  # pragma: no cover - stdlib fallback stays available.
    np = None


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGS = ROOT / "figures"
RESULTS = DATA / "experiment_results.csv"
SUMMARY = DATA / "experiment_summary.json"
MISSPEC = DATA / "passive_misspecification_stress.csv"
MISSPEC_TEX = DATA / "passive_misspecification_table.tex"
EVIDENCE_MD = ROOT / "docs" / "evidence_summary.md"


def dot(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def add(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def sub(a: tuple[float, float, float], b: tuple[float, float, float]) -> tuple[float, float, float]:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def mul(a: tuple[float, float, float], scale: float) -> tuple[float, float, float]:
    return (scale * a[0], scale * a[1], scale * a[2])


def noise_vec(rng: random.Random, sigma: float) -> tuple[float, float, float]:
    return (rng.gauss(0.0, sigma), rng.gauss(0.0, sigma), rng.gauss(0.0, sigma))


def run_trial(
    rng: random.Random,
    confound_strength: float,
    passive_estimation_noise: float,
    passive_scale: float = 1.0,
    passive_effect_leak: float = 0.0,
    candidates: int = 28,
) -> dict[str, float | int]:
    goal = (1.0, 0.0, 0.0)
    true_contact = rng.randrange(candidates)
    distractor = rng.randrange(candidates - 1)
    if distractor >= true_contact:
        distractor += 1

    passive = []
    effect = []
    observed_total = []
    passive_estimate = []

    for i in range(candidates):
        base_passive = noise_vec(rng, 0.04)
        base_effect = noise_vec(rng, 0.04)
        if i == true_contact:
            effect_mag = rng.uniform(0.75, 1.10)
            base_effect = add(base_effect, (effect_mag, rng.gauss(0.0, 0.05), rng.gauss(0.0, 0.02)))
            base_passive = add(base_passive, (rng.gauss(0.0, 0.08), rng.gauss(0.0, 0.08), 0.0))
        elif i == distractor:
            nuisance = confound_strength * rng.uniform(0.75, 1.25)
            base_passive = add(base_passive, (nuisance, rng.gauss(0.0, 0.04), 0.0))
            base_effect = add(base_effect, (rng.uniform(-0.10, 0.08), rng.gauss(0.0, 0.05), 0.0))
        else:
            if rng.random() < 0.20:
                base_passive = add(base_passive, (confound_strength * rng.uniform(0.05, 0.35), rng.gauss(0.0, 0.08), 0.0))
            base_effect = add(base_effect, (rng.uniform(-0.15, 0.22), rng.gauss(0.0, 0.08), 0.0))
        passive.append(base_passive)
        effect.append(base_effect)
        observed_total.append(add(add(base_passive, base_effect), noise_vec(rng, 0.035)))
        estimated_passive = add(mul(base_passive, passive_scale), mul(base_effect, passive_effect_leak))
        passive_estimate.append(add(estimated_passive, noise_vec(rng, passive_estimation_noise)))

    causal_estimate = [sub(observed_total[i], passive_estimate[i]) for i in range(candidates)]

    total_choice = max(range(candidates), key=lambda i: dot(observed_total[i], goal))
    causal_choice = max(range(candidates), key=lambda i: dot(causal_estimate[i], goal))
    oracle_choice = max(range(candidates), key=lambda i: dot(effect[i], goal))

    def progress(choice: int) -> float:
        return dot(effect[choice], goal)

    return {
        "total_success": int(progress(total_choice) > 0.50),
        "causal_success": int(progress(causal_choice) > 0.50),
        "oracle_success": int(progress(oracle_choice) > 0.50),
        "total_progress": progress(total_choice),
        "causal_progress": progress(causal_choice),
        "oracle_progress": progress(oracle_choice),
        "total_chose_distractor": int(total_choice == distractor),
        "causal_chose_distractor": int(causal_choice == distractor),
        "total_choice": total_choice,
        "causal_choice": causal_choice,
        "oracle_choice": oracle_choice,
        "true_contact": true_contact,
        "distractor": distractor,
    }


def aggregate(values: list[dict[str, float | int]], key: str) -> float:
    return sum(float(row[key]) for row in values) / max(1, len(values))


def run_trial_batch(
    seed: int,
    trials: int,
    confound_strength: float,
    passive_estimation_noise: float,
    passive_scale: float = 1.0,
    passive_effect_leak: float = 0.0,
    candidates: int = 28,
) -> dict[str, float]:
    if np is None:
        rng = random.Random(seed)
        trial_rows = [
            run_trial(
                rng,
                confound_strength,
                passive_estimation_noise,
                passive_scale=passive_scale,
                passive_effect_leak=passive_effect_leak,
                candidates=candidates,
            )
            for _ in range(trials)
        ]
        return {
            "total_success_rate": aggregate(trial_rows, "total_success"),
            "causal_success_rate": aggregate(trial_rows, "causal_success"),
            "oracle_success_rate": aggregate(trial_rows, "oracle_success"),
            "total_mean_progress": aggregate(trial_rows, "total_progress"),
            "causal_mean_progress": aggregate(trial_rows, "causal_progress"),
            "oracle_mean_progress": aggregate(trial_rows, "oracle_progress"),
            "total_distractor_rate": aggregate(trial_rows, "total_chose_distractor"),
            "causal_distractor_rate": aggregate(trial_rows, "causal_chose_distractor"),
        }

    rng = np.random.default_rng(seed)
    true_contact = rng.integers(0, candidates, size=trials)
    distractor = rng.integers(0, candidates - 1, size=trials)
    distractor = distractor + (distractor >= true_contact)

    passive_x = rng.normal(0.0, 0.04, size=(trials, candidates))
    effect_x = rng.normal(0.0, 0.04, size=(trials, candidates))
    row_idx = np.arange(trials)

    effect_x[row_idx, true_contact] += rng.uniform(0.75, 1.10, size=trials)
    passive_x[row_idx, true_contact] += rng.normal(0.0, 0.08, size=trials)

    passive_x[row_idx, distractor] += confound_strength * rng.uniform(0.75, 1.25, size=trials)
    effect_x[row_idx, distractor] += rng.uniform(-0.10, 0.08, size=trials)

    candidate_mask = np.ones((trials, candidates), dtype=bool)
    candidate_mask[row_idx, true_contact] = False
    candidate_mask[row_idx, distractor] = False
    nuisance_mask = (rng.random((trials, candidates)) < 0.20) & candidate_mask
    passive_x += nuisance_mask * confound_strength * rng.uniform(0.05, 0.35, size=(trials, candidates))
    effect_x += candidate_mask * rng.uniform(-0.15, 0.22, size=(trials, candidates))

    observed_x = passive_x + effect_x + rng.normal(0.0, 0.035, size=(trials, candidates))
    passive_estimate_x = (
        passive_scale * passive_x
        + passive_effect_leak * effect_x
        + rng.normal(0.0, passive_estimation_noise, size=(trials, candidates))
    )
    causal_x = observed_x - passive_estimate_x

    total_choice = np.argmax(observed_x, axis=1)
    causal_choice = np.argmax(causal_x, axis=1)
    oracle_choice = np.argmax(effect_x, axis=1)

    total_progress = effect_x[row_idx, total_choice]
    causal_progress = effect_x[row_idx, causal_choice]
    oracle_progress = effect_x[row_idx, oracle_choice]
    return {
        "total_success_rate": float(np.mean(total_progress > 0.50)),
        "causal_success_rate": float(np.mean(causal_progress > 0.50)),
        "oracle_success_rate": float(np.mean(oracle_progress > 0.50)),
        "total_mean_progress": float(np.mean(total_progress)),
        "causal_mean_progress": float(np.mean(causal_progress)),
        "oracle_mean_progress": float(np.mean(oracle_progress)),
        "total_distractor_rate": float(np.mean(total_choice == distractor)),
        "causal_distractor_rate": float(np.mean(causal_choice == distractor)),
    }


def run_grid() -> list[dict[str, float]]:
    rows = []
    confounds = [0.0, 0.25, 0.50, 0.75, 1.0, 1.5, 2.0, 3.0]
    noises = [0.0, 0.05, 0.10, 0.20, 0.35]
    trials = 2000
    row_id = 0
    for confound in confounds:
        for passive_noise in noises:
            metrics = run_trial_batch(14000 + row_id, trials, confound, passive_noise)
            rows.append(
                {
                    "confound_strength": confound,
                    "passive_estimation_noise": passive_noise,
                    "trials": trials,
                    **metrics,
                }
            )
            row_id += 1
    return rows


def run_misspecification_stress() -> list[dict[str, float | str]]:
    trials = 2000
    settings = [
        ("calibrated_noop", 1.0, 0.0),
        ("under_subtract_10pct", 0.90, 0.0),
        ("under_subtract_25pct", 0.75, 0.0),
        ("under_subtract_50pct", 0.50, 0.0),
        ("no_subtraction", 0.0, 0.0),
        ("over_subtract_25pct", 1.25, 0.0),
        ("effect_leak_25pct", 1.0, 0.25),
        ("effect_leak_50pct", 1.0, 0.50),
        ("effect_leak_75pct", 1.0, 0.75),
    ]
    rows: list[dict[str, float | str]] = []
    for row_id, (label, passive_scale, passive_effect_leak) in enumerate(settings):
        metrics = run_trial_batch(
            14200 + row_id,
            trials,
            confound_strength=2.0,
            passive_estimation_noise=0.10,
            passive_scale=passive_scale,
            passive_effect_leak=passive_effect_leak,
        )
        rows.append(
            {
                "scenario": label,
                "confound_strength": 2.0,
                "passive_estimation_noise": 0.10,
                "passive_scale": passive_scale,
                "passive_effect_leak": passive_effect_leak,
                "trials": trials,
                "total_success_rate": metrics["total_success_rate"],
                "residual_success_rate": metrics["causal_success_rate"],
                "oracle_success_rate": metrics["oracle_success_rate"],
                "residual_distractor_rate": metrics["causal_distractor_rate"],
                "residual_mean_progress": metrics["causal_mean_progress"],
            }
        )
    return rows


def write_results(rows: list[dict[str, float]]) -> dict[str, float]:
    DATA.mkdir(parents=True, exist_ok=True)
    FIGS.mkdir(parents=True, exist_ok=True)
    with RESULTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    hardest = [r for r in rows if math.isclose(r["passive_estimation_noise"], 0.10)]
    c2 = min(hardest, key=lambda r: abs(r["confound_strength"] - 2.0))
    c0 = min(hardest, key=lambda r: abs(r["confound_strength"] - 0.0))
    summary = {
        "rows": len(rows),
        "trials_per_row": int(rows[0]["trials"]),
        "total_trials": int(sum(r["trials"] for r in rows)),
        "at_confound_0_noise_0p10_total_success": c0["total_success_rate"],
        "at_confound_0_noise_0p10_causal_success": c0["causal_success_rate"],
        "at_confound_2_noise_0p10_total_success": c2["total_success_rate"],
        "at_confound_2_noise_0p10_causal_success": c2["causal_success_rate"],
        "at_confound_2_noise_0p10_total_distractor": c2["total_distractor_rate"],
        "at_confound_2_noise_0p10_causal_distractor": c2["causal_distractor_rate"],
        "causal_advantage_at_confound_2_noise_0p10": c2["causal_success_rate"] - c2["total_success_rate"],
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def latex_label(label: str) -> str:
    return label.replace("_", r"\_")


def write_misspecification_results(rows: list[dict[str, float | str]]) -> None:
    with MISSPEC.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    selected = [
        "calibrated_noop",
        "under_subtract_25pct",
        "under_subtract_50pct",
        "effect_leak_50pct",
        "effect_leak_75pct",
        "no_subtraction",
    ]
    row_by_name = {str(row["scenario"]): row for row in rows}
    lines = [
        r"\begin{tabular}{lccc}",
        r"\toprule",
        r"No-action estimate & Residual success & Residual distractor & Mean caused progress \\",
        r"\midrule",
    ]
    for name in selected:
        row = row_by_name[name]
        lines.append(
            f"{latex_label(name)} & "
            f"{float(row['residual_success_rate']):.3f} & "
            f"{float(row['residual_distractor_rate']):.3f} & "
            f"{float(row['residual_mean_progress']):.3f} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabular}", ""])
    MISSPEC_TEX.write_text("\n".join(lines), encoding="utf-8")


def try_plot(rows: list[dict[str, float]]) -> bool:
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        (FIGS / "plotting_unavailable.txt").write_text(str(exc), encoding="utf-8")
        return False

    noises = sorted({r["passive_estimation_noise"] for r in rows})
    confounds = sorted({r["confound_strength"] for r in rows})

    plt.figure(figsize=(6.5, 4.2))
    for noise in noises:
        subset = [r for r in rows if math.isclose(r["passive_estimation_noise"], noise)]
        subset.sort(key=lambda r: r["confound_strength"])
        if noise in {0.0, 0.10, 0.20, 0.35}:
            plt.plot(
                [r["confound_strength"] for r in subset],
                [r["causal_success_rate"] for r in subset],
                marker="o",
                label=f"causal, passive noise={noise:g}",
            )
    baseline = [r for r in rows if math.isclose(r["passive_estimation_noise"], 0.10)]
    baseline.sort(key=lambda r: r["confound_strength"])
    plt.plot(
        [r["confound_strength"] for r in baseline],
        [r["total_success_rate"] for r in baseline],
        color="black",
        marker="x",
        linestyle="--",
        label="total flow planner",
    )
    plt.xlabel("aligned passive-flow confound strength")
    plt.ylabel("successful contact selection rate")
    plt.ylim(0.0, 1.05)
    plt.grid(True, alpha=0.25)
    plt.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGS / "passive_confounding_success.pdf")
    plt.savefig(FIGS / "passive_confounding_success.png", dpi=180)
    plt.close()

    rng = random.Random(140)
    points_x = []
    points_y = []
    total_u = []
    total_v = []
    causal_u = []
    causal_v = []
    trial = None
    while trial is None:
        candidates = 28
        goal = (1.0, 0.0, 0.0)
        true_contact = rng.randrange(candidates)
        distractor = rng.randrange(candidates - 1)
        if distractor >= true_contact:
            distractor += 1
        passive = []
        effect = []
        observed_total = []
        passive_estimate = []
        for i in range(candidates):
            angle = 2.0 * math.pi * i / candidates
            radius = 1.0 + 0.15 * math.sin(3.0 * angle)
            points_x.append(radius * math.cos(angle))
            points_y.append(radius * math.sin(angle))
            base_passive = noise_vec(rng, 0.04)
            base_effect = noise_vec(rng, 0.04)
            if i == true_contact:
                base_effect = add(base_effect, (0.95, 0.04, 0.0))
            elif i == distractor:
                base_passive = add(base_passive, (2.0, -0.03, 0.0))
                base_effect = add(base_effect, (-0.06, 0.02, 0.0))
            passive.append(base_passive)
            effect.append(base_effect)
            observed_total.append(add(base_passive, base_effect))
            passive_estimate.append(passive[-1])
        causal_estimate = [sub(observed_total[i], passive_estimate[i]) for i in range(candidates)]
        total_choice = max(range(candidates), key=lambda i: dot(observed_total[i], goal))
        causal_choice = max(range(candidates), key=lambda i: dot(causal_estimate[i], goal))
        if total_choice == distractor and causal_choice == true_contact:
            trial = (true_contact, distractor, total_choice, causal_choice)
            total_u = [v[0] for v in observed_total]
            total_v = [v[1] for v in observed_total]
            causal_u = [v[0] for v in causal_estimate]
            causal_v = [v[1] for v in causal_estimate]

    colors = ["tab:gray"] * len(points_x)
    true_contact, distractor, _, _ = trial
    colors[true_contact] = "tab:green"
    colors[distractor] = "tab:red"
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.4), sharex=True, sharey=True)
    axes[0].quiver(points_x, points_y, total_u, total_v, color=colors, angles="xy", scale_units="xy", scale=3.0)
    axes[0].set_title("total scene flow")
    axes[1].quiver(points_x, points_y, causal_u, causal_v, color=colors, angles="xy", scale_units="xy", scale=3.0)
    axes[1].set_title("causal effect flow")
    for ax in axes:
        ax.set_aspect("equal")
        ax.set_xlim(-1.6, 1.6)
        ax.set_ylim(-1.45, 1.45)
        ax.grid(True, alpha=0.18)
    fig.tight_layout()
    fig.savefig(FIGS / "example_scene_flow_decomposition.pdf")
    fig.savefig(FIGS / "example_scene_flow_decomposition.png", dpi=180)
    plt.close(fig)
    return True


def write_evidence_md(summary: dict[str, float], misspec_rows: list[dict[str, float | str]], plotted: bool) -> None:
    misspec_by_name = {str(row["scenario"]): row for row in misspec_rows}
    calibrated = misspec_by_name["calibrated_noop"]
    under_50 = misspec_by_name["under_subtract_50pct"]
    leak_75 = misspec_by_name["effect_leak_75pct"]
    no_sub = misspec_by_name["no_subtraction"]
    EVIDENCE_MD.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE_MD.write_text(
        "\n".join(
            [
                "# Evidence Summary",
                "",
                "The experiment is a synthetic intervention test, not a real-robot claim. It isolates the exact failure mode targeted by the paper: passive motion aligned with the task goal can dominate total scene flow while being unaffected by the robot.",
                "",
                f"- Grid rows: {summary['rows']}",
                f"- Trials per row: {summary['trials_per_row']}",
                f"- Total trials: {summary['total_trials']}",
                f"- At passive-confound strength 0.0 and passive-estimation noise 0.10, total-flow success is {summary['at_confound_0_noise_0p10_total_success']:.3f}; causal-flow success is {summary['at_confound_0_noise_0p10_causal_success']:.3f}.",
                f"- At passive-confound strength 2.0 and passive-estimation noise 0.10, total-flow success is {summary['at_confound_2_noise_0p10_total_success']:.3f}; causal-flow success is {summary['at_confound_2_noise_0p10_causal_success']:.3f}.",
                f"- At that setting, the total-flow planner chooses the passive distractor {summary['at_confound_2_noise_0p10_total_distractor']:.3f} of trials; causal-flow chooses it {summary['at_confound_2_noise_0p10_causal_distractor']:.3f}.",
                f"- Causal advantage at confound 2.0/noise 0.10: {summary['causal_advantage_at_confound_2_noise_0p10']:.3f}.",
                f"- V2 misspecification stress at confound 2.0/noise 0.10: calibrated no-op residual success is {float(calibrated['residual_success_rate']):.3f}; under-subtracting passive flow by 50% lowers residual success to {float(under_50['residual_success_rate']):.3f}; leaking 75% of the robot effect into the no-op estimate lowers success to {float(leak_75['residual_success_rate']):.3f}; no subtraction has success {float(no_sub['residual_success_rate']):.3f}.",
                f"- Plots generated: {'yes' if plotted else 'no'}",
                "",
                "Interpretation: the evidence supports the mechanistic claim that planning on total flow is not invariant to passive exogenous motion, while planning on a do-difference field is robust when the passive estimate is accurate enough. It does not support claims about real-robot performance, learned perception accuracy, or benchmark superiority.",
                "The v2 stress makes the main boundary explicit: the no-action future must be calibrated and uncontaminated by the robot action, or the residual can collapse toward total-flow behavior or erase true action effects.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> int:
    print("running causal scene flow simulation", flush=True)
    rows = run_grid()
    summary = write_results(rows)
    misspec_rows = run_misspecification_stress()
    write_misspecification_results(misspec_rows)
    plotted = try_plot(rows)
    write_evidence_md(summary, misspec_rows, plotted)
    print(json.dumps(summary, indent=2), flush=True)
    print("wrote passive misspecification stress", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
