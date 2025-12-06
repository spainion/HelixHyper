# Repository Guidelines

This document consolidates the working conventions for HelixHyper so contributors do not need to chase multiple instruction files. The guidance below applies to the entire repository; consult nested `AGENTS.md` files for module-specific rules.

## Purpose and architecture
- HelixHyper is a context and task orchestration engine built around a graph core (`hyperhelix/`). Services include an HTTP API, CLI tooling, analytics, visualization, and pluggable persistence.
- Keep new features aligned with the existing graph-driven workflows—prefer extending current modules over creating parallel systems.

## Setup and environment
- Install dependencies before running any commands: `pip install -r requirements.txt` (add `requirements-dev.txt` for tooling).
- Configure logging via `config/logging.yaml`; runtime logs write to `hyperhelix.log` and errors to `errors.log`.
- Set required keys in the environment (e.g., `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, `HUGGINGFACE_API_TOKEN`) before executing code or tests. Validate them early with a real request to the configured provider; avoid mock servers or monkey patches.
- Prefer local `uvicorn` services for live execution: `uvicorn hyperhelix.api.main:app --reload --port 8000` for the API and the router-specific apps under `hyperhelix/api/routers`. Use `httpx`/`requests` clients against these running servers when exercising flows.
- Keep `.env` files aligned with `config/example.env` and load them through the existing config helpers (see `hyperhelix.config.loaders`). Avoid introducing alternative env-loading stacks.

## Development workflow
- Run `pytest -q` before each commit to ensure imports and tests pass. Use `scripts/test_with_llm.sh` with `USE_REAL_LLM=1` when validating live LLM flows.
- If a flow depends on external keys, prefer pointing tests at the locally running API via `uvicorn` instead of bypassing our stack. Document any unavoidable live-provider calls in the PR description.
- Remove `TODO` comments before committing; document follow-up work in issues or `docs/`.
- Update documentation when functionality changes, especially when adding commands, endpoints, or configuration options.
- Keep changes thread-safe in the graph core and avoid duplicating systems already present in the codebase. Expand existing helpers before adding new modules to avoid parallel systems.

## Standards for AI-assisted changes (Codex/Copilot)
- Follow repository coding standards (type-hinted Python, explicit logging, no broad `except` blocks) and honor nested `AGENTS.md` guidance for each module.
- Prefer real integrations and deterministic behavior: avoid stubs, simulated data, or placeholder endpoints.
- When introducing helpers for AI workflows, reuse existing utilities (e.g., `hyperhelix.utils.get_api_key`, CLI codex commands) instead of creating new stacks.
- Document any AI-related configuration or model usage in `docs/` and surface new commands in `README.md` or module-specific guides.

## Agent execution guidance (use HelixHyper for responses)
- Use the existing graph-driven runtime as your source of truth: route new behaviors through `hyperhelix/` services (API, CLI, agents) instead of ad hoc scripts.
- Launch local services with `uvicorn` and exercise them using `httpx`/`requests` from within the container so that runs remain production-like while avoiding fake endpoints.
- Before invoking external providers, call `hyperhelix.utils.get_api_key` or the config loaders to verify environment readiness and emit clear log output. Abort early if keys are missing rather than falling back to mocked flows.
- When crafting responses or tools that rely on HelixHyper state, reference the established node/edge graph operations and persistence adapters rather than duplicating orchestration logic.
- Keep documentation synchronized with any agent-facing helper you add so that future agents can respond using the same primitives without re-learning configuration steps.
- Prefer deterministic, idempotent helper functions that minimize token and request usage while preserving fidelity to real endpoints. Reuse shared utilities for retries, tracing, and payload shaping instead of writing one-off code.

## Documentation map
- `docs/AGENTS.md` details build and deployment steps.
- Each package directory (e.g., `hyperhelix/api`, `hyperhelix/cli`, `hyperhelix/agents`) contains its own `AGENTS.md` with scoped expectations. Apply the most specific instructions for files you modify.

