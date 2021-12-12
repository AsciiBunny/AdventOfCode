from itertools import groupby


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    data_pairs = list(map(str.split, data_lines))
    data_values = [(action, int(value)) for [action, value] in data_pairs]
    return data_values


def sum_actions(data):
    sorted_data = sorted(data)
    sums = {}
    for key, group in groupby(sorted_data, lambda x: x[0]):
        sums[key] = sum(value for (action, value) in group)
    return sums


def simulate_actions(data):
    depth = aim = horizontal = 0
    for direction, value in data:
        match direction:
            case "down":
                aim += value
            case "up":
                aim -= value
            case "forward":
                horizontal += value
                depth += value * aim
    return {
        "depth": depth,
        "aim": aim,
        "horizontal": horizontal
    }


if __name__ == '__main__':
    data = read_input()

    sums = sum_actions(data)
    depth = sums['down'] - sums['up']
    print("## Part 1 ##")
    print("Depth:", depth)
    print("Horizontal:", sums["forward"])
    print("Answer:", sums["forward"] * depth)

    results = simulate_actions(data)
    print("## Part 2 ##")
    print("Depth:", results["depth"])
    print("Horizontal:", results["horizontal"])
    print("Answer:", results["horizontal"] * results["depth"])
