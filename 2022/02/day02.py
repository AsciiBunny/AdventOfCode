
win = {
    "A": "Y",
    "B": "Z",
    "C": "X"
}

lose = {
    "A": "Z",
    "B": "X",
    "C": "Y"
}

draw = {
    "A": "X",
    "B": "Y",
    "C": "Z"
}

value = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

choose = {
    "X": lose,
    "Y": draw,
    "Z": win
}


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    rounds = [line.split(" ") for line in data_lines]
    return rounds


def score_round(round, debug=False):
    score = value[round[1]]

    if round[1] == win[round[0]]:
        score += 6
    if round[1] == draw[round[0]]:
        score += 3
    if round[1] == win[round[0]]:
        score += 0

    if debug:
        print("Playing", round[1], "against", round[0], "for", score, "points")

    return score


def decide_round(round):
    action = choose[round[1]]
    return [round[0], action[round[0]]]


if __name__ == '__main__':
    rounds = read_input()
    scores = [score_round(round) for round in rounds]
    print("Total score for direct moves is", sum(scores), "points")

    strategy = [decide_round(round) for round in rounds]
    strategy_scores = [score_round(round) for round in strategy]
    print("Total score for strategy is", sum(strategy_scores), "points")
