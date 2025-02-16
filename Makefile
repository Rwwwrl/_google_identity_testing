# DOCKER

up:
	docker compose up -d

down:
	docker compose down

restart:
	$(MAKE) down
	$(MAKE) up

drop_volume:
	docker volume rm gen_django_application_postgres_data



# MIGRATIONS

migrate:
	python main/manage.py migrate

makemigrations:
	python main/manage.py makemigrations
