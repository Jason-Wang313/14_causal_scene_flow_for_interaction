# Plan

## Objective
Create a complete anonymous ICLR-style robotics paper for paper 14, starting from the seed "Causal Scene Flow for Interaction" but replacing it if the literature sweep reveals a stronger direction. The run must produce the required literature artifacts, runnable evidence, a compiled PDF at `C:/Users/wangz/Downloads/14.pdf`, a complete public GitHub repository named `14_causal_scene_flow_for_interaction`, and an honest final audit.

## Execution Stages
1. Initialize run bookkeeping.
   - Create/update `child_status.md` with current stage, commands, failures, and recovery steps.
   - Inspect existing artifacts from the retry and reuse any valid caches.

2. Environment and source acquisition.
   - Check availability of Python, Git, LaTeX tools, and GitHub CLI safely.
   - Locate or fetch the latest official ICLR LaTeX template available at runtime.
   - Create project directories: `docs`, `scripts`, `experiments`, `paper`, `figures`, `data`.

3. Literature landscape.
   - Build `docs/related_work_matrix.csv` with at least 1000 entries from robotics, 3D perception, scene flow, causal representation, manipulation, interaction dynamics, dynamics modeling, and robot planning literature.
   - Mark 300 serious-skim papers, 200-250 deep-read papers, and 100 hostile-prior papers.
   - Extract required dimensions for important prior work: claimed problem, mechanism, hidden assumptions, fixed variables, ignored failures, novelty pressure, and open gaps.

4. Novelty pressure test.
   - Write `docs/literature_map.md`.
   - Write `docs/hostile_prior_work.md`.
   - Identify at least 20 falseable hidden assumptions and paper directions that break them.
   - Write `docs/novelty_boundary_map.md`.
   - Choose the strongest thesis only after hostile comparison and write `docs/novelty_decision.md`.

5. Method and evidence.
   - Define the central mechanism without relying on forbidden weak moves.
   - Implement a small runnable synthetic/analytic evidence package showing why separating passive scene flow from robot-caused scene flow matters for manipulation planning.
   - Save scripts, configs, generated tables, and figures.

6. Claims and attacks.
   - Write `docs/claims.md` with support status for each claim.
   - Write `docs/reviewer_attacks.md` with adversarial critiques and responses.
   - Keep unsupported claims marked honestly.

7. Paper writing and build.
   - Draft a complete anonymous ICLR-style paper in `paper/main.tex`.
   - Sanitize BibTeX and LaTeX for pdfLaTeX.
   - Compile with direct `pdflatex`/`bibtex` passes using explicit generous timeouts.
   - Save final PDF only to `C:/Users/wangz/Downloads/14.pdf`.

8. Repository and final audit.
   - Ensure the repo is runnable and documented.
   - Create/push public GitHub repo `14_causal_scene_flow_for_interaction`, or document the exact blocker.
   - Write `docs/final_audit.md` answering all required audit questions, including PDF path, GitHub URL, and desktop-copy status.

## Safety Rules
- Avoid brittle inline PowerShell and Python.
- Use checked-in helper scripts for literature synthesis, experiments, plotting, and BibTeX generation.
- Use explicit timeouts for long commands.
- Treat optional lookup failures as recoverable and document them.
- Do not delete existing useful retry artifacts unless they are demonstrably invalid.
