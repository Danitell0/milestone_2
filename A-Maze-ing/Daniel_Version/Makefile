#COLORS
GREEN = \033[1;92m
RED = \033[1;91m
YELLOW = \033[1;93m
RESET = \033[0m

NAME = A-Maze-ing

install:
	@pip install mypy flake8
	@echo "mypy... ${GREEN}Installed${RESET}"
	@echo "flake8... ${GREEN}Installed${RESET}"

run:
	@echo "${YELLOW}Running main program${RESET}"
	@python3 a_maze_ing.py config.txt

debug:
	@echo "${YELLOW}Running main program with debugger${RESET}"
	@python3 -m pdb a_maze_ing.py config.txt

clean:
	@echo "Finding and removing extra files..."
	@find . -name "__pycache__" -exec rm -rf {} \;
	@find . -name ".mypy_cache" -exec rm -rf {} \;
	@echo "${GREEN}Success${RESET}"

lint:
	@flake8 .
	@echo "flake8... ${GREEN}Success${RESET}"
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "mypy... ${GREEN}Success${RESET}"

lint-strict:
	@flake8 .
	@echo "flake8... ${GREEN}Success${RESET}"
	@mypy . --strict
	@echo "mypy --strict... ${GREEN}Success${RESET}"