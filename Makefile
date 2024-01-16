all: install lint ukmohsd

clean:
	find . -type d -name __pycache__ -exec rm -rf {} \;
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

ukmohsd:
	PYTHONPATH=./uk/gov/metoffice/historic-station-data/scripts pytest
