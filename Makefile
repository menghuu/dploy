default: all

.PHONY: all
all: lint test

.PHONY: clean
clean:
	git clean -x -d --force

.PHONY: lint
lint:
	pylint dploy setup.py tests/*

.PHONY: test
test: clean
	py.test
