import parsley


def read_input(filename):
    parser = parsley.makeGrammar("""
        number = <digit+>:ds -> int(ds)
        color = "blue" | "red" | "green"
        subset = ws number:number ws color:color -> (color, number) 
        set = subset:first ("," subset)*:sets ";"? -> [first] + sets
        game = ws "Game" ws number:id ":" (set+):sets -> (id, sets)
        input = game+:games ws end -> games
        """, {})

    with open(f"{filename}.txt", "r") as file:
        return parser(file.read()).input()


def part_one(games):
    valid_sum = 0

    max_allowed = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    for id, game in games:
        game_valid = True
        for game_set in game:
            for color, count in game_set:
                if max_allowed[color] < count:
                    game_valid = False
                    break
            if not game_valid:
                break
        if game_valid:
            valid_sum += id

    print("Sum of IDs of valid games:", valid_sum)


def part_two(games):
    total_power = 0
    for id, game in games:
        max_used = {
            "red": 0,
            "green": 0,
            "blue": 0
        }
        for game_set in game:
            for color, count in game_set:
                max_used[color] = max(max_used[color], count)

        game_power = max_used["red"] * max_used["green"] * max_used["blue"]
        total_power += game_power

    print("Sum of game powers:", total_power)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
