test:
	py.test

lint:
	pylint dploy setup.py tests/*

clean:
	git clean -x -d --force
