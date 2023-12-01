#!/usr/bin/env python

import sys

def parseInput(inputFile):
    # Parse the entire input file and returns a pair where the first element is
    # the stacks configuration (a dict. int -> list of str) and the second is
    # the procedure (e.g. list of moves).
    # The list in the stacks configuration represent the content of a given
    # stack where index 0 is the _bottom_ crate of the stack.
    # The list of moves is a list of tuple of the form (N, src, dst) indicating
    # that N crates should be moved from stack with id `src` to stack with id
    # `dst`.

    fd = open(inputFile, "r")
    lines = fd.readlines()

    # The stacks configuration
    stacks = {}

    def addToBottomOfStack(stackId, elem):
        # Add an element to the bottom of the stack. stackId must be >= 1, elem
        # is the str/char of the crate to be added to the stack.
        if not stackId in stacks.keys():
            # First time we are seeing this stack, create it.
            stacks[stackId] = [elem]
        else:
            stacks[stackId] = [elem] + stacks[stackId]
    
    # Parse the stacks initial configuration from top to bottom, hence why we
    # add at the bottom of the stacks at each step.
    stackConfig = list(filter(lambda l: "[" in l, lines))
    for row in stackConfig:
        # We can use the index of the A-Z chars in the line/row to compute which
        # stack they belong to. For stack id 1, the chars are in col/index 1,
        # for stack 2 the index is 5, for stack 3 it is 9, ...
        # Hence for stack i, the index of the crate name is 1 + 4*(i-1). NOTE: i
        # is >= 1 here!
        # crates[i] corresponds to stack[i+1] at this row. crates[i] might be
        # empty if stack[i+1] does not contain a crate at this height.
        crates = [row[i] for i in range(1, len(row), 4)]
        for i, crate in enumerate(crates):
            if crate != " ":
                stackId = i + 1
                addToBottomOfStack(stackId, crate)

    # Stacks initial configuration parsing done, parse the list of moves.
    # +2 because we need to take the line with the stack ids and the blank line
    # into account.
    moves = lines[len(stackConfig) + 2:]
    def parseMove(l):
        # Parse the move described by line l, which must be of the form "move N
        # from X to Y". Returns the tuple (N,X,Y).
        parts = l.replace("\n", "").split(" ")
        return (int(parts[1]), int(parts[3]), int(parts[5]))
    moves = list(map(lambda l: parseMove(l), moves))
    
    return (stacks, moves)

def applyMoves(stacks, moves, canMoveMultiple):
    # Given stacks configuration `stacks` (a dict) and a list of moves (list of
    # tuple), apply all the moves on the configuration. `stacks` is modified
    # directly, e.g. no copying.
    # `canMoveMultiple` indicates if the crane can pick-up and move multiple
    # crates at once.
    def applyMove(m):
        # Apply move `m` on `stacks`.
        N, src, dst = m
        # Moving N crates from `src` to `dst` is simply done by moving the top N
        # crates of stack `src` and add them top the top of `dst`:
        #   - the same order if canMoveMultiple == True
        #   - in reverse order if canMoveMultiple == False
        assert src in stacks.keys() and dst in stacks.keys()
        # The top N crates from src.
        topN = stacks[src][-N:]
        # Remove the top N crates from src.
        stacks[src] = stacks[src][:-N]
        # Add the N crates in reverse order to dst.
        if not canMoveMultiple:
            topN.reverse()
        stacks[dst] += topN

    for m in moves:
        applyMove(m)

def part1(inputFile):
    stacks, moves = parseInput(inputFile)
    # Apply all the moves on the stacks configuration.
    applyMoves(stacks, moves, False)
    # Compute the result by concatenating the top of each stack.
    numStacks = len(stacks.keys())
    return "".join([stacks[i+1][-1] for i in range(numStacks)])

def part2(inputFile):
    stacks, moves = parseInput(inputFile)
    # Apply all the moves on the stacks configuration.
    applyMoves(stacks, moves, True)
    # Compute the result by concatenating the top of each stack.
    numStacks = len(stacks.keys())
    return "".join([stacks[i+1][-1] for i in range(numStacks)])

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
