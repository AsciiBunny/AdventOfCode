import json
from itertools import permutations
from math import floor, ceil


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    data = list(map(json.loads, data_lines))
    return data


class Snailfish:
    parent: any
    left: any = None
    right: any = None
    depth: int

    def __init__(self, parent, left, right, depth=0):
        self.parent = parent

        if isinstance(left, list):
            self.left = Snailfish(self, left[0], left[1], depth + 1)
        elif isinstance(left, Snailfish):
            self.left = left
            left.set_depth(depth + 1)
            left.parent = self
        else:
            self.left = left

        if isinstance(right, list):
            self.right = Snailfish(self, right[0], right[1], depth + 1)
        elif isinstance(right, Snailfish):
            self.right = right
            right.set_depth(depth + 1)
            right.parent = self
        else:
            self.right = right

        self.depth = depth

    def is_left_snailfish(self):
        return isinstance(self.left, Snailfish)

    def is_right_snailfish(self):
        return isinstance(self.right, Snailfish)

    def increase_depth(self, depth=1):
        self.depth += depth
        if self.is_left_snailfish():
            self.left.increase_depth()
        if self.is_right_snailfish():
            self.right.increase_depth()

    def set_depth(self, depth: int):
        self.depth = depth
        if self.is_left_snailfish():
            self.left.set_depth(depth + 1)
        if self.is_right_snailfish():
            self.right.set_depth(depth + 1)

    def magnitude(self):
        left_magnitude = self.left.magnitude() if self.is_left_snailfish() else self.left
        right_magnitude = self.right.magnitude() if self.is_right_snailfish() else self.right
        return 3 * left_magnitude + 2 * right_magnitude

    def add(self, other):
        self.increase_depth()
        other.increase_depth()
        new = Snailfish(None, self, other, 0)
        new.reduce()
        return new

    def reduce(self):
        did_explode = did_split = True

        while did_explode or did_split:
            did_explode = did_split = False
            for sf in deep_traverse_snailfish(self):
                if sf.depth == 4:
                    sf.explode()
                    did_explode = True
                    break

            if (did_explode):
                continue

            for sf in deep_traverse_snailfish(self):
                if not sf.is_left_snailfish() and sf.left > 9:
                    sf.split_left()
                    did_split = True
                    break
                elif not sf.is_right_snailfish() and sf.right > 9:
                    sf.split_right()
                    did_split = True
                    break

    def explode(self):
        self.explode_left()
        self.explode_right()

        if self.parent.left == self:
            self.parent.left = 0
        elif self.parent.right == self:
            self.parent.right = 0

    def explode_left(self):
        child = self
        parent: Snailfish = self.parent
        while parent.left == child:
            if parent.parent == None:
                return

            child = parent
            parent = parent.parent

        if parent.is_left_snailfish():
            parent = parent.left
        else:
            parent.left += self.left
            return

        while parent.is_right_snailfish():
            parent = parent.right

        parent.right += self.left

    def explode_right(self):
        child = self
        parent: Snailfish = self.parent
        while parent.right == child:
            if parent.parent == None:
                return

            child = parent
            parent = parent.parent

        if parent.is_right_snailfish():
            parent = parent.right
        else:
            parent.right += self.right
            return

        while parent.is_left_snailfish():
            parent = parent.left

        parent.left += self.right

    def split_left(self):
        self.left = Snailfish(self, floor(self.left / 2), ceil(self.left / 2), self.depth + 1)

    def split_right(self):
        self.right = Snailfish(self, floor(self.right / 2), ceil(self.right / 2), self.depth + 1)

    def __str__(self):
        return "<" + str(self.left) + ", " + str(self.right) + ">"


def deep_traverse_snailfish(sf: Snailfish):
    if sf.is_left_snailfish():
        for left_child in deep_traverse_snailfish(sf.left):
            yield left_child
    yield sf
    if sf.is_right_snailfish():
        for right_child in deep_traverse_snailfish(sf.right):
            yield right_child


def add_snailfishes(sfs: list[Snailfish]):
    sum = sfs[0]
    for sf in sfs[1:]:
        sum = sum.add(sf)

    return sum


def find_highest_magnitude(sfs):
    highest_magnitude = 0
    for a, b in permutations(sfs, 2):
        pair = Snailfish(None, a, b, 0)
        pair.reduce()
        highest_magnitude = max(highest_magnitude, pair.magnitude())
    return highest_magnitude


if __name__ == '__main__':
    data = read_input()

    fishes = [Snailfish(None, *input) for input in data]
    total = add_snailfishes(fishes)
    print("Sum:", total)
    print("Magnitude:", total.magnitude())
    print("Highest Pair Magnitude:", find_highest_magnitude(data))
