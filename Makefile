all: install lint ukmo-hso

clean:
	docker system prune --all --force
	docker volume prune --all --force

install:
	pip install --upgrade pip
	pip freeze > /tmp/constraints.txt
	pip install -c /tmp/constraints.txt -r .devcontainer/requirements.txt

lint:
	yamllint -s .
	isort .
	flake8
	bandit -qr .

ukmo-hso:
	PYTHONPATH=./uk/gov/metoffice/historic-station-data/src pytest
