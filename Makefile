.PHONY: clean-pyc clean-build docs clean
##

help: # show help
	@echo ""
	@grep "^##" $(MAKEFILE_LIST) | grep -v grep
	@echo ""
	@grep "^[0-9a-zA-Z\-]*:.* #" $(MAKEFILE_LIST) | grep -v grep
	@echo ""

setup: # setup
	virtualenv env
	source env/bin/activate && pip install -r requirements.txt

clean: clean-build clean-pyc clean-test # clean - remove all build, test, coverage and Python artifacts

clean-build: # clean-build - remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: # clean-pyc - remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: # clean-test - remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: # lint - check style with flake8
	flake8 general_log_parser tests

test: # test - run tests quickly with the default Python
	python setup.py test

test-all: # test-all - run tests on every Python version with tox
	tox

macrotest : # macrotest
	python general_log_parser/parser.py -l a.{}.log --from 20150505 --to 20150506 -i tests # read from log
	cat tests/a.20150505.log | python general_log_parser/parser.py # read from input

coverage: # coverage - check code coverage quickly with the default Python
	coverage run --source general_log_parser setup.py test
	coverage report -m
	coverage html
	open htmlcov/index.html

docs: # docs - generate Sphinx HTML documentation, including API docs
	rm -f docs/general_log_parser.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ general_log_parser
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	open docs/_build/html/index.html

release: clean # release - package and upload a release
	python setup.py sdist upload
	python setup.py bdist_wheel upload

dist: clean # dist - package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean # install - install the package to the active Python's site-packages
	python setup.py install
