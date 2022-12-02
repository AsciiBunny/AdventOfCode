from dataclasses import dataclass
from typing import Callable, Generator


@dataclass()
class ALU:
    reg: dict[str, int]

    def inp(self, register: str, gen: Generator[int, None, None]):
        self.reg[register] = next(gen)

    def add(self, register: str, value: int | str):
        if type(value) == int:
            self.reg[register] += value
        if type(value) == str:
            self.reg[register] += self.reg[value]

    def mul(self, register: str, value: int | str):
        if type(value) == int:
            self.reg[register] *= value
        if type(value) == str:
            self.reg[register] *= self.reg[value]

    def div(self, register: str, value: int | str):
        if type(value) == int:
            if value == 0:
                raise "Invalid Operation"
            self.reg[register] //= value
        if type(value) == str:
            self.reg[register] //= self.reg[value]

    def mod(self, register: str, value: int | str):
        if type(value) == int:
            if value <= 0:
                raise "Invalid Operation"
            self.reg[register] %= value
        if type(value) == str:
            self.reg[register] %= self.reg[value]

    def eql(self, register: str, value: int | str):
        if type(value) == int:
            self.reg[register] = 1 if self.reg[register] == value else 0
        if type(value) == str:
            self.reg[register] = 1 if self.reg[register] == self.reg[value] else 0

    def reset(self):
        for register in self.reg:
            self.reg[register] = 0


@dataclass(frozen = True)
class Instruction:
    instruction: Callable[[str, int | str | Generator[int, None, None]], None]
    left: str
    right: int | str | Generator[int, None, None]



def read_input(alu: ALU, registers: list[str], inputs: Generator[int, None, None]):
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    commands = []
    for line in data_lines:
        words = line.split(" ")
        match words:
            case ["inp", value]:
                print("inp", value)
                commands.append(Instruction(alu.inp, value, inputs))

            case ["add", left, right] if left in registers and right in registers:
                print("add", left, right)
                commands.append(Instruction(alu.add, left, right))
            case ["add", left, right] if left in registers and right.lstrip("-").isnumeric():
                print("add", left, int(right))
                commands.append(Instruction(alu.add, left, int(right)))

            case ["mul", left, right] if left in registers and right in registers:
                print("mul", left, right)
                commands.append(Instruction(alu.mul, left, right))
            case ["mul", left, right] if left in registers and right.lstrip("-").isnumeric():
                print("mul", left, int(right))
                commands.append(Instruction(alu.mul, left, int(right)))

            case ["div", left, right] if left in registers and right in registers:
                print("div", left, right)
                commands.append(Instruction(alu.div, left, right))
            case ["div", left, right] if left in registers and right.lstrip("-").isnumeric():
                print("div", left, int(right))
                commands.append(Instruction(alu.div, left, int(right)))

            case ["mod", left, right] if left in registers and right in registers:
                print("mod", left, right)
                commands.append(Instruction(alu.mod, left, right))
            case ["mod", left, right] if left in registers and right.lstrip("-").isnumeric():
                print("mod", left, int(right))
                commands.append(Instruction(alu.mod, left, int(right)))

            case ["eql", left, right] if left in registers and right in registers:
                print("eql", left, right)
                commands.append(Instruction(alu.eql, left, right))
            case ["eql", left, right] if left in registers and right.lstrip("-").isnumeric():
                print("eql", left, int(right))
                commands.append(Instruction(alu.eql, left, int(right)))

    return commands


def digits(number: int):
    digits = [int(a) for a in str(number)]
    for digit in digits:
        yield digit

def gen_inputs():
    for i in range (99999999999999, 10000000000000, -1):
        yield i
        digits = [int(a) for a in str(i)]
        for digit in digits:
            yield digit

def run_program(program: list[Instruction]):
    for instruction in program:
        instruction.instruction(instruction.left, instruction.right)

if __name__ == '__main__':
    alu = ALU({"w": 0, "x": 0, "y": 0, "z": 0})
    registers = ["w", "x", "y", "z"]
    gen = digits(95859994999697)
    #gen = gen_inputs()
    program = read_input(alu, registers, gen)

    run_program(program)
    print(alu.reg["z"])

    while True and False:
        number = next(gen)
        run_program(program)
        if (alu.reg["z"] == 0):
            print("Model number", number, "is valid!")
            break
        alu.reset()


