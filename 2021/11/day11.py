import numpy as np

width = height = 10


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    input = [[int(digit) for digit in line] for line in data_lines]

    grid = np.array([np.array(line) for line in input])
    grid = np.pad(grid, pad_width=1, constant_values=11)
    return grid


def unpad(grid):
    return grid[1: width + 1, 1: height + 1]


def step(grid):
    unpadded = unpad(grid)
    unpadded += 1
    flash_count = 0
    for (x, y), energy_level in np.ndenumerate(unpadded):
        if energy_level == 10:
            flash_count += flash(grid, x + 1, y + 1)
    unpadded[unpadded > 9] = 0
    return flash_count


def flash(grid, x, y):
    flash_area = grid[x - 1: x + 2, y - 1: y + 2]
    flash_area[flash_area <= 9] += 1
    grid[x, y] = 11

    flash_count = 1

    for (x_offset, y_offset), energy_level in np.ndenumerate(flash_area):
        if energy_level == 10:
            flash_count += flash(grid, x + x_offset - 1, y + y_offset - 1)

    return flash_count


if __name__ == '__main__':
    grid = read_input()
    print("Input is of size", unpad(grid).shape)
    print("Grid before:")
    print(unpad(grid))

    flash_count = 0
    for _ in range(0, 100):
        flash_count += step(grid)

    print("Grid after:")
    print(unpad(grid))
    print("Flash count after 100 iterations:", flash_count)

    for i in range(0, 1000):
        step(grid)
        if unpad(grid).sum() == 0:
            print("Octopuses synchronized after", i + 101, "steps.")
            print(unpad(grid))
            break
