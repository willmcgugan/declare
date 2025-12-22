.PHONY: test
test:
	uv run pytest

.PHONY: install
install:
	uv sync --all-extras

.PHONY: dev
dev:
	uv sync --all-extras

.PHONY: clean
clean:
	rm -rf .pytest_cache .mypy_cache __pycache__ dist build *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
