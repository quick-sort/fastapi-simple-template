# How to do Unit Test

### Prepare Environment
prepare a test.env
```bash
cat << EOF > .env
ENV=dev
LOG_LEVEL=INFO
JWT_SECRET_KEY=$(tr -dc 'a-zA-Z0-9' < /dev/urandom | fold -w 20 | head -n 1)
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=600
SESSION_SECRET_KEY=secret_key
SQLALCHEMY_URI=postgresql+asyncpg://$USER_NAME:$USER_PASSWORD@localhost:5432/${DB_NAME}_test
EOF

CONFIG_ENV_FILE=test.env uv run alembic downgrade base
CONFIG_ENV_FILE=test.env uv run alembic upgrade head
```


### Unit Test
configuration of pytest is inside pyproject.toml, section \[tool.pytest.ini_options\]
```bash
CONFIG_ENV_FILE=test.env uv run pytest
```
coverage report will be generated in folder `cover`, use `serve cover` to open in browser.

### Pylint

```bash
uv run pylint app
```

To disable certain lint warning, edit .pylintrc, add lines to `disable`
```txt
disable=
    C0114, # missing-module-docstring
    C0115, # missing-class-docstring
```
