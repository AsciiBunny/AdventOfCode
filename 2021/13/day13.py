from dataclasses import dataclass

import numpy
import numpy as np


@dataclass
class Fold:
    axis: int
    index: int


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    input_pairs = [line for line in data_lines if ',' in line]
    input_pairs = [line.split(',') for line in input_pairs]
    input_pairs = [np.array([int(x), int(y)]) for x, y in input_pairs]

    width = max(point[0] for point in input_pairs) + 1
    height = max(point[1] for point in input_pairs) + 1

    input_pairs = np.array(input_pairs)
    grid = np.zeros(shape=(width, height))
    grid[tuple(input_pairs.T)] = 1

    input_folds = [line for line in data_lines if '=' in line]
    input_folds = [line[11:] for line in input_folds]
    input_folds = [line.split('=') for line in input_folds]
    input_folds = [Fold(1 if axis == 'x' else 0, int(index)) for axis, index in input_folds]

    return grid.T, input_folds


def fold_grid(grid, fold):
    front = grid.take(indices=range(0, fold.index), axis=fold.axis)
    back = grid.take(indices=range(fold.index + 1, grid.shape[fold.axis]), axis=fold.axis)
    back = np.flip(back, axis=fold.axis)

    if front.shape[fold.axis] > back.shape[fold.axis]:
        back = numpy.insert(back, 0, 0, axis=fold.axis)

    return np.maximum(front, back)


if __name__ == '__main__':
    grid, folds = read_input()
    print("Input is of size", grid.shape)
    # print("Grid before:")
    # print(grid)

    first_fold_grid = fold_grid(grid, folds[0])
    print("Dot count after first fold:", first_fold_grid.sum())

    for fold in folds:
        grid = fold_grid(grid, fold)

    for line in grid:
        print(*(" " if character == 0 else "#" for character in  line))