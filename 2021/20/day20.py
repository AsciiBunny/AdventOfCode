import numpy as np

def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    algorithm = np.array([char == "#" for char in data_lines[0]])

    field = np.array([np.array([char == "#" for char in line ]) for line in data_lines[2:]])
    field = np.pad(field, 5, mode='constant')
    return algorithm, field


def print_field(field):
    for line in field:
        print(*("#" if char else "." for char in line), sep="")
    print()


def enhance_step(algorithm, field, is_even_step):
    field = np.pad(field, 1, mode='constant', constant_values=is_even_step)
    new_field = np.ndarray(shape=field.shape, dtype=bool)
    print_field(field)
    for (x, y), element in np.ndenumerate(field):
        local_area = field[x - 1: x + 2, y - 1: y + 2]
        if local_area.size < 9:
            new_field[x, y] = not is_even_step
            continue
        value = ''.join("1" if char else "0" for char in local_area.flatten())
        value = int(value, base=2)
        new_field[x, y] = algorithm[value]

    return new_field



if __name__ == '__main__':
    algorithm, field = read_input()
    print_field(field)

    for step in range(50):
        field = enhance_step(algorithm, field, step % 2 == 1)
        print_field(field)

    print(field.sum())
