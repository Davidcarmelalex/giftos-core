# Contributing to GiftOS Core

Thank you for your interest in contributing to GiftOS! This document provides guidelines for participating in the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a new branch for your feature or fix
4. Make your changes
5. Run tests and linting
6. Submit a pull request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/giftos-core.git
cd giftos-core

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
black --check .
```

## Branch Naming

- `feature/description` — New features
- `fix/description` — Bug fixes
- `docs/description` — Documentation updates
- `refactor/description` — Code refactoring

## Commit Messages

Follow conventional commits:

```
feat: add NoOnes OAuth connector
fix: resolve race condition in price scanner
docs: update API authentication guide
refactor: simplify portfolio engine calculations
test: add coverage for market intelligence module
```

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add tests for new functionality
4. Request review from maintainers
5. Address review feedback
6. Squash commits if requested

## Code Style

- **Python**: PEP 8, Black formatting, Ruff linting
- **Type hints**: Required for all public functions
- **Docstrings**: Google style

## Reporting Issues

When reporting bugs, include:
- GiftOS version
- Python version
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs or screenshots

## Security Issues

Please do **not** open public issues for security vulnerabilities. See [SECURITY.md](SECURITY.md) for responsible disclosure.

## Questions?

Open a [Discussion](https://github.com/giftos/giftos-core/discussions) or reach out in our community channels.
