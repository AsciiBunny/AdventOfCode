import math


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    heightmap = [[char for char in line] for line in data_lines]
    return heightmap


def find(heightmap: list[list[str]], to_find: str):
    for i, row in enumerate(heightmap):
        if to_find in row:
            index = row.index(to_find)
            return i, index


def get_neighbours(heightmap: list[list[str]], current: (int, int)):
    current_height = heightmap[current[0]][current[1]]
    limit_height = chr(ord(current_height) + 1)

    if current_height == "S":
        limit_height = "a"

    if current[0] + 1 < len(heightmap) and heightmap[current[0] + 1][current[1]] <= limit_height:
        if heightmap[current[0] + 1][current[1]] != "E" or current_height == "z":
            yield current[0] + 1, current[1]

    if current[0] - 1 >= 0 and heightmap[current[0] - 1][current[1]] <= limit_height:
        if heightmap[current[0] - 1][current[1]] != "E" or current_height == "z":
            yield current[0] - 1, current[1]

    if current[1] + 1 < len(heightmap[0]) and heightmap[current[0]][current[1] + 1] <= limit_height:
        if heightmap[current[0]][current[1] + 1] != "E" or current_height == "z":
            yield current[0], current[1] + 1

    if current[1] - 1 >= 0 and heightmap[current[0]][current[1] - 1] <= limit_height:
        if heightmap[current[0]][current[1] - 1] != "E" or current_height == "z":
            yield current[0], current[1] - 1


def a_star(heightmap: list[list[str]], start_nodes: list[(int, int)], end: (int, int)):
    to_explore = {*start_nodes}
    previous = dict()
    cost = dict()
    for node in start_nodes:
        cost[node] = 0

    while len(to_explore) > 0:
        current = min(to_explore, key=lambda node: cost[node])
        if current == end:
            return cost[current]
        to_explore.remove(current)
        for neighbour in get_neighbours(heightmap, current):
            tentative_cost = cost[current] + 1
            if tentative_cost < cost.get(neighbour, math.inf):
                previous[neighbour] = current
                cost[neighbour] = tentative_cost
                to_explore.add(neighbour)


if __name__ == '__main__':
    heightmap = read_input()
    start = find(heightmap, "S")
    end = find(heightmap, "E")
    print(start, "->", end)
    print("Shortest route from S:", a_star(heightmap, [start], end))
    all_a_nodes = []
    for y, row in enumerate(heightmap):
        for x, value in enumerate(row):
            if value == "a":
                all_a_nodes.append((y, x))
    print("Shortest route from any a:", a_star(heightmap, all_a_nodes, end))
