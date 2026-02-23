from Maze_grid import Maze_grid
from typing import List, Dict, Any
import sys


def decode_cell(carac: str) -> List[int]:
    """Return a list with the four wall values
    unpackable with WEST, SOUTH, EAST, NORTH"""
    walls_proprieties: list[int] = [0, 0, 0, 0]
    try:
        cell = int(carac, 16)
        for i in range(0, 4):
            if cell & 1 == 1:
                walls_proprieties[3 - i] = 1
            cell = cell >> 1
        return walls_proprieties
    except ValueError as e:
        raise (e)


def run_viewer(config: Dict[str, Any],
               colors: list[str], with_path: bool = False) -> None:
    """Parse the output_maze.txt file. Initialize a Maze_grid, decode the maze
    representation in a list of line of Cells, get the entry and the exit,
    and then print the maze"""
    filename: str = config['output_file']
    try:
        with open(filename, 'r') as output_maze:
            content = output_maze.read()
    except FileNotFoundError:
        print(f'Error : {filename} not found')
        sys.exit(1)
    except PermissionError:
        print(f'Attempting access to {filename}')
        print("Error : Security protocols deny access")
        sys.exit(1)
    except Exception as e:
        print(f'Attempting access to {filename}...')
        print(f"Error : Unexpected system anomaly - {e}")
        sys.exit(1)

    maze_infos: List[str] = content.split("\n\n")
    if len(maze_infos) != 2:
        print(f"Error : file {filename} has an invalid format")
        sys.exit(1)
    maze_representation: str = maze_infos[0]
    maze_lines: List[str] = maze_representation.split("\n")
    if len(maze_lines) != config['height']:
        print("Error : maze output don't have the right number of lines")
        sys.exit(1)
    for line in maze_lines:
        if len(line) != config['width']:
            print("Error : maze output don't have the right number of column")
            sys.exit(1)

    path_infos: List[str] = maze_infos[1].split("\n")
    if len(path_infos) != 4:
        print(f"Error : file {filename} has an invalid format")
        sys.exit(1)
    parts_entry = path_infos[0].split(",")
    if len(parts_entry) != 2:
        print("Error : entry has an invalid format")
        sys.exit(1)
    try:
        entry: tuple[int, int] = (int(parts_entry[0]), int(parts_entry[1]))
    except ValueError:
        print("Error : entry has an invalid format")
        sys.exit(1)

    parts_exit = path_infos[1].split(",")
    if len(parts_exit) != 2:
        print("Error : exit has an invalid format")
        sys.exit(1)
    try:
        exit: tuple[int, int] = (int(parts_exit[0]), int(parts_exit[1]))
    except ValueError:
        print("Error : exit has an invalid format")
        sys.exit(1)

    path = path_infos[2]
    maze = Maze_grid(maze_lines, entry, exit, path)
    maze.set_grid()
    maze.print_maze(with_path, colors)
