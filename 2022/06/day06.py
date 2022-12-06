def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()
    return data_lines[0]


def find_start(data, section_length):
    queue = []
    for i in range(len(data)):
        char, data = data[0], data[1:]
        if len(queue) == section_length:
            queue.pop(0)
        if char in queue or len(queue) < section_length - 1 or len(queue) != len(set(queue)):
            queue.append(char)
        else:
            return i + 1



if __name__ == '__main__':
    data = read_input()
    start_packet = find_start(data, 4)
    print("Packet starts after", start_packet, "characters")
    start_message = find_start(data, 14)
    print("Message starts after", start_message, "characters")
