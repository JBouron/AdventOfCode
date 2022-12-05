#!/usr/bin/env python

import sys

def parseRangePair(line):
    # Parse the range pair encoded in a line of input. Return a pair of range
    # type described by the line.
    def parseRange(r):
        # Parse the range encoded in "a-b". Return a range type.
        parts = r.split("-")
        start = int(parts[0])
        end = int(parts[1])
        assert start <= end
        # +1 needed because range type does not include the end value.
        return range(start, end + 1)
    ranges = line.split(",")
    assert len(ranges) == 2
    return tuple(map(lambda r: parseRange(r), ranges))

def fullyContains(r1, r2):
    # Return True if r1 fully contains r2. r1 and r2 are range type, their step
    # must be 1.
    assert r1.step == 1 and r2.step == 1
    return r1.start <= r2.start and r2.stop <= r1.stop

def part1(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()

    rangePairs = list(map(lambda l: parseRangePair(l), lines))

    def pairFullyOverlap(p):
        # Return True if the ranges described in the pair `p` are so that one
        # fully contains the other.
        return fullyContains(p[0], p[1]) or fullyContains(p[1], p[0])

    fullOverlaps = list(filter(lambda p: pairFullyOverlap(p), rangePairs))
    return len(fullOverlaps)

def overlap(r1, r2):
    # Return True if r1 and r2 are overlapping. r1 and r2 are range type, their
    # step must be 1.
    assert r1.step == 1 and r2.step == 1
    # Either the start or stop of r1 are contain in r2, in which case the range
    # obviously overlap. The only edge case is if r2 is fully contained in r1,
    # hence the test "r2.start in r1".
    # stop-1 needed here because the stop is excluded from the range.
    return (r1.start in r2 or (r1.stop - 1) in r2) or r2.start in r1

def part2(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines();

    rangePairs = list(map(lambda l: parseRangePair(l), lines))
    overlaps = list(filter(lambda p: overlap(p[0], p[1]), rangePairs))
    return len(overlaps)

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
