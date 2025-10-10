.PHONY: help install setup test lint format run-api run-ui docker-up docker-down seed-data test-system clean

help:
	@echo "Swiss Medical Triage System - Available Commands"
	@echo "================================================"
	@echo "install        - Install Python dependencies"
	@echo "setup          - Setup AWS infrastructure"
	@echo "test           - Run tests"
	@echo "lint           - Run linters"
	@echo "format         - Format code with black"
	@echo "run-api        - Run FastAPI server"
	@echo "run-ui         - Run Streamlit UI"
	@echo "docker-up      - Start Docker containers"
	@echo "docker-down    - Stop Docker containers"
	@echo "seed-data      - Seed database with sample data"
	@echo "test-system    - Test complete system"
	@echo "clean          - Clean temporary files"

install:
	pip install -r requirements.txt

setup:
	chmod +x infrastructure/scripts/setup_aws.sh
	./infrastructure/scripts/setup_aws.sh

test:
	pytest tests/ -v --cov=src

lint:
	flake8 src tests
	mypy src --ignore-missing-imports

format:
	black src tests
	isort src tests

run-api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	streamlit run src/ui/app.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

seed-data:
	python scripts/seed_data.py

test-system:
	python scripts/test_system.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
