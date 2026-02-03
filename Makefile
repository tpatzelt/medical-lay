.PHONY: help install test lint format clean run-notebooks

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies with Poetry
	poetry install
	@echo "✅ Dependencies installed. Run 'poetry shell' to activate the environment."

install-dev:  ## Install dependencies including dev tools
	poetry install --with dev
	@echo "✅ Dev dependencies installed."

setup:  ## Run the setup script
	./setup.sh

test:  ## Run tests with pytest
	poetry run pytest tests/ -v

test-cov:  ## Run tests with coverage report
	poetry run pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "📊 Coverage report generated in htmlcov/index.html"

lint:  ## Run linting checks
	poetry run ruff check src/
	poetry run mypy src/ --ignore-missing-imports

format:  ## Format code with black
	poetry run black src/ tests/

format-check:  ## Check code formatting without making changes
	poetry run black --check src/ tests/

type-check:  ## Run type checking with mypy
	poetry run mypy src/ --ignore-missing-imports

clean:  ## Clean up cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage
	@echo "🧹 Cleaned up cache and temporary files"

pre-commit-install:  ## Install pre-commit hooks
	poetry run pre-commit install
	@echo "✅ Pre-commit hooks installed"

pre-commit-run:  ## Run pre-commit on all files
	poetry run pre-commit run --all-files

update-deps:  ## Update dependencies
	poetry update
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "✅ Dependencies updated"

notebook-clear:  ## Clear output from all notebooks
	jupyter nbconvert --clear-output --inplace notebooks/**/*.ipynb
	@echo "🧹 Cleared notebook outputs"

run-notebooks:  ## Start Jupyter notebook server
	poetry run jupyter notebook

security-check:  ## Check for security vulnerabilities
	@echo "🔒 Checking for hardcoded secrets..."
	@grep -r "api.*key.*=.*['\"][a-zA-Z0-9-]\{20,\}" --exclude-dir={.git,.venv,venv,node_modules,caches} --exclude=Makefile . || echo "✅ No hardcoded API keys found"
	@echo "🔒 Checking for absolute paths..."
	@grep -r "/home/tim" --exclude-dir={.git,.venv,venv,node_modules,caches} --exclude=Makefile . || echo "✅ No hardcoded absolute paths found"

build:  ## Build distribution packages
	poetry build
	@echo "📦 Distribution packages built in dist/"

check-all: format-check lint type-check test  ## Run all checks (format, lint, type-check, test)
	@echo "✅ All checks passed!"

ci:  ## Run CI pipeline locally
	@echo "🚀 Running CI pipeline..."
	@make format-check
	@make lint
	@make test-cov
	@echo "✅ CI pipeline completed successfully!"
