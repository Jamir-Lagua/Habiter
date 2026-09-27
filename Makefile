.PHONY: up down build logs backend-shell db-shell migrate

up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build

logs:
	docker-compose logs -f

backend-logs:
	docker-compose logs -f backend

frontend-logs:
	docker-compose logs -f frontend

backend-shell:
	docker-compose exec backend bash

db-shell:
	docker-compose exec db psql -U timetrack

migrate:
	docker-compose exec backend alembic upgrade head

migrate-create:
	docker-compose exec backend alembic revision --autogenerate -m "$(msg)"

test:
	docker-compose exec backend pytest -v
