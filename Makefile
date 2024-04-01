all: lint test

lint:
	isort -v .
	flake8
	bandit -qr .

test:
	PYTHONPATH=. pytest
