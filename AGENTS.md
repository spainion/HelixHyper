# Repository Guidelines

- Keep the directory structure described in `README.md` when adding files.
- Configure logging using `config/logging.yaml`; logs should write to `hyperhelix.log` and errors to `errors.log`.
- Remove any `TODO` comments before committing; track outstanding work in issues or documentation.
- Run available tests with `pytest` before each commit. If no tests exist, ensure your changes at least import correctly.
- Update documentation whenever new functionality is introduced.
- Detailed build instructions live in `docs/AGENTS.md`.
