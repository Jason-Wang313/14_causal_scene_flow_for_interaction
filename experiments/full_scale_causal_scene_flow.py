"""Full-scale causal-scene-flow hardening suite for Paper 14.

This remains a synthetic mechanism suite.  It expands the v2 counterexample into
multi-distractor, misspecification, overlap, ego-motion, learned-noop proxy,
metric-mismatch, and ablation families while storing only summary artifacts.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
DOCS = ROOT / "docs"
MASTER_SEED = 14014
METRICS = [
    "success_rate",
    "distractor_rate",
    "mean_progress",
    "regret",
    "ranking_margin",
    "endpoint_error",
]


def write_progress(stage: str, **extra: object) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "progress.json").write_text(json.dumps({"stage": stage, **extra}, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def tex_escape(value: object) -> str:
    return str(value).replace("\\", "\\textbackslash{}").replace("_", "\\_").replace("%", "\\%")


def mean(vals: Iterable[float]) -> float:
    vals = list(vals)
    return float(np.mean(vals)) if vals else 0.0


def stderr(vals: Iterable[float]) -> float:
    arr = np.array(list(vals), dtype=float)
    if len(arr) <= 1:
        return 0.0
    return float(arr.std(ddof=1) / math.sqrt(len(arr)))


def summarize(rows: list[dict[str, object]], keys: list[str]) -> list[dict[str, object]]:
    groups: dict[tuple[object, ...], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        groups[tuple(row[k] for k in keys)].append(row)
    out: list[dict[str, object]] = []
    for key, group in sorted(groups.items(), key=lambda item: tuple(str(x) for x in item[0])):
        summary = {k: v for k, v in zip(keys, key)}
        summary["n"] = len(group)
        for metric in METRICS:
            vals = [float(r[metric]) for r in group if metric in r]
            summary[f"{metric}_mean"] = mean(vals)
            summary[f"{metric}_se"] = stderr(vals)
        out.append(summary)
    return out


def save_table(path: Path, headers: list[str], rows: list[list[object]]) -> None:
    lines = ["\\begin{tabular}{" + "l" + "r" * (len(headers) - 1) + "}", "\\toprule"]
    lines.append(" & ".join(tex_escape(h) for h in headers) + "\\\\")
    lines.append("\\midrule")
    for row in rows:
        cells = []
        for cell in row:
            cells.append(f"{cell:.3f}" if isinstance(cell, float) else tex_escape(cell))
        lines.append(" & ".join(cells) + "\\\\")
    lines.extend(["\\bottomrule", "\\end{tabular}", ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def scene_batch(
    rng: np.random.Generator,
    *,
    trials: int,
    candidates: int,
    controllable_count: int,
    distractor_count: int,
    confound: float,
    passive_noise: float,
    passive_scale: float = 1.0,
    effect_leak: float = 0.0,
    passive_bias: float = 0.0,
    overlap: float = 0.0,
    occlusion: float = 0.0,
    global_field: float = 0.0,
    local_smooth: float = 0.0,
    estimator_extra_noise: float = 0.0,
) -> dict[str, np.ndarray]:
    row = np.arange(trials)
    effect = rng.normal(0.0, 0.04, size=(trials, candidates))
    passive = rng.normal(0.0, 0.04, size=(trials, candidates))

    order = np.argsort(rng.random((trials, candidates)), axis=1)
    controllable = order[:, :controllable_count]
    distractors = order[:, controllable_count : controllable_count + distractor_count]

    for j in range(controllable_count):
        idx = controllable[:, j]
        effect[row, idx] += rng.uniform(0.72, 1.10, size=trials) * (1.0 - 0.12 * j)
        passive[row, idx] += rng.normal(0.0, 0.06, size=trials)

    for j in range(distractor_count):
        idx = distractors[:, j]
        passive[row, idx] += confound * rng.uniform(0.70, 1.25, size=trials)
        effect[row, idx] += rng.uniform(-0.12, 0.12, size=trials)

    if overlap > 0.0:
        overlap_mask = rng.random((trials, distractor_count)) < overlap
        for j in range(distractor_count):
            target = controllable[:, j % controllable_count]
            source = distractors[:, j]
            mix = overlap_mask[:, j]
            passive[row[mix], target[mix]] += 0.55 * passive[row[mix], source[mix]]
            effect[row[mix], source[mix]] += 0.35 * effect[row[mix], target[mix]]

    if occlusion > 0.0:
        occluded = rng.random((trials, controllable_count)) < occlusion
        for j in range(controllable_count):
            idx = controllable[:, j]
            effect[row[occluded[:, j]], idx[occluded[:, j]]] *= rng.uniform(0.05, 0.35, size=int(occluded[:, j].sum()))

    if global_field:
        passive += global_field
    if local_smooth:
        passive += local_smooth * np.roll(passive, 1, axis=1)

    observed = passive + effect + rng.normal(0.0, 0.035, size=(trials, candidates))
    noop = (
        passive_scale * passive
        + effect_leak * effect
        + passive_bias
        + rng.normal(0.0, passive_noise + estimator_extra_noise, size=(trials, candidates))
    )
    residual = observed - noop
    return {
        "effect": effect,
        "passive": passive,
        "observed": observed,
        "noop": noop,
        "residual": residual,
        "controllable": controllable,
        "distractors": distractors,
    }


def score_methods(batch: dict[str, np.ndarray], rng: np.random.Generator) -> dict[str, np.ndarray]:
    observed = batch["observed"]
    residual = batch["residual"]
    passive = batch["passive"]
    effect = batch["effect"]
    contact_prior = np.zeros_like(effect)
    row = np.arange(effect.shape[0])
    for j in range(batch["controllable"].shape[1]):
        contact_prior[row, batch["controllable"][:, j]] += 0.35
    contact_prior += rng.normal(0.0, 0.08, size=effect.shape)
    global_removed = observed - observed.mean(axis=1, keepdims=True)
    action_conditioned = effect + 0.35 * passive + rng.normal(0.0, 0.07, size=effect.shape)
    random_noop = observed - rng.permutation(batch["noop"])
    return {
        "total_flow": observed,
        "causal_residual": residual,
        "attention_contact": observed + contact_prior,
        "action_conditioned_total": action_conditioned,
        "global_removed": global_removed,
        "passive_only": passive,
        "random_noop_residual": random_noop,
        "oracle_effect": effect,
    }


def metrics_for_scores(batch: dict[str, np.ndarray], scores: np.ndarray) -> dict[str, float]:
    effect = batch["effect"]
    row = np.arange(effect.shape[0])
    choice = np.argmax(scores, axis=1)
    oracle_choice = np.argmax(effect, axis=1)
    progress = effect[row, choice]
    oracle_progress = effect[row, oracle_choice]
    distractor_hit = np.zeros(effect.shape[0], dtype=bool)
    for j in range(batch["distractors"].shape[1]):
        distractor_hit |= choice == batch["distractors"][:, j]
    sorted_effect = np.sort(effect, axis=1)
    return {
        "success_rate": float(np.mean(progress > 0.50)),
        "distractor_rate": float(np.mean(distractor_hit)),
        "mean_progress": float(np.mean(progress)),
        "regret": float(np.mean(oracle_progress - progress)),
        "ranking_margin": float(np.mean(sorted_effect[:, -1] - sorted_effect[:, -2])),
    }


def endpoint_error(batch: dict[str, np.ndarray], estimate: np.ndarray) -> float:
    return float(np.mean(np.abs(estimate - (batch["passive"] + batch["effect"]))))


def run_setting(seed: int, *, trials: int = 1600, methods: list[str] | None = None, **kwargs: object) -> list[dict[str, object]]:
    rng = np.random.default_rng(MASTER_SEED + seed)
    batch = scene_batch(rng, trials=trials, **kwargs)
    scored = score_methods(batch, rng)
    methods = methods or list(scored.keys())
    rows = []
    for method in methods:
        row = {"seed": seed, "method": method}
        row.update(metrics_for_scores(batch, scored[method]))
        row["endpoint_error"] = endpoint_error(batch, scored[method])
        rows.append(row)
    return rows


def add_setting(rows: list[dict[str, object]], **setting: object) -> list[dict[str, object]]:
    out = []
    for row in rows:
        merged = dict(setting)
        merged.update(row)
        out.append(merged)
    return out


def run_family_a() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    settings = [
        ("main", 2, 8, 2.0, 0.10),
        ("one_distractor", 1, 1, 2.0, 0.10),
        ("many_distractors", 2, 16, 2.0, 0.10),
        ("low_confound", 2, 8, 0.5, 0.10),
        ("high_confound", 2, 8, 3.0, 0.10),
        ("high_noise", 2, 8, 2.0, 0.20),
    ]
    methods = ["total_flow", "causal_residual", "attention_contact", "action_conditioned_total", "oracle_effect"]
    rows: list[dict[str, object]] = []
    for seed in range(30):
        for setting, controllable, distractors, confound, noise in settings:
            if setting != "main" and seed >= 8:
                continue
            run_rows = run_setting(
                1000 + seed * 20 + len(rows) % 20,
                trials=1600,
                candidates=36,
                controllable_count=controllable,
                distractor_count=distractors,
                confound=confound,
                passive_noise=noise,
                methods=methods,
            )
            rows.extend(add_setting(run_rows, family="A", setting=setting, confound=confound, passive_noise=noise))
    summary = summarize(rows, ["family", "setting", "method"])
    write_csv(RESULTS / "family_a_multidistractor_seed.csv", rows)
    write_csv(RESULTS / "family_a_multidistractor_summary.csv", summary)
    return rows, summary


def run_family_b() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    methods = ["causal_residual", "total_flow", "oracle_effect"]
    rows: list[dict[str, object]] = []
    scale_errors = [0.25, 0.50, 0.75, 1.0, 1.25, 1.50]
    leaks = [0.0, 0.10, 0.25, 0.50, 0.75, 1.0]
    for seed in range(10):
        for scale in scale_errors:
            run_rows = run_setting(
                2000 + seed * 50 + int(scale * 10),
                trials=1400,
                candidates=32,
                controllable_count=2,
                distractor_count=8,
                confound=2.0,
                passive_noise=0.10,
                passive_scale=scale,
                methods=methods,
            )
            rows.extend(add_setting(run_rows, family="B", stress="scale", level=scale))
        for leak in leaks:
            run_rows = run_setting(
                2500 + seed * 50 + int(leak * 100),
                trials=1400,
                candidates=32,
                controllable_count=2,
                distractor_count=8,
                confound=2.0,
                passive_noise=0.10,
                effect_leak=leak,
                methods=methods,
            )
            rows.extend(add_setting(run_rows, family="B", stress="leak", level=leak))
    summary = summarize(rows, ["family", "stress", "level", "method"])
    write_csv(RESULTS / "family_b_misspecification_seed.csv", rows)
    write_csv(RESULTS / "family_b_misspecification_summary.csv", summary)
    return rows, summary


def run_family_c() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    methods = ["total_flow", "causal_residual", "attention_contact", "oracle_effect"]
    rows: list[dict[str, object]] = []
    for seed in range(10):
        for overlap in [0.0, 0.25, 0.50, 0.75, 1.0]:
            for occlusion in [0.0, 0.25, 0.50]:
                run_rows = run_setting(
                    3000 + seed * 100 + int(overlap * 10) + int(occlusion * 40),
                    trials=1200,
                    candidates=32,
                    controllable_count=2,
                    distractor_count=8,
                    confound=2.0,
                    passive_noise=0.10,
                    overlap=overlap,
                    occlusion=occlusion,
                    methods=methods,
                )
                rows.extend(add_setting(run_rows, family="C", overlap=overlap, occlusion=occlusion))
    summary = summarize(rows, ["family", "overlap", "occlusion", "method"])
    write_csv(RESULTS / "family_c_overlap_seed.csv", rows)
    write_csv(RESULTS / "family_c_overlap_summary.csv", summary)
    return rows, summary


def run_family_d() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    methods = ["total_flow", "global_removed", "causal_residual", "oracle_effect"]
    fields = [("none", 0.0, 0.0), ("conveyor", 0.8, 0.0), ("ego_motion", 1.2, 0.0), ("smooth_local", 0.8, 0.35)]
    rows: list[dict[str, object]] = []
    for seed in range(12):
        for label, global_field, smooth in fields:
            run_rows = run_setting(
                4000 + seed * 20 + fields.index((label, global_field, smooth)),
                trials=1400,
                candidates=34,
                controllable_count=2,
                distractor_count=8,
                confound=1.5,
                passive_noise=0.10,
                global_field=global_field,
                local_smooth=smooth,
                methods=methods,
            )
            rows.extend(add_setting(run_rows, family="D", field=label))
    summary = summarize(rows, ["family", "field", "method"])
    write_csv(RESULTS / "family_d_egomotion_seed.csv", rows)
    write_csv(RESULTS / "family_d_egomotion_summary.csv", summary)
    return rows, summary


def run_family_e() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    methods = ["causal_residual", "total_flow", "oracle_effect"]
    sample_sizes = [8, 16, 32, 64, 128, 256]
    for seed in range(12):
        for n in sample_sizes:
            extra_noise = 0.36 / math.sqrt(n)
            bias = 0.18 / math.sqrt(n)
            run_rows = run_setting(
                5000 + seed * 20 + n,
                trials=1400,
                candidates=32,
                controllable_count=2,
                distractor_count=8,
                confound=2.0,
                passive_noise=0.08,
                passive_bias=bias,
                estimator_extra_noise=extra_noise,
                methods=methods,
            )
            rows.extend(add_setting(run_rows, family="E", samples=n))
    summary = summarize(rows, ["family", "samples", "method"])
    write_csv(RESULTS / "family_e_learned_noop_seed.csv", rows)
    write_csv(RESULTS / "family_e_learned_noop_summary.csv", summary)
    return rows, summary


def run_family_f() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rows: list[dict[str, object]] = []
    variants = [
        ("low_epe_wrong_rank", "total_flow", 0.04, 2.0),
        ("higher_epe_correct_rank", "causal_residual", 0.14, 2.0),
        ("passive_noise_only", "total_flow", 0.02, 3.0),
        ("effect_noise_only", "causal_residual", 0.18, 1.0),
    ]
    for seed in range(12):
        for label, method, noise, confound in variants:
            run_rows = run_setting(
                6000 + seed * 20 + variants.index((label, method, noise, confound)),
                trials=1400,
                candidates=32,
                controllable_count=2,
                distractor_count=8,
                confound=confound,
                passive_noise=noise,
                methods=[method, "oracle_effect"],
            )
            rows.extend(add_setting(run_rows, family="F", estimator=label))
    summary = summarize(rows, ["family", "estimator", "method"])
    write_csv(RESULTS / "family_f_metric_mismatch_seed.csv", rows)
    write_csv(RESULTS / "family_f_metric_mismatch_summary.csv", summary)
    return rows, summary


def run_family_g() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    methods = ["total_flow", "passive_only", "causal_residual", "random_noop_residual", "attention_contact", "oracle_effect"]
    rows: list[dict[str, object]] = []
    for seed in range(16):
        run_rows = run_setting(
            7000 + seed,
            trials=1600,
            candidates=36,
            controllable_count=2,
            distractor_count=8,
            confound=2.0,
            passive_noise=0.10,
            methods=methods,
        )
        rows.extend(add_setting(run_rows, family="G", setting="main"))
    summary = summarize(rows, ["family", "setting", "method"])
    write_csv(RESULTS / "family_g_ablation_seed.csv", rows)
    write_csv(RESULTS / "family_g_ablation_summary.csv", summary)
    return rows, summary


def f(row: dict[str, object], key: str) -> float:
    return float(row[key])


def first(rows: list[dict[str, object]], **conditions: object) -> dict[str, object]:
    for row in rows:
        if all(str(row.get(k)) == str(v) for k, v in conditions.items()):
            return row
    raise KeyError(conditions)


def plot_bar(path_stem: str, labels: list[str], success: list[float], distractor: list[float], title: str) -> None:
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(max(7.0, len(labels) * 0.75), 3.7))
    ax.bar(x - 0.18, success, width=0.36, label="success", color="#2f6f8f")
    ax.bar(x + 0.18, distractor, width=0.36, label="distractor", color="#b65b42")
    ax.set_ylim(0, 1.0)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(RESULTS / f"{path_stem}.pdf")
    fig.savefig(RESULTS / f"{path_stem}.png", dpi=180)
    plt.close(fig)


def plot_line(path_stem: str, labels: list[str], success: list[float], distractor: list[float], title: str) -> None:
    x = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(8.0, 3.7))
    ax.plot(x, success, marker="o", label="success", color="#2f6f8f")
    ax.plot(x, distractor, marker="s", label="distractor", color="#b65b42")
    ax.set_ylim(0, 1.0)
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=25, ha="right")
    ax.grid(axis="y", alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(RESULTS / f"{path_stem}.pdf")
    fig.savefig(RESULTS / f"{path_stem}.png", dpi=180)
    plt.close(fig)


def make_artifacts(a: list[dict[str, object]], b: list[dict[str, object]], c: list[dict[str, object]], d: list[dict[str, object]], e: list[dict[str, object]], fsum: list[dict[str, object]], g: list[dict[str, object]]) -> dict[str, float]:
    main_methods = ["total_flow", "causal_residual", "attention_contact", "action_conditioned_total", "oracle_effect"]
    main = [first(a, setting="main", method=m) for m in main_methods]
    plot_bar(
        "figure_main_multidistractor",
        main_methods,
        [f(r, "success_rate_mean") for r in main],
        [f(r, "distractor_rate_mean") for r in main],
        "Multi-distractor passive confounds",
    )

    scale_rows = [r for r in b if str(r["stress"]) == "scale" and str(r["method"]) == "causal_residual"]
    plot_line(
        "figure_misspecification",
        [str(r["level"]) for r in scale_rows],
        [f(r, "success_rate_mean") for r in scale_rows],
        [f(r, "distractor_rate_mean") for r in scale_rows],
        "Passive scale misspecification",
    )

    overlap_rows = [r for r in c if str(r["method"]) == "causal_residual" and str(r["occlusion"]) == "0.0"]
    plot_line(
        "figure_overlap",
        [str(r["overlap"]) for r in overlap_rows],
        [f(r, "success_rate_mean") for r in overlap_rows],
        [f(r, "distractor_rate_mean") for r in overlap_rows],
        "Spatial overlap stress",
    )

    d_rows = [r for r in d if str(r["method"]) in {"total_flow", "global_removed", "causal_residual", "oracle_effect"} and str(r["field"]) == "ego_motion"]
    plot_bar(
        "figure_egomotion",
        [str(r["method"]) for r in d_rows],
        [f(r, "success_rate_mean") for r in d_rows],
        [f(r, "distractor_rate_mean") for r in d_rows],
        "Ego-motion/global passive field",
    )

    e_rows = [r for r in e if str(r["method"]) == "causal_residual"]
    plot_line(
        "figure_learned_noop",
        [str(r["samples"]) for r in e_rows],
        [f(r, "success_rate_mean") for r in e_rows],
        [f(r, "distractor_rate_mean") for r in e_rows],
        "Finite-sample no-op proxy",
    )

    metric_rows = [r for r in fsum if str(r["method"]) != "oracle_effect"]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    ax.scatter([f(r, "endpoint_error_mean") for r in metric_rows], [f(r, "success_rate_mean") for r in metric_rows], color="#2f6f8f")
    for r in metric_rows:
        ax.annotate(str(r["estimator"]), (f(r, "endpoint_error_mean"), f(r, "success_rate_mean")), fontsize=7)
    ax.set_xlabel("endpoint error proxy")
    ax.set_ylabel("planning success")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(RESULTS / "figure_metric_mismatch.pdf")
    fig.savefig(RESULTS / "figure_metric_mismatch.png", dpi=180)
    plt.close(fig)

    g_rows = [r for r in g if str(r["setting"]) == "main"]
    plot_bar(
        "figure_ablation",
        [str(r["method"]) for r in g_rows],
        [f(r, "success_rate_mean") for r in g_rows],
        [f(r, "distractor_rate_mean") for r in g_rows],
        "Causal-flow ablations",
    )

    save_table(
        RESULTS / "table_main_multidistractor.tex",
        ["Method", "Success", "Distractor", "Progress", "Regret"],
        [[r["method"], f(r, "success_rate_mean"), f(r, "distractor_rate_mean"), f(r, "mean_progress_mean"), f(r, "regret_mean")] for r in main],
    )
    save_table(
        RESULTS / "table_misspecification.tex",
        ["Stress", "Level", "Success", "Distractor"],
        [[r["stress"], r["level"], f(r, "success_rate_mean"), f(r, "distractor_rate_mean")] for r in b if str(r["method"]) == "causal_residual"],
    )
    save_table(
        RESULTS / "table_overlap.tex",
        ["Overlap", "Occlusion", "Success", "Distractor"],
        [[r["overlap"], r["occlusion"], f(r, "success_rate_mean"), f(r, "distractor_rate_mean")] for r in c if str(r["method"]) == "causal_residual" and str(r["occlusion"]) in {"0.0", "0.5"}],
    )
    save_table(
        RESULTS / "table_egomotion.tex",
        ["Field", "Method", "Success", "Distractor"],
        [[r["field"], r["method"], f(r, "success_rate_mean"), f(r, "distractor_rate_mean")] for r in d if str(r["method"]) in {"total_flow", "causal_residual", "global_removed"}],
    )
    save_table(
        RESULTS / "table_learned_noop.tex",
        ["Samples", "Success", "Distractor", "Regret"],
        [[r["samples"], f(r, "success_rate_mean"), f(r, "distractor_rate_mean"), f(r, "regret_mean")] for r in e_rows],
    )
    save_table(
        RESULTS / "table_metric_mismatch.tex",
        ["Estimator", "Method", "Endpoint err", "Success"],
        [[r["estimator"], r["method"], f(r, "endpoint_error_mean"), f(r, "success_rate_mean")] for r in metric_rows],
    )
    save_table(
        RESULTS / "table_ablation.tex",
        ["Method", "Success", "Distractor", "Regret"],
        [[r["method"], f(r, "success_rate_mean"), f(r, "distractor_rate_mean"), f(r, "regret_mean")] for r in g_rows],
    )
    save_table(
        RESULTS / "table_runtime_memory.tex",
        ["Family", "Seed rows", "Artifact", "Stress focus"],
        [
            ["A multidistractor", 350, "selector summaries", "passive distractors"],
            ["B misspecification", 360, "stress summaries", "scale and leakage"],
            ["C overlap", 600, "overlap summaries", "spatial overlap"],
            ["D ego-motion", 192, "field summaries", "global passive fields"],
            ["E learned no-op", 216, "sample summaries", "finite data"],
            ["F metric mismatch", 96, "estimator summaries", "EPE vs planning"],
            ["G ablation", 96, "method summaries", "negative controls"],
        ],
    )
    save_table(
        RESULTS / "table_claim_evidence.tex",
        ["Claim", "Evidence", "Boundary"],
        [
            ["Total flow can fail", "Family A", "synthetic passive distractors"],
            ["No-op calibration matters", "Family B", "analytic estimator errors"],
            ["Overlap is hard", "Family C", "point-score proxy"],
            ["Global passive fields matter", "Family D", "not real camera geometry"],
            ["Learned no-op needs data", "Family E", "linear proxy only"],
            ["EPE is not planning", "Family F", "proxy endpoint error"],
            ["Residual is the mechanism", "Family G", "finite candidates"],
        ],
    )
    headline = {
        "main_total_success": f(first(a, setting="main", method="total_flow"), "success_rate_mean"),
        "main_causal_success": f(first(a, setting="main", method="causal_residual"), "success_rate_mean"),
        "main_total_distractor": f(first(a, setting="main", method="total_flow"), "distractor_rate_mean"),
        "main_causal_distractor": f(first(a, setting="main", method="causal_residual"), "distractor_rate_mean"),
        "leak_075_success": f(first(b, stress="leak", level="0.75", method="causal_residual"), "success_rate_mean"),
        "scale_050_success": f(first(b, stress="scale", level="0.5", method="causal_residual"), "success_rate_mean"),
        "overlap_100_success": f(first(c, overlap="1.0", occlusion="0.0", method="causal_residual"), "success_rate_mean"),
    }
    report = f"""# Full-Scale Experiment Report

## Scope
- Seven experiment families: multi-distractor passive confounds, baseline misspecification, spatial overlap, ego/global passive fields, learned no-op proxy, endpoint-error mismatch, and ablations.
- Main headline setting uses 30 seeds; diagnostic grids use replicated summaries with vectorized trials.
- Outputs are under `results/full_scale/`.

## Key Findings
- Main setting: total-flow success {headline['main_total_success']:.3f}, causal-residual success {headline['main_causal_success']:.3f}.
- Main distractor rates: total-flow {headline['main_total_distractor']:.3f}, causal-residual {headline['main_causal_distractor']:.3f}.
- 50% passive under-subtraction: causal-residual success {headline['scale_050_success']:.3f}.
- 75% action-effect leakage: causal-residual success {headline['leak_075_success']:.3f}.
- Full spatial overlap with no occlusion: causal-residual success {headline['overlap_100_success']:.3f}.

## Plot Status
- All full-scale figures generated successfully.
"""
    (DOCS / "experiment_report.md").write_text(report, encoding="utf-8")
    return headline


def main() -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(exist_ok=True)
    write_progress("starting", master_seed=MASTER_SEED)
    a_seed, a_sum = run_family_a()
    write_progress("family_a_complete", family_a_rows=len(a_seed))
    b_seed, b_sum = run_family_b()
    write_progress("family_b_complete", family_b_rows=len(b_seed))
    c_seed, c_sum = run_family_c()
    write_progress("family_c_complete", family_c_rows=len(c_seed))
    d_seed, d_sum = run_family_d()
    write_progress("family_d_complete", family_d_rows=len(d_seed))
    e_seed, e_sum = run_family_e()
    write_progress("family_e_complete", family_e_rows=len(e_seed))
    f_seed, f_sum = run_family_f()
    write_progress("family_f_complete", family_f_rows=len(f_seed))
    g_seed, g_sum = run_family_g()
    write_progress("family_g_complete", family_g_rows=len(g_seed))
    headline = make_artifacts(a_sum, b_sum, c_sum, d_sum, e_sum, f_sum, g_sum)
    metadata = {
        "master_seed": MASTER_SEED,
        "families": [
            "multi_distractor",
            "misspecification",
            "spatial_overlap",
            "egomotion",
            "learned_noop_proxy",
            "metric_mismatch",
            "ablation",
        ],
        "headline": headline,
    }
    (RESULTS / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    write_progress(
        "complete",
        family_a_rows=len(a_seed),
        family_b_rows=len(b_seed),
        family_c_rows=len(c_seed),
        family_d_rows=len(d_seed),
        family_e_rows=len(e_seed),
        family_f_rows=len(f_seed),
        family_g_rows=len(g_seed),
        plot_failures=0,
    )
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
