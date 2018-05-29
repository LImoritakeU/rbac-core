SHELL=/bin/bash
TEST_PATH=./tests

.PHONY: auto install test clean static

auto: build36 install

build27:
	virtualenv venv --python=python2.7

build36:
	virtualenv venv --python=python3.6

install:
	venv/bin/pip install -r requirements.txt

clean-pyc:
	find . | grep -E "(*~|__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean-test:
	rm -rf reports/
	rm -rf .pytest_cache/

test: clean-pyc
	. venv/bin/activate && python -m pytest "$(TEST_PATH)"

clean: clean-pyc clean-build clean-test
	rm -rf venv
	rm -rf .ipynb_checkpoints

static:
	mkdir /tmp/www
	cp -r static/ /tmp/www

create_db:
	psql -h ${PGHOST} -p ${PGPORT} -d ${PGDATABASE} -U ${PGUSER}  -w ${PGPASSWORD} -f ./sql/rbac_core_pg.sql

