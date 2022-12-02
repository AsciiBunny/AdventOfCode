def read_input():
    data_file = open("input.txt", "r")
    data_list = data_file.read().splitlines()
    return data_list


def parse_binary(digits):
    return int(''.join(digits), 2)


def calculate_diagnostic(data):
    split = [x for x in zip(*data)]
    counts = [(digit.count("0"), digit.count("1")) for digit in split]
    gamma = ["1" if count[0] < count[1] else "0" for count in counts]
    epsilon = ["0" if count[0] < count[1] else "1" for count in counts]
    return parse_binary(gamma), parse_binary(epsilon)


def oxygen_filter_identifier(zeroes, ones):
    return "1" if zeroes <= ones else "0"


def CO2_filter_identifier(zeroes, ones):
    return "0" if zeroes <= ones else "1"


def calculate_life_support(data, filter_identifier):
    lines = data

    for index in range(len(data[0])):
        split = [x for x in zip(*lines)]
        counts = (split[index].count("0"), split[index].count("1"))
        filter_digit = filter_identifier(*counts)
        lines = list(filter(lambda digits: digits[index] ==  filter_digit, lines))
        if len(lines) == 1:
            break

    return parse_binary(lines[0])

if __name__ == '__main__':
    data = read_input()

    gamma, epsilon = calculate_diagnostic(data)
    print("Gamma:", gamma)
    print("Epsilon:", epsilon)
    print("Value One:", gamma * epsilon)

    oxygen = calculate_life_support(data, oxygen_filter_identifier)
    co2 = calculate_life_support(data, CO2_filter_identifier)
    print("Oxygen:", oxygen)
    print("CO2:", co2)
    print("Value Two:", oxygen * co2)
