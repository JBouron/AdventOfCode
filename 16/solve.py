#!/usr/bin/env python

import sys
import re

class Valve:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.next = set()

    def addNext(self, valve):
        self.next.add(valve)

    def delNext(self, valve):
        self.next = set(filter(lambda n: n[0] != valve, self.next))

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)

def parseInput(inputFile):
    fd = open(inputFile, "r")
    nextValve = {}
    lines = fd.readlines()
    # First create all the valves.
    nameToValve = {}
    valves = set()
    for l in lines:
        rate = int(re.findall("[0-9]+", l)[0])
        name = re.findall("[A-Z][A-Z]", l)[0]
        r = Valve(name, rate)
        nameToValve[name] = r
        valves.add(r)

    # Then parse all the tunnels.
    for l in lines:
        names = re.findall("[A-Z][A-Z]", l)
        valve = nameToValve[names[0]]
        nextValve = list(map(lambda n: nameToValve[n], names[1:]))
        for v in nextValve:
            valve.addNext(v)

    fd.close()
    return valves

def part1(inputFile):
    valves = parseInput(inputFile)

    # Implements memoization.
    cache = {}
    # Get the key associated to the arguments of find() for memoization.
    def getKey(startValue, opened, timeLeft):
        return (startValue, opened, timeLeft)

    calls = 0
    cached = 0

    # Find how much pressure can be released when starting in Valve `startValve`
    # while having the set of valves `opened` currently opened, with `timeLeft`
    # minutes left.
    def find(startValve, opened, timeLeft):
        nonlocal calls
        nonlocal cached
        #print((startValve, opened, timeLeft))
        calls += 1
        k = getKey(startValve, opened, timeLeft)
        if k in cache.keys():
            cached += 1
            return cache[k]
        if timeLeft <= 0 or len(opened) == len(valves):
            # Base-case 1: Running out of time.
            # Base-case 2: All valves have been opened.
            # In both cases the max pressure has been taken into accound in the
            # previous recursive calls, hence nothing to be added here.
            res = 0
            cache[k] = res
            return res
        # We now need to choose between:
        #   - Opening the current valve and moving to the next valve vi. Only
        #   possible if the valve is not already opened.
        #   - Not opening the current valve and moving to the next valve vi.
        # for all next valve vi. And take the maximum.
        choices = []
        # Case #1: We open the current valve. We only consider this if the rate
        # of that valve is non-zero.
        if startValve not in opened and startValve.rate > 0:
            for v in startValve.next:
                # The total pressure that will be release from this valve:
                dp = startValve.rate * (timeLeft - 1)
                newOpened = opened | frozenset([startValve])
                # We spent a minute opening the valve and another d minutes to
                # move to the next room. So we only have timeLeft - 1 - d
                # minutes left when arriving in the next room
                choices.append(dp + find(v, newOpened, timeLeft - 1 - 1))
        # Case #2: We do not open the current valve.
        for v in startValve.next:
            # We spent d minutes to move to the next room, so there will be
            # timeLeft - d minutes left when arriving in the next room.
            choices.append(find(v, opened, timeLeft - 1))
        res = max(choices)
        cache[k] = res
        return res

    startValve = list(filter(lambda v: v.name == "AA", valves))[0]
    return find(startValve, frozenset(), 30)

def part2(inputFile):
    valves = parseInput(inputFile)

    # Implements memoization.
    cache = {}
    # Get the key associated to the arguments of find() for memoization.
    def getKey(curr, opened, timeLeft):
        return (curr[0], curr[1], opened, timeLeft)

    calls = 0
    cached = 0

    # Find how much pressure can be released when starting in Valve `curr`
    # while having the set of valves `opened` currently opened, with `timeLeft`
    # minutes left.
    def find(curr, opened, timeLeft):
        nonlocal calls
        nonlocal cached
        #print((curr, opened, timeLeft))
        calls += 1
        k = getKey(curr, opened, timeLeft)
        if k in cache.keys():
            cached += 1
            return cache[k]
        if timeLeft <= 0 or len(opened) == len(valves):
            # Base-case 1: Running out of time.
            # Base-case 2: All valves have been opened.
            # In both cases the max pressure has been taken into accound in the
            # previous recursive calls, hence nothing to be added here.
            res = 0
            cache[k] = res
            return res
        # We now need to choose between:
        #   - Opening the current valve and moving to the next valve vi. Only
        #   possible if the valve is not already opened.
        #   - Not opening the current valve and moving to the next valve vi.
        # for all next valve vi. And take the maximum.
        choices = []
        elCurr = curr[0]
        myCurr = curr[1]
        # Case #1: We open the current valve. We only consider this if the rate
        # of that valve is non-zero. It turns out that checking for this
        # improves performance significantly since the input has a substantial
        # amount of valves with a max rate of 0.
        if elCurr not in opened and elCurr.rate > 0:
            dp = elCurr.rate * (timeLeft - 1)
            newOpened = opened | frozenset([elCurr])
            for v in myCurr.next:
                choices.append(dp + find((elCurr, v), newOpened, timeLeft - 1))
        if myCurr not in opened and myCurr.rate > 0:
            dp = myCurr.rate * (timeLeft - 1)
            newOpened = opened | frozenset([myCurr])
            for v in elCurr.next:
                choices.append(dp + find((v, myCurr), newOpened, timeLeft - 1))
        if (elCurr not in opened and elCurr.rate > 0) and \
           (myCurr not in opened and myCurr.rate > 0) and \
           myCurr != elCurr:
            dp = (elCurr.rate + myCurr.rate) * (timeLeft - 1)
            newOpened = opened | frozenset([myCurr, elCurr])
            for ev in elCurr.next:
                for mv in myCurr.next:
                    choices.append(dp + find((ev, mv), newOpened, timeLeft - 2))
        for ev in elCurr.next:
            for mv in myCurr.next:
                choices.append(find((ev, mv), opened, timeLeft - 1))
        res = max(choices)
        cache[k] = res
        return res

    curr = list(filter(lambda v: v.name == "AA", valves))[0]
    return find((curr, curr), frozenset(), 26)

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
