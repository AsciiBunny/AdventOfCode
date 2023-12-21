def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        fields = file.read().split("\n\n")
        fields = [field.splitlines() for field in fields]
        return fields


def differences(left: str, right: str):
    return sum(a != b for a, b in zip(left, right))  # counts wrong characters


def is_mirror_line(field: list[str], i: int, invalid_count):
    shortest = min(i, len(field[0][i:]))
    assert shortest > 0
    invalid = 0
    for row in field:
        left = row[i - shortest:i]
        right = "".join(reversed(row[i:i + shortest]))
        if left != right:
            invalid += differences(left, right)
            if invalid > invalid_count:
                return False
    return invalid == invalid_count


def find_mirror_line(field: list[str], invalid_count):
    for i in range(1, len(field[0])):
        if is_mirror_line(field, i, invalid_count):
            return i


def score_field(field: list[str], invalid_count):
    vertical_line = find_mirror_line(field, invalid_count)
    if vertical_line:
        return vertical_line
    
    transposed_field = list(map("".join, zip(*field)))
    horizontal_line = find_mirror_line(transposed_field, invalid_count)
    if horizontal_line:
        return 100 * horizontal_line


def part_one(fields):
    total_score = 0
    for field in fields:
        total_score += score_field(field, 0)
    print("Total score of mirrored rows/columns:", total_score)


def part_two(fields):
    total_score = 0
    for field in fields:
        total_score += score_field(field, 1)
    print("Total score of smudgy mirrored rows/columns:", total_score)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
