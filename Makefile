PROJECT_NAME = $(shell pwd | rev | cut -f1 -d'/' - | rev)

runserver:
	poetry run python quizhero-app/manage.py runserver

migrate:
	poetry run python quizhero-app/manage.py migrate

makemigrations:
	poetry run python quizhero-app/manage.py makemigrations

lint:
	poetry run pre-commit run --all-files

run-gunicorn:
	gunicorn -c gunicorn_config.py quizhero_api.wsgi:application

test:
	poetry run pytest -sx $(PROJECT_NAME) --reuse-db --create-db

collect-static:
	poetry run python quizhero-app/manage.py collectstatic

createsuperuser:
	poetry run python quizhero-app/manage.py createsuperuser

seed:
	poetry run python quizhero-app/manage.py seed

clean-seed:
	poetry run python quizhero-app/manage.py seed --clean

# SSH
generate-key:
	ssh-keygen -t rsa -b 2048 -f quizhero-key-pair.pem


change-permission:
	chmod 400 ./iac/quizhero-key-pair.pem

ssh:
	ssh -i ./iac/quizhero-key-pair.pem ec2-user@----ip------

# DOCKER
run-container:
	docker run -p 8000:8000 quizhero-app