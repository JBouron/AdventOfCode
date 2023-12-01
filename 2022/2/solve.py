#!/usr/bin/env python

import sys

# rock = 0
# paper = 1
# scissors = 2

def outcome(h1, h2):
    # Return -1 if h1 beats h2, 0 if draw, 1 if h2 beats h1.
    if h1 == (h2 + 1) % 3:
        return -1
    elif h1 == h2:
        return 0
    else:
        return 1

def part1(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()

    totalScore = 0
    for l in lines:
        hands = l.replace("\n","").split(" ")
        oppoHand = ord(hands[0]) - ord("A")
        myHand = ord(hands[1]) - ord("X")

        result = outcome(oppoHand, myHand)
        # Map [-1;1] to [0;6]
        totalScore += (result + 1) * 3
        totalScore += myHand + 1

    return totalScore

def part2(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()

    totalScore = 0
    for l in lines:
        parts = l.replace("\n","").split(" ")
        oppoHand = ord(parts[0]) - ord("A")
        # neededOutcome:
        #   -1 if oppo needs to win
        #   0 if draw
        #   1 if need to win
        neededOutcome = ord(parts[1]) - ord("X") - 1
        neededHand = (oppoHand + neededOutcome) % 3
        totalScore += (neededOutcome + 1) * 3
        totalScore += neededHand + 1

    return totalScore

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
