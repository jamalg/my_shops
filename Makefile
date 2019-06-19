default: up

fill-db:
	docker-compose exec back poetry run flask db fill

migrate:
	docker-compose exec back poetry run alembic revision  --autogenerate --message="${message}"

upgrade:
	docker-compose exec back poetry run alembic upgrade head

downgrade:
	docker-compose exec back poetry run alembic downgrade -1

drop:
	docker-compose exec back poetry run alembic downgrade base

ipy:
	docker-compose exec back poetry run ipython

up:
	docker-compose up

down:
	docker-compose down

stop:
	docker-compose stop

build:
	docker-compose build

flake8:
	docker-compose exec back poetry run flake8 .

test:
	docker-compose exec -e TESTING=True back poetry run pytest