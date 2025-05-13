PKG = backend

.PHONY: init flake8 pylint lint test clean dev commit run simple-clean pre-commit-clean prod dev pre-commit

init: simple-clean
	pipenv --python 3.7
	git submodule update --init --recursive

service_up:
	docker-compose up -d analysis-scheduler-redis

service_down:
	docker-compose down && docker volume rm analysis-scheduler-redis-data

prod: init
	pipenv install

dev: init
	pipenv install --dev
	yes | pipenv run mypy ./scheduler --install-types --non-interactive || true

pre-commit: dev
	pipenv run pre-commit install
	pipenv run pre-commit install -t commit-msg

commit: ## Commit with commitizen
	pipenv run cz commit

commit-retry: ## Retry Commit with previous commit messages
	pipenv run cz commit --retry

lint: pylint flake8

format:
	pipenv run black **/*.py
	pipenv run isort **/*.py

flake8:
	pipenv run flake8 --max-line-length=120

pylint:
	pipenv run pylint scheduler --ignore=tests

test:
	pipenv run pytest --cov=./scheduler -rsx ./tests

build: build-docker

build-docker:
	docker build -t private-cloud-scheduler . --no-cache

run:
	pipenv run python -m scheduler.main

simple-clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .mypy_cache
	rm -rf .hypothesis
	rm -rf .pytest_cache
	rm -rf .tox
	rm -f report.xml
	rm -f coverage.xml

pre-commit-clean:
	pipenv run pre-commit uninstall
	pipenv run pre-commit clean

clean:
	make simple-clean
	make pre-commit-clean

help:
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sed -n 's/^\(.*\): \(.*\)##\(.*\)/\1\3/p' \
	| column -t  -s ' '