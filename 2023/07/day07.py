import parsley


def read_input(filename):
    parser = parsley.makeGrammar("""
        number = ws <digit+>:ds -> int(ds)
        cards = letterOrDigit{5}
        hand = ws cards:cards ws number:bid -> (cards, bid)
        input = hand+:hands ws end -> hands
        """, {})

    with open(f"{filename}.txt", "r") as file:
        parsed = parser(file.read()).input()
        for hand, bid in parsed:
            for i, card in enumerate(hand):
                hand[i] = card_values[card]
        return parsed


card_values = {
    "*": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def get_hand_type(cards: list[int]):
    counts = [0] * 14
    for card in cards:
        counts[card - 1] += 1
    jokers = counts[0]
    counts = counts[1:]
    counts.sort(reverse=True)
    counts[0] += jokers
    return counts[:2]


def hand_to_key(hand: tuple[list[int], int]):
    return get_hand_type(hand[0]) + hand[0]


def part_one(hands):
    hands = sorted(hands, key=hand_to_key)
    total_winnings = 0
    for i, (cards, bid) in enumerate(hands):
        total_winnings += bid * (i + 1)
    print("Total winnings:", total_winnings)

def part_two(hands):
    for cards, bid in hands:
        for i, card in enumerate(cards):
            if card == 11:
                cards[i] = 1
    print("Remapped all J[11] to *[1]")
    part_one(hands)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
