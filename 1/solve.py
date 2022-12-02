#!/usr/bin/env python

import sys

def part1(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()
    sums = []
    curr = 0
    for l in lines:
        if l == "\n":
            sums.append(curr)
            curr = 0
        else:
            curr += int(l)
    # Last elf does not have a blank line after it.
    sums.append(curr)
    return max(sums)

def part2(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()
    sums = []
    curr = 0
    for l in lines:
        if l == "\n":
            sums.append(curr)
            curr = 0
        else:
            curr += int(l)
    # Last elf does not have a blank line after it.
    sums.append(curr)
    sums.sort()
    return sum(sums[-3:])

def main():
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))

if __name__ == "__main__":
    main();
