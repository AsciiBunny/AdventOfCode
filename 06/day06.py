def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    numbers = list(map(int, data_lines[0].split(",")))

    counts = [numbers.count(i) for i in range(0, 9)]
    print(counts)
    return counts


def generation(fishes):
    next_generation = [0] * 9

    for i in range(0, 8):
        next_generation[i] = fishes[i + 1]

    next_generation[6] += fishes[0]
    next_generation[8] += fishes[0]

    return next_generation


def simulate(fishes, generations):
    for i in range(0, generations):
        fishes = generation(fishes)
        print("Day", i + 1, ":", sum(fishes))

    return fishes

if __name__ == '__main__':
    fishes = read_input()
    simulate(fishes, 256)

