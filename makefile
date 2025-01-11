# Makefile

# Run makemigrations in the backend container
makemigrations:
	docker-compose exec backend python manage.py makemigrations

createsuperuser:
	docker-compose exec backend python manage.py createsuperuser

shell:
	docker-compose exec backend sh

# Start the Django development server
startserver:
	docker-compose up --build

# Apply migrations in the backend container
migrate:
	docker-compose exec backend python manage.py migrate

# Run tests with coverage in the backend container
tests:
	docker-compose exec backend pytest -rP -v

# Run tests with coverage in the backend container
test-coverage:
	docker-compose exec backend coverage run -m pytest -rP -v && coverage report -m

test-ci:
	docker compose exec backend coverage run -m pytest

build-ci:
	docker compose build --parallel && docker compose up -d && docker compose exec backend python manage.py makemigrations && docker compose exec backend python manage.py migrate
