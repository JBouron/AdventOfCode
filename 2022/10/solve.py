#!/usr/bin/env python

import sys

def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = list(map(lambda l: l.replace("\n", ""), fd.readlines()))
    fd.close()
    return lines

def part1(inputFile):
    cycle = 0
    X = 1

    ss = {}
    def updateSignalStrengths():
        for i in range(20, 221, 40):
            if i <= cycle and i not in ss.keys():
                ss[i] = i * X

    instructions = parseInput(inputFile)
    for inst in instructions:
        if inst == "noop":
            cycle += 1
            updateSignalStrengths()
        else:
            assert "addx" in inst
            v = int(inst.split(" ")[1])
            cycle += 2
            updateSignalStrengths()
            X += v
    assert len(ss.keys()) == 6
    return sum(ss.values())

def part2(inputFile):
    cycle = 0
    X = 1
    CRTCol = 0

    # Draw a pixel. n indicates the number of times the operation should be
    # repeated.
    def drawPixel(n):
        nonlocal CRTCol
        for i in range(n):
            print("#" if abs(CRTCol - X) <= 1 else ".", end="")
            CRTCol = (CRTCol + 1) % 40
            if CRTCol == 0:
                # new row
                print("")

    instructions = parseInput(inputFile)
    for inst in instructions:
        if inst == "noop":
            cycle += 1
            drawPixel(1)
        else:
            assert "addx" in inst
            v = int(inst.split(" ")[1])
            cycle += 2
            drawPixel(2)
            X += v
    return 0

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
