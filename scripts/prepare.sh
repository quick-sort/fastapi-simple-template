#!/bin/bash
USER_NAME=fastapi
USER_PASSWORD=fastapi
DB_NAME=fastapi
sudo su - postgres -c "psql -c \"CREATE USER $USER_NAME WITH PASSWORD '$USER_PASSWORD';\""
sudo su - postgres -c "psql -c 'ALTER ROLE $USER_NAME SUPERUSER;'"
sudo su - postgres -c "psql -c 'CREATE DATABASE $DB_NAME OWNER $USER_NAME;'"
sudo su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USER_NAME;'"
sudo su - postgres -c "psql -c 'CREATE DATABASE ${DB_NAME}_test OWNER $USER_NAME;'"
sudo su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME}_test TO $USER_NAME;'"

cat >> '.env' << EOF
SQLALCHEMY_URI=postgresql+asyncpg://${USER_NAME}:${USER_PASSWORD}@localhost:5432/${DB_NAME}
EOF