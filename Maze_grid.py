from Cell import Cell
from typing import List


class Maze_grid():
    """
    Create an instance of Maze, able to store a grid representation with
    every Cells, the start, the end, the width and the height and the path.
    A methode is available to print the maze_grid.
    """
    def __init__(self, brut_lines: List[str],
                 entry: tuple[int, int], exit: tuple[int, int], path: str):
        self.grid: List[list[Cell]] = []
        self.brut_lines: List[str] = brut_lines
        self.entry: tuple[int, int] = entry
        self.exit: tuple[int, int] = exit
        self.path = path
        self.width_print: int = 2 * len(brut_lines[0]) + 1
        self.width = len(brut_lines[0]) - 1
        self.height = len(brut_lines) - 1
        self.current_path: tuple[int, int] = entry

    def set_grid(self):
        """
        Convert all cells to Cells instances and add thems in grid with theres
        properties. Check the cells around to adapt the commun walls.
        Add the path in the concerning cells.
        """
        from terminal_rendering import decode_cell
        y = 0
        if self.brut_lines:
            for line in self.brut_lines:
                line_convert: List[Cell] = []
                x = 0
                for cell in line:
                    cell = Cell(decode_cell(cell), x, y, self.entry, self.exit)
                    line_convert.append(cell)
                    x += 1
                self.grid.append(line_convert)
                y += 1

            for y in range(0, len(self.brut_lines)):
                for x in range(0, len(self.brut_lines[0])):
                    self.check_cells_around(x, y)
        else:
            print("No path founded")
        self.add_path()

    def print_maze(self, with_path: bool, colors: list[str]):
        """Print the cells with a boucle of two steps :
        first step print the North of the cells line,
        second step print the middle """
        WALL, EMPTY, PATH, START, END = colors
        x = 0
        for line in self.grid:
            for i in range(2):
                y = 0
                for cell in line:
                    values = cell.cell_proprities[i]
                    for value in values:
                        if value == 0:
                            print(EMPTY, end='')
                        if value == 1:
                            print(WALL, end='')
                        elif value == 2:
                            print(START, end='')
                        elif value == 3:
                            print(END, end='')
                        elif value == 4:
                            if with_path:
                                print(PATH, end='')
                            else:
                                print(EMPTY, end='')
                    y += 1
                print(WALL)
            x += 1
        for _ in range(self.width_print):
            print(WALL, end='')
        print("\n")

    def add_path(self):
        """Read the path generated and add it in the concerning
        cells depending the given direction"""
        for carac in self.path:
            x_current, y_current = self.current_path
            try:
                if carac == 'S':
                    self.grid[y_current + 1][x_current].put_path((0, 1))
                    self.grid[y_current + 1][x_current].put_path((1, 1))
                    self.current_path = (x_current, y_current + 1)
                elif carac == 'E':
                    self.grid[y_current][x_current + 1].put_path((1, 0))
                    self.grid[y_current][x_current + 1].put_path((1, 1))
                    self.current_path = (x_current + 1, y_current)
                elif carac == 'W':
                    self.grid[y_current][x_current].put_path((1, 0))
                    self.grid[y_current][x_current - 1].put_path((1, 1))
                    self.current_path = (x_current - 1, y_current)
                elif carac == 'N':
                    self.grid[y_current][x_current].put_path((0, 1))
                    self.grid[y_current - 1][x_current].put_path((1, 1))
                    self.current_path = (x_current, y_current - 1)
            except IndexError:
                raise IndexError("Index value out of grid")

    def check_cells_around(self, x: int, y: int) -> None:
        """Change the North-WEST corner in comparison with the
        three cells around, whose corner is shared with the cell checked"""
        if x > 0 and y > 0:
            if (
                self.grid[y][x - 1].west == 1 or
                self.grid[y - 1][x].north == 1 or
                self.grid[y - 1][x - 1].east == 1
            ):
                self.grid[y][x].cell_proprities[0][0] = 1
