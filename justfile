set shell := ["powershell.exe", "-c"]

# Show help message
help:
    @just --list

# Install dependinces
install:
    @echo "🚀 Installing dependencies"
    @poetry install

# Check project
check-project:
    @echo "🚀 Checking consistency between poetry.lock and pyproject.toml"
    @poetry check --lock

# Ryn ruff without fix
ruff:
    @ruff check $(git ls-files '*.py')

# Run mypy
mypy:
    @poetry run mypy $(git ls-files '*.py')

# Run isort
isort:
    @poetry run isort $(git ls-files '*.py')

# Audit packages
audit:
    @pip-audit .

# Run black linter
black:
    @poetry run black $(git ls-files '*.py')

# Run pre-commit lint
lint:
    @pre-commit run --all-files
