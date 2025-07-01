.PHONY: help install test lint format type-check security clean docker-build docker-test

help:			## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:		## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

install-hooks:		## Install pre-commit hooks
	pre-commit install

test:			## Run tests
	pytest

test-cov:		## Run tests with coverage
	pytest --cov=app --cov-report=html --cov-report=term-missing

lint:			## Run linting
	flake8 app/ tests/

format:			## Format code
	black app/ tests/
	isort app/ tests/

format-check:		## Check code formatting
	black --check app/ tests/
	isort --check-only app/ tests/

type-check:		## Run type checking
	mypy app/

security:		## Run security checks
	bandit -r app/

clean:			## Clean up generated files
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf **/__pycache__/
	rm -rf *.egg-info/

docker-build:		## Build Docker image
	docker build -t majo-budgeting-api:latest .

docker-test:		## Test Docker image
	docker run --rm -d --name test-app -p 8000:8000 majo-budgeting-api:latest
	sleep 5
	curl -f http://localhost:8000/health
	docker stop test-app

ci:			## Run full CI pipeline locally
	make format-check
	make lint
	make type-check
	make security
	make test-cov

# ===== Setup Commands =====
"""
To set up this testing infrastructure:

1. Install dependencies:
   pip install -r requirements-dev.txt

2. Install pre-commit hooks:
   pre-commit install

3. Run sample tests:
   pytest tests/test_sample.py -v

4. Run with coverage:
   pytest --cov=app --cov-report=html

5. Run all quality checks:
   make ci

6. Build and test Docker:
   make docker-build
   make docker-test

7. Format code:
   make format

8. Run security check:
   make security
"""
