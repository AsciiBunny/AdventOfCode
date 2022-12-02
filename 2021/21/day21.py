from dataclasses import dataclass

import numpy as np


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    start_1 = int(data_lines[0][data_lines[0].find(":") + 2:])
    start_2 = int(data_lines[1][data_lines[1].find(":") + 2:])
    return start_1, start_2


def gen_deterministic_die(max: int):
    i = 0

    while True:
        yield i + 1
        i = (i + 1) % max


def deterministic_die(start_1, start_2):
    player1_pos = start_1 - 1
    player2_pos = start_2 - 1

    player1_score = 0
    player2_score = 0

    current = "PLAYER 1"

    dice = gen_deterministic_die(100)
    throws = 0
    while True:
        throw = next(dice) + next(dice) + next(dice)
        throws += 3
        if current == "PLAYER 1":
            player1_pos = (player1_pos + throw) % 10
            player1_score += player1_pos + 1
            current = "PLAYER 2"
        elif current == "PLAYER 2":
            player2_pos = (player2_pos + throw) % 10
            player2_score += player2_pos + 1
            current = "PLAYER 1"
        else:
            print("It broke")
            break

        if player1_score >= 1000 or player2_score >= 1000:
            print("Player 1 Score:", player1_score)
            print("Player 2 Score:", player2_score)
            print("Throws:", throws)
            print("Solution:", throws * min([player1_score, player2_score]))
            break


@dataclass(frozen=True)
class DiracState:
    position_1: int
    score_1: int
    position_2: int
    score_2: int
    is_turn_1: bool # "PLAYER 1" or "PLAYER 2"


def get_dirac_wins(dice_values, states, state):
    if state in states:
        return states[state]

    if state.score_1 >= 21:
        return 1, 0
    elif state.score_2 >= 21:
        return 0, 1

    total_wins_1 = 0
    total_wins_2 = 0

    for throw in dice_values:
        count = dice_values[throw]

        if state.is_turn_1:
            new_position = (state.position_1 + throw) % 10
            new_score = state.score_1 + new_position + 1
            new_state = DiracState(new_position, new_score, state.position_2, state.score_2, False)
        else:
            new_position = (state.position_2 + throw) % 10
            new_score = state.score_2 + new_position + 1
            new_state = DiracState(state.position_1, state.score_1, new_position, new_score, True)

        assert new_state.is_turn_1 != state.is_turn_1

        wins_1, wins_2 = get_dirac_wins(dice_values, states, new_state)

        total_wins_1 = total_wins_1 + (wins_1 * count)
        total_wins_2 = total_wins_2 + (wins_2 * count)

    states[state] = (total_wins_1, total_wins_2)
    return total_wins_1, total_wins_2


def dirac_die(start_1, start_2):
    dice_values = dict()
    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                dice_values[a + b + c] = dice_values.get(a + b + c, 0) + 1

    states = dict()
    start_state = DiracState(start_1 - 1, 0, start_2 - 1, 0, True)
    wins_1, wins_2 = get_dirac_wins(dice_values, states, start_state)
    print("Total wins for Player 1:", wins_1)
    print("Total wins for Player 2:", wins_2)



if __name__ == '__main__':
    start_1, start_2 = read_input()

    deterministic_die(start_1, start_2)
    dirac_die(start_1, start_2)
