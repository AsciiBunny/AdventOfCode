import numpy as np

def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    input = [[int(digit) for digit in line] for line in data_lines]

    return np.array([np.array(line) for line in input])


def get_value(input, x, y):
    if x < 0 or x >= len(input[0]):
        return 9
    if y < 0 or y >= len(input):
        return 9
    return input[x][y]


def keep_low_point_filter(input, x, y):
    value = get_value(input, x, y)

    if get_value(input, x - 1, y) <= value:
        return -1

    if get_value(input, x + 1, y) <= value:
        return -1

    if get_value(input, x, y - 1) <= value:
        return -1

    if get_value(input, x, y + 1) <= value:
        return -1

    return value


def filtered_copy(input, filter):
    copy = np.zeros(shape=input.shape)
    for x in range(0, input.shape[0]):
        for y in range(0, input.shape[1]):
            copy[x][y] = filter(input, x, y)
    return copy


def generate_low_points(is_low_point):
    for x in range(0, is_low_point.shape[0]):
        for y in range(0, is_low_point.shape[1]):
            if is_low_point[x][y]:
                yield x,y


def flood_fill(input, x, y, value):
    if x < 0 or x >= input.shape[0]:
        return

    if y < 0 or y >= input.shape[1]:
        return

    if input[x][y] == -1 or input[x][y] == value:
        return

    input[x][y] = value

    flood_fill(input, x + 1, y, value)
    flood_fill(input, x - 1, y, value)
    flood_fill(input, x, y + 1, value)
    flood_fill(input, x, y - 1, value)


def flood_fill_low_points(input, is_low_point):
    copy = np.zeros(shape=input.shape)
    copy[input == 9] = -1

    uid = 1
    for low_point in generate_low_points(is_low_point):
        flood_fill(copy, *low_point, uid)
        uid += 1

    return copy

if __name__ == '__main__':
    input = read_input()
    print("Input is of size", input.shape)

    low_point_map = filtered_copy(input, keep_low_point_filter)

    risk_map = low_point_map + 1
    print("Total risk =", risk_map.sum())

    np.set_printoptions(threshold=np.inf)

    is_low_point = low_point_map >= 0
    print("Low Points =", is_low_point.sum())

    flood_filled = flood_fill_low_points(input, is_low_point)

    unique, counts = np.unique(flood_filled, return_counts=True)
    unique_counts = dict(zip(unique, counts))
    del unique_counts[-1]

    largest = sorted(unique_counts.values())[-3:]
    print("Answer =", largest[0] * largest[1] * largest[2])





