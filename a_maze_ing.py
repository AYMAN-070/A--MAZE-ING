import sys
from typing import Dict, Any
from typing import List, Tuple
from mazegen.generator import MazeGenerator
from terminal_rendering import run_viewer
import os
import random

COLORS_DATA = {
    "blue": "\033[34m██\033[0m",
    "white": "\033[97m██\033[0m",
    "grey": "\033[90m██\033[0m",
    "green": "\033[32m██\033[0m",
    "yellow": "\033[33m██\033[0m",
    "cyan": "\033[36m██\033[0m",
    "light_green": "\033[92m██\033[0m",
    "light_yellow": "\033[93m██\033[0m",
    "light_blue": "\033[94m██\033[0m",
    "light_cyan": "\033[96m██\033[0m",
}


def get_random_colors() -> List[str]:
    """Return a list of 3 uniques colors selected randomly"""
    colors_values = list(COLORS_DATA.values())
    selection = random.sample(colors_values, 3)
    return [
        selection[0],
        selection[1],
        selection[2],
    ]


WALL, EMPTY, PATH = get_random_colors()
START = "\033[95m██\033[0m"
END = "\033[91m██\033[0m"
PATERN = "\033[38;5;90m██\033[0m"


def parse_config(file_path: str) -> Dict[str, Any]:
    """Read the configuration file and retourn a dictionnary"""
    config: Dict[str, Any] = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
                else:
                    print("Error: invalid format", line)
    except FileNotFoundError:
        print(f"Error: file {file_path} not found")
        sys.exit(1)
    except PermissionError:
        print(f"Error : Permission denied to read {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error while reading: {e}")
        sys.exit(1)

    return config


def validate_and_convert(raw_config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate brut datas and convert them into python types useables"""
    valid_config: dict[str, Any] = {}
    required_keys = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE',
                     'PERFECT']
    for key in required_keys:
        if key not in raw_config:
            raise ValueError(f"Missing mandatory key '{key}'")
    try:
        valid_config['width'] = int(raw_config.get('WIDTH', ''))
        valid_config['height'] = int(raw_config.get('HEIGHT', ''))
        if valid_config['width'] < 5 or valid_config['height'] < 5:
            raise ValueError("The size of the maze must be at least 5x5.")
        if valid_config['width'] > 100 or valid_config['height'] > 100:
            raise ValueError("The size of the maze must not exceed 100 x 100.")
    except ValueError as e:
        if "size" in str(e):
            raise
        raise ValueError("WIDTH or HEIGHT should be integers")
    for key in ['ENTRY', 'EXIT']:
        try:
            raw_val = raw_config[key].strip()
            if not raw_val:
                raise ValueError
            parts = raw_val.split(',')
            if len(parts) != 2:
                raise ValueError
            x, y = int(parts[0]), int(parts[1])
            if not (0 <= x < valid_config['width'] and
                    0 <= y < valid_config['height']):
                raise ValueError(f"{key}({x},{y}) out of the maze size")
            valid_config[key.lower()] = (x, y)
        except (ValueError, AttributeError) as e:
            if str(e):
                raise e
            raise ValueError(f"{key} should be in 'x,y' format with integers "
                  "(ex: 0,0).")
    if valid_config['entry'] == valid_config['exit']:
        raise ValueError("Error : Entry and Exit can't be in the same place")
    valid_config['output_file'] = raw_config.get('OUTPUT_FILE')
    if valid_config['output_file'] == "":
        raise ValueError("Error : OUTPUT_FILE cannot be empty")
    try:
        with open(str(valid_config['output_file']), 'a'):
            pass
    except PermissionError:
        raise ValueError("Permission denied: Cannot write to output_file")
    for key in ["PERFECT", "ANIMATE"]:
        if key not in raw_config and key == "ANIMATE":
            valid_config['animate'] = False
            continue
        if raw_config[key] == "True":
            valid_config[key.lower()] = True
        elif raw_config[key] == "False":
            valid_config[key.lower()] = False
        else:
            raise ValueError(f"Invalid boolean value for {key}, "
                             "expected True or False")
    if 'SEED' in raw_config:
        seed = raw_config.get('SEED')
        if not seed:
            raise ValueError("The SEED value is empty in the"
                  "configuration file.")
        valid_config['seed'] = seed
    else:
        valid_config['seed'] = None
    return valid_config


def maze_hexa(grid: List[List[int]], solution: str, start: Tuple[int, int],
              end: Tuple[int, int], filename: str) -> None:
    """
    Writes the generated maze using one hexadecimal digit per cell to represent
    its walls and its solution to the specified output file."""
    try:
        with open(filename, 'w') as f:
            for row in grid:
                hex_line = "".join([f"{cell:X}" for cell in row])
                f.write(hex_line + '\n')
            f.write("\n")
            f.write(f"{start[0]},{start[1]}\n")
            f.write(f"{end[0]},{end[1]}\n")
            f.write(f"{solution}\n")
        print(f"File {filename} generated with success !")
    except Exception as e:
        print("Error :", e)


def generate_maze(file_config: str) -> None:
    """Parse the config, define the MazeGenerator, generate a
    maze randomly with the configuration given, then display it"""
    raw_config = parse_config(file_config)
    config = validate_and_convert(raw_config)
    if 'seed' in config and config['seed'] is not None:
        random.seed((config['seed']))
    else:
        random.seed()
    gen = MazeGenerator(config['height'], config['width'], config['perfect'])
    current_colors = [WALL, EMPTY, PATH, START, END, PATERN]
    grid = gen.generate(current_colors, config['animate'])
    start = config['entry']
    end = config['exit']
    path = gen.solve(start[0], start[1], end[0], end[1])
    if not path:
        print("Solution not found !")
    maze_hexa(grid, path, start, end, config['output_file'])
    os.system('clear' if os.name == 'posix' else 'cls')
    run_viewer(config, gen.patern, [WALL, EMPTY, PATH, START, END, PATERN])
    print_menu(config, gen.patern)


def print_menu(config: Dict[str, Any], patern: set) -> None:
    """Display the menu and propose differents choices to the user"""
    global WALL, EMPTY, PATH
    with_path = False
    while True:
        print("₪₪₪₪₪₪₪₪₪₪ A-Maze-ing ₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪")
        print("1. Re-generate a new maze")
        print("2. Show/Hide path from entry to exit")
        print("3. Rotate maze colors")
        print("4. Quit")
        print("Choice? (1-4):")
        try:
            choice = int(input())
            if choice not in [1, 2, 3, 4]:
                raise (ValueError)
        except (ValueError, Exception):
            os.system('clear' if os.name == 'posix' else 'cls')
            print("You must choose an option between 1 and 4)")
            print("₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪₪")
            continue
        if choice == 1:
            with_path = False
            generate_maze(sys.argv[1])
        elif choice == 2:
            if with_path is False:
                with_path = True
            else:
                with_path = False
            os.system('clear' if os.name == 'posix' else 'cls')
            run_viewer(config, patern,
                       [WALL, EMPTY, PATH, START, END, PATERN], with_path)
        elif choice == 3:
            WALL, EMPTY, PATH = get_random_colors()
            os.system('clear' if os.name == 'posix' else 'cls')
            run_viewer(config, patern,
                       [WALL, EMPTY, PATH, START, END, PATERN], with_path)
        elif choice == 4:
            print("\nThank you for using our maze generator! ₪₪")
            sys.exit(0)


def main() -> None:
    if len(sys.argv) != 2:
        print("Error : too many arguments provided")
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    try:
        generate_maze(sys.argv[1])
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
