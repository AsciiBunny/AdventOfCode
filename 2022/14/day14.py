import itertools

import numpy as np
from PIL import Image as im


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    data_pairs = [line.split(" -> ") for line in data_lines]
    coords = [[(int(pair.split(",")[0]), int(pair.split(",")[1])) for pair in pairs] for pairs in data_pairs]

    return coords


def generate_field(coords, infinite=True):
    all_coords = list(itertools.chain.from_iterable(coords))
    x_coords = [coord[0] for coord in all_coords]
    y_coords = [coord[1] for coord in all_coords]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    height = y_max + 2
    x_pad = (height + 5) if not infinite else 5
    x_offset, y_offset = x_min - x_pad, 0
    x_size, y_size = x_max - x_min + x_pad + x_pad, y_max + 5
    field = np.zeros((y_size, x_size), dtype=int)

    for line in coords:
        for start, end in zip(line, line[1:]):
            assert start[0] == end[0] or start[1] == end[1]
            x_start, y_start = start[0] - x_offset, start[1] - y_offset
            x_end, y_end = end[0] - x_offset, end[1] - y_offset

            x_start, x_end = min(x_start, x_end), max(x_start, x_end)
            y_start, y_end = min(y_start, y_end), max(y_start, y_end)
            # print(x_start, "->", x_end, "  |  ", y_start, "->", y_end)
            if x_start == x_end:
                field[y_start: y_end + 1, x_start] = 255
            if y_start == y_end:
                field[y_start, x_start: x_end + 1] = 255

    if not infinite:
        field[y_max + 2, 0:] = 255

    return field, (500 - x_offset, 0)


def drop_sand(field, drop_point, i=128):
    x, y = drop_point
    if field[y, x] > 0:
        return False

    while True:
        col = field[y:, x]
        hit = np.argmax(col > 0)
        if hit > 0:
            if field[y + hit, x - 1] == 0:
                y += hit
                x -= 1
                continue
            elif field[y + hit, x + 1] == 0:
                y += hit
                x += 1
                continue
            else:
                col[hit - 1] = i
                return True
        else:
            return False


def show_field(field, name):
    image = im.fromarray(field)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    image.save(f'out_{name}.png')
    # image.show()


if __name__ == '__main__':
    coords = read_input()

    field, drop_point = generate_field(coords)
    dropped = 0
    while drop_sand(field, drop_point):
        dropped += 1
    print("Dropped sand:", dropped)
    show_field(field, "a")

    field, drop_point = generate_field(coords, False)
    dropped = 0
    while drop_sand(field, drop_point):
        dropped += 1
    print("Dropped sand:", dropped)

    show_field(field, "b")
