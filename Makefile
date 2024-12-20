.EXPORT_ALL_VARIABLES:

GIT_TAG = 1.2.11

all: lint avro build test

avro:
	make -C avro

build:
	./uk/gov/metoffice/historic_station_data/scripts/etl.py
	./gx.py -v
	LOG_LEVEL=INFO python workflows/gbp_exchange_rates.py

changelog:
	GIT_TAG=$(GIT_TAG) gitchangelog > CHANGELOG.md

lint:
	isort -v .
	flake8
	bandit -qr .

tag:
	@echo $(GIT_TAG)

test:
	PYTHONPATH=.:workflows pytest
