from Maze_grid import Maze_grid
from parse_output import read_output, parse_output
from typing import List, Dict, Any


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
    """Initialize a Maze_grid, decode the maze
    representation in a list of line of Cells, get the entry and the exit,
    and then print the maze"""
    content = read_output(config['output_file'])
    viewer_config: Dict[str, Any] = parse_output(content, config)

    maze = Maze_grid(
        viewer_config['maze_lines'],
        viewer_config['entry'],
        viewer_config['exit'],
        viewer_config['path']
        )

    maze.set_grid()
    maze.print_maze(with_path, colors)
