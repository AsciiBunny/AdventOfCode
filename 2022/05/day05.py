def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    structure, instructions = data_lines[:data_lines.index("")], data_lines[data_lines.index("")+1:]

    structure = [line[1::4] for line in structure]
    stacks = dict()
    for index, key in enumerate(structure[-1]):
        stack = stacks[key] = []
        for line in structure[:-1][::-1]:
            if index < len(line) and line[index] != " ":
                stack += [line[index]]

    instructions = [line.split(" ") for line in instructions]
    instructions = [(int(line[1]), line[3], line[5]) for line in instructions]

    return stacks, instructions


def run_instructions_9000(stacks, instructions):
    for instruction in instructions:
        count, before, after = instruction
        for _ in range(count):
            crate = stacks[before].pop()
            stacks[after].append(crate)

def run_instructions_9001(stacks, instructions):
    for instruction in instructions:
        count, before, after = instruction
        crates = stacks[before][-count:]
        stacks[before] = stacks[before][:-count]
        stacks[after] += crates


def fancy_print_stacks(stacks: dict[str,list[str]]):
    heights = [len(stack) for stack in stacks.values()]
    max_height = max(heights)
    for i in range(max_height, -1, -1):
        string = ""
        for stack in stacks.values():
            if len(stack) > i:
                string += f'[{stack[i]}] '
            else:
                string += '    '
        print(string)

    string = ""
    for key in stacks.keys():
        string += f" {key}  "
    print(string)


def print_stack_top(stacks):
    string = ""
    for stack in stacks.values():
        string += f'[{stack[-1]}] '
    string +=" | "
    for stack in stacks.values():
        string += stack[-1]
    print(string)


if __name__ == '__main__':
    stacks, instructions = read_input()
    fancy_print_stacks(stacks)
    run_instructions_9000(stacks, instructions)
    fancy_print_stacks(stacks)
    print_stack_top(stacks)

    stacks, instructions = read_input()
    run_instructions_9001(stacks, instructions)
    fancy_print_stacks(stacks)
    print_stack_top(stacks)

