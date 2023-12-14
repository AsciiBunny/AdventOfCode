def read_input(filename):
    data_file = open(f"{filename}.txt", "r")
    data_lines = data_file.read().splitlines()
    return data_lines

numbers = set(str(number) for number in range(10))
number_names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def part_one(lines: list[str]):
    # Filter out all non-digit characters
    filtered_lines = ["".join(x for x in line if x in numbers) for line in lines]
    calibration_values = [int(line[0] + line[-1]) for line in filtered_lines]

    calibration_sum = sum(calibration_values)
    print("Calibration sum:", calibration_sum)


def part_two(lines: list[str]):
    new_lines = []
    # Build new filtered lines with original digits and converted names, new_line only contains digits now
    for line in lines:
        new_line = ""
        # Keep removing first character until line is empty, check starting character(s) for digits or names
        for i in range(len(line)):
            sub_line = line[i:]
            if sub_line[0] in numbers:
                new_line += sub_line[0]
                continue

            for number_index in range(len(number_names)):
                if sub_line.startswith(number_names[number_index]):
                    new_line += str(number_index)
        new_lines.append(new_line)

    # Feed filtered data into solution for part 1
    part_one(new_lines)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
