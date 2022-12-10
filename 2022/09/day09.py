import numpy as np


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    movements = [(line.split(" ")[0], int(line.split(" ")[1])) for line in data_lines]
    return movements


def get_instruction_direction(instruction: tuple[str, int]):
    dir = (0, 0)
    match instruction:
        case ("U", _):
            dir = (0, 1)
        case ("D", _):
            dir = (0, -1)
        case ("L", _):
            dir = (-1, 0)
        case ("R", _):
            dir = (1, 0)
    return dir


def move(direction: tuple[int, int], head_position: tuple[int, int], tail_positions: list[tuple[int, int]], positions: set[tuple[int, int]]):
    head_position = (head_position[0] + direction[0], head_position[1] + direction[1])

    parent_position = head_position
    for index, tail_position in enumerate(tail_positions):
        tail_x_position, tail_y_position = tail_position
        if abs(parent_position[0] - tail_position[0]) > 1 or abs(parent_position[1] - tail_position[1]) > 1:
            tail_x_position += np.sign(parent_position[0] - tail_position[0])
            tail_y_position += np.sign(parent_position[1] - tail_position[1])
            tail_positions[index] = (tail_x_position, tail_y_position)
        parent_position = tail_positions[index]

    positions.add(tail_positions[-1])

    return head_position, tail_positions


def do_moves(instructions, knot_count):
    h_pos = (0, 0)
    t_pos = [(0, 0)] * knot_count
    positions = {(0, 0)}

    for instruction in instructions:
        direction = get_instruction_direction(instruction)
        count = instruction[1]
        for _ in range(count):
            h_pos, t_pos = move(direction, h_pos, t_pos, positions)

    return positions


if __name__ == '__main__':
    instructions = read_input()
    positions = do_moves(instructions, 1)
    print("Tail has been in", len(positions), "different positions with", 1, "knots")
    positions = do_moves(instructions, 9)
    print("Tail has been in", len(positions), "different positions with", 9, "knots")

