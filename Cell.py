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

    def __repr__(self):
        return "C"
