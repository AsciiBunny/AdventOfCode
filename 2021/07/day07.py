from statistics import  median

def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    positions = list(map(int, data_lines[0].split(",")))

    return positions


def calculate_simple_fuel_cost(positions, target_position):
    fuel_cost = sum([abs(pos - target_position) for pos in positions])
    return fuel_cost


def calculate_complicated_fuel_cost(positions, target_position):
    distances = [abs(pos - target_position) for pos in positions]
    fuel_costs = [dist * (dist + 1) / 2 for dist in distances]
    return sum(fuel_costs)


def brute_force_target(positions, fuel_cost):
    cost = 1_000_000_000_000_000
    for i in range(min(positions), max(positions) + 1):
        cost = min(fuel_cost(positions, i), cost)
    return cost


if __name__ == '__main__':
    positions = read_input()
    print(len(positions), "Crabs from", min(positions), "to", max(positions))

    simple_target_position =  median(positions)
    print("Part 1 fuel cost:", calculate_simple_fuel_cost(positions, simple_target_position))

    cost = brute_force_target(positions, calculate_complicated_fuel_cost)
    print("Part 2 fuel cost:", cost)
