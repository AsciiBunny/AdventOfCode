from itertools import pairwise


def read_input():
    data_file = open("input.txt", "r")
    data_list = data_file.read().splitlines()
    data_numbers = list(map(int, data_list))
    return data_numbers


# Part 1
def count_increases(data):
    pairs = pairwise(data)
    increases = [y - x > 0 for (x, y) in pairs]
    return sum(increases)

# Part 2
def count_aggregated_increases(data):
    triples = zip(data, data[1:], data[2:])
    sums = [sum(a) for a in triples]
    return count_increases(sums)


if __name__ == '__main__':
    data = read_input()
    print(count_increases(data))
    print(count_aggregated_increases(data))
