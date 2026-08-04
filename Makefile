.EXPORT_ALL_VARIABLES:

GIT_TAG = 1.6.0

all: lint

changelog:
	docker run --quiet --rm --volume "${PWD}:/mnt/source" --workdir /mnt/source ghcr.io/cbdq-io/gitchangelog > CHANGELOG.md


lint:
	isort -v .
	flake8

tag:
	@echo $(GIT_TAG)
