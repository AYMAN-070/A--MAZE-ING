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
		$(PYTHON) -m pdb $(MAIN_FILE) $(CONFIG_FILE)
clean:
		find . -type d -name "__pycache__" -exec rm -rf {} +
		rm -rf .mypy_cache
		rm -rf *.pyc
lint:
		@echo "--- Running Flake8---"
		python3 -m flake8 .
		@echo "--- Running Mypy---"
		python3 -m mypy $(MYPY_FLAGS) .

.PHONY: install run debug clean lint
