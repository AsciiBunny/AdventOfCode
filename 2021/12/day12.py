def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    input_split = [line.split("-") for line in data_lines]
    input_edges = [(start, end) for start, end in input_split]

    graph = dict()
    for edge in input_edges:
        add_to_graph(graph, edge)

    return graph


def add_to_graph(graph: dict[set], edge):
    start, end = edge
    graph.setdefault(start, set())
    graph.setdefault(end, set())
    graph[start].add(end)
    graph[end].add(start)


def remove_from_graph(graph: dict[set], vector):
    if vector in graph:
        del graph[vector]

    for key in graph:
        if vector in graph[key]:
            graph[key].remove(vector)


def path_search(graph, path, can_double_visit=False):
    if path[-1] == 'end':
        yield path
        return

    next_vertices = graph.get(path[-1])
    visited = {edge for edge in path if edge.islower()}
    if not can_double_visit:
        next_vertices = next_vertices - visited

    # Can never go back to start
    next_vertices -= {'start'}

    if len(next_vertices) == 0:
        return False

    for next in next_vertices:
        new_path = path + [next]
        can_still_double_visit = can_double_visit and (next not in path or next.isupper())
        for finished_path in path_search(graph, new_path, can_still_double_visit):
            yield finished_path


def find_paths(graph, can_double_visit=False):
    path = ['start']
    for finished_path in path_search(graph, path, can_double_visit):
        yield finished_path


if __name__ == '__main__':
    graph = read_input()

    print("Input graph:")
    for key in graph:
        print("~", key, 'lc' if key.islower() else 'UC', graph[key])

    print("Paths found:", sum(1 for path in find_paths(graph)))

    print("Paths found:", sum(1 for path in find_paths(graph, True)))
