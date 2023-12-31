Point = tuple[int, int]


class Grid:
    def __init__(self, grid: list[list[str | int]]):
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.size = (self.width, self.height)

    @staticmethod
    def read(input_text: str) -> "Grid":
        lines = input_text.splitlines()
        rows = [list(line) for line in lines]
        return Grid(rows)

    def __contains__(self, item):
        if type(item) != tuple or len(item) != 2:
            return False
        x, y = item
        if type(x) != int or type(y) != int:
            return False

        if (not 0 <= x < self.width) or \
                (not 0 <= y < self.height):
            return False

        return True

    def __getitem__(self, key):
        if key not in self:
            raise IndexError(f"coords {key} not in {repr(self)}")
        return self.grid[key[1]][key[0]]

    def __setitem__(self, key, value):
        if key not in self:
            raise IndexError(f"coords {key} not in {repr(self)}")
        self.grid[key[1]][key[0]] = value

    def __iter__(self):
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y), self[x, y]

    def neighbours_8(self, key, skip_self=True):
        if key not in self:
            raise IndexError(f"coords {key} not in {repr(self)}")
        for y in range(key[1] - 1, key[1] + 2):
            for x in range(key[0] - 1, key[0] + 2):
                if (x, y) in self and not (skip_self and (x, y) == key):
                    yield (x, y), self[x, y]

    def neighbours_4(self, key: Point):
        if key not in self:
            raise IndexError(f"coords {key} not in {repr(self)}")
        for x, y in neighbours_4(key):
            if (x, y) in self:
                yield (x, y), self[x, y]

    def __str__(self):
        return "\n".join("".join(row) for row in self.grid)

    def __repr__(self):
        return f"<Grid {self.width}x{self.height}>"

    def find(self, find_value):
        found = []
        for (x, y), grid_value in self:
            if grid_value == find_value:
                found.append((x, y))
        return found


def neighbours_4(start: Point):
    for x, y in [(start[0], start[1] - 1),
                 (start[0] + 1, start[1]),
                 (start[0], start[1] + 1),
                 (start[0] - 1, start[1])]:
        yield x, y

# with open(f"grid_test.txt", "r") as file:
#     grid = Grid.read(file.read())
#     print(repr(grid))
#     print(grid[2, 3])
