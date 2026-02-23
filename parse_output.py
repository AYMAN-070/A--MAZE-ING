import sys
from typing import List, Dict, Any


def read_output(filename: str) -> str:
    """Read the output file and retourn its content"""
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
    return content


def parse_output(content: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Parse the output file, handle every error cases and retourn a Dict with
    these informations : maze_lines, entry, exit and path"""
    viewer_config: Dict[str, Any] = {}

    maze_infos: List[str] = content.split("\n\n")
    if len(maze_infos) != 2:
        print(f"Error : file {config['output_file']} has an invalid format")
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
    viewer_config['maze_lines'] = maze_lines

    path_infos: List[str] = maze_infos[1].split("\n")
    if len(path_infos) != 4:
        print(f"Error : file {config['output_file']} has an invalid format")
        sys.exit(1)
    entry_position = path_infos[0].split(",")
    if len(entry_position) != 2:
        print("Error : entry has an invalid format")
        sys.exit(1)
    try:
        entry: tuple[int, int] = (int(entry_position[0]),
                                  int(entry_position[1]))
    except ValueError:
        print("Error : entry has an invalid format")
        sys.exit(1)
    viewer_config['entry'] = entry

    exit_position = path_infos[1].split(",")
    if len(exit_position) != 2:
        print("Error : exit has an invalid format")
        sys.exit(1)
    try:
        exit: tuple[int, int] = (int(exit_position[0]), int(exit_position[1]))
    except ValueError:
        print("Error : exit has an invalid format")
        sys.exit(1)
    viewer_config['exit'] = exit

    path = path_infos[2]
    viewer_config['path'] = path

    return viewer_config
