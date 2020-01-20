pip=env/bin/python -m pip
python=env/bin/python3
sequentia=env/bin/sequentia

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
	$(pip) install dist/sequentia*.whl

test: install
	cd tests && ../$(python) test.py

.PHONY: all configure test lint build install


