class Range:
    def __init__(self, start: int, end: int):
        assert start <= end
        self.start = start
        self.end = end

    def __str__(self):
        return "r(" + str(self.start) + "," + str(self.end) + ")"

    def __repr__(self):
        return self.__str__()

    def contains(self, value):
        return self.start < value < self.end

    # split_on is not contained in left
    def split(self, split_on):
        assert self.contains(split_on)
        left = Range(self.start, split_on - 1)
        right = Range(split_on, self.end)
        return left, right

    def duplicate(self):
        return Range(self.start, self.end)

