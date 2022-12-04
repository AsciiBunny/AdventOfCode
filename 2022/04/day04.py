from dataclasses import dataclass

@dataclass
class Elf:
    start: int
    end: int

    def contains(self, other: 'Elf'):
        return other.start >= self.start and other.end <= self.end

    def overlaps(self, other: 'Elf'):
        return not (other.start > self.end or other.end < self.start)


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    pairs = [line.split(",") for line in data_lines]
    pairs = [(a.split("-"), b.split("-")) for a, b in pairs]
    pairs = [(Elf(int(a[0]), int(a[1])), Elf(int(b[0]), int(b[1]))) for a, b in pairs]
    return pairs


def count_containments(pairs: list[tuple[Elf, Elf]]):
    count = 0
    for pair in pairs:
        if pair[0].contains(pair[1]) or pair[1].contains(pair[0]):
            count += 1
    return count


def count_overlaps(pairs: list[tuple[Elf, Elf]]):
    count = 0
    for pair in pairs:
        if pair[0].overlaps(pair[1]):
            count += 1
    return count


if __name__ == '__main__':
    pairs = read_input()
    containments = count_containments(pairs)
    overlaps = count_overlaps(pairs)
    print(containments, "pairs have a containment")
    print(overlaps, "pairs have an overlap")
