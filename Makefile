.PHONY: check duplicate delete debug help

# check a path to the master data file is set
check:
	PYTHONPATH=$(shell pwd) python -m utils.file_manager --check

# duplicate the master data file to a local sub-directory
duplicate:
	PYTHONPATH=$(shell pwd) python -m utils.file_manager --duplicate

# delete the local data repository
delete:
	PYTHONPATH=$(shell pwd) python -m utils.file_manager --delete

# debug the Python path to ensure PYTHONPATH is set correctly
debug:
	@echo "========================="
	@echo "Makefile PWD: $(shell pwd)"
	@echo "========================="
	PYTHONPATH=$(shell pwd) python -c "import sys; from pprint import pprint; print('\nPython sys.path:\n================='); pprint(sys.path)"

# print available commands
help:
	@echo "Available commands:"
	@echo "  make check      - Check if the master data file exists"
	@echo "  make duplicate  - Duplicate the master data file locally"
	@echo "  make delete     - Delete the local data repository"
	@echo "  make debug      - Debug the Python path to ensure PYTHONPATH is set correctly"