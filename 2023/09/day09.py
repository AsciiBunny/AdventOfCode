def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        lines = file.read().splitlines()
        lines = [[int(value) for value in line.split(" ")] for line in lines]
        return lines


def get_next_value(seq):
    diff = list(b - a for a, b in zip(seq[:-1], seq[1:]))
    if all(x == 0 for x in diff):
        return seq[-1]
    return seq[-1] + get_next_value(diff)


def get_previous_value(seq):
    diff = list(b - a for a, b in zip(seq[:-1], seq[1:]))
    if all(x == 0 for x in diff):
        return seq[0]
    return seq[0] - get_previous_value(diff)


def part_one(lines):
    next_values = list(map(get_next_value, lines))
    print("Total extrapolated values:", sum(next_values))


def part_two(lines):
    prev_values = list(map(get_previous_value, lines))
    print("Total extrapolated values:", sum(prev_values))
    pass


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
