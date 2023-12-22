def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        return file.read().split(",")


def HASH(string: str):
    hash_value = 0
    for char in string.strip():
        ascii_value = ord(char)
        hash_value += ascii_value
        hash_value *= 17
        hash_value %= 256
    return hash_value


def op_equals(boxes, step):
    label, value = step.split("=")
    value = int(value)
    box_id = HASH(label)
    box = boxes[box_id]
    for i in range(len(box)):
        if box[i][0] == label:
            box[i] = (label, value)
            return
    box.append((label, value))


def op_minus(boxes, step):
    label = step[:-1]
    box_id = HASH(label)
    box = boxes[box_id]
    for i in range(len(box)):
        if box[i][0] == label:
            box.pop(i)
            return


def focal_power(box):
    total = 0
    for i in range(len(box)):
        total += box[i][1] * (i + 1)
    return total


def part_one(steps):
    validation_value = sum(HASH(string) for string in steps)
    print("validation sum:", validation_value)


def part_two(steps):
    boxes = [[] for _ in range(256)]
    for step in steps:
        if "=" in step:
            op_equals(boxes, step)
        else:
            op_minus(boxes, step)

    total_focal_power = sum(focal_power(box) * (i + 1) for i, box in enumerate(boxes))
    print("total focal power:", total_focal_power)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
