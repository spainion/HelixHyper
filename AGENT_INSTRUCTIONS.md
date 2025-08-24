# Agent Operations & Debugging Instructions

Purpose
- Provide a safe, reproducible workflow for an AI agent with repo access to debug, test, edit, and track changes.
- Ensure all edits are tested, logged, and created on topic branches with PRs following the repository conventions.

Principles
1. Safety & Permission: Use a dedicated bot/service account (not a personal user token). Limit token scopes to repo:contents, pull_requests, workflow if writes/pushes are required.
2. Reproducibility: Every run must create a run-log artifact and a short summary entry in AGENT_RUNS.md.
3. Tests-first: Never open a PR with code that fails unit tests or static checks unless the PR purpose is to fix failing tests and includes a clear justification and failing logs.
4. Audit trail: All changes must be on a branch and accompanied by commits that pass pre-commit/CI checks.

Preflight (agent bootstrap)
1. Clone:
   git clone https://github.com/spainion/HelixHyper.git
   cd HelixHyper
2. Create a branch:
   BRANCH=agent/<agent-name>/YYYYMMDD-short-desc
   git checkout -b $BRANCH
3. Set env:
   - GITHUB_TOKEN: personal/CI token for push/PR (use secrets for automation)
   - PYPI/CLOUD creds only if needed by workflow
4. Install deps (prefer venv):
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

Debug & Verify Flow (script-driven)
- Use scripts/agent_debugger.py (recommended) which runs:
  - linters (ruff/flake8) if present
  - type checks (mypy) if present
  - security/static scans (bandit/safety) if present
  - tests (pytest)
  - coverage (optional)
  - docker build (optional)
- The script writes a structured JSON log (logs/agent_run_*.json) and can optionally append a human summary to AGENT_RUNS.md.

Edit & Commit Flow
1. Make small, focused changes. Follow conventional commit messages:
   feat: brief description
   fix: bug description
   chore: non-code changes
2. Run the full debug flow locally (scripts/agent_debugger.py).
3. Run pre-commit (if configured) and ensure it passes.
4. Commit:
   git add .
   git commit -m "fix: <short description>\n\nDetailed description..."
5. Push:
   git push origin $BRANCH
6. Open PR with:
   - Summary of change
   - Test results and logs attached (link logs/ file or attach artifacts)
   - Required reviewers & labels
7. Do not merge a PR until CI passes.

Rollback / Emergency Revert
- If a merged change causes regressions, open a revert PR:
  git revert <commit-sha> -m "revert: <reason>"
- Add a clear postmortem in PR.

Tracking & Log Format
- Each agent run should produce:
  - logs/agent_run_<timestamp>.json  (structured)
  - AGENT_RUNS.md append entry (human summary)
- Minimal AGENT_RUNS.md entry template:
  - timestamp (UTC)
  - agent id
  - branch
  - summary (what changed)
  - checks run (list + result)
  - artifacts path (logs/*)

Security considerations
- Never print secrets to logs.
- Mask secrets in CI logs and set environment secrets in repository settings.
- Limit token scope and rotate tokens periodically.

PR Checklist (agent must satisfy)
- [ ] Branch created with appropriate name
- [ ] All unit tests pass
- [ ] Linters & type checks pass
- [ ] Security scan completed (bandit/safety), or a reason why it was skipped
- [ ] Log artifact attached (logs/agent_run_*.json)
- [ ] Short description + detailed rationale

Minimal API health checks (if editing server code)
- After server changes, run a smoke curl:
  curl -sSf http://localhost:8000/health || (echo "SMOKE FAILED" && exit 1)

Contact & Escalation
- For anything that risks repository integrity, create a GitHub issue and request a human reviewer.

End of instructions.