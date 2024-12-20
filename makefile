# Makefile

# Run makemigrations in the backend container
makemigrations:
	docker-compose exec backend python manage.py makemigrations

# Start the Django development server
startserver:
	docker-compose up

migrate:
	docker-compose exec backend python manage.py migrate