import parsley
from pyvis.network import Network

Modules = dict[str, (str, list[str])]


def read_input(filename):
    parser = parsley.makeGrammar("""
        name = <letter+>
        module_type = "%" | "&"
        module = (module_type:t name:n ws -> (n, t)) | "broadcaster" -> ("broadcaster", "broadcaster")
        names = name:first ("," ws name:name -> name)*:names -> [first, *(names if names else [])]
        line = ws module:m ws "->" ws names:names ws -> (m[0],(m[1], names))
        input = line+:lines ws end -> dict(lines)
        """, {})

    with open(f"{filename}.txt", "r") as file:
        return parser(file.read()).input()


def part_one(modules: Modules):
    flipflops = dict((key, False) for key in modules.keys() if modules[key][0] == "%")

    conjunctions = dict((key, dict()) for key in modules.keys() if modules[key][0] == "&")
    # fill conjunction states with incoming modules
    for key in modules:
        for key_out in modules[key][1]:
            if key_out in conjunctions:
                conjunctions[key_out][key] = False

    signal_counts = {False: 0, True: 0}

    for i in range(1000):
        queue = [("broadcaster", False, "button")]
        while len(queue) != 0:
            name, signal, origin = queue.pop()

            signal_counts.setdefault(signal, 0)
            signal_counts[signal] += 1

            if name == "rx":
                continue

            module_type, targets = modules[name]
            match module_type:
                case "%":
                    if signal:
                        continue
                    new_signal = flipflops[name] = not flipflops[name]
                case "&":
                    memory = conjunctions[name]
                    # memory[origin] = signal
                    new_signal = any(not s for s in memory.values())
                    if name in ["gr", "db", "vc", "lz"] and not new_signal:
                        print(name, i + 1, origin, modules[origin][1])
                case "broadcaster":
                    new_signal = False
                case _:
                    assert False, "Invalid module_type: " + module_type

            for target in targets:
                queue.append((target, new_signal, name))
                if  target in conjunctions and modules[target][0] == "&":
                    memory = conjunctions[target]
                    memory[name] = new_signal

    print(signal_counts)
    print(signal_counts[False] * signal_counts[True])


def find_cycle(modules: Modules, start, final_target):
    flipflops = dict((key, False) for key in modules.keys() if modules[key][0] == "%")

    conjunctions = dict((key, dict()) for key in modules.keys() if modules[key][0] == "&")
    # fill conjunction states with incoming modules
    for key in modules:
        for key_out in modules[key][1]:
            if key_out in conjunctions:
                conjunctions[key_out][key] = False

    counter = [start]
    incoming = []

    while True:
        current_node = counter[-1]
        _, next_nodes = modules[counter[-1]]
        for next_node in next_nodes:
            next_type, _ = modules[next_node]
            if next_type == "&":
                incoming.append(current_node)
            if next_type == "%":
                counter.append(next_node)
        if len(next_nodes) == 1 and modules[next_nodes[0]][0] == "&":
            break

    return counter, incoming


def print_state(d: dict[str, bool]):
    string = ""
    for key in d:
        string += "#" if d[key] else "_"
    print(string)


# print('{0:0=11b}'.format(middle))
def part_two(modules):
    cycle_pairs = [("sg", "gr"), ("gt", "db"), ("pc", "vc"), ("qf", "lz")]

    cycle_counts = []
    for pair in cycle_pairs:
        print(pair)
        counter, incoming = find_cycle(modules, *pair)
        incoming_mask_string = "0b0"
        inverse_mask_string = "0b0"
        for node in reversed(counter):
            incoming_mask_string += "1" if node in incoming else "0"
            inverse_mask_string += "0" if node in incoming else "1"
        incoming_mask = int(incoming_mask_string, 2)
        inverse_mask = int(inverse_mask_string, 2)
        print(incoming_mask_string, incoming_mask)
        print(inverse_mask_string, inverse_mask)

        state = 0
        first = -1
        second = -1
        for i in range(1, 100000):
            state += 1
            middle = (state & incoming_mask) | inverse_mask

            # if middle == 0b0111111111111:
            if state == incoming_mask:
                state += inverse_mask
                state -= 4095
                if first == -1:
                    first = i
                else:
                    second = i
                    break
        cycle_counts.append(second - first)
    print(cycle_counts)
    value = 1
    for x in cycle_counts:
        value *= x
    print(value)

    # print("gr", 7858 - 3929)
    # print("db", 7538 - 3769)
    # print("vc", 7726 - 3863)
    # print("lz", 8140 - 4078)
    #
    # print("idk", 3929 * 3769 * 3863 * 4078)


    # state = 0
    # for i in range(0, 100000, 2):
    #     state += 1
    #     middle = (state & 0b0111101011001) | 0b0000010100110
    #
    #     if middle == 0b0111111111111:
    #         print("Hit steps:", i)
    #         state += 2 ** 1 + 2 ** 2 + 2 ** 5 + 2 ** 7

def visualize_graph(modules):
    net = Network(height=900)

    for module in modules:
        module_type, targets = modules[module]
        match module_type:
            case "%":
                color = "red"
            case "&":
                color = "blue"
            case _:
                color = "green"
        net.add_node(module, module, color=color)

    net.add_node("rx", "rx", color="pink")

    for module in modules:
        module_type, targets = modules[module]
        for target in targets:
            net.add_edge(module, target, arrows="to")

    net.show("example.html", notebook=False)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)

    # print("\nVisualizing Part 2")
    # visualize_graph(data)

    print("\nPart 2")
    part_two(data)
