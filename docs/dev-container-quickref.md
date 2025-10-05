# Development Container Quick Reference

This is a quick reference for using the HelixHyper development container.

## Quick Start

```bash
# Start interactive development session
docker-compose up dev

# Or with docker directly
docker build -f Dockerfile.dev -t helixhyper-dev .
docker run -it -p 8000:8000 -v $(pwd):/app helixhyper-dev
```

## Common Tasks

### Running Tests

```bash
# All tests (with mocked LLM calls)
pytest -q

# With live LLM calls (requires API keys)
USE_REAL_LLM=1 pytest -q
# or
./scripts/test_with_llm.sh

# Specific test file
pytest tests/test_api.py -v

# With coverage
pytest --cov=hyperhelix --cov-report=html
```

### Starting the API Server

```bash
# Development mode with hot reload
uvicorn hyperhelix.api.main:app --host 0.0.0.0 --port 8000 --reload

# Production mode
uvicorn hyperhelix.api.main:app --host 0.0.0.0 --port 8000
```

### Using CLI Commands

```bash
# Scan a directory
python -m hyperhelix.cli.commands scan .

# Get LLM completion
python -m hyperhelix.cli.commands codex "Hello" --provider openrouter

# List models
python -m hyperhelix.cli.commands models --provider openrouter
python -m hyperhelix.cli.commands models --provider huggingface --query gpt2

# Export graph
python -m hyperhelix.cli.commands export graph.json

# List GitHub issues
python -m hyperhelix.cli.commands issues owner/repo
```

### Setting API Keys

Before running LLM-related features, set your API keys:

```bash
export OPENAI_API_KEY=your-key-here
export OPENROUTER_API_KEY=your-key-here
export HUGGINGFACE_API_TOKEN=your-token-here
```

### Code Editing

The container includes:
- **vim** - Advanced text editor
- **nano** - Simple text editor

```bash
vim hyperhelix/core.py
nano README.md
```

### Version Control

Git is available for version control tasks:

```bash
git status
git diff
git log
git add .
git commit -m "Your message"
```

Note: Push operations should be done from your host machine to use your SSH keys.

### Package Management

Install additional Python packages as needed:

```bash
pip install package-name
```

For permanent additions, add to `requirements.txt` or `requirements-dev.txt`.

## Development Tools Available

- **Python 3.11+** - Runtime environment
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **git** - Version control
- **vim** - Text editor
- **nano** - Text editor
- **curl** - HTTP client
- **bash** - Shell with completion

## File Structure

When using volume mounting (`-v $(pwd):/app`), changes you make:
- On your host machine → reflected in container
- In the container → reflected on host machine

This allows you to:
- Edit with your favorite IDE on the host
- Run tests in the container
- See results immediately

## Troubleshooting

### Container won't start
```bash
# Check if port 8000 is in use
lsof -i :8000

# Use a different port
docker run -it -p 8001:8000 -v $(pwd):/app helixhyper-dev
```

### Tests fail with API errors
- Ensure API keys are set in the environment
- Run without `USE_REAL_LLM=1` to use mocks
- Check internet connectivity

### Changes not reflected
- Ensure you're using volume mounting: `-v $(pwd):/app`
- For server, ensure you're using `--reload` flag

### Permission issues
- The container runs as root, files created may have root ownership
- On the host, use `sudo` if needed to modify container-created files

## Best Practices

1. **Always use volume mounting** for development to persist changes
2. **Don't commit API keys** - use environment variables
3. **Run tests before committing** code changes
4. **Use hot reload** (`--reload`) when developing the API
5. **Keep dependencies minimal** - only add what's necessary

## Next Steps

- See `docs/docker.md` for comprehensive Docker documentation
- See `README.md` for overall project documentation
- See `docs/modules.md` for module-specific documentation
- Run `./scripts/demo_dev_workflow.sh` for a guided demo
