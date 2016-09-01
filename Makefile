default: test lint

# use a platform in depended path separator
ifdef ComSpec
    PATHSEP2=\\
else
    PATHSEP2=/
endif
PATHSEP=$(strip $(PATHSEP2))

.PHONY: setup
setup: setup-requirements

.PHONY: clean
clean:
	git clean -x -d --force

.PHONY: lint
lint:
	python3 -m pylint --output-format=parseable dploy setup.py tests$(PATHSEP)*.py

.PHONY: test
test:
	py.test -v

.PHONY: setup-requirements
setup-requirements:
	pip install -r requirements.txt

.PHONY: build
build: clean
	pyinstaller -n dploy --onefile dploy$(PATHSEP)__main__.py
