SHELL := /bin/bash

.PHONY: init venv install clean run-api lint test

init:
	@echo "Initializing project..."
	python3 -m venv .venv && \
	source .venv/bin/activate && \
	pip install -e .

install:
	pip install -e .

run-api:
	uvicorn app.main:app --reload

lint:
	flake8 src/ --ignore=E501

test:
	pytest tests/

clean:
	rm -rf __pycache__ .pytest_cache .venv