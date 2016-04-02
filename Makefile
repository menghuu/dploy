test:
	py.test

lint:
	pylint dploy setup.py tests/*
