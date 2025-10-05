#!/bin/bash
# Demonstration of the full development workflow in the container
# This script shows various development tasks you can perform

set -e

echo "=== HelixHyper Development Container Workflow Demo ==="
echo

echo "1. Building development container..."
docker build -f Dockerfile.dev -t helixhyper-dev . > /dev/null 2>&1
echo "   ✓ Development container built successfully"
echo

echo "2. Running tests..."
docker run --rm helixhyper-dev pytest -q
echo "   ✓ Tests passed"
echo

echo "3. Checking installed development tools..."
docker run --rm helixhyper-dev bash -c "
  echo '   - Git: '$(git --version)
  echo '   - Pytest: '$(pytest --version | head -1)
  echo '   - Uvicorn: '$(uvicorn --version)
  echo '   - Python: '$(python --version)
"
echo "   ✓ All dev tools available"
echo

echo "4. Verifying CLI commands work..."
docker run --rm helixhyper-dev python -c "
import hyperhelix.cli.commands
print('   ✓ CLI commands module loads successfully')
"
echo

echo "5. Testing code imports..."
docker run --rm helixhyper-dev python -c "
from hyperhelix.core import HyperHelix
from hyperhelix.node import Node
from hyperhelix.api.main import app
print('   ✓ Core modules import successfully')
"
echo

echo "=== Development Workflow Demo Complete ==="
echo
echo "To start an interactive development session, run:"
echo "  docker run -it -p 8000:8000 -v \$(pwd):/app helixhyper-dev"
echo
echo "Or use Docker Compose:"
echo "  docker-compose up dev"
echo
echo "Inside the container you can:"
echo "  - Run tests: pytest -q"
echo "  - Start API server: uvicorn hyperhelix.api.main:app --host 0.0.0.0 --reload"
echo "  - Use CLI: python -m hyperhelix.cli.commands <command>"
echo "  - Edit code with vim or nano"
echo "  - Use git for version control"
