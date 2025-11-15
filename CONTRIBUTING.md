# Contributing to HelixHyper

Thank you for your interest in contributing to HyperHelix! This guide will help you get started.

## Quick Start

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/HelixHyper.git
   cd HelixHyper
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

3. **Run Tests**
   ```bash
   pytest -q
   ```

4. **Create Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

- **Python 3.12+** with full type hints
- Use `from __future__ import annotations` for forward references
- Follow dataclass patterns for data structures
- Module-level loggers: `logger = logging.getLogger(__name__)`
- Never use bare `except` clauses
- No TODO comments in committed code (use issues instead)

### Testing

- Write tests for all new features
- Maintain or improve code coverage
- Use pytest fixtures from `tests/conftest.py`
- Mock external services (OpenAI, OpenRouter, HuggingFace)
- Run `pytest -q` before committing

Example test:
```python
def test_add_node(graph):
    node = Node(id="test", payload={"data": "value"})
    graph.add_node(node)
    assert "test" in graph.nodes
    assert graph.nodes["test"].payload == {"data": "value"}
```

### Logging

- Configure via `config/logging.yaml`
- Logs go to `hyperhelix.log`, errors to `errors.log`
- Use appropriate log levels:
  - DEBUG: Detailed information for debugging
  - INFO: General operational information
  - WARNING: Warning messages for potentially problematic situations
  - ERROR: Error messages for failures

Example:
```python
import logging

logger = logging.getLogger(__name__)

def my_function():
    logger.debug("Starting function")
    try:
        # code
        logger.info("Operation successful")
    except Exception as e:
        logger.error("Operation failed: %s", e)
        raise
```

### Documentation

- Update relevant `AGENTS.md` files when changing modules
- Add docstrings to all public functions and classes
- Include usage examples in docstrings
- Update `README.md` for user-facing changes
- Update `docs/` for architectural changes

Example docstring:
```python
def add_edge(self, a: str, b: str, weight: float = 1.0) -> None:
    """Create a bidirectional edge between two nodes.
    
    Args:
        a: ID of first node
        b: ID of second node
        weight: Edge weight (default: 1.0)
        
    Raises:
        KeyError: If either node doesn't exist
        
    Example:
        >>> graph.add_edge("node1", "node2", weight=0.5)
    """
```

## Module-Specific Guidelines

Each module has specific guidelines in its `AGENTS.md` file:

- `/hyperhelix/AGENTS.md` - Core module
- `/hyperhelix/api/AGENTS.md` - API development
- `/hyperhelix/cli/AGENTS.md` - CLI commands
- `/hyperhelix/agents/AGENTS.md` - LLM integration
- `/hyperhelix/tasks/AGENTS.md` - Task management
- `/hyperhelix/persistence/AGENTS.md` - Database adapters
- And more...

## Common Contribution Types

### Adding a New LLM Provider

1. Create model class in `hyperhelix/agents/llm.py`:
   ```python
   class MyLLMChatModel(BaseChatModel):
       def generate_response(self, messages: list) -> str:
           # Implementation
   ```

2. Add tests in `tests/test_llm.py`
3. Update `hyperhelix/cli/commands.py` to support new provider
4. Update `hyperhelix/api/routers/suggest.py` and `chat.py`
5. Document in `hyperhelix/agents/AGENTS.md`
6. Add example to `README.md`

### Adding a New Persistence Adapter

1. Implement `BaseAdapter` in `hyperhelix/persistence/`:
   ```python
   class MyAdapter(BaseAdapter):
       def save_node(self, node_id: str, payload: Any) -> None:
           pass
       # Implement other methods
   ```

2. Add configuration to `config/persistence.yaml`
3. Add tests in `tests/test_persistence.py`
4. Document in `hyperhelix/persistence/AGENTS.md`
5. Add usage example to `README.md`

### Adding an API Endpoint

1. Create router in `hyperhelix/api/routers/`:
   ```python
   from fastapi import APIRouter, Request
   
   router = APIRouter()
   
   @router.get("/my-endpoint")
   def my_endpoint(request: Request):
       graph = request.app.state.graph
       # Implementation
   ```

2. Register router in `hyperhelix/api/main.py`
3. Add Pydantic schemas to `hyperhelix/api/schemas.py` if needed
4. Add tests in `tests/test_api.py`
5. Document in `hyperhelix/api/AGENTS.md` and `README.md`

### Adding a CLI Command

1. Add command to `hyperhelix/cli/commands.py`:
   ```python
   @cli.command()
   @click.argument("arg")
   def mycommand(arg: str) -> None:
       """Description of command."""
       # Implementation
   ```

2. Add tests in `tests/test_cli_commands.py`
3. Document in `hyperhelix/cli/AGENTS.md` and `README.md`

## Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/description
   ```

2. **Make Changes**
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation

3. **Test Locally**
   ```bash
   pytest -q
   python -c "import hyperhelix; print('✓')"
   ```

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "feat: description of changes"
   ```
   
   Commit message format:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Test changes
   - `refactor:` Code refactoring
   - `chore:` Maintenance tasks

5. **Push and Create PR**
   ```bash
   git push origin feature/description
   ```
   
   Then create pull request on GitHub

6. **PR Review**
   - CI tests will run automatically
   - Address review feedback
   - Keep commits focused and clean

## Environment Setup for Development

### Required Environment Variables

For LLM features (optional):
```bash
export OPENAI_API_KEY="your-key"
export OPENROUTER_API_KEY="your-key"
export HUGGINGFACE_API_TOKEN="your-key"
export GITHUB_TOKEN="your-token"  # For CLI issues command
```

### Development with Docker

```bash
# Build development container
docker build -f Dockerfile.dev -t helixhyper-dev .

# Run with volume mount for live reloading
docker run -it -p 8000:8000 -v $(pwd):/app helixhyper-dev

# Or use Docker Compose
docker-compose up dev
```

## Testing Strategy

### Unit Tests
Test individual components in isolation:
```bash
pytest tests/test_core.py -v
```

### Integration Tests
Test with real services (requires API keys):
```bash
USE_REAL_LLM=1 pytest tests/test_llm.py -v
# or
scripts/test_with_llm.sh
```

### Coverage Report
```bash
pytest --cov=hyperhelix --cov-report=html
# Open htmlcov/index.html in browser
```

## Debugging Tips

1. **Check Logs**
   ```bash
   tail -f hyperhelix.log
   tail -f errors.log
   ```

2. **Run with Debug Logging**
   Edit `config/logging.yaml` to set level to DEBUG

3. **Use Python Debugger**
   ```python
   import pdb; pdb.set_trace()
   ```

4. **Test Single Function**
   ```bash
   pytest tests/test_core.py::test_add_node -v
   ```

## Working with AI Tools

### GitHub Copilot
- Read `.github/copilot-instructions.md` for context
- Keep relevant files open for better suggestions
- Write clear comments describing intent

### Cursor / Other AI IDEs
- Use `.cursorrules` for project-specific guidance
- Reference module `AGENTS.md` files
- See `.github/AGENT_INSTRUCTIONS.md` for comprehensive guide

### ChatGPT / Codex
- Provide `.github/AGENT_INSTRUCTIONS.md` as context
- Reference specific `AGENTS.md` files for detailed guidance
- Look at test files for usage examples

## Code Review Checklist

Before submitting PR, ensure:

- [ ] Tests pass (`pytest -q`)
- [ ] Code follows style guidelines
- [ ] Type hints added to all functions
- [ ] Docstrings added to public APIs
- [ ] Logging statements appropriate
- [ ] No bare except clauses
- [ ] No TODO comments
- [ ] Documentation updated
- [ ] Module `AGENTS.md` updated if needed
- [ ] Commits are clean and focused

## Common Issues

### Import Errors
```bash
pip install -r requirements.txt
python -c "import hyperhelix"
```

### Test Failures
```bash
# Run specific test with verbose output
pytest tests/test_file.py::test_name -vv

# Check logs
cat hyperhelix.log
```

### API Key Issues
```bash
# Test key access
python -c "from hyperhelix.utils import get_api_key; print(get_api_key('OPENAI_API_KEY'))"
```

## Getting Help

- **Issues**: Check existing issues or create a new one
- **Documentation**: Read `README.md`, `docs/`, and `AGENTS.md` files
- **Examples**: Look at test files in `tests/`
- **Logs**: Check `hyperhelix.log` and `errors.log`

## Project Structure

```
HelixHyper/
├── hyperhelix/              # Main package
│   ├── core.py             # Graph operations
│   ├── node.py, edge.py    # Core types
│   ├── api/                # REST API
│   ├── cli/                # CLI commands
│   ├── agents/             # LLM integrations
│   ├── persistence/        # Database adapters
│   └── ...
├── tests/                  # Test suite
├── docs/                   # Documentation
├── config/                 # Configuration files
├── .github/                # GitHub config
│   ├── copilot-instructions.md
│   ├── AGENT_INSTRUCTIONS.md
│   └── workflows/
├── README.md               # Getting started
├── CONTRIBUTING.md         # This file
└── AGENTS.md               # Repository guidelines
```

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Questions?

If you have questions not covered here:
1. Check the documentation in `docs/`
2. Read module-specific `AGENTS.md` files
3. Look at existing code and tests
4. Open an issue for clarification

---

Thank you for contributing to HelixHyper! 🚀
