from itertools import combinations
from dataclasses import dataclass
import numpy as np


@dataclass
class Point:
    x: int
    y: int


@dataclass
class Vent:
    start: Point
    end: Point


def read_input() -> list[Vent]:
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    numbers = [line.split(" -> ") for line in data_lines]
    vents = list(map(read_pair, numbers))
    print("Loaded", len(vents), "vents")
    return vents


def read_pair(line: list[str]) -> Vent:
    ax, ay = line[0].split(",")
    bx, by = line[1].split(",")

    ax, ay = int(ax), int(ay)
    bx, by = int(bx), int(by)

    if ax == bx and ay > by:
        ay, by = by, ay
    elif ay == by and ax > bx:
        ax, bx = bx, ax

    return Vent(Point(ax, ay), Point(bx, by))


def generate_empty_image(vents: list[Vent]):
    width: int = max(vent.end.x for vent in vents) + 1
    height: int = max(vent.end.y for vent in vents) + 1
    return np.zeros(shape=(width, height))


def is_horizontal(vent: Vent) -> bool:
    return vent.start.y == vent.end.y


def is_vertical(vent: Vent) -> bool:
    return vent.start.x == vent.end.x


def is_orthogonal(vent: Vent) -> bool:
    return is_horizontal(vent) or is_vertical(vent)


def is_diagonal(vent: Vent) -> bool:
    return abs(vent.start.x - vent.end.x) == abs(vent.start.y - vent.end.y)


def is_valid(vent: Vent) -> bool:
    return is_orthogonal(vent) or is_diagonal(vent)


def generate_diagram(vents):
    ocean_floor = generate_empty_image(vents)
    for vent in vents:
        if is_horizontal(vent):
            y = vent.start.y
            for x in range(vent.start.x, vent.end.x + 1):
                ocean_floor[x][y] += 1
        if is_vertical(vent):
            x = vent.start.x
            for y in range(vent.start.y, vent.end.y + 1):
                ocean_floor[x][y] += 1
        if is_diagonal(vent):
            x_sign = np.sign(vent.end.x - vent.start.x)
            x_range = range(vent.start.x, vent.end.x + x_sign, x_sign)
            y_sign = np.sign(vent.end.y - vent.start.y)
            y_range = range(vent.start.y, vent.end.y + y_sign, y_sign)
            for x, y in zip(x_range, y_range):
                ocean_floor[x][y] += 1
    return ocean_floor


def find_overlaps(ocean_floor):
    overlap = ocean_floor > 1
    return overlap.sum()


if __name__ == '__main__':
    vents = read_input()
    vents = list(filter(is_valid, vents))
    print(*zip(range(0, -5, -1), range(10, 15)))

    orthogonal_vents = list(filter(is_orthogonal, vents))
    orthogonal_ocean_floor = generate_diagram(orthogonal_vents)
    print("Orthogonal Overlaps:", find_overlaps(orthogonal_ocean_floor))

    ocean_floor = generate_diagram(vents)
    print("Total Overlaps:", find_overlaps(ocean_floor))
