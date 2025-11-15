# GitHub Configuration for HelixHyper

This directory contains GitHub-specific configuration files to enhance productivity for developers, AI agents, and automation tools.

## Files Overview

### `copilot-instructions.md`
Comprehensive instructions for GitHub Copilot to understand the HelixHyper codebase and provide context-aware suggestions. This file includes:
- Project architecture overview
- Module structure and responsibilities
- Development guidelines and best practices
- Common patterns and code examples
- API and CLI usage
- Testing strategies

**Usage**: GitHub Copilot automatically reads this file when providing code suggestions in the repository.

### `AGENT_INSTRUCTIONS.md`
Detailed instructions for AI agents (Codex, ChatGPT, Claude, etc.) to effectively work with the HelixHyper repository. Includes:
- System identity and use cases
- Quick start guides
- Architecture deep dive
- Environment configuration
- API reference documentation
- Common patterns for AI agents
- Troubleshooting guides
- Module-specific guidelines

**Usage**: Reference this file when providing repository context to AI agents or LLMs.

### `workflows/ci.yml`
GitHub Actions workflow for continuous integration:
- Automated testing on push and pull requests
- Multi-version Python testing
- Code coverage reporting
- Import verification
- Docker build testing

**Usage**: Automatically runs on commits to main branches and pull requests.

## For GitHub Copilot Users

GitHub Copilot will automatically use `copilot-instructions.md` to provide better suggestions. To get the most value:

1. **Keep context files open**: Open relevant `AGENTS.md` files from module directories
2. **Use descriptive comments**: Write clear comments about what you want to achieve
3. **Reference patterns**: Copilot knows about the patterns in this repo (see copilot-instructions.md)
4. **Type hints help**: Copilot uses type hints for better suggestions

Example workflow:
```python
# Create a new LLM integration for Anthropic Claude
from hyperhelix.agents.llm import BaseChatModel
# Copilot will suggest a complete class implementation following existing patterns
```

## For Codex/ChatGPT Users

When working with this repository through Codex or ChatGPT:

1. **Start with AGENT_INSTRUCTIONS.md**: Provide this file as context for comprehensive understanding
2. **Reference module AGENTS.md**: Each module has specific guidelines in its directory
3. **Check examples**: Look at test files for usage patterns
4. **Use graph summaries**: LLM integrations include automatic graph context

Example prompt:
```
I'm working with the HelixHyper repository. [Paste AGENT_INSTRUCTIONS.md content]

Now help me implement a new persistence adapter for PostgreSQL.
```

## For Developers

### Setting Up Your Environment

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. **Configure API keys** (optional for LLM features):
   ```bash
   export OPENAI_API_KEY="your-key"
   export OPENROUTER_API_KEY="your-key"
   export HUGGINGFACE_API_TOKEN="your-key"
   export GITHUB_TOKEN="your-token"  # For CLI issues command
   ```

3. **Run tests**:
   ```bash
   pytest -q
   ```

4. **Start developing** with Copilot assistance!

### Enhancing Copilot Suggestions

To get better suggestions from Copilot:

1. **Open relevant files**: Keep related modules open in your editor
2. **Write clear docstrings**: Copilot uses them for context
3. **Use consistent naming**: Follow existing patterns (see copilot-instructions.md)
4. **Add type hints**: Helps Copilot understand interfaces
5. **Write comments**: Describe intent before implementation

### Contributing Workflow

1. Create a feature branch
2. Make changes with Copilot assistance
3. Write tests (Copilot can help generate test cases)
4. Run `pytest -q` to verify
5. Check `hyperhelix.log` for any issues
6. Submit pull request
7. CI automatically runs tests

## For Repository Maintainers

### Updating Agent Instructions

When making significant changes to the codebase:

1. **Update copilot-instructions.md**: Add new patterns, modules, or guidelines
2. **Update AGENT_INSTRUCTIONS.md**: Add new API endpoints, CLI commands, or examples
3. **Update module AGENTS.md**: Keep module-specific guidelines current
4. **Update main README.md**: Ensure getting started guide is accurate

### Maintaining CI/CD

The `workflows/ci.yml` file runs on:
- Pushes to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`

Consider adding:
- Code quality checks (flake8, mypy, black)
- Security scanning
- Deployment workflows
- Release automation

### Adding New Workflows

Create new workflow files in `.github/workflows/`:
- `release.yml` - Automated releases
- `security.yml` - Security scanning
- `docs.yml` - Documentation deployment
- `performance.yml` - Performance testing

## Directory Structure

```
.github/
├── README.md                    # This file
├── copilot-instructions.md      # GitHub Copilot configuration
├── AGENT_INSTRUCTIONS.md        # AI agent comprehensive guide
└── workflows/
    └── ci.yml                   # Continuous integration
```

## Additional Resources

- **Main README**: `/README.md` - Getting started guide
- **Architecture**: `/docs/architecture.md` - System design
- **Modules**: `/docs/modules.md` - Component guide
- **Root AGENTS.md**: `/AGENTS.md` - Repository guidelines
- **Module AGENTS.md**: Each module directory has specific guidelines

## Best Practices

### For All Users

1. **Read documentation first**: Start with `README.md`, then relevant `AGENTS.md` files
2. **Follow patterns**: Use existing code as examples
3. **Test frequently**: Run `pytest -q` after changes
4. **Check logs**: Review `hyperhelix.log` for debugging
5. **Use type hints**: Helps both humans and AI understand code

### For AI Agents

1. **Load context**: Start with `AGENT_INSTRUCTIONS.md`
2. **Check module guidelines**: Refer to module-specific `AGENTS.md` files
3. **Follow conventions**: Use patterns from existing code
4. **Generate tests**: Create tests alongside implementation
5. **Validate changes**: Ensure code imports and tests pass

### For Developers

1. **Configure editor**: Enable Copilot/AI assistant
2. **Keep files open**: More context = better suggestions
3. **Write comments**: Guide AI suggestions with clear intent
4. **Review suggestions**: AI is helpful but not perfect
5. **Commit frequently**: Small, focused commits work best

## Troubleshooting

### Copilot Not Working Well

1. Ensure `copilot-instructions.md` is present and up-to-date
2. Open related files to provide more context
3. Write clearer comments describing intent
4. Check your editor's Copilot settings

### CI Failing

1. Run tests locally: `pytest -q`
2. Check logs: `hyperhelix.log` and `errors.log`
3. Verify dependencies: `pip install -r requirements.txt`
4. Review workflow logs in GitHub Actions tab

### Agent Context Issues

1. Ensure you're referencing `AGENT_INSTRUCTIONS.md`
2. Provide relevant module `AGENTS.md` content
3. Include specific error messages or requirements
4. Reference existing code examples

## Feedback and Improvements

To improve these configurations:

1. Open an issue describing the enhancement
2. Submit a pull request with changes
3. Update documentation alongside code changes
4. Test with actual AI tools before merging

---

**Remember**: These configurations exist to make development more productive. Keep them updated as the codebase evolves!
