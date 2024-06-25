FastAPI Simple Template
========================

### Dependencies:
- **[Python3.12](https://docs.python.org/3/whatsnew/3.12.html)**: Based on 3.12 release information, The asyncio package has had a number of performance improvements, with some benchmarks showing a **75% speed up**.
- **[Poetry](https://python-poetry.org/)**: A great python virtual environment management tool
- **[Async SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)**: Popular and stable DB ORM framework to manage db models 
- **[Alembic](https://alembic.sqlalchemy.org/en/latest/)**: DB model migration management tool
- **[Pytest Asyncio](https://docs.pytest.org/en/8.2.x/)**: Unit test framework, coverage, asyncio support alread installed

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
