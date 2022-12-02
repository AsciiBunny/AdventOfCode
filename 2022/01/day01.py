import numpy as np

def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()


    packs = np.array(data_lines)
    splits = np.nonzero(packs == "")[0]
    packs[splits] = 0
    packs = np.array(packs, dtype=int)
    packs = np.split(packs, splits)
    packs = [pack[1:] for pack in packs ]

    return packs


def find_largest(packs, count):
    sums = [np.sum(pack) for pack in packs]
    largest_index = np.argmax(sums)
    largest = sums[largest_index]
    print("The elf with most calories has ", largest,  " calories")
    largest_n = np.sum(np.sort(sums)[-count:])
    print("The", count, "elfs with most calories have", largest_n,  "calories together")


if __name__ == '__main__':
    packs = read_input()
    find_largest(packs, 3)
