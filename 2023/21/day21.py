from util.grid import Grid, Point, neighbours_4


def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        return Grid.read(file.read())


def find_reachable_positions(grid: Grid, start_positions: list[Point]):
    reachable = set()
    for start_position in start_positions:
        for neighbour, value in grid.neighbours_4(start_position):
            if value != "#":
                reachable.add(neighbour)
    return list(reachable)


def part_one(grid):
    start = grid.find("S")[0]
    reachable = [start]
    for i in range(64):
        reachable = find_reachable_positions(grid, reachable)
    print("reachable spots with 64 steps:", len(reachable))


def find_reachable_positions_infinite(grid: Grid, start_positions: list[Point]):
    reachable = set()
    for start_position in start_positions:
        for neighbour in neighbours_4(start_position):
            offset = (neighbour[0] % grid.width, neighbour[1] % grid.height)
            value = grid[offset]
            if value != "#":
                reachable.add(neighbour)
    return list(reachable)


def find_step_values(grid, magic_step_count):
    step_size = grid.width
    offset = magic_step_count % grid.width
    start = grid.find("S")[0]
    reachable = [start]
    step_values = []
    for i in range(1, offset + 4 * step_size + 2):
        reachable = find_reachable_positions_infinite(grid, reachable)
        if i % step_size == offset:
            step_values.append(len(reachable))
            print(i // step_size, len(reachable))
    return step_values


# Day 09 answer to extrapolate later steps
def get_next_value(seq):
    diff = list(b - a for a, b in zip(seq[:-1], seq[1:]))
    if all(x == 0 for x in diff):
        return seq[-1]
    return seq[-1] + get_next_value(diff)


def part_two(grid):
    magic_step_count = 26501365
    step_count = magic_step_count // grid.width
    # step_values = find_step_values(grid, magic_step_count)
    # print(step_values)
    step_values = [3738, 33270, 92194, 180510, 298218]

    current = step_values[:-2]
    for i in range(step_count - 2):
        current = current[1:] + [get_next_value(current)]
    print("reachable plots with", magic_step_count, "steps:", current[-1])


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
