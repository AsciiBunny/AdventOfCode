from functools import cache


def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        return file.read().splitlines()


tiles = {
    ".": lambda dir: [dir],
    "|": lambda dir: [dir] if dir[0] == 0 else [(0, 1), (0, -1)],
    "-": lambda dir: [dir] if dir[1] == 0 else [(1, 0), (-1, 0)],
    "/": lambda dir: [(-dir[1], -dir[0])],
    "\\": lambda dir: [(dir[1], dir[0])]
}


@cache
def beam(point: tuple[int, int], direction: tuple[int, int]):
    next_point = (point[0] + direction[0], point[1] + direction[1])
    if next_point[0] >= len(grid[0]) or next_point[0] < 0:
        return [], []
    if next_point[1] >= len(grid) or next_point[1] < 0:
        return [], []

    points = [next_point]

    next_tile = grid[next_point[1]][next_point[0]]
    next_directions = tiles[next_tile](direction)
    if len(next_directions) > 1:
        next_beams = []
        for next_direction in next_directions:
            next_beams.append((next_point, next_direction))
        return points, next_beams
    elif len(next_directions) == 1:
        next_points, next_beams = beam(next_point, next_directions[0])
        return points + next_points, next_beams
    else:
        assert False


def all_beams(start_beam):
    beams = [start_beam]
    seen = set()
    checked = set()

    while len(beams) > 0:
        point, direction = beams.pop()
        checked.add((point, direction))

        new_points, new_beams = beam(point, direction)

        for new_point in new_points:
            seen.add(new_point)

        for new_beam in new_beams:
            if new_beam not in checked:
                beams.append(new_beam)

    return seen


def part_one():
    energized = all_beams(((-1, 0), (1, 0)))
    print("energized tile count:", len(energized))


def part_two():
    start_beams = []
    start_beams += [((-1, i), (1, 0)) for i in range(len(grid))]
    start_beams += [((len(grid), i), (-1, 0)) for i in range(len(grid))]
    start_beams += [((0, 1), (0, -1)) for i in range(len(grid[0]))]
    start_beams += [((0, -1), (0, len(grid[0]))) for i in range(len(grid[0]))]

    best_field = max(map(lambda start_beam: len(all_beams(start_beam)), start_beams))
    print("best energized tile count:", best_field)


if __name__ == '__main__':
    grid = read_input('input')
    print("Part 1")
    part_one()
    print("\nPart 2")
    part_two()
