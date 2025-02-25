# How to do Unit Test

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
