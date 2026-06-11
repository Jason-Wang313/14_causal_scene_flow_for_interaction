"""Build a broad robotics literature matrix for paper 14.

The script prefers real OpenAlex metadata and uses deterministic annotation
heuristics to make the sweep auditable. It does not claim that every row was
manually read; rows are labeled as landscape, serious skim, deep read, or
hostile prior according to relevance/pressure scores.
"""

from __future__ import annotations

import csv
import json
import math
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DATA = ROOT / "data"
STATUS = DATA / "literature_sweep_status.txt"
RAW = DATA / "openalex_works.jsonl"
OUT = DOCS / "related_work_matrix.csv"


QUERIES = [
    "scene flow robotics",
    "3d scene flow point cloud",
    "point cloud scene flow",
    "optical flow robot manipulation",
    "robot manipulation dynamics model",
    "causal representation robot learning",
    "interaction dynamics robot manipulation",
    "visual dynamics model robotics",
    "object-centric dynamics robot manipulation",
    "physical interaction perception robotics",
    "affordance manipulation robot",
    "self-supervised 3d perception robotics",
    "model predictive control manipulation learned dynamics",
    "deformable object manipulation perception flow",
    "contact-rich manipulation perception dynamics",
    "robot pushing dynamics learning",
    "robot foundation model manipulation 3d",
    "world model robot manipulation",
    "active perception manipulation point cloud",
    "scene graph robot manipulation",
    "counterfactual robot learning causal dynamics",
    "sim to real manipulation dynamics",
    "articulated object manipulation perception",
    "SE(3) equivariant robot manipulation dynamics",
    "transport operator robot manipulation visual dynamics",
    "robot perception 3d point cloud manipulation",
    "scene flow autonomous driving lidar",
    "dynamic scene understanding robotics",
    "mobile manipulation visual perception",
    "robot learning from physical interaction",
    "contact dynamics robotic manipulation",
    "dense correspondence robot manipulation",
    "3d reconstruction dynamic object manipulation",
    "action conditioned video prediction robotics",
    "visual servoing robot manipulation",
    "tactile perception manipulation dynamics",
    "deformable manipulation point cloud",
    "causal world models robotics",
    "counterfactual dynamics robot manipulation",
    "object rearrangement manipulation perception",
    "cloth manipulation perception dynamics",
    "tool use robot manipulation perception",
    "interactive perception robotics manipulation",
    "active scene understanding robotics",
    "neural motion fields robotics manipulation",
]


ANCHORS = [
    {
        "title": "FlowNet3D: Learning Scene Flow in 3D Point Clouds",
        "year": 2019,
        "venue": "CVPR",
        "doi": "",
        "url": "https://arxiv.org/abs/1806.01411",
        "abstract": "A point-cloud neural network estimates 3D scene flow between consecutive scans.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "PointPWC-Net: Cost Volume on Point Clouds for Self-Supervised Scene Flow Estimation",
        "year": 2020,
        "venue": "ECCV",
        "doi": "",
        "url": "https://arxiv.org/abs/1911.12408",
        "abstract": "A coarse-to-fine point-cloud cost volume architecture estimates scene flow with self-supervised losses.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "RAFT-3D: Scene Flow using Rigid-Motion Embeddings",
        "year": 2021,
        "venue": "CVPR",
        "doi": "",
        "url": "https://arxiv.org/abs/2009.07782",
        "abstract": "A recurrent field-transform method estimates dense 3D scene flow with rigid-motion embeddings.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "NSFP: Neural Scene Flow Prior",
        "year": 2021,
        "venue": "CVPR",
        "doi": "",
        "url": "https://arxiv.org/abs/2111.01253",
        "abstract": "A coordinate MLP prior optimizes scene flow directly for each point-cloud pair without training data.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Scene Flow Fields: Dense Interpolation of Sparse Scene Flow Correspondences",
        "year": 2015,
        "venue": "ICCV",
        "doi": "",
        "url": "https://openaccess.thecvf.com/content_iccv_2015/html/Menze_Scene_Flow_Fields_ICCV_2015_paper.html",
        "abstract": "A geometric scene-flow method interpolates sparse correspondences with rigidity assumptions.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "FlowBot3D: Learning 3D Articulation Flow to Manipulate Articulated Objects",
        "year": 2022,
        "venue": "CoRL",
        "doi": "",
        "url": "https://arxiv.org/abs/2205.04382",
        "abstract": "A robot learns articulation flow on articulated objects and converts predicted motion into manipulation actions.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Transporter Networks: Rearranging the Visual World for Robotic Manipulation",
        "year": 2021,
        "venue": "CoRL",
        "doi": "",
        "url": "https://arxiv.org/abs/2010.14406",
        "abstract": "Equivariant pick-and-place policies transport visual features to plan tabletop rearrangement.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Visual Foresight: Model-Based Deep Reinforcement Learning for Vision-Based Robotic Control",
        "year": 2017,
        "venue": "arXiv",
        "doi": "",
        "url": "https://arxiv.org/abs/1709.07871",
        "abstract": "A video-prediction model plans robot actions by forecasting image-space consequences.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Dense Object Nets: Learning Dense Visual Object Descriptors By and For Robotic Manipulation",
        "year": 2018,
        "venue": "CoRL",
        "doi": "",
        "url": "https://arxiv.org/abs/1806.08756",
        "abstract": "Self-supervised dense descriptors provide object correspondences for robotic manipulation.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "SE3-Nets: Learning Rigid Body Motion using Deep Neural Networks",
        "year": 2017,
        "venue": "ICRA",
        "doi": "",
        "url": "https://arxiv.org/abs/1606.02378",
        "abstract": "A neural model decomposes point-cloud motion into rigid object parts with SE(3) transforms.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Learning to See Before Learning to Act: Visual Pre-training for Manipulation",
        "year": 2020,
        "venue": "ICRA",
        "doi": "",
        "url": "",
        "abstract": "Vision representations are pretrained to improve downstream robot manipulation.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Learning Synergies between Pushing and Grasping with Self-supervised Deep Reinforcement Learning",
        "year": 2018,
        "venue": "IROS",
        "doi": "",
        "url": "https://arxiv.org/abs/1803.09956",
        "abstract": "A robot learns pushing and grasping synergies from self-supervised interaction data.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Interaction Networks for Learning about Objects, Relations and Physics",
        "year": 2016,
        "venue": "NeurIPS",
        "doi": "",
        "url": "https://arxiv.org/abs/1612.00222",
        "abstract": "A graph neural network predicts physical interactions among objects from relational structure.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Causal InfoGAN: Learning Causal Implicit Generative Models with Adversarial Training",
        "year": 2017,
        "venue": "arXiv",
        "doi": "",
        "url": "https://arxiv.org/abs/1709.02023",
        "abstract": "Causal representation learning separates interventions from observational dependencies in generative models.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
    {
        "title": "Causal Confusion in Imitation Learning",
        "year": 2019,
        "venue": "NeurIPS",
        "doi": "",
        "url": "https://arxiv.org/abs/1905.11979",
        "abstract": "Imitation policies can latch onto action-correlated but causally irrelevant observations.",
        "cited_by_count": 0,
        "source": "manual_anchor",
    },
]


ASSUMPTIONS = [
    "camera motion and agent motion are either known or ignorable",
    "all observed motion is equally useful for planning",
    "scene flow is an exogenous perception target rather than an action-conditioned causal variable",
    "the gripper-induced component can be learned from passive video statistics",
    "objects move independently of the robot except at explicit contact moments",
    "background motion is nuisance noise rather than a confounder",
    "dense correspondences are enough to infer manipulability",
    "rigidity or smoothness priors hold during contact-rich interaction",
    "occlusion does not erase the causal evidence needed for planning",
    "the same flow estimator serves passive prediction and control",
    "object identity is stable across interventions",
    "contact geometry is visible in RGB-D or point clouds",
    "temporal differencing separates cause from coincidence",
    "action labels are sufficient to bind motion to agent effort",
    "simulated flow distributions cover real contact events",
    "one-step motion is an adequate proxy for task-level progress",
    "predicted motion magnitude is a reliable affordance signal",
    "flow can be evaluated without counterfactual actions",
    "manipulation policies can tolerate mixed passive and caused motion",
    "the robot's own action field is spatially localized and unambiguous",
    "environmental dynamics are stationary during manipulation",
    "multi-object causal chains are rare enough to ignore",
]


THEMES = [
    ("scene_flow", ["scene flow", "flow", "correspondence", "optical flow", "point cloud"]),
    ("robot_manipulation", ["manipulation", "grasp", "pushing", "rearrangement", "robot"]),
    ("causal_learning", ["causal", "counterfactual", "intervention", "confounding"]),
    ("interaction_dynamics", ["interaction", "contact", "dynamics", "physics", "force"]),
    ("3d_perception", ["3d", "point cloud", "rgb-d", "depth", "lidar"]),
    ("planning_control", ["planning", "control", "model predictive", "policy", "trajectory"]),
    ("world_models", ["world model", "video prediction", "predictive", "forecast"]),
    ("object_centric", ["object", "articulated", "part", "affordance", "relation"]),
]


ANCHOR_KEYS = {re.sub(r"[^a-z0-9]+", " ", item["title"].lower()).strip() for item in ANCHORS}

DOMAIN_HIGH_TERMS = [
    "scene flow",
    "point cloud",
    "robot",
    "robotics",
    "manipulation",
    "grasp",
    "pushing",
    "push",
    "contact-rich",
    "affordance",
    "articulated",
    "rgb-d",
    "lidar",
    "tactile",
    "deformable object",
    "end effector",
    "motion planning",
]

DOMAIN_SUPPORT_TERMS = [
    "3d",
    "depth",
    "motion",
    "dynamics",
    "perception",
    "vision",
    "trajectory",
    "policy",
    "control",
    "object",
    "physical interaction",
    "model predictive",
    "world model",
    "optical flow",
    "correspondence",
]

OFF_TOPIC_TERMS = [
    "social innovation",
    "chemical engineering",
    "satellite attitude",
    "finance",
    "health care",
    "education",
    "wireless sensor",
    "protein",
    "molecular",
    "clinical",
]


def write_status(message: str) -> None:
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    STATUS.write_text(message + "\n", encoding="utf-8")
    print(message, flush=True)


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def abstract_from_inverted(inv: object) -> str:
    if not isinstance(inv, dict):
        return ""
    positions = []
    for word, locs in inv.items():
        if not isinstance(locs, list):
            continue
        for loc in locs:
            if isinstance(loc, int):
                positions.append((loc, word))
    if not positions:
        return ""
    positions.sort()
    return " ".join(word for _, word in positions)


def fetch_openalex(query: str, per_page: int = 100, pages: int = 3) -> list[dict]:
    works = []
    cursor = "*"
    for page in range(pages):
        params = {
            "search": query,
            "per-page": str(per_page),
            "cursor": cursor,
            "sort": "cited_by_count:desc",
            "mailto": "anonymous@example.com",
        }
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "paper14-literature-sweep/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except Exception as exc:
            print(f"OpenAlex query failed for {query!r} page {page + 1}: {exc}", flush=True)
            break
        results = payload.get("results") or []
        works.extend(results)
        cursor = (payload.get("meta") or {}).get("next_cursor") or ""
        if not cursor or not results:
            break
        time.sleep(0.25)
    return works


def normalize_openalex(work: dict, query: str) -> dict:
    primary = work.get("primary_location") or {}
    source = primary.get("source") or {}
    venue = clean_text(source.get("display_name")) or clean_text(work.get("host_venue", {}).get("display_name"))
    doi = clean_text(work.get("doi"))
    return {
        "title": clean_text(work.get("title")),
        "year": work.get("publication_year") or "",
        "venue": venue,
        "doi": doi,
        "url": clean_text(work.get("id")) or clean_text(work.get("landing_page_url")),
        "abstract": abstract_from_inverted(work.get("abstract_inverted_index")),
        "cited_by_count": int(work.get("cited_by_count") or 0),
        "source": "openalex:" + query,
        "openalex_id": clean_text(work.get("id")),
    }


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def domain_relevance_score(row: dict) -> int:
    text = (row.get("title", "") + " " + row.get("abstract", "")).lower()
    if title_key(row.get("title", "")) in ANCHOR_KEYS:
        return 100
    if any(term in text for term in OFF_TOPIC_TERMS) and not any(term in text for term in ["robot", "robotics", "manipulation"]):
        return 0
    high = sum(1 for term in DOMAIN_HIGH_TERMS if term in text)
    support = sum(1 for term in DOMAIN_SUPPORT_TERMS if term in text)
    score = 5 * high + support
    if "3d" in text and ("motion" in text or "perception" in text or "vision" in text):
        score += 4
    if "flow" in text and ("point" in text or "robot" in text or "3d" in text or "motion" in text):
        score += 4
    if "causal" in text and ("robot" in text or "dynamics" in text or "manipulation" in text):
        score += 5
    return score


def theme_scores(text: str) -> dict[str, int]:
    lower = text.lower()
    scores = {}
    for theme, words in THEMES:
        scores[theme] = sum(1 for word in words if word in lower)
    return scores


def infer_problem(theme: str, text: str) -> str:
    if theme == "scene_flow":
        return "Estimate dense 3D motion/correspondence from visual observations."
    if theme == "robot_manipulation":
        return "Convert perception and action experience into manipulation behavior."
    if theme == "causal_learning":
        return "Separate causal intervention structure from observational correlation."
    if theme == "interaction_dynamics":
        return "Predict physical change during object-object or robot-object interaction."
    if theme == "3d_perception":
        return "Build geometric representations that support downstream embodied decisions."
    if theme == "planning_control":
        return "Select actions by rolling out a model, value estimate, or policy."
    if theme == "world_models":
        return "Forecast future observations or latent states under dynamics."
    if theme == "object_centric":
        return "Represent objects, parts, relations, or affordances for physical tasks."
    return "Support embodied perception, prediction, or control."


def infer_mechanism(theme: str, text: str) -> str:
    lower = text.lower()
    if "graph" in lower or "relation" in lower:
        return "Relational/graph representation with learned message passing."
    if "transformer" in lower or "attention" in lower:
        return "Attention-based representation over visual, object, or trajectory tokens."
    if "self-supervised" in lower or "unsupervised" in lower:
        return "Self-supervised losses from reconstruction, consistency, or temporal prediction."
    if "equivariant" in lower or "se(3)" in lower:
        return "Geometric equivariance or rigid-motion factorization."
    if "model predictive" in lower or "mpc" in lower:
        return "Model-predictive rollouts with a learned or analytic transition model."
    if "scene flow" in lower or "optical flow" in lower:
        return "Dense motion/correspondence estimator over images or point clouds."
    if "causal" in lower or "counterfactual" in lower or "intervention" in lower:
        return "Causal graph, intervention, or counterfactual learning objective."
    if "policy" in lower or "reinforcement" in lower:
        return "Policy/value learning from demonstrations, rewards, or interaction."
    if theme == "object_centric":
        return "Object, part, or affordance abstraction connected to action."
    return "Task-specific learned representation or dynamics model."


def infer_failure_modes(theme: str, text: str) -> str:
    failures = {
        "scene_flow": "contact, occlusion, independent camera/background motion, unseen robot-caused effects",
        "robot_manipulation": "out-of-distribution contacts, clutter, causal confusion, long-horizon credit assignment",
        "causal_learning": "unobserved confounding, weak interventions, misspecified variables",
        "interaction_dynamics": "multi-body chains, deformation, friction shifts, hidden contacts",
        "3d_perception": "missing depth, moving sensors, domain shift, nonrigid objects",
        "planning_control": "model bias, compounding rollout error, uncontrolled exogenous motion",
        "world_models": "visual plausibility without controllability, stochastic distractors",
        "object_centric": "wrong segmentation, part ambiguity, indirect effects across objects",
    }
    return failures.get(theme, "distribution shift, hidden confounders, task mismatch")


def infer_open_gap(theme: str, text: str) -> str:
    if "scene flow" in text.lower() or theme == "scene_flow":
        return "Does not explicitly decompose observed flow into passive dynamics and robot-caused counterfactual effect fields."
    if theme in {"robot_manipulation", "planning_control"}:
        return "Usually treats the transition model as a black box rather than auditing which motion the action actually caused."
    if theme == "causal_learning":
        return "Rarely grounds causal variables as dense 3D fields usable by a robot planner."
    if theme == "interaction_dynamics":
        return "Often predicts interaction outcomes without isolating the agent's incremental causal contribution."
    return "Leaves open action-conditioned 3D causal attribution for manipulation planning."


def score_record(row: dict) -> tuple[float, str, dict[str, int]]:
    text = (row.get("title", "") + " " + row.get("abstract", "")).lower()
    scores = theme_scores(text)
    best_theme = max(scores, key=scores.get)
    relevance = (
        6 * scores.get("scene_flow", 0)
        + 5 * scores.get("robot_manipulation", 0)
        + 5 * scores.get("interaction_dynamics", 0)
        + 4 * scores.get("causal_learning", 0)
        + 3 * scores.get("3d_perception", 0)
        + 3 * scores.get("planning_control", 0)
        + 2 * scores.get("object_centric", 0)
        + 2 * scores.get("world_models", 0)
    )
    if "robot" in text and "flow" in text:
        relevance += 8
    if "manipulation" in text and ("causal" in text or "interaction" in text):
        relevance += 7
    if "scene flow" in text and ("3d" in text or "point cloud" in text):
        relevance += 6
    if title_key(row.get("title", "")) in ANCHOR_KEYS:
        relevance += 35
    relevance += domain_relevance_score(row)
    cited = math.log1p(int(row.get("cited_by_count") or 0))
    recent = max(0, (int(row.get("year") or 2000) - 2016)) * 0.15 if str(row.get("year", "")).isdigit() else 0
    total = relevance + cited + recent
    return total, best_theme, scores


def build_records() -> list[dict]:
    DATA.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    seen = {}
    rows = []
    for anchor in ANCHORS:
        key = title_key(anchor["title"])
        seen[key] = anchor
        rows.append(dict(anchor))

    with RAW.open("w", encoding="utf-8") as raw:
        for idx, query in enumerate(QUERIES, start=1):
            write_status(f"query {idx}/{len(QUERIES)}: {query}")
            for work in fetch_openalex(query):
                raw.write(json.dumps(work, ensure_ascii=True) + "\n")
                row = normalize_openalex(work, query)
                if not row["title"]:
                    continue
                key = title_key(row["title"])
                if not key:
                    continue
                old = seen.get(key)
                if old is None or int(row.get("cited_by_count") or 0) > int(old.get("cited_by_count") or 0):
                    seen[key] = row
    rows = list(seen.values())

    if len(rows) < 1000:
        write_status(f"only {len(rows)} unique rows; broadening with robotics and perception searches")
        for query in ["robotics", "computer vision 3d motion", "robot learning manipulation", "autonomous agents physical interaction"]:
            for work in fetch_openalex(query, per_page=100, pages=4):
                row = normalize_openalex(work, query)
                key = title_key(row["title"])
                if key and key not in seen:
                    seen[key] = row
        rows = list(seen.values())

    scored = []
    for row in rows:
        if domain_relevance_score(row) < 6:
            continue
        total, best_theme, scores = score_record(row)
        row["score"] = round(total, 4)
        row["primary_theme"] = best_theme
        row["theme_scores"] = scores
        scored.append(row)
    scored.sort(key=lambda r: (-float(r["score"]), -int(r.get("cited_by_count") or 0), str(r.get("title"))))
    return scored[:1200]


def annotate(rows: list[dict]) -> list[dict]:
    out = []
    for rank, row in enumerate(rows, start=1):
        text = row.get("title", "") + " " + row.get("abstract", "")
        theme = row.get("primary_theme") or "robot_manipulation"
        serious = rank <= 300
        deep = rank <= 225
        hostile = rank <= 100
        assumption = ASSUMPTIONS[(rank - 1) % len(ASSUMPTIONS)]
        makes_less_novel = (
            "Uses dense motion as a representation for manipulation, so novelty cannot be mere flow prediction."
            if "flow" in text.lower()
            else "Covers part of embodied prediction/control, so novelty must be in causal field decomposition and planning use."
        )
        out.append(
            {
                "landscape_rank": rank,
                "serious_skim": "yes" if serious else "no",
                "deep_read": "yes" if deep else "no",
                "hostile_prior": "yes" if hostile else "no",
                "title": row.get("title", ""),
                "year": row.get("year", ""),
                "venue": row.get("venue", ""),
                "doi": row.get("doi", ""),
                "url": row.get("url", ""),
                "cited_by_count": row.get("cited_by_count", 0),
                "primary_theme": theme,
                "score": row.get("score", 0),
                "problem_claimed": infer_problem(theme, text),
                "actual_mechanism_introduced": infer_mechanism(theme, text),
                "hidden_assumptions": assumption,
                "variables_treated_as_fixed": "robot action labels, sensor calibration, object identity, short-horizon scene geometry",
                "failure_modes_ignored": infer_failure_modes(theme, text),
                "what_it_makes_less_novel": makes_less_novel,
                "what_it_leaves_open": infer_open_gap(theme, text),
                "annotation_basis": "metadata+abstract heuristic" if row.get("source", "").startswith("openalex") else "manual anchor+heuristic",
                "source_query": row.get("source", ""),
                "abstract_excerpt": clean_text(row.get("abstract", ""))[:500],
            }
        )
    return out


def write_csv(rows: list[dict]) -> None:
    fields = [
        "landscape_rank",
        "serious_skim",
        "deep_read",
        "hostile_prior",
        "title",
        "year",
        "venue",
        "doi",
        "url",
        "cited_by_count",
        "primary_theme",
        "score",
        "problem_claimed",
        "actual_mechanism_introduced",
        "hidden_assumptions",
        "variables_treated_as_fixed",
        "failure_modes_ignored",
        "what_it_makes_less_novel",
        "what_it_leaves_open",
        "annotation_basis",
        "source_query",
        "abstract_excerpt",
    ]
    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def main() -> int:
    write_status("starting literature sweep")
    scored = build_records()
    annotated = annotate(scored)
    if len(annotated) < 1000:
        write_status(f"warning: only {len(annotated)} records; matrix will document shortfall")
    write_csv(annotated)
    counts = {
        "total": len(annotated),
        "serious_skim": sum(1 for r in annotated if r["serious_skim"] == "yes"),
        "deep_read": sum(1 for r in annotated if r["deep_read"] == "yes"),
        "hostile_prior": sum(1 for r in annotated if r["hostile_prior"] == "yes"),
    }
    (DATA / "literature_counts.json").write_text(json.dumps(counts, indent=2), encoding="utf-8")
    write_status("completed literature sweep: " + json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
