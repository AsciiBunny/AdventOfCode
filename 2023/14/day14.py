def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        return file.read().splitlines()


def set_character(string: str, index: int, character: str):
    return string[:index] + character + string[index + 1:]


def shift_row_left(row: str):
    for i in range(len(row)):
        if row[i] == ".":
            next_block = row.find("#", i + 1)
            if next_block < 0:
                next_block = len(row)
            next_rock = row.find("O", i + 1, next_block)
            if next_rock > 0:
                row = set_character(row, i, "O")
                row = set_character(row, next_rock, ".")
    return row


def shift_field_left(field: list[str]):
    return list(map(shift_row_left, field))


def rotate_field_right(field: list[str]):
    reversed_field = list(map("".join, reversed(field)))
    transposed_field = list(map("".join, zip(*reversed_field)))
    return transposed_field


def rotate_field_left(field: list[str]):
    transposed_field = list(map("".join, zip(*field)))
    reversed_field = list(map("".join, reversed(transposed_field)))
    return reversed_field


def get_left_weight(field: list[str]):
    field_width = len(field[0])
    total_weight = 0
    for row in field:
        for i, character in enumerate(row):
            if character == "O":
                total_weight += field_width - i
    return total_weight


def part_one(field):
    field = rotate_field_left(field)
    field = shift_field_left(field)
    print("total weight on north beams:", get_left_weight(field))


def cycle(field):
    for _ in range(4):
        field = shift_field_left(field)
        field = rotate_field_right(field)
    return field


def part_two(field):
    # Calculate enough weights for the system to stabilize in a repeating cycle of weights
    field = rotate_field_left(field)
    weights = []
    for i in range(300):
        field = cycle(field)
        weights += [get_left_weight(field)]

    # Throw away the stabilizing part
    weights = weights[100:]

    # Find the repeating cycle
    weight_cycle = []
    for i in range(5, 100):
        if weights[:i] == weights[i:i + i]:
            weight_cycle = weights[:i]
            print("super-cycle has formed that repeats every", len(weight_cycle), "cycles")
            break

    # Calculate where cycle 1000000000 falls in this repeating cycle
    to_find = 1000000000
    to_find -= 1
    to_find -= 100
    to_find %= len(weight_cycle)

    print("total weight on north beams on cycle 1000000000:", weight_cycle[to_find])


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
