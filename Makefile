PACKAGE_NAME?=vidispine

flake8:
	flake8 $(PACKAGE_NAME) tests


test:
	pytest tests


coverage:
	pytest --cov=vidispine/ --cov-fail-under=100 tests
