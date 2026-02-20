from Cell import Cell

WALL = "\033[90m██\033[0m"  # Gris foncé
WALL_EAST = "\033[90m█\033[0m"  # Gris foncé
PATH = "\033[97m██\033[0m"  # Blanc
START = "\033[95m██\033[0m"  # Violet
END = "\033[91m██\033[0m"   # Rouge


class Maze_grid():
    def __init__(self, brut_lines: list, entry: tuple, exit: tuple, path: str):
        self.grid = []
        self.brut_lines: list = brut_lines
        self.entry = entry
        self.exit = exit
        self.path = path
        self.width_print = 2 * len(brut_lines[0]) + 1
        self.width = len(brut_lines[0]) - 1
        self.height = len(brut_lines) - 1

    def add_cells_in_grid(self):
        from terminal_default_rendering import decode_cell
        """ Convert all cells to Cells instances and
        add thems in grid with theres properties"""
        y = 0
        for line in self.brut_lines:

            line_convert = []
            x = 0
            for cell in line:
                cell = Cell(decode_cell(cell), x, y, self.entry, self.exit)
                line_convert.append(cell)
                x += 1
            self.grid.append(line_convert)
            y += 1

    def print_maze(self):
        """Print the cells with a boucle of two steps :
        first step print the North of the cells line,
        second step print the middle """
        # for line in self.grid:
        #     for cell in line:
        #         print(cell.cell_proprities)
        x = 0
        for line in self.grid:
            for i in range(2):
                y = 0
                for cell in line:
                    values = cell.cell_proprities[i]
                    if i == 0:
                        self.check_cells_around(x, y)
                    for value in values:
                        if value == 1:
                            print(WALL, end='')
                        elif value == 2:
                            print(START, end='')
                        elif value == 3:
                            print(END, end='')
                        else:
                            print(PATH, end='')
                    y += 1
                print(WALL)
            x += 1
        for _ in range(self.width_print):
            print(WALL, end='')
        print("\n")

    def check_cells_around(self, x: int, y: int) -> None:
        """Modifie the North-WEST corner in comparison
        with the three cells around"""
        if x > 0 and y > 0:
            if (
                self.grid[x - 1][y].west == 1 or
                self.grid[x][y - 1].north == 1 or
                self.grid[x - 1][y - 1].east == 1
            ):
                self.grid[x][y].cell_proprities[0][0] = 1