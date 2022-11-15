lint:
	poetry run flake8 page_loader
	poetry run flake8 tests

test:
	poetry run pytest tests/tests.py