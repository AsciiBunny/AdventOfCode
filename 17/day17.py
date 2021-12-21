from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


def is_point_in_range(point, range):
    in_x_range = point.x >= range[0].x and point.x <= range[1].x
    in_y_range = point.y >= range[0].y and point.y <= range[1].y
    return in_x_range and in_y_range


def is_point_past_range(point, range):
    past_x_range = point.x > range[1].x
    past_y_range = point.y < range[0].y
    return past_x_range or past_y_range


def brute_force(input):
    most_highest_y = 0
    total = 0
    for x_velocity in range(1, input[1].x + 1):
        for y_velocity in range(-abs(input[0].y) - 1, abs(input[0].y) + 1):
            velocity = Point(x_velocity, y_velocity)
            highest_y = 0
            point = Point(0, 0)

            while not is_point_past_range(point, input):
                point.x += velocity.x
                point.y += velocity.y

                velocity.y -= 1
                if velocity.x > 0:
                    velocity.x -= 1

                highest_y = max(highest_y, point.y)

                if is_point_in_range(point, input):
                    most_highest_y = max(most_highest_y, highest_y)
                    total += 1
                    break

    return most_highest_y, total


if __name__ == '__main__':
    input = Point(235, -118) , Point(259, -62)
    highest_y, total = brute_force(input)
    print("Highest Y =", highest_y)
    print("Velocity pair count =", total)
