## Init Template

You can git clone the template to your local workspace, or [fork](https://github.com/quick-sort/fastapi-simple-template/fork) / [import](https://github.com/new/import) on github directly.
```bash
git clone --depth=1 https://github.com/quick-sort/fastapi-simple-template.git myapp
cd myapp
rm -rf .git
git init
git remote add origin git@github.com:quick-sort/myapp.git
git add .
git commit -m 'init commit'
```

## Prerequisites

Install following softwares:

- [Python3.12](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [PostgreSQL](https://www.postgresql.org/download/)

## Install Project Dependencies

```bash
poetry env use 3.12
poetry install
```

## Init Database

### Create Database and User in PostgreSQL
```bash
USER_NAME=fastapi
USER_PASSWORD=fastapi
DB_NAME=app
sudo su - postgres -c "psql -c \"CREATE USER $USER_NAME WITH PASSWORD '$USER_PASSWORD';\""
sudo su - postgres -c "psql -c 'create database $DB_NAME OWNER $USER_NAME;'"
sudo su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USER_NAME;'"
```

### Create Environment File `.env`

```bash
cat << EOF > .env
ENV=dev
LOG_LEVEL=INFO
JWT_SECRET_KEY=$(tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w 20 | head -n 1)
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=600
SESSION_COOKIE_NAME=session
SQLALCHEMY_URI=postgresql+asyncpg://$USER_NAME:$USER_PASSWORD@localhost:5432/$DB_NAME
EOF
```

### Create Tables in Database

```bash
poetry run alembic upgrade head
```

## Start Service in Dev mode

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Start Service in Production mode
recommend using docker deployment method.
```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Check Service Running
open `http://localhost:8000/api/docs` in browser