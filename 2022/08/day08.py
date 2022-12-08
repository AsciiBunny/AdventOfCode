import numpy as np


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    lines = [[int(character) for character in line] for line in data_lines]
    lines = np.array(lines)
    return lines


def check_visible(field, results):
    for field_line, result_line in zip(field, results):
        for i in range(len(field_line)):
            result_line[i] = result_line[i] or np.all(field_line[:i] < field_line[i])


def calculate_side_visibility(field):
    results = np.full(field.shape, False)

    for i in range(4):
        check_visible(field, results)
        field = np.rot90(field)
        results = np.rot90(results)

    return results


def calculate_vision_range(vision, height):
    first = -1
    for i, x in enumerate(vision):
        if x >= height:
            first = i + 1
            break
    if first == -1:
        first = len(vision)
    return first


def calculate_vision_range_field(field):
    results = np.full(field.shape, 0)

    for iy, ix in np.ndindex(field.shape):
        height = field[iy][ix]

        left = np.flip(field[iy, :ix])
        right = field[iy, ix + 1:]
        up = np.flip(field[:iy, ix])
        down = field[iy + 1:, ix]

        first_left = calculate_vision_range(left, height)
        first_right = calculate_vision_range(right, height)
        first_down = calculate_vision_range(down, height)
        first_up = calculate_vision_range(up, height)

        scenic_score = first_left * first_right * first_up * first_down
        results[iy, ix] = scenic_score

    return results


if __name__ == '__main__':
    field = read_input()
    results = calculate_side_visibility(field)
    print("There are", results.sum(), "visible trees")

    results_scenic = calculate_vision_range_field(field)
    print(results_scenic)
    max_scenic = np.max(results_scenic)
    print("Highest scenic score:", max_scenic)