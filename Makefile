all: clean lint test

clean:
	git clean -x -d --force

lint:
	pylint dploy setup.py tests/*

test:
	py.test
