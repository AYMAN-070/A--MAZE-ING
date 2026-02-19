import sys
from typing import Dict, Any
from typing import List, Tuple
from mazegen.generator import MazeGenerator
from terminal_default_rendering import run_viewer


def parse_config(file_path: str) -> Dict[str, Any]:
    """Lit le fichier de configuration et retourne un dictionnaire"""
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
                    print("Attention: format invalid", line)
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
    """Valide les données brutes et les convertit en types Python utilisables.
    """
    valid_config = {}
    try:
        valid_config['width'] = int(raw_config.get('WIDTH', ''))
        valid_config['height'] = int(raw_config.get('HEIGHT', ''))
        if valid_config['width'] < 5 or valid_config['height'] < 5:
            print("Error: The size of the maze must be at least 5x5.")
            sys.exit(1)
    except ValueError:
        print("Error: WIDTH or HEIGHT should be integers")
        sys.exit(1)
    for key in ['ENTRY', 'EXIT']:
        try:
            raw_val = raw_config.get(key, '')
            if not raw_val:
                raise ValueError("Missing value")
            parts = raw_val.split(',')
            if len(parts) != 2:
                raise ValueError("Format incorrect")
            x, y = int(parts[0]), int(parts[1])
            if not (0 <= x < valid_config['width']
               or not 0 <= y < valid_config['height']):
                print(f"Error : {key}({x},{y}) out of the maze size")
                sys.exit(1)
            valid_config[key.lower()] = (x, y)
        except ValueError:
            print(f"Error : {key} should be in 'x,y' format with integers "
                  "(ex: 0,0).")
    if valid_config['entry'] == valid_config['exit']:
        print("Error : Entry and Exit can't be in the same place")
        sys.exit(1)
    valid_config['output_file'] = raw_config.get('OUTPUT_FILE', 'maze.txt')
    if valid_config['width'] < 10 or valid_config['height'] < 10:
        print("Warning : Maze too small for 42 pattern")
    valid_config['perfect'] = raw_config.get('PERFECT', False)
    return valid_config


def maze_hexa(grid: List[List[int]], solution: str, start: Tuple[int, int],
              end: Tuple[int, int], filename: str):
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


def generate_maze(file_config):
    raw_config = parse_config(file_config)
    config = validate_and_convert(raw_config)
    gen = MazeGenerator(config['height'], config['width'], config['perfect'])
    grid = gen.generate()
    start = config['entry']
    end = config['exit']
    path = gen.solve(start[0], start[1], end[0], end[1])
    if not path:
        print("Solution not found !")
    maze_hexa(grid, path, start, end, config['output_file'])
    run_viewer(config['output_file'])


def print_menu():
    from a_maze_ing import generate_maze
    while True:
        print("=== A-Maze-ing ===")
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
            print("You must choose an option between 1 and 4)")
            print("===========================================")
            continue
        if choice == 1:
            generate_maze(sys.argv[1])
        elif choice == 2:
            print("show path")
        elif choice == 3:
            print("rotate colors")
        elif choice == 4:
            break


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)
    generate_maze(sys.argv[1])
    print_menu()


if __name__ == "__main__":
    main()
