#!/usr/bin/env python

import sys

def getDuplicateItemType(sackContent):
    # For a sack's content, compute the type of item that appear in both
    # compartments.
    l = len(sackContent)
    h = l//2
    firstCompartment = set(sackContent[:h])
    secondCompartment = set(sackContent[h:])
    inter = firstCompartment.intersection(secondCompartment)
    assert len(inter) == 1
    # Get first and only element of the set.
    return next(iter(inter))

def getPriorityForItemType(t):
    # For an item type t = [a-z][A-Z], compute its numerical priority.
    return (ord(t) - ord('A') + 27) if ord(t) <= ord('Z') else (ord(t) - ord('a') + 1)

def part1(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()
    commonTypes = list(map(lambda l: getDuplicateItemType(l.replace("\n","")), lines))
    priorities = list(map(lambda l: getPriorityForItemType(l), commonTypes))
    return sum(priorities)

def part2(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines();
    lines = list(map(lambda l: l.replace("\n", ""), lines))
    groupSacks = [lines[i*3:(i+1)*3] for i in range(len(lines) // 3)]
    # Compute the common item in the sacks of a given group.
    common = lambda s: set(s[0]).intersection(set(s[1])).intersection(set(s[2]))
    groupCommon = list(map(common, groupSacks))
    # Get the only element from the set
    groupCommon = list(map(lambda s: next(iter(s)), groupCommon))
    return sum(map(lambda t: getPriorityForItemType(t), groupCommon))

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
