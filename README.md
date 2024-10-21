FastAPI Simple Template
========================

### Dependencies:
#### Production Deployment
- **[Python3.12](https://docs.python.org/3/whatsnew/3.12.html)** is the latest stabe version. Based on the release information, The asyncio package has had a number of performance improvements, with some benchmarks showing a **75% speed up**.
- **[Poetry](https://python-poetry.org/)** is a great python virtual environment management tool.
- **[Async SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)** is a popular and stable DB ORM framework to manage db models.
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)** is a db model migration management tool, working with sqlalchemy.

#### Development
- **[Pytest](https://docs.pytest.org/en/8.2.x/)** is a unit test framework. Coverage, asyncio extention has alread been installed.
- **[Pylint](https://pylint.readthedocs.io/en/stable/)** is a static code analyser. Can make suggestions about how the code could be refactored.
- **[Mkdocs Material](https://squidfunk.github.io/mkdocs-material/)** generates clean and good looking document like FastAPI documents.

### How to start the project
```bash
poetry run uvicorn app.main:app
```

## Setup Dependencies
### How to install Python 3.12
```bash
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa
apt install python3.12
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
```

### How to install poetry
```bash
pip3.12 install poetry
```

### How to prepare project

1. Prepare project dependencies

```bash
poetry config virtualenvs.in-project true
poetry env use 3.12
poetry lock --no-upgrade
poetry install --no-root
```

### Document Generation

use 
```bash
mkdocs 
```

### Development related 

#### Unit Test
configuration of pytest is inside pyproject.toml, section \[tool.pytest.ini_options\]
```bash
poetry run pytest
```

#### Pylint

```bash
poetry run pylint app
```

To disable certain lint warning, edit .pylintrc, add lines to `disable`
```txt
disable=
    C0114, # missing-module-docstring
    C0115, # missing-class-docstring
```


#### Alembic
To init alembic.ini
```bash
poetry run alembic init --template async app/db/migrations
```
To init a new db
```bash
poetry run alembic upgrade head

```

To generate a new revision

```bash
poetry run alembic revision --autogenerate -m "Added New table"
```
