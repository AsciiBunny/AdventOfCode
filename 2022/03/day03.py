def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    return data_lines


def split(packs):
    return [(line[:len(line)//2], line[len(line)//2:]) for line in packs]


def find_duplicate(split_pack):
    front = set(split_pack[0])
    back = set(split_pack[1])
    duplicate = front & back
    assert len(duplicate) == 1
    return duplicate.pop()


def find_duplicate_triplet(pack_a, pack_b, pack_c):
    set_a = set(pack_a)
    set_b = set(pack_b)
    set_c = set(pack_c)
    duplicate = set_a & set_b & set_c
    assert len(duplicate) == 1
    return duplicate.pop()


def get_priority(item:str):
    priority = ord(item)

    if item.islower():
        priority -= ord('a')
        priority += 1 # index starts at 1

    if item.isupper():
        priority -= ord('A')
        priority += 26
        priority += 1 # index starts at 1

    return priority


if __name__ == '__main__':
    packs = read_input()

    # Part 1
    split_packs = split(packs)
    duplicates = list(map(find_duplicate, split_packs))
    priorities = list(map(get_priority, duplicates))
    print("Sum of priorities:", sum(priorities))

    # Part 2
    groups = [packs[i:i+3] for i in range(0, len(packs), 3)]
    badges = [find_duplicate_triplet(*group) for group in groups]
    badge_priorities = list(map(get_priority, badges))
    print("Sum of badge priorities:", sum(badge_priorities))
