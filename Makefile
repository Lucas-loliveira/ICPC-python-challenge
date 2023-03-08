build up:
	docker-compose up -d --build

up:
	docker-compose up -d

test:
	docker-compose exec api bash -c "pytest"

down:
	docker-compose down 