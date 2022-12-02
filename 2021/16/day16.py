from dataclasses import dataclass
from math import prod

@dataclass
class Packet:
    version: int
    type_id: int
    length: int
    content: any

packet_types = [
    'SUM',
    'PRD',
    'MIN',
    'MAX',
    'LIT',
    'GRT',
    'LST',
    'EQT'
]


def read_input():
    data_file = open("input.txt", "r")
    return data_file.read()


def print_triple(value, bit_count=0):
    bits = format(value, '0' + str(bit_count) +  'b' if bit_count else '08b')
    if (bit_count):
        bits = ' ' * (8 - bit_count) + bits

    print(format(value, '2x'), format(value, '3d'), bits)


def print_packet(packet: Packet, depth=0):
    print('   ' * depth, "<", packet_types[packet.type_id], "v" + str(packet.version), "|",  packet.length, "bits", ">")

    if isinstance(packet.content, list):
        for contained_packet in packet.content:
            print_packet(contained_packet, depth + 1)
    else:
        print('   ' * (depth + 1), "=", packet.content)


def get_bit_stream(input_stream):
    for character in input_stream:
        if character == '\n':
            continue
        value = int(character, base=16)
        yield (value & 0b1000) >> 3
        yield (value & 0b0100) >> 2
        yield (value & 0b0010) >> 1
        yield value & 0b0001


def get_bits(bit_stream, amount):
    value = 0
    for _ in range(amount):
        value = value << 1
        value += next(bit_stream)
    return value


def read_literal(bit_stream):
    sum = 0
    length = 0
    while True:
        bits = get_bits(bit_stream, 5)
        prefix = bits & 0b10000
        value = bits & 0b01111

        sum = sum << 4
        sum += value

        length += 5

        if prefix == 0:
            break
    return sum, length


def read_packet(bit_stream):
    packet_version = get_bits(bit_stream, 3)
    packet_type = get_bits(bit_stream, 3)

    match packet_type:
        case 4:
            packet_literal, literal_length = read_literal(bit_stream)
            packet_length = 3 + 3 + literal_length
            return Packet(packet_version, packet_type, packet_length, packet_literal)
        case _:
            packet_contents, contents_length = read_packets(bit_stream)
            packet_length = 3 + 3 + contents_length
            return Packet(packet_version, packet_type, packet_length, packet_contents)



def read_packets(bit_stream):
    packet_length_type = get_bits(bit_stream, 1)

    if packet_length_type:
        packet_count = get_bits(bit_stream, 11)
        packet_contents = list(read_packet(bit_stream) for _ in range(packet_count))
        packet_length = 1 + 11 + sum(packet.length for packet in packet_contents)
        return packet_contents, packet_length
    else:
        packet_content_length = get_bits(bit_stream, 15)
        packet_contents = []
        length_sum = 0
        while length_sum < packet_content_length:
            next_packet = read_packet(bit_stream)
            length_sum += next_packet.length
            packet_contents.append(next_packet)
        assert length_sum == packet_content_length
        packet_length = 1 + 15 + packet_content_length
        return packet_contents, packet_length


def sum_versions(packet: Packet):
    if isinstance(packet.content, list):
        return packet.version + sum(sum_versions(list_packet) for list_packet in packet.content)
    else:
        return packet.version


def evaluate_packet(packet: Packet):
    match packet.type_id:
        case 0:
            return sum(evaluate_packet(nested) for nested in packet.content)
        case 1:
            return prod(evaluate_packet(nested) for nested in packet.content)
        case 2:
            return min(evaluate_packet(nested) for nested in packet.content)
        case 3:
            return max(evaluate_packet(nested) for nested in packet.content)
        case 4:
            return packet.content
        case 5:
            return evaluate_packet(packet.content[0]) > evaluate_packet(packet.content[1])
        case 6:
            return evaluate_packet(packet.content[0]) < evaluate_packet(packet.content[1])
        case 7:
            return evaluate_packet(packet.content[0]) == evaluate_packet(packet.content[1])
        case _:
            return 0


if __name__ == '__main__':
    input = read_input()
    #input = "9C0141080250320F1802104A08"
    bit_stream = get_bit_stream(input)

    packet = read_packet(bit_stream)
    print_packet(packet)
    print("Total version sum:", sum_versions(packet))
    print("Packet evaluation:", evaluate_packet(packet))
