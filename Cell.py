class Cell():
    """
    Create an instance of Cell, able to store all the information of it,
    like if it is the start or the end of the maze, or if the path pass
    into the cell.
    The Cell will be represented in a size of 3x3 in the maze, but only the
    North-West corner, the North, the West and the center are stored, because
    the rest of the Cell will be completed with the adjacent cells, to avoid
    duplicates with the commun walls.
    """
    def __init__(self, values: list[int], x: int, y: int,
                 entry: tuple[int, int], exit: tuple[int, int]):
        self.west, self.south, self.east, self.north = values
        self.x: int = int(x)
        self.y: int = int(y)
        corner_NW = self.set_corner_NW(self.north, self.west)
        center = 0

        if (self.x, self.y) == (int(entry[0]), int(entry[1])):
            center = 2
        elif (self.x, self.y) == (int(exit[0]), int(exit[1])):
            center = 3
        self.cell_proprities = [
            [corner_NW, self.north],
            [self.west, center],
        ]

    def set_corner_NW(self, north_value: int, west_value: int) -> int:
        """Set the North West corner, depending if the North wall
        or the West Wall exist"""
        if north_value | west_value == 1:
            return 1
        return 0

    def set_center(self, entry: tuple[int, int], exit: tuple[int, int]) -> int:
        """Set the center of the Cell to 2 if it is the entry, to 3 if
        it is the exit, and to 0 if there is nothing"""
        x_entry, y_entry = entry
        x_exit, y_exit = exit

        if self.x == int(x_entry) and self.y == int(y_entry):
            return 2
        elif self.x == int(x_exit) and self.y == int(y_exit):
            return 3
        return 0

    def put_path(self, direction: tuple[int, int]):
        """Modifie the cell_proprities to add the path, the path is set to 4"""
        if self.cell_proprities[direction[0]][direction[1]] not in [2, 3]:
            self.cell_proprities[direction[0]][direction[1]] = 4
