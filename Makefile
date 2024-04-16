test:
	poetry run coverage run manage.py test

test-coverage: test
	poetry run coverage xml