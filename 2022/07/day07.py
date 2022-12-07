from dataclasses import dataclass


@dataclass
class File:
    name: str
    size: int

    def isFolder(self):
        return False

    def getSize(self):
        return self.size


@dataclass
class Folder:
    name: str
    parent: "Folder" or None
    contents: list[File or "Folder"]

    def isFolder(self):
        return True

    def getSize(self):
        sizes = [x.getSize() for x in self.contents]
        return sum(sizes)


def read_input():
    data_file = open("input.txt", "r")
    data_lines = data_file.read().splitlines()

    filetree = Folder("/", None, [])
    file = filetree

    for line in data_lines:
        # print(line)
        line = line.split(" ")
        match line:
            case ["$", "cd", "/"]:
                file = filetree
                # print("Setting file back to root:", file)
            case ["$", "cd", ".."]:
                file = file.parent
                # print("Setting file back to parent:", file.name)
            case ["$", "cd", name]:
                file = next(child for child in file.contents if child.name == name)
                # print("Setting file to child:", file.name)
            case ["$", "ls"]:
                pass
            case ["dir", name]:
                file.contents.append(Folder(name, file, []))
                # print("Creating folder", name, "in", file.name)
            case [size, name]:
                file.contents.append(File(name, int(size)))
                # print("Creating file", name, "in", file.name, "with size", size)
            case other:
                print("Did not cover:", other)

    return filetree


def descendants(folder: Folder):
    for child in folder.contents:
        yield child
        if isinstance(child, Folder):
            for descendant in descendants(child):
                yield descendant



def sum_sizes_below(folder: Folder, max_value: int):
    total = 0
    for child in descendants(folder):
        if isinstance(child, Folder):
            size = child.getSize()
            if size <= max_value:
                total += size
    return total

def find_smallest_bigger_than(folder: Folder, min_value: int):
    smallest = folder
    smallest_size = smallest.getSize()
    for child in descendants(folder):
        if isinstance(child, Folder):
            size = child.getSize()
            if size >= min_value and size < smallest_size:
                smallest = child
                smallest_size = size

    return smallest, smallest_size


if __name__ == '__main__':
    tree = read_input()
    sizes_below = sum_sizes_below(tree, 100000)
    print("Total sum of folder sizes below 100000:", sizes_below)

    total_size = tree.getSize()
    unused_space = 70000000 - total_size
    remaining_space = 30000000 - unused_space
    print("Still need to remove", remaining_space, "to make space for update")
    smallest, smallest_size = find_smallest_bigger_than(tree, remaining_space)
    print("Remove folder", smallest.name, "to clear up", smallest_size)
