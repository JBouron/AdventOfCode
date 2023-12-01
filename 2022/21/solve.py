#!/usr/bin/env python

import sys
import re
from enum import Enum

PART2 = False

# The trick here is to build an AST of the computation made by the `root`
# monkey. For part 1 we simply evaluate the AST. For part 2 we solve for the
# equation recursively, "peeling off" every node one by one.

class Node:
    # To be overwritten by sub-classes.
    def value(self):
        raise Exception("Abstract method Node.value()")

    # Resolve all references under this node and replace them with their
    # corresponding AST. ctx is a dict mapping ref names to their AST.
    def resolveRefs(self, ctx):
        raise Exception("Abstract method Node.resolveRefs()")

    # Check if this node depends on human input, that is if it references a
    # reference node to "humn".
    def hasInput(self):
        raise Exception("Abstract method Node.hasInput()")

    def solve(self, eqRight):
        raise Exception("Abstract method Node.solve()")

# Node corresponding to a yelled number.
class ConstNode(Node):
    def __init__(self, val):
        self.val = val

    def value(self):
        return self.val

    def resolveRefs(self, ctx):
        return self

    def hasInput(self):
        return False

    def solve(self, eqRight):
        raise Exception("Calling solve() on ConstNode")

    def __repr__(self):
        return str("CONST({})".format(self.val))

class RefNode(Node):
    def __init__(self, name):
        self.name = name

    def value(self):
        raise Exception("Node.value() on RefNode")

    def resolveRefs(self, ctx):
        if PART2 and self.name == "humn":
            return self
        else:
            return ctx[self.name].resolveRefs(ctx)

    def hasInput(self):
        return self.name == "humn"

    def solve(self, eqRight):
        assert self.name == "humn"
        return eqRight.value()

    def __repr__(self):
        return str("REF({})".format(self.name))

class AddNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() + self.right.value()

    def resolveRefs(self, ctx):
        return AddNode(self.left.resolveRefs(ctx), self.right.resolveRefs(ctx))

    def hasInput(self):
        return self.left.hasInput() or self.right.hasInput()

    def solve(self, eqRight):
        if self.left.hasInput():
            assert not self.right.hasInput()
            newEqRight = SubNode(eqRight, ConstNode(self.right.value()))
            return self.left.solve(newEqRight)
        else:
            assert self.right.hasInput()
            assert not self.left.hasInput()
            newEqRight = SubNode(eqRight, ConstNode(self.left.value()))
            return self.right.solve(newEqRight)

    def __repr__(self):
        return str("ADD({},{})".format(str(self.left), str(self.right)))

class SubNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() - self.right.value()

    def resolveRefs(self, ctx):
        return SubNode(self.left.resolveRefs(ctx), self.right.resolveRefs(ctx))

    def hasInput(self):
        return self.left.hasInput() or self.right.hasInput()

    def solve(self, eqRight):
        if self.left.hasInput():
            assert not self.right.hasInput()
            newEqRight = AddNode(eqRight, ConstNode(self.right.value()))
            return self.left.solve(newEqRight)
        else:
            assert self.right.hasInput()
            assert not self.left.hasInput()
            newEqRight = SubNode(eqRight, ConstNode(self.left.value()))
            return self.right.solve(SubNode(ConstNode(0),newEqRight))

    def __repr__(self):
        return str("SUB({},{})".format(str(self.left), str(self.right)))

class MulNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() * self.right.value()

    def resolveRefs(self, ctx):
        return MulNode(self.left.resolveRefs(ctx), self.right.resolveRefs(ctx))

    def hasInput(self):
        return self.left.hasInput() or self.right.hasInput()

    def solve(self, eqRight):
        if self.left.hasInput():
            assert not self.right.hasInput()
            newEqRight = DivNode(eqRight, ConstNode(self.right.value()))
            return self.left.solve(newEqRight)
        else:
            assert self.right.hasInput()
            assert not self.left.hasInput()
            newEqRight = DivNode(eqRight, ConstNode(self.left.value()))
            return self.right.solve(newEqRight)

    def __repr__(self):
        return str("MUL({},{})".format(str(self.left), str(self.right)))

class DivNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def value(self):
        return self.left.value() // self.right.value()

    def resolveRefs(self, ctx):
        return DivNode(self.left.resolveRefs(ctx), self.right.resolveRefs(ctx))

    def hasInput(self):
        return self.left.hasInput() or self.right.hasInput()

    def solve(self, eqRight):
        if self.left.hasInput():
            assert not self.right.hasInput()
            newEqRight = MulNode(eqRight, ConstNode(self.right.value()))
            return self.left.solve(newEqRight)
        else:
            assert self.right.hasInput()
            assert not self.left.hasInput()
            newEqRight = MulNode(eqRight, ConstNode(self.left.value()))
            return self.right.solve(newEqRight)

    def __repr__(self):
        return str("DIV({},{})".format(str(self.left), str(self.right)))

def parseInput(inputFile, skipHuman):
    fd = open(inputFile, "r")
    nodes = {}
    for l in fd.readlines():
        l = l.replace("\n", "")
        name = l[:4]
        if skipHuman and name == "humn":
            continue
        nums = re.findall("[0-9]+", l)
        if len(nums) > 0:
            # This is a ConstNode.
            const = int(nums[0])
            nodes[name] = ConstNode(const)
        else:
            # This is a Math Op yell.
            left = RefNode(l[6:10])
            right = RefNode(l[13:])

            if "+" in l:
                nodes[name] = AddNode(left, right)
            elif "-" in l:
                nodes[name] = SubNode(left, right)
            elif "*" in l:
                nodes[name] = MulNode(left, right)
            else:
                assert "/" in l
                nodes[name] = DivNode(left, right)

    fd.close()

    if not skipHuman:
        # Part 1.
        root = nodes["root"]
        root = root.resolveRefs(nodes)
        return root
    else:
        # Part 2.
        root = nodes["root"]
        left = root.left.resolveRefs(nodes)
        right = root.right.resolveRefs(nodes)
        return (left, right)


def part1(inputFile):
    root = parseInput(inputFile, False)
    return root.value()

def part2(inputFile):
    global PART2
    PART2 = True
    left, right = parseInput(inputFile, True)
    if left.hasInput() and not right.hasInput():
        return left.solve(right)
    else:
        return right.solve(left)

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
