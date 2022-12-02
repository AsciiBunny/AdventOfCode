from collections import Counter

def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    polymer_string = data_lines[0]
    polymer= dict()
    for a, b in zip(polymer_string, polymer_string[1:]):
        polymer.setdefault(a + b, 0)
        polymer[a + b] += 1

    rules = [line.split(" -> ") for line in data_lines[2:]]
    rules = {pair: insert for pair, insert in rules}

    return polymer, rules, polymer_string


def step(polymer, rules):
    new_polymer = dict()
    for pair in polymer:
        a, b = pair
        if a + b in rules:
            new_polymer.setdefault(a + rules[a + b], 0)
            new_polymer[a + rules[a + b]] += polymer[a + b]
            new_polymer.setdefault(rules[a + b] + b, 0)
            new_polymer[rules[a + b] + b] += polymer[a + b]
        else:
            new_polymer.setdefault(a + b, 0)
            new_polymer[a + b] += polymer[a + b]
    return new_polymer


def count_elements(polymer, polymer_string):
    counts = dict()
    for pair in polymer:
        counts.setdefault(pair[0], 0)
        counts[pair[0]] += polymer[pair]

    counts[polymer_string[-1]] += 1

    return counts


if __name__ == '__main__':
    polymer, rules, polymer_string = read_input()
    print("Input is of size", len(polymer))

    # print("Rules:")
    # for key in rules:
    #     print("~", key, "->", rules[key])

    # print(polymer)

    for i in range(0, 40):
        polymer = step(polymer, rules)
        print("Step", i + 1, "| elements:", sum(polymer[element] for element in polymer))

    counts = count_elements(polymer, polymer_string)
    print("Value:", max(counts[element] for element in counts) - min(counts[element] for element in counts))