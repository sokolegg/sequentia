pip=env/bin/python -m pip
python=env/bin/python3
titanoboa=env/bin/projector

all: install

lint:
	@poetry check
	@flake8

configure:
	@poetry install

build: 
	@poetry build
	@rm -rf env
	@python -m venv env

install: build
	$(pip) install dist/titanoboa*.whl

test: install
	cd tests && ../$(python) test.py

.PHONY: all configure test lint build install


