from Cell import Cell


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
        self.current_path = entry

    def set_grid(self):
        from terminal_rendering import decode_cell
        """ Convert all cells to Cells instances and
        add thems in grid with theres properties
        Check the cells around to adapt the commun walls
        Add the path in the concerning cells """
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

        for y in range(0, len(self.brut_lines)):
            for x in range(0, len(line)):
                self.check_cells_around(x, y)
        self.add_path()

    def print_maze(self, with_path: bool, colors: tuple[str]):
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
        """Modifie the North-WEST corner in comparison
        with the three cells around"""
        if x > 0 and y > 0:
            if (
                self.grid[y][x - 1].west == 1 or
                self.grid[y - 1][x].north == 1 or
                self.grid[y - 1][x - 1].east == 1
            ):
                self.grid[y][x].cell_proprities[0][0] = 1
