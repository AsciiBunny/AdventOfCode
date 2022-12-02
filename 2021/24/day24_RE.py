import json

def persist_to_file(file_name):

    def decorator(original_func):
        try:
            cache = json.load(open(file_name, 'r'))
        except (IOError, ValueError):
            cache = {}

        def new_func(param):
            if "data" not in cache:
                cache["data"] = original_func(param)
                json.dump(cache, open(file_name, 'w'))
            return cache["data"]

        return new_func

    return decorator


def digits(number: int):
    digits = [int(a) for a in str(number)]
    for digit in digits:
        yield digit


def cycle(output, digit, magic):
    a, b, c = magic

    x = (output % 26) + b

    # a = 1 | 26
    output //= a

    if  x != digit:
        output *= 26
        output += digit + c

    return output

def cycle2(output, digit, magic):
    a, b, c = magic

    # inp w
    w = digit

    # mul x 0
    # add x z
    # mod x 26
    # add x 13
    x = (output % 26) + b

    # div z 1
    output //= a

    # eql x w
    # eql x 0
    x = 0 if x == w else 1

    # mul y 0
    # add y 25
    # mul y x
    # add y 1
    # mul z y
    y = 25 * x + 1
    output *= y

    # mul y 0
    # add y w
    # add y 3
    # mul y x
    # add z y
    y = w + c
    output += y * x

    return output


def naivesearch(magic):
    for i in range(99999999999999, 10000000000000, -1):
        if "0" in str(i):
            print("skip", i)
            continue
        if i % 100000 == 9:
            print(i)

        digit = digits(i)
        output = 0
        for pair in magic:
            output = cycle(output, next(digit), pair)
        if output == 0:
            print("Winner:", i)


def deep(output, digit, magic, depth):
    if magic[depth][0] == 26 and (output % 26) + magic[depth][1] != digit:
        return False

    output = cycle(output, digit, magic[depth])

    if output == 0 and depth == 13:
        return str(digit)
    elif depth == 13:
        return False

    #for i in range(9, 0, -1):
    for i in range(1, 10):
        result = deep(output, i, magic, depth + 1)
        if result != False:
            return str(digit) + result

    return False

def deepbase(magic):
    output = 0
    #for i in range(9, 0, -1):
    for i in range(1, 10):
        result = deep(output, i, magic, 0)
        if result != False:
            print(result)
            break


#@persist_to_file("state_space_simple.json")
def construct_state_space(magic):
    valid = [set()] * 14
    valid_z = [0]

    for depth in range(13, -1, -1):
        for digit in range(1, 10):
            for z in range(0, 1000000):
                out = cycle(z, digit, magic[depth])
                if out in valid_z:
                    valid[depth].add(z)

        valid_z = valid[depth]
        print("State size:", len(valid[depth]), "valid z|digit pairs at depth", depth)

    assert 0 in valid[0]

    valid = [list(a) for a in valid]
    return valid


def backwards_state_space_construction(magic):
    valid = construct_state_space(magic)
    print("Statespace found, constructing number now...")

    number = ""
    valid.append([0])

    current_z = 0
    for depth in range(0, 14):
        for digit in range(9, 0, -1):
            if cycle(current_z, digit, magic[depth]) in valid[depth + 1]:
                print(number, digit)
                number = number + str(digit)
                break

    print(number)

if __name__ == '__main__':
    magic = [
        [1, 13, 3],
        [1, 11, 12],
        [1, 15, 9],
        [26, -6, 12],
        [1, 15, 2],
        [26, -8, 1],
        [26, -4, 1],
        [1, 15, 13],
        [1, 10, 1],
        [1, 11, 6],
        [26, -11, 2],
        [26, 0, 11],
        [26, -8, 10],
        [26, -7, 3]
    ]

    # Change out comments in deepbase and deep to loop largest first instead of smallest first to find largest output
    deepbase(magic)


