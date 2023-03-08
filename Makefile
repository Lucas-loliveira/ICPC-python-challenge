build up:
	docker-compose up -d --build

up:
	docker-compose up -d

migrate:
	docker-compose exec api bash -c "python manage.py migrate"

test:
	docker-compose exec api bash -c "pytest"

down:
	docker-compose down 