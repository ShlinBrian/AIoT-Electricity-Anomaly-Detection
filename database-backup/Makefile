init: ## Initialize pipenv environment
	pipenv --python 3.7

prod: ## Build up the production environment
	pipenv install

dev: ## Build up the development environment
	pipenv install --dev
	pipenv run pre-commit install
	pipenv run pre-commit install -t commit-msg

commit: ## Commit with commitizen
	pipenv run cz commit

commit-retry: ## Retry Commit with previous commit messages
	pipenv run cz commit --retry

start: ## Start up the DB service
	docker-compose up -d

build: ## Build postgres with mock data
	pipenv run alembic upgrade head
	pipenv run ./setup.sh -o init -u '$$DB_URL'
	pipenv run ./setup.sh -o mock -u '$$DB_URL'

db_shell:
	psql postgresql://nighteen_gale:password@localhost:5435/itoc

format: ## Format the code and sort the import package
	pipenv run black **/*.py
	pipenv run isort **/*.py

shutdown: ## Shutdown the database and remove the volume
	docker-compose down
	docker volume rm database_postgres_data

rebuild: shutdown start build ## Build again after shutdown db and volume

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
