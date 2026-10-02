# Mio

A Windows desktop companion and utility hub.

## Status

- **Version:** V1 — Desktop Companion
- **Stage:** Early development

## Documentation

- [PROJECT.md](PROJECT.md) — Product purpose and principles
- [ARCHITECTURE.md](ARCHITECTURE.md) — Technical architecture and boundaries
- [ROADMAP.md](ROADMAP.md) — Development phases and scope

## Development Setup

Requires Python 3.12+.

```bash
# Create a virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check src/ tests/
```
