.EXPORT_ALL_VARIABLES:

GIT_TAG = 0.2.1

all: lint build test

build:
	make -C avro
	./uk/gov/metoffice/historic_station_data/scripts/etl.py

changelog:
	GIT_TAG=$(GIT_TAG) gitchangelog > CHANGELOG.md

lint:
	isort -v .
	flake8
	bandit -qr .

test:
	PYTHONPATH=. pytest
