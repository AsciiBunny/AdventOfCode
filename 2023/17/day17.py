import heapq

# Todo: can be optimized by reconsidering what constitutes the "graph" we're traveling here, smaller state -> more speed
Node = tuple[int, int, int, int]
Grid = list[list[int]]


def read_input(filename):
    with open(f"{filename}.txt", "r") as file:
        lines = file.read().splitlines()
        lines = [[int(digit) for digit in line] for line in lines]
        return lines


def get_straight_length(current: Node, target: Node, previous_node: dict[Node, Node]):
    length = 1
    if current not in previous_node:
        return length

    direction = (target[0] - current[0], target[1] - current[1])
    while current in previous_node:
        previous = previous_node[current]
        next_direction = (current[0] - previous[0], current[1] - previous[1])
        if next_direction == direction:
            length += 1
        else:
            return length
        current = previous

    return length


def get_neighbours(current_node: Node, previous_node: dict[Node, Node], node_costs: Grid,
                   turning_limits: tuple[int, int]):
    previous = previous_node[current_node] if current_node in previous_node else None

    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        neighbour = (
            current_node[0] + direction[0],
            current_node[1] + direction[1],
            current_node[2] * abs(direction[0]) + direction[0],
            current_node[3] * abs(direction[1]) + direction[1],
        )

        if previous and (neighbour[0], neighbour[1]) == (previous[0], previous[1]):
            continue

        if not (0 <= neighbour[0] < len(node_costs[0])) \
                or not (0 <= neighbour[1] < len(node_costs)):
            continue

        if (0 < abs(current_node[2]) < turning_limits[0] and direction[0] == 0) \
                or (0 < abs(current_node[3]) < turning_limits[0] and direction[1] == 0):
            continue

        if abs(neighbour[2]) >= turning_limits[1] or abs(neighbour[3]) >= turning_limits[1]:
            continue

        yield neighbour


def modified_dijkstra(start: Node, goal: Node, node_costs: Grid, turning_limits: tuple[int, int]):
    frontier = [(0, start)]
    previous_node: dict[Node, Node] = dict()
    cost_so_far: dict[Node, int] = dict()
    cost_so_far[start] = 0

    while len(frontier) > 0:
        current_node = heapq.heappop(frontier)[1]
        if (current_node[0], current_node[1]) == (goal[0], goal[1]) and (
                current_node[2] >= turning_limits[0] or current_node[3] >= turning_limits[0]):
            goal = current_node
            break

        for neighbour in get_neighbours(current_node, previous_node, node_costs, turning_limits):
            new_cost = cost_so_far[current_node] + node_costs[neighbour[1]][neighbour[0]]
            if neighbour not in cost_so_far or new_cost <= cost_so_far[neighbour]:
                previous_node[neighbour] = current_node
                cost_so_far[neighbour] = new_cost

                if (new_cost, neighbour) not in frontier:
                    heapq.heappush(frontier, (new_cost, neighbour))

    return goal, previous_node, cost_so_far


def get_path(start: Node, goal: Node, previous: dict[Node, Node]):
    path = [goal]
    while path[0] != start:
        path = [previous[path[0]]] + path
    path = [(x, y) for x, y, _, _ in path]
    return path


def print_path(path: list[tuple[int, int]], grid: Grid):
    for y, line in enumerate(grid):
        string = ""
        for x, character in enumerate(line):
            string += "X" if (x, y) in path else "_"
        print(string)


def part_one(grid: Grid):
    start = (0, 0, 0, 0)
    goal = (len(grid[0]) - 1, len(grid) - 1, 0, 0)
    goal, previous, cost = modified_dijkstra(start, goal, grid, (0, 4))

    # path = get_path(start, goal, previous)
    # print_path(path, grid)

    print("path found for crucible with a heat loss of:", cost[goal])


def part_two(grid):
    start = (0, 0, 0, 0)
    goal = (len(grid[0]) - 1, len(grid) - 1, 0, 0)
    goal, previous, cost = modified_dijkstra(start, goal, grid, (4, 11))

    # path = get_path(start, goal, previous)
    # print_path(path, grid)

    print("path found for ultra-crucible with a heat loss of:", cost[goal])


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
