# How to Guides

## How to view docs

```bash
poetry run mkdocs serve
```

## How to manage DB

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


To rollback to brand new
```bash
poetry un alembic downgrade base
```