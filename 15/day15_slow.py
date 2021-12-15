import numpy as np

def read_input():
    data = np.genfromtxt("input.txt", delimiter=1)
    return data


def generate_full_field(field):
    extended_row = field
    for x in range(1,5):
        new_field = field + x
        new_field[new_field >= 10] -= 9
        extended_row = np.append(extended_row, new_field, axis = 1)

    extended_field = extended_row
    for y in range(1,5):
        new_field = extended_row + y
        new_field[new_field >= 10] -= 9
        extended_field = np.append(extended_field, new_field, axis = 0)

    return extended_field


def get_neighbours(current, visited):
    x, y = current

    neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in neighbours:
        if nx < 0 or ny < 0:
            continue
        if nx >= visited.shape[0] or ny >= visited.shape[1]:
            continue
        if visited[nx, ny]:
            continue
        yield nx, ny


def dijkstra_path_find(field):
    distances = np.full(field.shape, 1_000_000)
    visited = np.zeros(field.shape)

    distances[0, 0] = 0

    current = (0, 0)

    while True:
        for neighbour in get_neighbours(current, visited):
            distances[neighbour] = min(distances[current] + field[neighbour], distances[neighbour])
        visited[current] = 1

        # get new current
        masked_distances = np.ma.masked_array(distances, mask=visited)
        current_index = np.argmin(masked_distances)
        if (current_index == 0):
            break

        if visited.sum() % 100 == 0:
            print(visited.sum(), "/", visited.shape[0] * visited.shape[1])

        current = np.unravel_index(current_index, field.shape)

    return distances[-1,-1]


if __name__ == '__main__':
    field = read_input()
    print("Input is of size", field.shape)
    print("Lowest cost path:", dijkstra_path_find(field))

    full_field = generate_full_field(field)
    print("Extended input is of size", full_field.shape)
    print("Lowest cost path:", dijkstra_path_find(full_field))
