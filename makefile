# Makefile

# Run makemigrations in the backend container
makemigrations:
	docker-compose exec backend python manage.py makemigrations

# Start the Django development server
startserver:
	docker-compose up --build

# Apply migrations in the backend container
migrate:
	docker-compose exec backend python manage.py migrate

# Run tests with coverage in the backend container
test-coverage:
	docker-compose exec backend coverage run -m pytest -rP -v && coverage report -m

test-ci:
	docker compose exec backend coverage run -m pytest -rP -v && coverage report -m

build-ci:
	docker compose build --parallel && docker compose up -d && docker compose exec backend python manage.py makemigrations && docker compose exec backend python manage.py migrate
