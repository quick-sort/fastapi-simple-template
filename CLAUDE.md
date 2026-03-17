# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI-based backend API service template with PostgreSQL, supporting multiple authentication methods (session, JWT, API key, OAuth). Uses UV for dependency management and pytest for testing.

## Common Commands

```bash
# Install dependencies
uv sync

# Run development server (with auto-reload)
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest

# Run tests with verbose output and coverage
uv run pytest -v

# Run a single test file
uv run pytest tests/api/endpoints/test_auth.py

# Run CLI commands
uv run python -m app.cli.main <command>

# Create initial admin user
uv run python -m app.cli.main init-user --username admin --email admin@example.com --password <password> --role admin

# Database migrations
uv run alembic upgrade head
uv run alembic revision --autogenerate -m "description"

# Build Docker image
docker build -t app .

# Run Docker container
docker run -p 8000:8000 app
```

## Environment Configuration

Copy `sample.env` to `.env` and configure required variables:
- `SQLALCHEMY_URI` - PostgreSQL connection string
- `SESSION_SECRET_KEY` - Secret for session authentication
- `JWT_SECRET_KEY` - Secret for JWT tokens

For testing, a `.env.test` file is used automatically (configured via pytest-env).

## Architecture

### Directory Structure
- `app/api/endpoints/v1/` - API route handlers
- `app/api/middlewares/` - Middleware (auth, db)
- `app/api/depends.py` - FastAPI dependency injection
- `app/db/models/` - SQLAlchemy ORM models
- `app/db/session.py` - Async database session setup
- `app/cli/` - CLI commands with auto-discovery pattern
- `app/utils/` - Utility functions (security, etc.)
- `tests/` - Test files mirroring app structure

### Authentication
Multiple auth methods in `app/api/middlewares/auth/`:
- `token.py` - JWT bearer tokens
- `session.py` - Cookie-based sessions
- `api_key.py` - API key authentication
- `basic.py` - HTTP Basic auth

### Adding New CLI Commands
Create a new file in `app/cli/` with a `registry_command(parser)` function that registers subcommands:

```python
async def my_command(args):
    # command logic
    pass

def registry_command(parser):
    subparser = parser.add_parser("my-command", help="Description")
    subparser.set_defaults(func=my_command)
    subparser.add_argument("--arg", required=True)
    return subparser
```

### Adding API Endpoints
Endpoints are auto-registered in `app/api/endpoints/v1/__init__.py`. Create new route files following the existing pattern with FastAPI routers.

### Database Models
Models inherit from `Base` in `app/db/models/base.py`. The base class provides a `create()` class method for async object creation.

### Testing
- Tests use pytest-asyncio with async fixtures
- A test database is created/dropped per test session
- Default `admin` and `user` fixtures are created automatically
- Access `db_session` fixture for database operations in tests

## Dependencies

Key libraries:
- FastAPI (web framework)
- SQLAlchemy + asyncpg (async ORM)
- Authlib (OAuth)
- Pydantic Settings (configuration)
- PyJWT (JWT tokens)
- pwdlib (password hashing with argon2)
