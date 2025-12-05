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
