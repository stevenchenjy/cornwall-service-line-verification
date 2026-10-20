.PHONY: setup check fetch preflight
setup:
	uv sync --locked
check:
	uv run python -m unittest discover -s tests -v
	uv run python scripts/validate_setup.py
	uv run python scripts/check_language.py
fetch:
	uv run python scripts/fetch_inventory.py
preflight:
	uv run python scripts/audit_inventory.py
