class Cell():
    def __init__(self, values: list[int], x: int, y: int):
        self.west, self.south, self.east, self.north = values
        self.x: int = int(x)
        self.y: int = int(y)
        corner_NW = self.set_corner(self.north, self.west)

        self.cell_proprities = [
            [corner_NW, self.north],
            [self.west, 0],
            ]

    def set_corner(self, value1: int, value2: int) -> int:

        if value1 | value2 == 1:
            return 1
        return 0

    def __repr__(self):
        return "C"
