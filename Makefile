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
	@python -m compileall ${src_dir} >> ${compile_log_file} 2>> ${compile_log_file}

unit: compile
	@echo "Running unit tests..."
	nosetests -d -s --verbose --with-coverage --cover-package=spellmatcher ${unit_tests_dir}
	
func: compile
	@echo "Running unit tests..."
	nosetests -d -s --verbose --with-coverage --cover-package=spellmatcher ${functional_tests_dir}
	
run:
	@PYTHONPATH=$$PYTHONPATH:${root_dir} python ${src_dir}/infra/server.py
	
