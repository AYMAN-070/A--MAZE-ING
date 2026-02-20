from Maze_grid import Maze_grid


def decode_cell(carac: str) -> list:
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


def run_viewer(filename: str):
    try:
        with open(filename, 'r') as output_maze:
            content = output_maze.read()
    except FileNotFoundError:
        raise FileNotFoundError(f'{filename} not found')
    except PermissionError:
        print(f'Attempting access to {filename}')
        raise PermissionError("Security protocols deny access")
    except Exception as e:
        print(f'Attempting access to {filename}...')
        raise Exception(f"Unexpected system anomaly - {e}")

    maze_infos = content.split("\n\n")
    maze_representation = maze_infos[0]
    maze_lines = maze_representation.split("\n")

    path_infos = maze_infos[1].split("\n")
    entry = tuple(int(x) for x in path_infos[0].split(","))
    exit = tuple(int(x) for x in path_infos[1].split(","))
    path = path_infos[2]
    print(path)
    maze = Maze_grid(maze_lines, entry, exit, path)
    maze.set_grid()
    maze.print_maze(with_path=False)
