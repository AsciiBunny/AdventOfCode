import math

import parsley


def read_input(filename):
    parser = parsley.makeGrammar("""
        number = ws <digit+>:ds -> int(ds)
        instruction = "L" | "R"
        node_name = <letter{3}>
        node = ws node_name:a ws "=" ws "(" node_name:b "," ws node_name:c ")" -> (a,(b,c))
        input = instruction+:instructions ws node+:nodes ws end -> (instructions, nodes)
        """, {})

    with open(f"{filename}.txt", "r") as file:
        return parser(file.read()).input()


def get_node_map(nodes):
    node_map = {}
    for start, connections in nodes:
        node_map[start] = connections
    return node_map


def find_cycle_length(node_map, start_node, instructions):
    instruction_counter = 0
    node = start_node

    while True:
        instruction = instructions[instruction_counter % len(instructions)]
        instruction_counter += 1
        instruction = 0 if instruction == "L" else 1

        node = node_map[node][instruction]

        if node[2] == "Z":
            return instruction_counter


def part_one(instructions, nodes):
    node_map = get_node_map(nodes)
    cycle_count = find_cycle_length(node_map, "AAA", instructions)

    print(f"Found ZZZ in {cycle_count} steps")


def part_two(instructions, nodes):
    node_map = get_node_map(nodes)
    start_nodes = [node for node, _ in nodes if node[2] == "A"]
    cycle_counts = []

    for start_node in start_nodes:
        cycle_counts.append(find_cycle_length(node_map, start_node, instructions))

    print(f"Found all xxZ in {math.lcm(*cycle_counts)} steps")


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(*data)
    print("\nPart 2")
    part_two(*data)
