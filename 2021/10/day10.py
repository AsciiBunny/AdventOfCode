openers = ["(", "[", "{", "<"]
closers = [")", "]", "}", ">"]
error_scores = [3, 57, 1197, 25137]
completion_scores = [1, 2, 3, 4]

closer_partners = dict(zip(closers, openers))
opener_partners = dict(zip(openers, closers))
closer_error_scores = dict(zip(closers, error_scores))
closer_completion_scores = dict(zip(closers, completion_scores))


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    return data_lines


def find_error(line):
    stack = []
    for character in line:
        if character in openers:
            stack.append(character)
        elif character in closers:
            if closer_partners[character] == stack[-1]:
                stack.pop()
            else:
                return character


def sum_errors(lines):
    errors = [find_error(line) for line in lines]
    errors = list(filter(lambda error: error != None, errors))
    scores = [closer_error_scores[error] for error in errors]
    return sum(scores)


def complete_line(line):
    stack = []
    for character in line:
        if character in openers:
            stack.append(character)
        elif character in closers:
            assert closer_partners[character] == stack[-1]
            stack.pop()

    to_add = []
    while (len(stack) > 0):
        to_add.append(opener_partners[stack.pop()])
    return to_add


def score_completion(completion):
    score = 0
    for character in completion:
        score *= 5
        score += closer_completion_scores[character]
    return score


def find_completion_score(inputs):
    completions = [complete_line(input) for input in inputs]
    scores = [score_completion(completion) for completion in completions]
    scores = sorted(scores)
    return scores[len(scores) // 2]

if __name__ == '__main__':
    inputs = read_input()
    print("Input is of size", len(inputs))

    print("Total error score:", sum_errors(inputs))

    incomplete_inputs = [line for line in inputs if find_error(line) is None]

    print("Middle completion score:", find_completion_score(incomplete_inputs))

