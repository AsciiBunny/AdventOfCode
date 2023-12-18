import re


def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        return file.read().splitlines()


def get_expansions(universe: list[str]):
    vertical_expansions = list(filter(lambda row: all(c == "." for c in universe[row]), range(len(universe))))
    horizontal_expansions = list(
        filter(lambda col: all(c == "." for row in universe for c in row[col]), range(len(universe[0]))))
    return horizontal_expansions, vertical_expansions


def expand_universe_once(universe: list[str]):
    size_before = len(universe[0]), len(universe)
    horizontal_expansions, vertical_expansions = get_expansions(universe)

    for y in reversed(vertical_expansions):
        universe = universe[:y] + ["".join(["."] * len(universe[0]))] + universe[y:]

    for x in reversed(horizontal_expansions):
        for y in range(len(universe)):
            universe[y] = universe[y][:x] + "." + universe[y][x:]

    size_after = len(universe[0]), len(universe)
    print(f"Universe expanded from {size_before} to {size_after}")


def find_galaxies(universe: list[str]):
    # find galaxies
    galaxies = []
    for line_index, line in enumerate(universe):
        for match in re.finditer(r"#", line):
            galaxies.append((match.start(), line_index))
    return galaxies

def is_between(a, b, between):
    return a < between < b or b < between < a

def calculate_distances(universe: list[str], expansion_distance=1):
    galaxies = find_galaxies(universe)
    horizontal_expansions, vertical_expansions = get_expansions(universe)

    total_distance = 0
    for i in range(len(galaxies)):
        a = galaxies[i]
        for b in galaxies[i + 1:]:
            distance = abs(b[0] - a[0]) + abs(b[1] - a[1])
            for hex in horizontal_expansions:
                if is_between(a[0], b[0], hex):
                    distance += expansion_distance - 1

            for vex in vertical_expansions:
                if is_between(a[1], b[1], vex):
                    distance += expansion_distance - 1

            total_distance += distance

    return  total_distance

def part_one(universe: list[str]):
    print("total distance between all galaxies after short expansion:", calculate_distances(universe, 2))


def part_two(universe: list[str]):
    print("total distance between all galaxies after long expansion:", calculate_distances(universe, 1000000))


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
