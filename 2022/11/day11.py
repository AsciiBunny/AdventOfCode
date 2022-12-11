import math
import re
from dataclasses import dataclass
from typing import Callable


@dataclass
class Monkey:
    items: list[int]
    operation: Callable[[int], int]
    test: int
    if_test_true: int
    if_test_false: int

    inspections = 0

    def inspect(self, value):
        self.inspections += 1
        return self.operation(value)


def parse_operation(line):
    value: str = re.findall("\d+|old$", line)[0]
    operation_value = int(value) if value.isnumeric() else value
    if operation_value == "old":
        return lambda x: x * x
    if "*" in line:
        return lambda x: x * operation_value
    if "+" in line:
        return lambda x: x + operation_value
    assert False, "This should not happen"


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    monkeys: list[Monkey] = []
    while len(data_lines) > 0:
        monkey_lines = data_lines[:7]
        data_lines = data_lines[7:]

        items = re.findall("\d+", monkey_lines[1])
        items = [int(item) for item in items]

        operation = parse_operation(monkey_lines[2])

        test = int(re.findall("\d+", monkey_lines[3])[0])
        if_test_true = int(re.findall("\d+", monkey_lines[4])[0])
        if_test_false = int(re.findall("\d+", monkey_lines[5])[0])

        monkey = Monkey(items, operation, test, if_test_true, if_test_false)
        monkeys.append(monkey)

    return monkeys


def monkey_business(monkeys: list[Monkey], cycles, not_stressing=True):
    biggest_divisor = math.prod(monkey.test for monkey in monkeys)
    for round_number in range(cycles):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item = monkey.items.pop()
                item = monkey.inspect(item)
                if not_stressing:
                    item //= 3
                item %= biggest_divisor
                next_monkey_index = monkey.if_test_true if item % monkey.test == 0 else monkey.if_test_false
                monkeys[next_monkey_index].items.append(item)
        if cycles < 25 or (round_number + 1) % 1000 == 0 or round_number == 0 or round_number == 19:
            inspections = [monkey.inspections for monkey in monkeys]
            print("#### Round", round_number + 1, "(", sum(len(monkey.items) for monkey in monkeys), "items) ####")
            print_monkeys(monkeys)
            inspections = sorted(inspections)
            biggest = inspections[-2:]
            print("Level of monkey business:", biggest[0] * biggest[1])
            print()


def print_monkeys(monkeys):
    for index, monkey in enumerate(monkeys):
        print("Monkey", index, "(", monkey.inspections, "inspections)", monkey.items)


if __name__ == '__main__':
    monkeys = read_input()
    monkey_business(monkeys, 20)

    monkeys = read_input()
    monkey_business(monkeys, 10000, not_stressing=False)
