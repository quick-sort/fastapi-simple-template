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
poetry lock --no-update
poetry install --no-root
```

2. Prepare PostgreSQL

First install and start postgreSQL service.
```bash
sudo apt install postgresql
sudo service postgresql start
```

3. Setup user and database
login using postgres user, create db and alter user password
```bash
sudo su - postgres -c "psql -c 'create database app'"
sudo su - postgres -c "psql -c \"alter user postgres password 'postgres'\""
```

edit '.env' file in the project, change the user:password in the SQLALCHEMY_URI accordingly.
```bash
SQLALCHEMY_URI=postgresql+asyncpg://postgres:postgres@localhost:5432/app
```

### How to start the project
Edit `.env` file
```
ENV=dev
LOG_LEVEL=INFO
JWT_SECRET_KEY=a_secret_string
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=600
SESSION_COOKIE_NAME=session
SQLALCHEMY_URI=postgresql+asyncpg://postgres:postgres@localhost:5432/app
```

Before starting the project, setup environment dependencies first.
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
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
CONFIG_ENV_FILE=test.env poetry run pytest
```
coverage report will be generated in folder `cover`, use `serve cover` to open in browser.

How to install serve
```bash
npm install serve -g
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
To init alembic.ini, already inited
```bash
poetry run alembic init --template async app/db/migrations
```

To generate a new revision

```bash
poetry run alembic revision --autogenerate -m "Added New table"
```

To show all revisions
```bash
poetry run alembic history
```

To init a new db to latest
```bash
poetry run alembic upgrade head

```

To rollback to brand new
```bash
poetry un alembic downgrade base
```