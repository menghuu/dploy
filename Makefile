default: lint-errors-only test

.PHONY: all
all: clean lint test

.PHONY: clean
clean:
	git clean -x -d --force

.PHONY: lint
lint:
	pylint dploy setup.py tests/*

.PHONY: lint-errors-only
lint-errors-only:
	pylint --errors-only dploy setup.py tests/*

.PHONY: test
test:
	py.test

.PHONY: install-requirements
install-requirements:
	python3 -m pip install -r requirments.txt
