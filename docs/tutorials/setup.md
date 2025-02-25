## Install Prerequisites

### Python 3.12
```bash
apt install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa
apt install python3.12
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12
```

### Poetry
```bash
pip3.12 install poetry
```

## Install Dependencies

```bash
poetry install
```

## Create Database
log in postgre service using postgres user, create db and alter user password

```bash
sudo su - postgres -c "psql -c 'create database app'"
sudo su - postgres -c "psql -c \"alter user postgres password 'postgres'\""
```

## Update Environment File `.env`
```markdown
ENV=dev
LOG_LEVEL=INFO
JWT_SECRET_KEY=a_secret_string
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=600
SESSION_COOKIE_NAME=session
SQLALCHEMY_URI=postgresql+asyncpg://postgres:postgres@localhost:5432/app
```

## Init Database Schema

```bash
poetry run alembic upgrade head
```

## Start Service in dev mode

```bash
poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
