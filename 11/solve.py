#!/usr/bin/env python

# This is an overkill solution to Day 11, creating ASTs for the operations to be
# performed on worry levels.
# Of course there are faster ways to solves this (e.g. by abusing exec()), but
# this wouldn't be fun without adding an AST in the mix.

import sys
from abc import ABC, abstractmethod
from enum import Enum

# A schedule describes what a monkey does with an item, that is how worry levels
# are updated, what test condition is performed on worry levels and to which
# monkeys to send the item to.
class Schedule:
    # An operation describes how a worry level is updated.
    class Operation:
        # Operation are using a mini-AST under the hood for evaluation.
        # Base class for a node in the AST.
        class AstNode(ABC):
            def __init__(self):
                self.saved = {}

            # Evaluate the value of this node with the given context. Context is
            # a dict name -> value.
            # Return the value of the node.
            @abstractmethod
            def evaluate(self, context):
                pass

        # Multiplication AST node.
        class MultNode(AstNode):
            # Create a MultNode multiplying a and b. a and b are AstNodes.
            def __init__(self, a, b):
                super().__init__()
                self.a = a
                self.b = b

            def evaluate(self, context):
                return self.a.evaluate(context) * self.b.evaluate(context)

        # Addition AST node.
        class AddNode(AstNode):
            # Create an AddNode adding a and b.
            def __init__(self, a, b):
                super().__init__()
                self.a = a
                self.b = b

            def evaluate(self, context):
                return self.a.evaluate(context) + self.b.evaluate(context)

        # Reference AST node. This node evaluate to the value of a variable.
        class RefNode(AstNode):
            # Create a RefNode, a reference to a variable named `varName`.
            def __init__(self, varName):
                super().__init__()
                self.varName = varName

            def evaluate(self, context):
                return context[self.varName]

        # Immediate AST node. This represent a constant value.
        class ImmNode(AstNode):
            # Create an ImmNode, a constant immediate value.
            def __init__(self, value):
                super().__init__()
                self.value = value

            def evaluate(self, context):
                return self.value

        # Create an operation implemented by the given AST.
        def __init__(self, ast):
            self.ast = ast

        # Create an Operation from its string representation, that is how it is
        # represented in the input file of this problem.
        @staticmethod
        def fromString(string):
            assert "Operation: new =" in string
            opStr = string.split("= ")[1]
            a, operator, b = opStr.split(" ")

            # Create an AST node for a given operand.
            def nodeForOperand(operand):
                if operand == "old":
                    return Schedule.Operation.RefNode("old")
                else:
                    return Schedule.Operation.ImmNode(int(operand))

            nodeA = nodeForOperand(a)
            nodeB = nodeForOperand(b)
            if operator == "*":
                ast = Schedule.Operation.MultNode(nodeA, nodeB)
            else:
                ast = Schedule.Operation.AddNode(nodeA, nodeB)
            return Schedule.Operation(ast)

        # Compute the new worry level from the old one.
        def __call__(self, old):
            context = {"old": old}
            return self.ast.evaluate(context)

    # Create a schedule where:
    #   - operation indicates how to update worry levels.
    #   - modulus is the modulus to use in the test to decide where to send the
    #   item.
    #   - trueMonkey is the destination monkey if the test is true.
    #   - falseMonkey is the destination monkey if the test is false.
    #   - The worry level of an item after inspection is divided by `div`.
    def __init__(self, operation, modulus, trueMonkey, falseMonkey, div):
        self.operation = operation
        self.modulus = modulus
        self.destination = {False: falseMonkey, True: trueMonkey}
        self.div = div

    # Execute the schedule on an item.
    # Return a pair (ID, worryLevel) where ID indicates to which monkey to send
    # the item to and worryLevel is the updated worry level for the item.
    def destinationMonkeyForItem(self, item):
        # The trick:
        # At each turn, we are interested in worryLevel % self.modulus in order
        # to know to which monkey the item should be sent.
        # worryLevel is the cumulation of all updates performed by monkeys that
        # had this item before us. This number can be extremely big in part 2.
        # However, algebra tells us that (a mod kn) mod n == a mod n for any k.
        # So, with wl representing worryLevel:
        #   (wl mod k*self.modulus) mod self.modulus = wl mod self.modulus
        # Therefore instead of computing wl mod self.modulus to get the
        # destination monkey, we can compute
        #   (wl mod k*self.modulus) mod self.modulus
        # instead. In other words wl can be replaced with wl mod k*self.modulus.
        # The good thing is that wl mod k*self.modulus is bouned to k * modulus
        # and therefore does not explode like wl does.
        # Therefore, instead of passing wl to the next monkey, we can pass
        # (wl mod k*self.modulus) and the problem of exploding numbers goes
        # away.
        # How do we choose k? The problem here is that each monkey has a
        # different modulus and therefore we need to choose a k such that
        # k * self.modulus is a multiple of other.modulus.
        # The easy choice is to take k = m0 * m1 * m2 * ... where mi is the
        # modulus of monkey i.
        kn = 1
        for m in MONKEYS:
            kn *= m.schedule.modulus

        worryLevel = (self.operation(item) // self.div) % kn
        d = (worryLevel % self.modulus == 0)
        return (self.destination[d], worryLevel)

# The list of monkeys, indexed by their numerical ID.
MONKEYS = []

# A monkey. A monkey has a list of item and a schedule that it follows for each
# item.
class Monkey:
    def __init__(self, startingItems, schedule):
        self.items = startingItems
        self.schedule = schedule
        self.inspectedItems = 0

    def doTurn(self):
        self.inspectedItems += len(self.items)
        for it in self.items:
            nextMonkey, worryLevel = self.schedule.destinationMonkeyForItem(it)
            MONKEYS[nextMonkey].receiveItem(worryLevel)
        self.items = []

    def receiveItem(self, item):
        self.items.append(item)

# Perform a full round where each monkey perform a turn once.
def doRound():
    for m in MONKEYS:
        m.doTurn()

# Parse the input file and populates MONKEYS.
def parseInput(inputFile, part2):
    fd = open(inputFile, "r")
    it = iter(fd)

    global MONKEYS
    MONKEYS = []

    # Iterate over the input file and parse each monkey.
    for line in it:
        if line == "\n":
            continue
        # This for loop makes sure that each iteration starts on a line defining
        # a new monkey.
        assert "Monkey" in line
        
        # Parse starting items.
        startingItems = next(it).replace("\n", "")
        assert "Starting items:" in startingItems
        startingItems = startingItems.split(": ")[1]
        startingItems = startingItems.replace(",", "")
        startingItems = [int(val) for val in startingItems.split(" ")]

        # Parse operation.
        operation = next(it).replace("\n", "")
        assert "Operation:" in operation
        operation = Schedule.Operation.fromString(operation)

        # Parse schedule.
        testCond = next(it).replace("\n", "")
        assert "Test:" in testCond
        modulus = int(testCond.split(" ")[-1])
        trueMonkey = int(next(it).replace("\n", "").split(" ")[-1])
        falseMonkey = int(next(it).replace("\n", "").split(" ")[-1])
        div = 1 if part2 else 3
        schedule = Schedule(operation, modulus, trueMonkey, falseMonkey, div)

        MONKEYS.append(Monkey(startingItems, schedule))
    fd.close()

def part1(inputFile):
    parseInput(inputFile, False)

    for i in range(20):
        doRound()
    inspItems = sorted([m.inspectedItems for m in MONKEYS])
    return inspItems[-1] * inspItems[-2]

def part2(inputFile):
    parseInput(inputFile, True)

    for i in range(10000):
        doRound()
    inspItems = sorted([m.inspectedItems for m in MONKEYS])
    return inspItems[-1] * inspItems[-2]

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
