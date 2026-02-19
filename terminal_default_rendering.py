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


def main():
    try:
        with open("output_maze.txt", 'r') as output_maze:
            content = output_maze.read()
    except FileNotFoundError:
        raise FileNotFoundError('"output_maze.txt" not found')
    except PermissionError:
        print('Attempting access to "output_maze.txt"...')
        raise PermissionError("Security protocols deny access")
    except Exception as e:
        print('Attempting access to "output_maze.txt"...')
        raise Exception(f"Unexpected system anomaly - {e}")

    maze_infos = content.split("\n\n")
    maze_representation = maze_infos[0]
    maze_lines = maze_representation.split("\n")

    path_infos = maze_infos[1].split("\n")
    entry = tuple(path_infos[0].split(","))
    print(entry)
    exit = tuple(path_infos[1].split(","))
    print(exit)
    path = path_infos[2]
    print(path)
    maze = Maze_grid(maze_lines, entry, exit, path)
    maze.add_cells_in_grid()
    maze.print_maze()


if __name__ == "__main__":
    main()
