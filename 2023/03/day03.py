import re
from dataclasses import dataclass


def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        return file.read().splitlines()


digits = list(str(number) for number in range(10))
ignore_characters = ["."] + digits


@dataclass
class Number:
    line_index: int
    start: int
    end: int
    value: int


def find_numbers(grid) -> list[Number]:
    numbers = []
    for line_index, line in enumerate(grid):
        for match in re.finditer(r"\d+", line):
            numbers.append(Number(line_index, match.start(), match.end(), int(match.group())))
    return numbers


def is_part_number(grid):
    def validity_check(number):
        for y in range(number.line_index - 1, number.line_index + 2):
            if y < 0 or y >= len(grid):
                continue
            for x in range(number.start - 1, number.end + 1):
                if x < 0 or x >= len(grid[0]):
                    continue
                if grid[y][x] not in ignore_characters:
                    return True
        return False

    return validity_check


def part_one(grid):
    all_numbers = find_numbers(grid)
    part_numbers = list(filter(is_part_number(grid), all_numbers))
    part_numbers = [number.value for number in part_numbers]
    print("Part number sum:", sum(part_numbers))


def get_neighboring_parts(grid, number: Number):
    for y in range(number.line_index - 1, number.line_index + 2):
        if y < 0 or y >= len(grid):
            continue
        for x in range(number.start - 1, number.end + 1):
            if x < 0 or x >= len(grid[0]):
                continue
            if grid[y][x] not in ignore_characters:
                yield grid[y][x], x, y


def part_two(grid):
    all_numbers = find_numbers(grid)
    gears = {}
    for number in all_numbers:
        for part, x, y in get_neighboring_parts(grid, number):
            if part == "*":
                gears.setdefault((x, y), []).append(number)

    total_gear_ratio = 0
    for gear in gears:
        gear_numbers = gears[gear]
        if len(gear_numbers) != 2:
            continue
        gear_ratio = gear_numbers[0].value * gear_numbers[1].value
        total_gear_ratio += gear_ratio

    print("Total gear ratio", total_gear_ratio)

if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
