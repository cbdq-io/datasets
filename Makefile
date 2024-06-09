.EXPORT_ALL_VARIABLES:

GIT_TAG = 1.0.0

all: lint avro build test

avro:
	make -C avro

build:
	./uk/gov/metoffice/historic_station_data/scripts/etl.py
	./gx.py -v

changelog:
	GIT_TAG=$(GIT_TAG) gitchangelog > CHANGELOG.md

lint:
	isort -v .
	flake8
	bandit -qr .

tag:
	@echo $(GIT_TAG)

test:
	PYTHONPATH=. pytest
