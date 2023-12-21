import sys
from functools import cache


def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        lines = file.read().splitlines()
        lines = [line.split(" ") for line in lines]
        lines = [(pattern, tuple(int(number) for number in groups.split(","))) for pattern, groups in lines]
        return lines


def match_pattern(pattern, test):
    assert len(pattern) == len(test), (pattern, test)

    for i in range(len(pattern)):
        if pattern[i] == "?" or test[i] == "?":
            continue
        if pattern[i] != test[i]:
            return False
    return True


@cache
def build_test(pattern, groups):
    min_required_length = sum(groups) + len(groups) - 1
    if min_required_length > len(pattern):
        return 0

    valid_tests = 0
    for i in range(len(pattern) - min_required_length + 1):
        test = "." * i + "#" * groups[0]
        if len(groups) > 1:
            test += "."
            test_filled = test.ljust(len(pattern), "?")
        else:
            test_filled = test.ljust(len(pattern), ".")

        if not match_pattern(pattern, test_filled):
            continue

        if len(groups) > 1:
            valid_tests += build_test(pattern[len(test):], groups[1:])
        else:
            valid_tests += 1

    return valid_tests


def part_one(lines):
    total_valid = 0
    for i, (pattern, groups) in enumerate(lines):
        valid_arrangements = build_test(pattern, groups)
        total_valid += valid_arrangements
        sys.stdout.write(f"\r {i} {valid_arrangements}")
    sys.stdout.write(f"\r")

    print("total valid arrangements:", total_valid)


def part_two(lines):
    for i, line in enumerate(lines):
        lines[i] = ("?".join([line[0]] * 5), line[1] * 5)

    part_one(lines)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
