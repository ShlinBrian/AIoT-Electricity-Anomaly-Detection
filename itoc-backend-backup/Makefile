PKG = api

init:
	pipenv --python 3.8

prod: ## Build up the production environment
	pipenv install
	
run-dev:
	cd ${PKG} && uvicorn --host 0.0.0.0 --port 9000 main:app --reload