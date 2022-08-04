from dataclasses import dataclass

import numpy as np

@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)


Scanner = set[Point]

def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    data_lines = np.array(data_lines)

    scanners_raw = np.split(data_lines, np.where(data_lines == "")[0])[1:]
    scanners = [[Point(*map(int, line.split(","))) for line in scanner[2:]] for scanner in scanners_raw]
    scanners = [set(points) for points in scanners]

    return scanners

def rotate_clockwise_around_x(point: Point) -> Point:
    return Point(point.x, point.z, -point.y)

def rotate_clockwise_around_z(point: Point) -> Point:
    return Point(point.y, -point.x, point.z)

def rotate_clockwise_around_y(point: Point) -> Point:
    return Point(point.z, point.y, -point.x)

def rotate_scanner(scanner: Scanner, func) -> Scanner:
    return set(map(func, scanner))

def translate_scanner(scanner: Scanner, translation: Point) -> Scanner:
    return set(point + translation for point in scanner)

def clone_point(point: Point):
    return point + Point(0,0,0)

def call_multiple(funcs):
    def function(point: Point):
        for func in funcs:
            point = func(point)
        return point
    return function

rotation_pattern = [
    clone_point,
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,

    call_multiple([rotate_clockwise_around_z, rotate_clockwise_around_y]),
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,

    call_multiple([rotate_clockwise_around_z, rotate_clockwise_around_y]),
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,

    call_multiple([rotate_clockwise_around_z, rotate_clockwise_around_y]),
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,

    call_multiple([rotate_clockwise_around_z, rotate_clockwise_around_x]),
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,

    call_multiple([rotate_clockwise_around_z, rotate_clockwise_around_x, rotate_clockwise_around_x]),
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,
    rotate_clockwise_around_z,
]

def compare_scanners(a: Scanner, b: Scanner):
    r = b
    for rotation in rotation_pattern:
        r = rotate_scanner(r, rotation)

        # for each pair of points from a and r
        for pa in a:
            for pr in r:
                # translate r to align point pair
                diff = pa - pr
                t = translate_scanner(r, diff)

                # t and a should now have at least 12 beacons in common
                common = a & t
                if len(common) >= 12:
                    # Return the new superset of aligned points
                    return a | t, diff


def find_pair(super: Scanner, scanners: list[Scanner]):
    for other in scanners:
        comparison = compare_scanners(super, other)
        if comparison:
            super, translation = comparison
            return super, other, translation
    return super, False, Point(0,0,0)


if __name__ == '__main__':
    scanners = read_input()

    super = scanners.pop(0)
    print(len(super), super)

    translations = []

    while len(scanners) > 0:
        super, found, translation = find_pair(super, scanners)
        scanners.remove(found)
        translations.append(translation)
        print(len(super), super)

    print(f"A total of {len(super)} Beacons were found, using {len(translations)} Scanners")

    distances = [a - b for a in translations for b in translations if a != b]
    manhattans = [abs(d.x) + abs(d.y) + abs(d.z) for d in distances]

    print(f"Largest manhattan distance between scanners is {max(manhattans)}")








