SERVICE_NAME = notification_producer_api

CONTAINER ?=

startenv:
	source .venv/bin/activate

run:
	uv run uvicorn $(SERVICE_NAME).main:app --reload --host 0.0.0.0 --port 8001

destroy:
	docker compose down
	docker container prune -f

upbuild:
	docker compose up --build

up:
	docker compose up -d


logs:
	docker compose logs

down:
	docker compose down
