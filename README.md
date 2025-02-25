FastAPI Simple Template
========================

### How to prepare project

1. Prepare project dependencies
2. Prepare PostgreSQL

First install and start postgreSQL service.
```bash
sudo apt install postgresql
sudo service postgresql start
```

3. Setup user and database


edit '.env' file in the project, change the user:password in the SQLALCHEMY_URI accordingly.
```bash
SQLALCHEMY_URI=postgresql+asyncpg://postgres:postgres@localhost:5432/app
```

### How to start the project
Edit `.env` file
```

```

Before starting the project, setup environment dependencies first.
```bash

```
