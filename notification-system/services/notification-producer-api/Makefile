SERVICE_NAME = notification_producer_api

startenv:
	source .venv/bin/activate

run:
	uv run uvicorn $(SERVICE_NAME).main:app --reload --host 0.0.0.0 --port 8001