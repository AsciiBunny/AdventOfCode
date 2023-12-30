import parsley

from util.util import Range

Rule = tuple[str, str, int, str]
Workflow = tuple[list[Rule], str]
Part = dict[str, int]


def read_input(filename):
    parser = parsley.makeGrammar("""
        number = ws <digit+>:ds -> int(ds)
        name = <letter+>:name -> name
        category = "x" | "m" | "a" | "s"
        operator = ">" | "<"
        rule = category:cat operator:op number:value ":" name:next "," -> (cat, op, value, next)
        workflow = ws name:name "{" (rule)+:rules name:fallback "}" -> (name, (rules, fallback))
        part = ws "{x=" number:x ",m=" number:m ",a=" number:a ",s=" number:s "}" -> dict(x=x, m=m, a=a, s=s)
        input = workflow+:workflows ws part+:parts ws end -> (dict(workflows), parts)
        """, {})

    with open(f"{filename}.txt", "r") as file:
        return parser(file.read()).input()


def applies(rule: Rule, part: Part):
    part_value = part[rule[0]]
    rule_value = rule[2]
    rule_operator = rule[1]
    if rule_operator == "<":
        return part_value < rule_value
    elif rule_operator == ">":
        return part_value > rule_value
    else:
        assert False, "Invalid operator: " + rule_operator


def part_one(workflows: dict[str, Workflow], parts: list[Part]):
    accepted = []
    for part in parts:
        workflow = workflows["in"]
        while True:
            rules, next_workflow = workflow
            for rule in rules:
                if applies(rule, part):
                    next_workflow = rule[3]
                    break
            if next_workflow == "A":
                accepted.append(part)
                break
            if next_workflow == "R":
                break
            workflow = workflows[next_workflow]

    total = sum(sum(part.values()) for part in accepted)
    print("total value of accepted parts:", total)


class CombinedRange:
    def __init__(self, x: Range = Range(1, 4000), m: Range = Range(1, 4000), a: Range = Range(1, 4000),
                 s: Range = Range(1, 4000)):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __str__(self):
        return "{" + str(self.x) + "," + str(self.m) + "," + str(self.a) + "," + str(self.s) + "}"

    def __repr__(self):
        return self.__str__()

    def duplicate(self):
        return CombinedRange(self.x.duplicate(), self.m.duplicate(), self.a.duplicate(), self.s.duplicate())

    def split(self, axis, split_on):
        x = [self.x.duplicate(), self.x.duplicate()] if axis != "x" \
            else self.x.split(split_on)
        m = [self.m.duplicate(), self.m.duplicate()] if axis != "m" \
            else self.m.split(split_on)
        a = [self.a.duplicate(), self.a.duplicate()] if axis != "a" \
            else self.a.split(split_on)
        s = [self.s.duplicate(), self.s.duplicate()] if axis != "s" \
            else self.s.split(split_on)
        return list(map(lambda pair: CombinedRange(*pair), zip(x, m, a, s)))


def part_two(workflows: dict[str, Workflow], parts: list[Part]):
    to_split = [("in", CombinedRange())]

    accepted: list[CombinedRange] = []
    refused: list[CombinedRange] = []

    while len(to_split) > 0:
        name, current = to_split.pop()

        if name == "A":
            accepted.append(current)
            continue
        if name == "R":
            refused.append(current)
            continue

        rules, fallback_name = workflows[name]

        for rule_rating, rule_operator, rule_value, rule_target in rules:
            if rule_operator == ">":
                left, right = current.split(rule_rating, rule_value + 1)
                to_split.append((rule_target, right))
                current = left
            if rule_operator == "<":
                left, right = current.split(rule_rating, rule_value)
                to_split.append((rule_target, left))
                current = right

        to_split.append((fallback_name, current))

    total = 0
    for r in accepted:
        size = 1
        size *= (r.x.end - r.x.start) + 1
        size *= (r.m.end - r.m.start) + 1
        size *= (r.a.end - r.a.start) + 1
        size *= (r.s.end - r.s.start) + 1
        total += size
    print("amount of distinct combinations possible:", total)


if __name__ == '__main__':
    data = read_input('input')
    print("Part 1")
    part_one(*data)
    print("\nPart 2")
    part_two(*data)
