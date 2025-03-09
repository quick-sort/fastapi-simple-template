# Database Related

## Install Postgres in Github Codespace

```bash
sudo apt install postgresql
sudo service postgresql start
```

## Init Database
### Create Database

create database and user using cmd below and update the values into `.env` file

```bash
USER_NAME=fastapi
USER_PASSWORD=fastapi
DB_NAME=app
sudo su - postgres -c "psql -c \"CREATE USER $USER_NAME WITH PASSWORD '$USER_PASSWORD';\""
sudo su - postgres -c "psql -c 'ALTER ROLE $USER_NAME SUPERUSER;'"
sudo su - postgres -c "psql -c 'CREATE DATABASE $DB_NAME OWNER $USER_NAME;'"
sudo su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USER_NAME;'"
sudo su - postgres -c "psql -c 'CREATE DATABASE ${DB_NAME}_test OWNER $USER_NAME;'"
sudo su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME}_test TO $USER_NAME;'"
```

```bash
SQLALCHEMY_URI=postgresql+asyncpg://fastapi:fastapi@localhost:5432/app
```

### Create Tables

```bash
poetry run alembic upgrade head
```

### View Schema Change History

To show all revisions
```bash
poetry run alembic history
```

### Uprade Table Schema

To generate a new revision
```bash
poetry run alembic revision --autogenerate -m "Added New table"
poetry run alembic upgrade head
```

### Downgrade Table Schema

To rollback to brand new
```bash
poetry run alembic downgrade base
```