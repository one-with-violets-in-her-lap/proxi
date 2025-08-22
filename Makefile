run-ui:
	uv run python -m proxi.ui.main

run-cli:
	uv run python -m proxi.cli.main

format:
	uv run ruff format

lint:
	uv run ruff check --fix

type-check:
	uv run pyright .

test:
	uv run pytest

build-ui-exe:
	uv run pyinstaller -n proxy-ui --add-data ./assets:./assets ./proxi/ui/main.py

build-cli-exe:
	uv run pyinstaller -n proxy-cli --add-data ./proxi/cli/main.py

