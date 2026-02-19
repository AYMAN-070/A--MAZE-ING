PYTHON = python3
MAIN_FILE = a_maze_ing.py
CONFIG_FILE = config.txt

MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
all: run
install:
		pip install -r requirements.txt
run:
		$(PYTHON) $(MAIN_FILE) $(CONFIG_FILE)
debug:
		$(PYTHON) -m pdp $(MAIN_FILE) $(CONFIG_FILE)
clean:
		rm -rf __pycache__
		rm -rf .mypy_cache
		rm -rf *.pyc
lint:
		@echo "--- Running Flake8---"
		flake8 $(MAIN_FILE)
		@echo "--- Running Mypy"
		mypy $(MYPY_FLAGS) $(MAIN_FILE)

.PHONY: install run debug clean lint
