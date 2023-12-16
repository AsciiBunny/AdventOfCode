import parsley


def read_input(filename):
    parser = parsley.makeGrammar("""
        number = ws <digit+>:ds -> int(ds)
        card = ws "Card" ws number:id ":" (number+):winners ws "|" (number+):numbers -> (id, winners, numbers)
        input = card+:cards ws end -> cards
        """, {})

    with open(f"{filename}.txt", "r") as file:
        return parser(file.read()).input()


def part_one(cards):
    points = 0
    for card in cards:
        winning_numbers = set(card[1]) & set(card[2])
        if len(winning_numbers) > 0:
            points += 2 ** (len(winning_numbers) - 1)

    print("Total points:", points)


def part_two(cards):
    card_counts = [1] * len(cards)
    for card_index, card in enumerate(cards):
        wins = len(set(card[1]) & set(card[2]))
        for i in range(card_index + 1, card_index + wins + 1):
            card_counts[i] += card_counts[card_index]

    print("Total card count:", sum(card_counts))


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
