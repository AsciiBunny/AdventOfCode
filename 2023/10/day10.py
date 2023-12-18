import math


def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        return file.read().splitlines()


class Pipe:
    def __init__(self, a: tuple[int, int], b: tuple[int, int]):
        self.a = a
        self.b = b

    def enter(self, direction: tuple[int, int]):
        opposite = (direction[0] * -1, direction[1] * -1)
        if opposite == self.a:
            return self.b
        if opposite == self.b:
            return self.a
        assert False, direction

    def is_open(self, direction: tuple[int, int]):
        opposite = (direction[0] * -1, direction[1] * -1)
        return opposite == self.a or opposite == self.b


top = (0, -1)
bottom = (0, 1)
left = (-1, 0)
right = (1, 0)

pipe_parts = {
    "|": Pipe(top, bottom),
    "-": Pipe(left, right),
    "L": Pipe(top, right),
    "J": Pipe(top, left),
    "7": Pipe(bottom, left),
    "F": Pipe(bottom, right),
    ".": Pipe((0, 0), (0, 0))
}


def find_start(grid: list[str]):
    for y, row in enumerate(grid):
        for x, col in enumerate(row):
            if col == "S":
                return x, y


def find_start_direction(grid: list[str], start_coords: tuple[int, int]):
    for start_direction in [top, right, bottom, left]:
        new_coords = add(start_coords, start_direction)
        pipe = pipe_parts[grid[new_coords[1]][new_coords[0]]]
        if pipe.is_open(start_direction):
            return start_direction


def add(a: [int, int], b: [int, int]):
    return a[0] + b[0], a[1] + b[1]


def part_one(grid: list[str]):
    coords = find_start(grid)
    direction = find_start_direction(grid, coords)

    step_counter = 0
    while True:
        coords = add(coords, direction)
        next_part = grid[coords[1]][coords[0]]
        if next_part == "S":
            break
        pipe = pipe_parts[next_part]
        direction = pipe.enter(direction)
        step_counter += 1

    print("total pipe length:", step_counter)
    print("middle at:", math.ceil(step_counter / 2))


def count_intersections(row: str, filter: list[bool]):
    count = 0
    last = ""
    for x in range(len(row)):
        if filter[x]:
            pipe = row[x]
            if pipe == "|":
                count += 1
            if (pipe == "J" and last == "L") or (pipe == "7" and last == "F"):
                last = ""
                count += 1
            if (pipe == "L") or (pipe == "F"):
                last = pipe
                count += 1

    return count


def part_two(grid):
    filtered_grid = []
    for i in range(len(grid)):
        filtered_grid.append([False] * len(grid[0]))

    # Mark visited pipes to filter, so we can ignore all others
    coords = find_start(grid)
    direction = find_start_direction(grid, coords)
    while True:
        coords = add(coords, direction)
        next_part = grid[coords[1]][coords[0]]
        filtered_grid[coords[1]][coords[0]] = True
        if next_part == "S":
            break
        pipe = pipe_parts[next_part]
        direction = pipe.enter(direction)

    # Clean up S TODO: dirty hardcoded value
    grid[coords[1]] = grid[coords[1]][:coords[0]] + "|" + grid[coords[1]][coords[0] + 1:]

    # Print pretty map of pipe network
    for y, row in enumerate(filtered_grid):
        line = ""
        for x, char in enumerate(row):
            if filtered_grid[y][x]:
                # line += grid[y][x]
                line += "░░"
            else:
                edge_count = count_intersections(grid[y][:x], filtered_grid[y][:x])
                if edge_count % 2 == 1:
                    line += "██"
                else:
                    line += "  "
        print(line)

    # calculate inside tiles
    inside_tiles = 0
    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            if not filtered_grid[y][x]:
                edge_count = count_intersections(grid[y][:x], filtered_grid[y][:x])
                if edge_count % 2 == 1:
                    inside_tiles += 1

    print("tiles inside:", inside_tiles)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
