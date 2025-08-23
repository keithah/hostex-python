.PHONY: help install install-dev test test-cov lint format type-check clean build upload docs

help:
	@echo "Available commands:"
	@echo "  install      Install package"
	@echo "  install-dev  Install package with development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage"
	@echo "  lint         Run linting (flake8)"
	@echo "  format       Format code (black)"
	@echo "  type-check   Run type checking (mypy)"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload       Upload to PyPI (requires credentials)"
	@echo "  docs         Generate documentation"

install:
	pip install .

install-dev:
	pip install -e ".[dev]"

test:
	pytest

test-cov:
	pytest --cov=hostex --cov-report=term-missing --cov-report=html

lint:
	flake8 hostex tests

format:
	black hostex tests

format-check:
	black --check hostex tests

type-check:
	mypy hostex

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python setup.py sdist bdist_wheel

upload: build
	twine upload dist/*

docs:
	@echo "Documentation is in docs/ folder"
	@echo "View docs/README.md for user guide"
	@echo "View docs/API.md for API reference"
	@echo "View docs/examples.md for examples"

check: lint type-check test

all: format lint type-check test