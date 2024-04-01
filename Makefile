.EXPORT_ALL_VARIABLES:

GIT_TAG = 0.1.0

all: lint test

changelog:
	GIT_TAG=$(GIT_TAG) gitchangelog > CHANGELOG.md

lint:
	isort -v .
	flake8
	bandit -qr .

test:
	PYTHONPATH=. pytest
