#!/usr/bin/env python

import sys

def part1(inputFile):
    def outcome(hand1,hand2):
        # Returns -1 if hand1 beats hand2, 0 if draw, 1 if hand2 beats hand1.
        # hand1 must be in {A,B,C}, hand2 must be in {X,Y,Z}.

        # Translate hand2 into {A,B,C}
        hand2 = chr(ord(hand2[0]) - (ord("X") - ord("A")))

        if hand1 == hand2:
            return 0

        rock = "A"
        paper = "B"
        scissors = "C"

        if hand1 == rock:
            return -1 if hand2 == scissors else 1
        elif hand1 == paper:
            return -1 if hand2 == rock else 1
        else:
            return -1 if hand2 == paper else 1

    fd = open(inputFile, "r")
    lines = fd.readlines()

    totalScore = 0
    for l in lines:
        hands = l.replace("\n","").split(" ")
        result = outcome(hands[0], hands[1])
        # Map [-1;1] to [0;6]
        totalScore += (result + 1) * 3
        totalScore += ord(hands[1][0]) - ord("X") + 1

    return totalScore

def part2(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()

    totalScore = 0
    for l in lines:
        parts = l.replace("\n","").split(" ")
        oppoHand = parts[0]
        outcome = parts[1]
        totalScore += (ord(outcome) - ord("X")) * 3

        # Helper values
        lose = "X"
        draw = "Y"
        win = "Z"
        rock = "A"
        paper = "B"
        scissors = "C"

        if outcome == draw:
            # Easy case
            neededHand = oppoHand
        elif outcome == lose:
            if oppoHand == rock:
                neededHand = scissors
            elif oppoHand == paper:
                neededHand = rock
            else:
                neededHand = paper
        else:
            # outcome == win
            if oppoHand == rock:
                neededHand = paper
            elif oppoHand == paper:
                neededHand = scissors
            else:
                neededHand = rock

        # Compute the contribution of needed hand to the score
        totalScore += (ord(neededHand) - ord("A")) + 1

    return totalScore

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
