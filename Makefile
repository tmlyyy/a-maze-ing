.PHONY: install run debug clean lint lint-strict

PYTHON := $(shell python3 -c 'import sys; print(sys.executable)')
USER_BIN := $(shell $(PYTHON) -m site --user-base)/bin
export PATH := $(PATH):$(USER_BIN)

install:
	$(PYTHON) -m pip install . flake8 mypy

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	find . -type d -name __pycache__ -prune -exec rm -r {} +
	find . -type d -name .mypy_cache -prune -exec rm -r {} +
	find . -type d -name .pytest_cache -prune -exec rm -r {} +

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict
