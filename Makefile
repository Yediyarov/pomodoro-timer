.DEFAULT_GOAL := help

ENV ?= local

# run: ## Run the application using uvicorn with provided arguments or defaults
# 	ENV=$(ENV) poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --reload

run: ## Run the application using gunicorn
	ENV=$(ENV) gunicorn main:app -c infra/gunicorn.conf.py

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstalling dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

migrate-create: ## Create a new migration
	ENV=$(ENV) alembic revision --autogenerate -m "$(MIGRATION)"

migrate-apply: ## Apply migrations
	ENV=$(ENV) alembic upgrade head

docker-up: ## Start Docker services with specified environment
	./scripts/run.sh $(ENV)

docker-down: ## Stop Docker services
	docker compose down

help: ## Show this help message
	@echo "Usage: make [command] [ENV=local|prod]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'