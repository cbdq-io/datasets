.EXPORT_ALL_VARIABLES:

GIT_TAG = 1.3.6

all: lint avro build test

BSA:
	curl -s -H "X-Auth-Token: ${FOOTBALL_DATA_API_KEY}" \
	    https://api.football-data.org/v4/competitions/BSA/matches \
	    | ./org/football-data/scripts/etl.py

avro:
	make -C avro

build:
	./uk/gov/metoffice/historic_station_data/scripts/etl.py
	./gx.py -v
	LOG_LEVEL=INFO python workflows/gbp_exchange_rates.py

changelog:
	docker run --quiet --rm --volume "${PWD}:/mnt/source" --workdir /mnt/source ghcr.io/cbdq-io/gitchangelog > CHANGELOG.md

lint:
	isort -v .
	flake8
	bandit -qr .

tag:
	@echo $(GIT_TAG)

test:
	PYTHONPATH=.:workflows pytest
