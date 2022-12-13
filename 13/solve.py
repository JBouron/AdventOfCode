#!/usr/bin/env python

import sys
from functools import cmp_to_key

# Parse the input file an return a list of pairs.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    data = fd.read()
    pairsData = data.split("\n\n")
    pairs = list(map(lambda p: p.split("\n"), pairsData))

    # Return the list encoded in string. Potentially contains nested lists.
    def parseString(string):
        # The current state of the input.
        curr = string

        # Get the value of the next in the input, also removes that char from
        # the input.
        def nextChar():
            nonlocal curr
            c = curr[0]
            curr = curr[1:]
            return c

        # Get the value of the next char in the input without removing it from
        # the input.
        def peek():
            nonlocal curr
            return curr[0]

        # Parse the next element from the input, either a list or an integer.
        # Return the parsed element.
        def parse():
            # Parse the integer from the input. Assumes that the integer is
            # starting in the first character of the input.
            def parseInt():
                valueStr = ""
                # Consume all digits.
                while peek() in list("0123456789"):
                    valueStr += nextChar()
                return int(valueStr)

            # Parse the list from the input. Assumes that the very first char is
            # the opening bracket for that list.
            def parseList():
                c = nextChar()
                assert c == "["
                l = []
                while peek() != "]":
                    # Each iteration is a new element of the list. Parse it and
                    # add it to the list.
                    l.append(parse())
                    # We then expect either a comma or a closing bracket.
                    if peek() == ",":
                        # Next char is a comma, we will iterate once again.
                        assert nextChar() == ","
                    # If the char is a closing bracket then the next check on
                    # the while's condition will terminate the loop.
                # Consume the closing bracket.
                assert nextChar() == "]"
                return l

            # Peek next char.
            p = peek()
            if p == "[":
                # Start of a list.
                return parseList()
            elif p in list("0123456789"):
                # Integer.
                return parseInt()

        return parse()

    pairs = list(map(lambda p: (parseString(p[0]), parseString(p[1])), pairs))
        
    fd.close()
    return pairs

# Compare the two elements of a pair.
# Return -1 if the left element is smaller, e.g. inputs are in the right order.
# Return 0 if both elements are the same.
# Return 1 if the right element is smaller.
def compare(l, r):
    def compareInt(l, r):
        return -1 if l < r else (0 if l == r else 1)

    def compareList(l, r):
        L = min(len(l), len(r))
        for i in range(L):
            c = compare(l[i], r[i])
            if c == 0:
                # The comparison cannot make a decision.
                continue
            else:
                # We already know the result of the comparison
                return c
        # If we reach here then this means either:
        #   - We ran out of elements in one of the list.
        #   - Both lists have the same len but all elements compare to 0.
        if len(l) == len(r):
            # Case #2.
            return 0
        else:
            return -1 if len(l) < len(r) else 1

    if type(l) == type(r) == int:
        return compareInt(l, r)
    elif type(l) == type(r) == list:
        return compareList(l, r)
    elif type(l) != type(r):
        # One of the element is a list while the other is an int. Promote
        # the int to a list.
        if type(l) == int:
            return compareList([l], r)
        else:
            return compareList(l, [r])

def part1(inputFile):
    pairs = parseInput(inputFile)
    cmpRes = enumerate([compare(p[0], p[1]) for p in pairs])
    cmpRes = list(filter(lambda r: r[1] == -1, cmpRes))
    return sum(map(lambda r: r[0] + 1, cmpRes))

def part2(inputFile):
    pairs = parseInput(inputFile)
    elems = [e for p in pairs for e in p]
    elems.append([[2]])
    elems.append([[6]])
    elems = sorted(elems, key=cmp_to_key(compare))

    div1Idx = list(map(lambda e: e[0]+1, filter(lambda e: e[1] == [[2]], enumerate(elems))))[0]
    div2Idx = list(map(lambda e: e[0]+1, filter(lambda e: e[1] == [[6]], enumerate(elems))))[0]
    return div1Idx * div2Idx

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
