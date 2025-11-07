.PHONY: help install download-data preprocess train evaluate api docker clean test format lint

help:
	@echo "Available commands:"
	@echo "  make install          - Install dependencies"
	@echo "  make download-data    - Download dataset"
	@echo "  make preprocess       - Preprocess data"
	@echo "  make train            - Train models"
	@echo "  make evaluate         - Evaluate models"
	@echo "  make api              - Start API server"
	@echo "  make docker           - Build and run Docker"
	@echo "  make test             - Run tests"
	@echo "  make format           - Format code with black"
	@echo "  make lint             - Lint code with flake8"
	@echo "  make clean            - Clean generated files"

install:
	pip install -r requirements.txt

download-data:
	python src/utils/download_data.py

preprocess:
	python src/features/preprocessing.py

train:
	python src/models/train.py

evaluate:
	python src/models/evaluate.py

predict:
	python src/models/predict.py

api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

api-prod:
	uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4

docker-build:
	docker build -t churn-prediction-api .

docker-run:
	docker run -p 8000:8000 -v $(PWD)/data:/app/data churn-prediction-api

docker:
	docker-compose up --build

docker-down:
	docker-compose down

test:
	pytest tests/ -v

test-coverage:
	pytest tests/ -v --cov=src --cov-report=html

format:
	black src/ tests/

lint:
	flake8 src/ tests/ --max-line-length=100 --ignore=E203,W503

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name "*.pyo" -delete
	find . -name ".pytest_cache" -exec rm -rf {} +
	find . -name ".coverage" -delete
	find . -name "htmlcov" -exec rm -rf {} +
	find . -name "*.log" -delete

mlflow:
	mlflow ui --host 0.0.0.0 --port 5000

all: install download-data preprocess train evaluate
	@echo "✅ Complete pipeline executed!"
