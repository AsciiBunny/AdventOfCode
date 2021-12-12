def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    numbers = list(map(int, data_lines[0].split(",")))

    data_lines = data_lines[2:]
    boards = list(divide_chunks(data_lines, 6))
    boards = [board[:5] for board in boards]
    boards = [[list(divide_chunks(row, 3)) for row in board] for board in boards]
    boards = [[[int(value.strip()) for value in row] for row in board] for board in boards]

    return numbers, boards


def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def check_board(board):
    for i in range(0, 5):
        if board[i].count("Mark") == 5:
            return True


def check_bingo(board):
    return check_board(board) or check_board(list(zip(*board)))


def play_bingo(numbers, boards):
    for number in numbers:
        # Replace all occurrences of value with True
        boards = [[["Mark" if value == number else value for value in row] for row in board] for board in boards]

        for board in boards:
            if check_bingo(board):
                return number, board


def calculate_bingo_value(number, board):
    board = [[0 if value == "Mark" else value for value in row] for row in board]
    board_sum = sum(sum(row) for row in board)
    return number * board_sum


def play_losing_bingo(numbers, boards):
    for number in numbers:
        # Replace all occurrences of value with True
        boards = [[["Mark" if value == number else value for value in row] for row in board] for board in boards]

        if len(boards) == 1 and check_bingo(boards[0]):
            return number, boards[0]

        boards = list(filter(lambda board: not check_bingo(board), boards))


if __name__ == '__main__':
    numbers, boards = read_input()
    winning_number, winning_board = play_bingo(numbers, boards)
    print("Winning Number:", winning_number)
    print("Winning Board:", winning_board)
    print("Winning Board Value:", calculate_bingo_value(winning_number, winning_board))

    losing_number, losing_board = play_losing_bingo(numbers, boards)
    print("Losing Number:", losing_number)
    print("Losing Board:", losing_board)
    print("Losing Board Value:", calculate_bingo_value(losing_number, losing_board))
