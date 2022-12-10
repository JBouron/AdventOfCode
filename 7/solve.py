#!/usr/bin/env python

# A rather overkill solution that is also nasty at the same time, go figure.

import sys
from enum import Enum
from abc import abstractmethod

# A node of the filesystem tree.
class Node:
    class Type(Enum):
        FILE = 1
        DIR = 2

    def __init__(self, name, nodeType, parent):
        self.name = name
        self.nodeType = nodeType
        self.parent = parent

    # Size of the node in bytes.
    @abstractmethod
    def size(self):
        pass

    # Compute answer to part 1 recursively.
    @abstractmethod
    def part1(self):
        pass

    # Compute answer to part 2 recursively. Returns a list of Directory Nodes
    # for which their size is >= minSize.
    @abstractmethod
    def part2(self, minSize):
        pass

# Special type of node representing a file in the filesystem tree.
class File(Node):
    def __init__(self, name, parent, size):
        super().__init__(name, Node.Type.FILE, parent)
        self._fileSize = size

    def size(self):
        return self._fileSize

    def print(self, nestLevel):
        print(" " * nestLevel + "{} {}".format(self._fileSize, self.name))

    def part1(self):
        return 0

    def part2(self, minSize):
        return []

# Special type of node representing a directory in the filesystem tree.
class Dir(Node):
    def __init__(self, name, parent):
        super().__init__(name, Node.Type.DIR, parent)
        self._children = {}

    def size(self):
        return sum([c.size() for c in self._children.values()])

    def child(self, childName):
        # Get a reference to a child from its name.
        assert childName in self._children.keys()
        return self._children[childName]

    def addChild(self, child):
        self._children[child.name] = child
        # The caller must make sure the parent backpointer is correct.
        assert child.parent == self

    def part1(self):
        res = 0
        size = self.size()
        if size <= 100000:
            res += size
        for c in self._children.keys():
            res += self._children[c].part1()
        return res

    def part2(self, minSize):
        res = []
        if self.size() >= minSize:
            res.append(self)
        for c in self._children.keys():
            res += self._children[c].part2(minSize)
        return res

def parseFilesystem(inputFile):
    # Compute the filesystem tree from the input file containing commands and
    # their outputs.
    # Return a reference to the root directory (node) of the filesystem tree.
    fd = open(inputFile, "r")
    lines = list(map(lambda l: l.replace("\n", ""), fd.readlines()))

    # The current node.
    root = Dir("/", None)
    currNode = root

    def parseCd(output):
        # Parse a cd command and change cwd accordingly.
        # `output` is the output of the command including the cmd line. In the
        # case of cd this should only contains the cmdline itself.
        assert len(output) == 1
        cmd = output[0]
        assert "$ cd" in cmd
        dest = cmd.split(" ")[2]
        nonlocal currNode
        if dest == "/":
            currNode = root
        elif dest == "..":
            # Go up a directory.
            assert currNode.parent is not None
            currNode = currNode.parent
        else:
            currNode = currNode.child(dest)

    def parseLs(output):
        # Parse a ls command and change cwd accordingly.
        # `output` is the output of the command including the cmd line.
        assert output[0] == "$ ls"
        # The list of files/dirs under the current dir, e.g the output of ls.
        files = output[1:]
        # The cwd is always absolute, so remove the leading '/' before calling
        # child().
        for f in files:
            parts = f.split(" ")
            name = parts[1]
            if parts[0] == "dir":
                # f is a directory, add a new child.
                child = Dir(name, currNode)
                currNode.addChild(child)
            else:
                # f is a file.
                size = int(parts[0])
                child = File(name, currNode, size)
                currNode.addChild(child)

    while len(lines) > 0:
        cmd = lines[0]
        lines = lines[1:]
        assert "$" in cmd
        if "$ cd" in cmd:
            parseCd([cmd])
        elif "$ ls" in cmd:
            output = []
            for l in lines:
                if l[0] != "$":
                    output.append(l)
                else:
                    # Reached end of command's ouput.
                    break
            lines = lines[len(output):]
            # Due to a quirk on how parseLs is written.
            output = ["$ ls"] + output
            parseLs(output)
        else:
            # Unknown command? Most likely a bug.
            assert False

    return root

def part1(inputFile):
    root = parseFilesystem(inputFile)
    return root.part1();

def part2(inputFile):
    root = parseFilesystem(inputFile)
    free = 70000000 - root.size()
    toDel = 30000000 - free
    assert toDel > 0
    dirs = root.part2(toDel);
    return min([d.size() for d in dirs])

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
