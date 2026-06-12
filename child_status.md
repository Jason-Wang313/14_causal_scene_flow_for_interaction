# Child Status

- Paper: 14, `causal_scene_flow_for_interaction`
- Stage: parent recovery complete
- Current facts:
  - `plan.md` created with staged execution plan.
  - Workspace: `C:\Users\wangz\robotics_60_paper_batch\14_causal_scene_flow_for_interaction`
  - Required final PDF path: `C:/Users/wangz/Downloads/14.pdf`
  - Existing retry artifacts are minimal: `.gitignore`, `plan.md`, `child_status.md`, and `docs/`.
  - Tool availability: Python, Git, GitHub CLI, `pdflatex`, `bibtex`, and `curl` found.
  - Latest template lead found by web search: official ICLR 2026 formatting instructions point to `iclr2026_conference.sty`, `.bst`, and `.tex`.
  - Project directories and README created.
  - `docs/related_work_matrix.csv` generated with 1200 entries, 300 serious-skim labels, 225 deep-read labels, and 100 hostile-prior labels.
  - Initial sweep had off-topic high-citation rows; repaired by tightening domain filtering and adding targeted robotics/3D/manipulation queries.
  - Runnable evidence completed: 80,000 synthetic trials in `experiments/causal_scene_flow_sim.py`.
  - Research docs generated: literature map, hostile prior work, novelty boundary, novelty decision, claims, reviewer attacks, evidence summary.
  - Chosen thesis: plan with dense action/no-action causal effect flow, not total scene flow.
  - Official ICLR 2026 template files fetched from `https://github.com/ICLR/Master-Template/raw/master/iclr2026.zip`.
  - Paper source and bibliography generated in `paper/`.
  - PDF compiled successfully and copied to `C:/Users/wangz/Downloads/14.pdf`.
  - Build warnings remaining: one tiny overfull hbox and MiKTeX update reminder; no unresolved references/citations in final pass.
  - Parent recovery copied `14.pdf` to `C:/Users/wangz/OneDrive/Desktop/14.pdf`.
  - Parent recovery published the repository at `https://github.com/Jason-Wang313/14_causal_scene_flow_for_interaction`.
  - Parent recovery wrote `docs/build_status.md`, `docs/final_audit.md`, and `data/github_push_status.json`.
- Exact commands/actions so far:
  - `apply_patch` add `plan.md`
  - `apply_patch` add `child_status.md`
  - `Get-ChildItem -Force | Select-Object Name,Mode,Length,LastWriteTime | Format-Table -AutoSize; exit 0`
  - `git status --short; exit 0`
  - `if (Get-Command rg -ErrorAction SilentlyContinue) { rg --files | Select-Object -First 200 } else { Get-ChildItem -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 200 -ExpandProperty FullName }; exit 0`
  - `$tools = 'python','git','gh','pdflatex','bibtex','curl'; foreach ($t in $tools) { ... }; exit 0`
  - Web search for latest official ICLR LaTeX template.
  - `apply_patch` add `README.md`, directory `.gitkeep` files.
  - `apply_patch` add `scripts/literature_sweep.py`
  - `python scripts/literature_sweep.py; exit 0` (first filtered pass shortfall: 858 rows)
  - `apply_patch` update `scripts/literature_sweep.py` with 20 targeted queries
  - `python scripts/literature_sweep.py; exit 0` (final: 1200 rows)
  - `apply_patch` add `experiments/causal_scene_flow_sim.py`
  - `python experiments/causal_scene_flow_sim.py; exit 0`
  - `apply_patch` add `scripts/write_research_docs.py`
  - `python scripts/write_research_docs.py; exit 0`
  - `apply_patch` add `scripts/fetch_iclr_template.py`
  - `python scripts/fetch_iclr_template.py; exit 0`
  - `apply_patch` add `scripts/write_paper_assets.py`
  - `python scripts/write_paper_assets.py; exit 0`
  - `apply_patch` add `scripts/build_paper.py`
  - `python scripts/build_paper.py; exit 0`
- Failures:
  - First strict literature rerun produced only 858 relevant entries; recovered by adding targeted queries and rerunning to 1200 entries.
- Recovery steps:
  - Preserved strict domain filter and broadened with focused robotics/3D/manipulation searches instead of loosening relevance.
  - Parent monitor recovered the publish/final-audit step after child exit 999.
- Next:
  - Queue row must be marked `SUCCESS` by parent monitor.

Exit code: 999
End time: 2026-06-11 13:34:35 +01:00
PDF exists: True

## Submission-hardening v2 terminal status

Checked: 2026-06-12 23:49:37 +01:00

- Added passive-baseline misspecification stress tests for under-subtraction and action-effect leakage.
- Main counterexample retained: total-flow success 0.000 versus calibrated residual success 1.000 at confound 2.0/noise 0.10.
- 50% passive under-subtraction: residual success 0.387 and residual distractor selection 0.613.
- 75% action-effect leakage into the no-action estimate: residual success 0.505.
- Rebuilt the manuscript and copied the canonical v2 PDF to `C:/Users/wangz/Downloads/14.pdf` (210,277 bytes).
- Local `paper/main.pdf` was removed by the build helper; no new Desktop copy was created during v2 hardening.
- Terminal decision: workshop-only / revise before main-conference submission.
