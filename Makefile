# Makefile for spellmatcher
SHELL := /bin/bash

# Internal variables.
root_dir=.
src_dir=${root_dir}/spellmatcher

tests_dir=${root_dir}/tests
unit_tests_dir=${tests_dir}/unit
functional_tests_dir=${tests_dir}/functional

# orchestrator targets

prepare_build: clean

test: unit func acceptance

all: prepare_build compile test report_success

run_unit: prepare_build compile unit report_success
run_functional: prepare_build compile func report_success

clean:
	@find . -name '*.pyc' -delete

# action targets

report_success:
	@echo "Build succeeded!"

compile: clean
	@echo "Compiling source code..."
	@python -m compileall ${src_dir}

unit: compile
	@echo "Running unit tests..."
	nosetests -d -s --verbose --with-coverage --cover-package=spellmatcher ${unit_tests_dir}

func: compile
	@echo "Running unit tests..."
	nosetests -d -s --verbose --with-coverage --cover-package=spellmatcher ${functional_tests_dir}

acceptance: compile
	@echo "Running unit tests..."
	pyccuracy_console -l pt-br -u 'http://localhost:4000' -d '/tests/acceptance'

createdb:
	@db-migrate -c ./spellmatcher/db/simple-db-migrate.conf --drop --color

upgradedb:
	@db-migrate -c ./spellmatcher/db/simple-db-migrate.conf --color

run:
	@PYTHONPATH=$$PYTHONPATH:${root_dir} python ${src_dir}/infra/server.py

