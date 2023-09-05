PROJECT_NAME = $(shell pwd | rev | cut -f1 -d'/' - | rev)

runserver:
	poetry run python quizhero-app/manage.py runserver

lint:
	poetry run pre-commit run --all-files

run-gunicorn:
	gunicorn -c gunicorn_config.py quizhero_api.wsgi:application

test:
	poetry run pytest -sx $(PROJECT_NAME) --reuse-db --create-db
