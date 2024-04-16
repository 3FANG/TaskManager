build:
	./build.sh

start:
	poetry run python -m gunicorn -w 5  task_manager.wsgi

test:
	poetry run coverage run manage.py test

test-coverage: test
	poetry run coverage xml