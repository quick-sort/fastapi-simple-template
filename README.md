# Simple FastAPI Project Template

![Test Status](https://github.com/quick-sort/fastapi-simple-template/actions/workflows/test.yml/badge.svg?event=push&branch=main)

This is a backend api service template based on python stack. 

## Key Features Ready
### Authentication
There are several authentication methods supported:
- session
- api_key
- jwt token
- oauth

### Async
Async from top to bottom. 
- using AsyncSession from SQLAlchemy
- using AsyncOAuth from authlib

### Document serving
use mkdocs serving documentation

## Key Libraries:
- [**FastAPI**](https://fastapi.tiangolo.com) base service framework.
- [**SQLAlchemy**](https://www.sqlalchemy.org) for the Python SQL database interactions (ORM).
- [PostgreSQL](https://www.postgresql.org) as the SQL database.
- [**UV**](https://docs.astral.sh/uv/) for managing Python project dependencies.
- [PyTest](https://docs.pytest.org/en/stable/) for unit test.
- [PyLint](https://pylint.readthedocs.io/en/stable/) for static code analysis.
- [Mkdocs Material](https://squidfunk.github.io/mkdocs-material/) generates clean and good looking document like FastAPI documents.
- [Authlib](https://authlib.org) for oauth protocol.
