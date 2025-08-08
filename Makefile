start:
	uv run python -m proxi.ui.main

format:
	uv run ruff format

lint:
	uv run ruff check --fix

type-check:
	uv run pyright .

build-ui-exe:
	uv run pyinstaller --onefile --add-data ./assets:./assets ./proxi/ui/main.py

