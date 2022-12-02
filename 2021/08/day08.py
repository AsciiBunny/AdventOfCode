def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    inputs = [line[0: line.index(" | ")] for line in data_lines]
    inputs = [[set(word) for word in line.split()] for line in inputs]

    outputs = [line[line.index(" | ") + 3:] for line in data_lines]
    outputs = [[set(word) for word in line.split()] for line in outputs]

    return inputs, outputs


def print_digit(display, digit):
    display = list(map(lambda char: char if char in digit else '.', display))
    print('.' + display[0] * 4 + '.')
    print(display[1] + ' ' * 4 + display[2])
    print(display[1] + ' ' * 4 + display[2])
    print('.' + display[3] * 4 + '.')
    print(display[4] + ' ' * 4 + display[5])
    print(display[4] + ' ' * 4 + display[5])
    print('.' + display[6] * 4 + '.')


def count_digits(outputs):
    lengths = [[len(word) for word in line] for line in outputs]
    total = sum(sum(1 for _ in filter(lambda word: word in [2, 3, 4, 7], line)) for line in lengths)
    return total


def solve(input: list[set[str]]):
    digits = dict()
    digits['1'] = next(filter(lambda digit: len(digit) == 2, input))
    digits['4'] = next(filter(lambda digit: len(digit) == 4, input))
    digits['7'] = next(filter(lambda digit: len(digit) == 3, input))
    digits['8'] = next(filter(lambda digit: len(digit) == 7, input))

    digits['6'] = next(filter(lambda digit: len(digit) == 6 and len(digit & digits['1']) == 1, input))
    digits['9'] = next(filter(lambda digit: len(digit) == 6 and len(digit - digits['4']) == 2, input))
    digits['0'] = next(filter(lambda digit: len(digit) == 6 and digit != digits['6'] and digit != digits['9'], input))

    input_left = list(filter(lambda digit: len(digit) == 5, input))

    digits['2'] = next(filter(lambda digit: len(digit - digits['9']) == 1, input_left))
    digits['3'] = next(filter(lambda digit: len(digit - digits['2']) == 1, input_left))
    digits['5'] = next(filter(lambda digit: len(digit - digits['2']) == 2, input_left))

    return digits


def generate_display(digits):
    display = ['?'] * 7

    display[0] = (digits['7'] - digits['1']).pop()
    display[1] = (digits['5'] - digits['3']).pop()
    display[2] = (digits['8'] - digits['6']).pop()
    display[3] = (digits['9'] - digits['0']).pop()
    display[4] = (digits['8'] - digits['9']).pop()
    display[5] = (digits['3'] - digits['2']).pop()
    display[6] = (digits['9'] - digits['4'] - digits['7']).pop()

    return  display


def translate(digits, output):
    output_string = ""
    for word in output:
        for char in digits:
            if word == digits[char]:
                output_string += char
                break

    return int(output_string)


def solve_all(inputs, outputs):
    values = []
    for input, output in zip(inputs, outputs):
        digits = solve(input)
        values += [translate(digits, output)]
    return values


if __name__ == '__main__':
    inputs, outputs = read_input()
    print(count_digits(outputs), "identifiable digits in output data")

    print(sum(solve_all(inputs, outputs)))


