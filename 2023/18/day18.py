def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        lines = file.read().splitlines()
        instructions = []
        for line in lines:
            d, a, c = line.split(" ")
            instructions.append((d, int(a), c[2:-1]))
        return instructions


directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}

direction_labels = ["R", "D", "L", "U"]


def get_polygon_segments(p):
    return zip(p, p[1:] + [p[0]])


def get_polygon_area(p):
    return 0.5 * abs(sum(x0 * y1 - x1 * y0
                         for ((x0, y0), (x1, y1)) in get_polygon_segments(p)))


def get_polygon_perimeter(p):
    return sum(abs(x0 - x1) + abs(y0 - y1) for ((x0, y0), (x1, y1)) in get_polygon_segments(p))


def get_pit_size(path):
    return get_polygon_area(path) + get_polygon_perimeter(path) / 2 + 1


def part_one(instructions):
    path = [(0, 0)]
    for direction, count, _ in instructions:
        direction = directions[direction]
        next_position = (path[-1][0] + direction[0] * count, path[-1][1] + direction[1] * count)
        path.append(next_position)
    path = path[:-1]

    print(f"the pit can hold {get_pit_size(path)} cubic meters of lava")


def parse_color(color):
    count = int(color[:5], 16)
    direction = directions[direction_labels[int(color[5])]]
    return count, direction


def part_two(instructions):
    path = [(0, 0)]
    for _, _, color in instructions:
        count, direction = parse_color(color)
        next_position = (path[-1][0] + direction[0] * count, path[-1][1] + direction[1] * count)
        path.append(next_position)
    path = path[:-1]
    print(f"the pit can hold {get_pit_size(path)} cubic meters of lava")


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
