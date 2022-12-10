def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    instructions = [line.split(" ") for line in data_lines]
    for instruction in instructions:
        if len(instruction) > 1:
            instruction[1] = int(instruction[1])
    return instructions


def run_instructions(instructions):
    register = 1
    log = [1]

    for instruction in instructions:
        match instruction:
            case ["noop"]:
                log.append(register)
            case ["addx", value]:
                log.append(register)
                register += value
                log.append(register)

    return log


def print_special_signal_strengths(log):
    signal_strengths = [value * (index + 1) for index, value in enumerate(log)]
    signal_sum = signal_strengths[20 - 1] \
                 + signal_strengths[60 - 1] \
                 + signal_strengths[100 - 1] \
                 + signal_strengths[140 - 1] \
                 + signal_strengths[180 - 1] \
                 + signal_strengths[220 - 1]

    print("Signal Strengths:")
    print("  * 020:", log[20 - 1], signal_strengths[20 - 1])
    print("  * 060:", log[60 - 1], signal_strengths[60 - 1])
    print("  * 100:", log[100 - 1], signal_strengths[100 - 1])
    print("  * 140:", log[140 - 1], signal_strengths[140 - 1])
    print("  * 180:", log[180 - 1], signal_strengths[180 - 1])
    print("  * 220:", log[220 - 1], signal_strengths[220 - 1])
    print("  -------------------")
    print("  * Sum:", signal_sum)
    print()


def draw_crt(log: list[int]):
    for line in range(6):
        full_line = ""
        for pixel in range(40):
            register = log[line * 40 + pixel]
            if abs(register - pixel) <= 1:
                full_line += "██"
            else:
                full_line += "  "
        print(full_line)


if __name__ == '__main__':
    instructions = read_input()
    log = run_instructions(instructions)
    print_special_signal_strengths(log)
    draw_crt(log)
