import math

import parsley


def read_input(filename):
    parser = parsley.makeGrammar("""
        number = ws <digit+>:ds -> int(ds)
        times = "Time:" (number+):times -> times
        distances = "Distance:" (number+):distances -> distances
        input = times:a ws distances:b ws end -> (a,b)
        """, {})

    with open(f"{filename}.txt", "r") as file:
        return parser(file.read()).input()


def part_one(races):
    count_product = 1
    races = list(zip(*races))
    for time, distance in races:
        print("time:", time, "   record:",distance)
        count = 0
        for pushed in range(time):
            reached = (time - pushed) * pushed
            if reached > distance:
                count += 1
                print("x", end="")
            else:
                print("-", end="")
        print("\n")
        count_product *= count
    print("winning count product:", count_product)


def part_two(races):
    time = int("".join(str(x) for x in races[0]))
    record = int("".join(str(x) for x in races[1]))

    print("time:", time, "   record:", record)

    a = -1
    b = time
    c = - record
    root = math.sqrt(b * b - (4 * a * c))
    minus = (-b - root) / (2 * a)
    plus = (-b + root) / (2 * a)

    range_start = math.ceil(min(minus, plus))
    range_end = math.floor(max(minus, plus))

    print("winning range:",range_start, " -> ", range_end)
    print("winning range size:", range_end - range_start + 1)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
