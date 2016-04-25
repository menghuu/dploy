default: lint test

.PHONY: clean
clean:
	git clean -x -d --force

.PHONY: lint
lint:
	pylint --files-output=n --reports=n dploy setup.py tests/*.py

.PHONY: lint-full
lint-full:
	pylint dploy setup.py tests/*.py

.PHONY: test
test:
	py.test -v

.PHONY: install-requirements
install-requirements:
	python3 -m pip install -r requirments.txt
