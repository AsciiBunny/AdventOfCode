import parsley


def read_input(filename):
    parser = parsley.makeGrammar("""
        number = ws <digit+>:ds -> int(ds)
        seeds = "seeds:" (number+):seeds -> seeds
        triplet = number:a number:b number:c -> (a, b, c)
        map_name = <letter+>:from_name "-to-" <letter+>:to_name ws "map:" -> (from_name, to_name)
        map = ws map_name:map_name ws triplet+:ranges -> (map_name, ranges)
        input = seeds:seeds map+:maps ws end -> (seeds, maps)
        """, {})

    with open(f"{filename}.txt", "r") as file:
        return parser(file.read()).input()


def get_mappings(data):
    seeds: list[int] = data[0]
    mappings: list[list[tuple[int, int, int]]] = []

    for _mapping in data[1]:
        mapping: list[tuple[int, int, int]] = _mapping[1]
        mapping = sorted(mapping)
        mappings.append(mapping)

    return seeds, mappings


def apply_mapping(mapping: list[tuple[int, int, int]], value: int):
    for map_range in mapping:
        if map_range[1] <= value < map_range[1] + map_range[2]:
            return value - map_range[1] + map_range[0]
    return value


def part_one(data):
    seeds, mappings = get_mappings(data)

    mapped_seeds = []
    for value in seeds:
        for mapping in mappings:
            value = apply_mapping(mapping, value)
        mapped_seeds.append(value)
    print("Lowest location number:", min(mapped_seeds))


def apply_mapping_to_range(mapping: list[tuple[int, int, int]], value: tuple[int, int]):
    for map_range in mapping:
        # if start value within map_range:
        if map_range[1] <= value[0] < map_range[1] + map_range[2]:
            # mapped_start = start offset by mapping
            mapped_start = value[0] - map_range[1] + map_range[0]
            # if mapped end does not fit within map_range
            if value[0] - map_range[1] + value[1] > map_range[2]:
                # this part was mapped, recurse for rest
                mapped_distance = map_range[2] - (value[0] - map_range[1])
                # start where the range ends, reduce distance by mapped distance
                remaining_value = (map_range[1] + map_range[2], value[1] - mapped_distance)
                return [(mapped_start, mapped_distance)] + apply_mapping_to_range(mapping, remaining_value)
            else:
                return [(mapped_start, value[1])]

    # Todo, start is not in any range, but some part of the range could be still
    # Does just work without this though, so ¯\_(ツ)_/¯
    # Containments are solved by end not fitting in current range
    return [value]


def part_two(data):
    seeds, mappings = get_mappings(data)
    total_min_location = 1_000_000_000_000
    for i in range(0, len(seeds), 2):
        values = [(seeds[i], seeds[i + 1])]
        for mapping in mappings:
            new_values = []
            for value in values:
                new_values += apply_mapping_to_range(mapping, value)
            values = new_values
        seed_min_location = min(value[0] for value in values)
        total_min_location = min(total_min_location, seed_min_location)
    print("Lowest location number:", total_min_location)



if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(data)
    print("\nPart 2")
    part_two(data)
