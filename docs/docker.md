# Docker Development Guide

This guide explains how to use Docker for both production and development workflows with HelixHyper.

## Quick Start with Docker Compose

The easiest way to get started is with Docker Compose:

```bash
# Start the production API server
docker-compose up api

# Start the development environment
docker-compose up dev

# Or run in detached mode
docker-compose up -d api
```

The compose file automatically:
- Builds the appropriate image
- Maps port 8000 to your host
- Passes through API keys from your environment
- Mounts logs and source code (for dev)

## Production Container

The standard `Dockerfile` builds a minimal production container that runs the API server:

```bash
docker build -t helixhyper .
docker run -p 8000:8000 helixhyper
```

This container:
- Installs only production dependencies from `requirements.txt`
- Automatically starts the uvicorn API server on port 8000
- Is optimized for deployment and running the service

## Development Container

The `Dockerfile.dev` builds a full development environment container with all tools needed for development:

```bash
docker build -f Dockerfile.dev -t helixhyper-dev .
docker run -it -p 8000:8000 -v $(pwd):/app helixhyper-dev
```

This container:
- Installs development dependencies from `requirements-dev.txt` (including pytest)
- Includes development tools (git, vim, nano, curl)
- Drops you into a bash shell for interactive development
- Supports volume mounting for live code editing

### Development Workflow in Container

Once inside the development container, you can:

1. **Run tests:**
   ```bash
   pytest -q
   # or with live LLM tests:
   USE_REAL_LLM=1 pytest -q
   # or using the helper script:
   ./scripts/test_with_llm.sh
   ```

2. **Start the API server with hot reload:**
   ```bash
   uvicorn hyperhelix.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Use CLI commands:**
   ```bash
   python -m hyperhelix.cli.commands scan .
   python -m hyperhelix.cli.commands codex "Hello" --provider openrouter
   python -m hyperhelix.cli.commands models --provider openrouter
   ```

4. **Edit code:**
   - If you mounted the volume (`-v $(pwd):/app`), edit files on your host and they'll be reflected in the container
   - Or use vim/nano inside the container

5. **Set API keys:**
   ```bash
   export OPENAI_API_KEY=your-key-here
   export OPENROUTER_API_KEY=your-key-here
   export HUGGINGFACE_API_TOKEN=your-token-here
   ```
   
   Or pass them when running the container:
   ```bash
   docker run -it -p 8000:8000 \
     -e OPENAI_API_KEY=your-key \
     -e OPENROUTER_API_KEY=your-key \
     -v $(pwd):/app \
     helixhyper-dev
   ```

### Best Practices

- **Volume mounting:** Use `-v $(pwd):/app` to mount your local code into the container so changes persist
- **API keys:** Pass sensitive keys via environment variables (`-e KEY=value`) rather than building them into the image
- **Port mapping:** Always expose port 8000 with `-p 8000:8000` if you plan to access the API
- **Interactive mode:** Use `-it` flags for an interactive terminal session

### Running Specific Commands

If you want to run a specific command without entering an interactive shell:

```bash
# Run tests
docker run --rm helixhyper-dev pytest -q

# Start the server
docker run --rm -p 8000:8000 helixhyper-dev \
  uvicorn hyperhelix.api.main:app --host 0.0.0.0 --port 8000 --reload

# Run CLI commands
docker run --rm helixhyper-dev \
  python -m hyperhelix.cli.commands models --provider openrouter
```

## Container Differences

| Feature | Production (`Dockerfile`) | Development (`Dockerfile.dev`) |
|---------|---------------------------|--------------------------------|
| Dependencies | Production only | Production + dev tools |
| System packages | Minimal | git, vim, nano, curl, etc. |
| Default command | Runs uvicorn server | Drops to bash shell |
| Size | Smaller | Larger (includes dev tools) |
| Use case | Deployment | Development & testing |

## Internet Connectivity

Both containers have internet access enabled, allowing you to:
- Install additional packages with pip
- Access external APIs (OpenAI, OpenRouter, HuggingFace)
- Clone repositories with git (in dev container)
- Download models and data

Make sure your Docker daemon has internet access and isn't blocked by firewalls or proxy settings.

## Troubleshooting

### SSL Certificate Errors

Both Dockerfiles include `--trusted-host` flags when installing packages to work around SSL certificate verification issues that can occur in some CI/CD environments or corporate networks with proxies. This is a known workaround and does not compromise security when installing from official PyPI mirrors.

If you encounter SSL errors when building the images, these flags help bypass self-signed certificate issues in the build environment.

### Container Won't Start

If the production container won't start, check the logs:

```bash
docker logs <container-id>
```

Common issues:
- Port 8000 already in use: Use `-p 8001:8000` to map to a different host port
- Missing configuration: Ensure `config/` directory exists and contains required YAML files

### Tests Fail in Container

When running tests with `USE_REAL_LLM=1` or `./scripts/test_with_llm.sh`, tests will fail if API keys are not set. This is expected behavior. Either:

1. Set API keys as environment variables when running the container
2. Run tests without the flag (default mocks will be used)
3. Run only specific tests that don't require API access
