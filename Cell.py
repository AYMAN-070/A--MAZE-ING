class Cell():
    def __init__(self, values: list[int], x: int, y: int, entry: tuple,
                 exit: tuple):
        self.west, self.south, self.east, self.north = values
        self.x: int = int(x)
        self.y: int = int(y)
        corner_NW = self.set_corner(self.north, self.west)
        centre = 0

        if (self.x, self.y) == (int(entry[0]), int(entry[1])):
            centre = 2
        elif (self.x, self.y) == (int(exit[0]), int(exit[1])):
            centre = 3
        self.cell_proprities = [
            [corner_NW, self.north],
            [self.west, centre],  # 3. On remplace le 0 par la variable centre
        ]

    def set_corner(self, value1: int, value2: int) -> int:

        if value1 | value2 == 1:
            return 1
        return 0

    def set_center(self, entry: int, exit: int) -> int:
        x_entry, y_entry = entry
        x_exit, y_exit = exit

        if self.x == int(x_entry) and self.y == int(y_entry):
            return 2
        elif self.x == int(x_exit) and self.y == int(y_exit):
            return 3
        return 0

    def put_path(self, direction: tuple[int, int]):
        if self.cell_proprities[direction[0]][direction[1]] not in [2, 3]:
            self.cell_proprities[direction[0]][direction[1]] = 4
