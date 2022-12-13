import functools


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    lines = [parse_line(line) for line in data_lines if line != ""]
    pairs = list(zip(lines[0::3], lines[1::3]))
    return lines, pairs


def parse_line(line):
    root = []
    stack: list[list | int] = [root]
    number = []
    for char in line[1: -1]:
        if char == ",":
            if len(number) > 0:
                stack[-1].append(int("".join(number)))
                number.clear()
        if char.isnumeric():
            number.append(char)
        if char == "[":
            stack.append([])
        if char == "]":
            if len(number) > 0:
                stack[-1].append(int("".join(number)))
                number.clear()
            done = stack.pop()
            stack[-1].append(done)

    if len(number) > 0:
        stack[-1].append(int("".join(number)))
        number.clear()

    return root


def compare_packets(left, right):
    # print("Compare", left, "against", right)
    if type(left) == int and type(right) == int:
        if left == right:
            return
        return left < right
    if type(left) == list and type(right) == int:
        return compare_packets(left, [right])
    if type(left) == int and type(right) == list:
        return compare_packets([left], right)

    assert type(left) == list and type(right) == list

    # Do all possible comparisons first
    for left_val, right_val in zip(left, right):
        result = compare_packets(left_val, right_val)
        if not result and result is not None:
            return False
        if result:
            return True

    # Zip only makes complete pairs so check lengths now for any remaining singles
    if len(left) < len(right):
        return True
    if len(left) > len(right):
        return False


def print_pairs(pairs):
    for left, right in pairs:
        print(left)
        print(right)
        print()


if __name__ == '__main__':
    lines, pairs = read_input()
    # print_pairs(pairs)
    results = [compare_packets(*pair) for pair in pairs]
    correct_pairs = [index + 1 for index, result in enumerate(results) if result]
    print("Sum of indices of correct packet-pairs:", sum(correct_pairs))

    divisorA = [[2]]
    divisorB = [[6]]
    lines.append(divisorA)
    lines.append(divisorB)

    def compare(left, right):
        result = compare_packets(left, right)
        return -1 if result else (0 if result is None else 1)
    lines.sort(key=functools.cmp_to_key(compare))
    print("index of [[2]]", lines.index(divisorA) + 1)
    print("index of [[6]]", lines.index(divisorB) + 1)
    print("decoder key:", (lines.index(divisorA) + 1) * (lines.index(divisorB) + 1))



