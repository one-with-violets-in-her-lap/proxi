start:
	uv run python -m proxi.ui.main

format:
	uv run ruff format

lint:
	uv run ruff check --fix

type-check:
	uv run pyright .

full-check:
	make format
	make lint
	make type-check
