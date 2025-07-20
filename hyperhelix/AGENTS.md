# HyperHelix Module Guidelines

This package hosts the core graph engine. When extending modules keep the following in mind:

- Maintain thread safety when modifying `HyperHelix` methods.
- The graph may be initialised with a persistence adapter; ensure integration
  code remains optional.
- Always log actions using the `hyperhelix` logger configured at package import.
- Avoid TODO comments in the code. Document future work in `docs/` or issues.
- New modules should include unit tests under `tests/`.
