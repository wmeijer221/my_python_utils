
build:
	python setup.py sdist

build_reqs:
	pip-compile pyproject.toml

