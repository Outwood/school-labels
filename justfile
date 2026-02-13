test *args:
    uv run pytest {{ args }}

lint:
    uv run ruff check

format:
    uv run ruff check --select I --fix
    uv run ruff format

check: lint test
