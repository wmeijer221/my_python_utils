test_all: tests build local_install
publish: build test_push push

build:
	rm -r -f ./dist/*
	python -m build
	twine check ./dist/*

test_push:
	twine upload -r testpypi ./dist/*

push:
	twine upload ./dist/*

local_install:
	pip install -e .

build_reqs:
	pip-compile pyproject.toml

bump_major:
	bumpver update --major

bump_minor:
	bumpver update --minor

bump_patch:
	bumpver update --patch
	
tests:
	python -m unittest discover -v -p "test_*.py"
