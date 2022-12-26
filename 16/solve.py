#!/usr/bin/env python

import sys
import re
import copy
import cProfile
import itertools

class Valve:
    def __init__(self, name, rate):
        self.name = name
        self.rate = rate
        self.next = []

    def addNext(self, valve, dist):
        self.next.append((valve, dist))

    def delNext(self, valve):
        self.next = list(filter(lambda n: n[0][0] != valve, self.next))

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
    valves = []
    for l in lines:
        rate = int(re.findall("[0-9]+", l)[0])
        name = re.findall("[A-Z][A-Z]", l)[0]
        r = Valve(name, rate)
        nameToValve[name] = r
        valves.append(r)

    # Then parse all the tunnels.
    for l in lines:
        names = re.findall("[A-Z][A-Z]", l)
        valve = nameToValve[names[0]]
        nextValve = list(map(lambda n: nameToValve[n], names[1:]))
        for v in nextValve:
            valve.addNext(v, 1)
    
    # For a valve, compute the shortest distance to all other valves. Return a
    # list of pairs (valves, dist).
    def computeShortestPaths(v):
        Q = [v]
        visited = set()
        dist = {v: 0}
        while len(Q) > 0:
            curr = Q.pop(0)
            assert curr in dist.keys()
            for n, d in curr.next:
                if n not in visited:
                    visited.add(n)
                    if n not in dist.keys():
                        dist[n] = dist[curr] + d
                    else:
                        dist[n] = min(dist[n], dist[curr] + d)
                    Q.append(n)
        # Delete self.
        del dist[v]
        return list(dist.items())

    # Updates the `next` of each valves so that there is a "direct" path to
    # every other valve.
    # NOTE: We need to be careful here and only update the 'next' of each valves
    # once all shortest paths have been computed. Otherwise the shortest path
    # computation won't work since it assumes that all paths between valves are
    # length 1 (thus uses BFS instead of Dijikstra).
    dists = []
    for v in valves:
        dists.append(computeShortestPaths(v))
    for i in range(len(valves)):
        valves[i].next = dists[i]

    # Prune all valves that have a zero rate, those are never opened. However we
    # need to keep the starting valve "AA" around!
    valves = [v for v in valves if v.rate > 0 or v.name == "AA"]
    # Also need to get rid of all the 'next' pointing to 0-rate valves.
    for v in valves:
        v.next = [p for p in v.next if p[0].rate > 0 or p[0].name == "AA"]

    fd.close()
    return frozenset(valves)

# Compute the maximum pressure that can be released when starting at valve
# `startValve` under `timeLimit` minutes.
maxPressureCache = {}
def maxPressureKey(valves, startValves, timeLimit):
    return (valves, startValves, timeLimit)

def maxPressure(valves, startValve, timeLimit):
    K = maxPressureKey(valves, startValve, timeLimit)
    if K in maxPressureCache.keys():
        return maxPressureCache[K]

    class State:
        def __init__(self):
            self.remainingTime = timeLimit
            self.opened = frozenset()
            self.curr = startValve
            self.totalReleased = 0
            # The previous valve we were to. Note that this attribute is not
            # taken into account when hashing or comparing states. This
            # attribute is only used to avoid sub-optimal next states.
            self.prev = None

        def __eq__(self, other):
            return self.remainingTime == other.remainingTime and \
                   self.opened        == other.opened and \
                   self.curr          == other.curr and \
                   self.totalReleased == other.totalReleased

        def __hash__(self):
            return hash((self.remainingTime, \
                         self.opened, \
                         self.curr, \
                         self.totalReleased))

        def __repr__(self):
            return "remainingTime = {}\n".format(self.remainingTime) + \
            "opened        = {}\n".format(self.opened) + \
            "curr          = {}\n".format(self.curr) + \
            "totalReleased = {}\n".format(self.totalReleased)

        # Compute the score of this state. This is a heuristic used to speed-up
        # the search for the optimal solution.
        def score(self):
            res = self.totalReleased
            res += self.remainingTime * sum([v.rate for v in self.opened])
            res += self.curr.rate if self.curr not in self.opened else 0
            # Small penalty if going back to an open valve.
            res -= 10 if self.curr in self.opened else 0
            return res

        # Compute the best release this state can reach in the very best case
        # scenario.
        def bestCaseRelease(self):
            # In the perfect scenario we can open the best valve at each step.
            # Since it takes a minute to open a valve and a least a minute to go
            # to the next valves, this means in the perfect scenario we can open
            # the best valve every 2 minutes.
            r = self.totalReleased
            toOpen = list(valves - self.opened)
            toOpen.sort(key=lambda v: -v.rate)
            r += self.remainingTime * sum([v.rate for v in self.opened])
            t = self.remainingTime
            for i, v in enumerate(toOpen):
                if i > 0 and i % 2 == 0:
                    t -= 2
                    if t <= 0:
                        break

                r += v.rate * t

            return r

        # Compute the set of possible next states from this one.
        def nextStates(self):
            # Update the total release pressure.
            prev = self.prev
            self.prev = self.curr
            maxRate = max([v.rate for v in (valves - self.opened)])

            nonZeroValves = [v for v in valves if v.rate > 0]
            if len(self.opened) == len(nonZeroValves):
                # All valves are opened, nothing to do anymore except wait.
                newState = copy.copy(self)
                newState.totalReleased += sum([v.rate for v in self.opened])
                newState.remainingTime -= 1
                return [newState]

            if self.curr not in self.opened and self.curr.rate > 0:
                # We can open the current valve.
                # Since it takes a minute to open a valve, we stay on self.curr
                # in the next state.
                newState = copy.copy(self)
                newState.remainingTime -= 1
                newState.opened = newState.opened | frozenset([self.curr])
                # Account for the pressure released while opening the valve.
                # Note: the valve being opened does not add to the released
                # pressure just yet.
                newState.totalReleased += sum([v.rate for v in self.opened])
                return [newState]

            nextStates = []
            for n, d in self.curr.next:
                if n in self.opened:
                    # The graph has been re-worked into a fully connected graph.
                    # As a result, there is no reason whatsoever to walk to an
                    # opened valve.
                    continue
                elif n.rate == 0:
                    # We are going to a zero-rate valve, that is the starting
                    # valve (since all other zero-rate valves were pruned). This
                    # is a sub-optimal choice.
                    continue
                elif self.remainingTime - d <= 0:
                    # We won't have enough time to make it to this next valve,
                    # let alone open it. Skip.
                    continue
                elif n == prev:
                    # We are attempting to immediately go back to where we came
                    # from. This is obviously a bad move.
                    continue
                newState = copy.copy(self)
                newState.remainingTime -= d
                newState.curr = n
                # Account for the pressure released while walking to the next
                # valve.
                newState.totalReleased += d * sum([v.rate for v in self.opened])
                nextStates.append(newState)

            if len(nextStates) == 0:
                newState = copy.copy(self)
                newState.remainingTime -= 1
                newState.totalReleased += sum([v.rate for v in self.opened])
                return [newState]

            return nextStates

    start = State()

    S = [start]
    visited = set()
    maxRelease = 0

    while len(S) > 0:
        curr = S.pop(0)

        if curr in visited:
            continue
        else:
            visited.add(copy.copy(curr))

        if curr.remainingTime == 0:
            maxRelease = max(maxRelease, curr.totalReleased)
            continue
        
        if curr.bestCaseRelease() < maxRelease:
            continue

        nextStates = curr.nextStates()
        nextStates.sort(key=lambda s: s.score())
        for n in nextStates:
            S.insert(0, n)
    maxPressureCache[K] = maxRelease
    return maxRelease

def part1(inputFile):
    valves = parseInput(inputFile)
    startValve = list(filter(lambda v: v.name == "AA", valves))[0]
    return maxPressure(valves, startValve, 30)

def subsets(valves, length):
    if length == 1:
        res = []
        for v in valves:
            res.append(set([v]))
        return res
    else:
        res = []
        for i, v in enumerate(valves):
            first = v
            for s in subsets(valves[i+1:], length - 1):
                res.append(set([first]) | s)
        return res

def valvesForSubset(sub):
    res = [Valve(v.name, v.rate) for v in sub]
    nameToValve = {}
    for v in res:
        nameToValve[v.name] = v
    for v in sub:
        cpy = nameToValve[v.name]
        cpy.next = [(nameToValve[n.name], d) for n, d in v.next if n in sub]
    return frozenset(res)

def part2(inputFile):
    valves = parseInput(inputFile)
    startValve = list(filter(lambda v: v.name == "AA", valves))[0]
    otherValves = list(filter(lambda v: v.name != "AA", valves))
    num = 0
    maxRelease = 0
    for subsetLen in range(1, 1 + (len(valves) - 1) // 2):
        for subset in subsets(list(otherValves), subsetLen):
            # AA should always be in the subset since this is the starting
            # valve. The subset are computed on Valves \{AA}.
            assert startValve not in subset
            subset.add(startValve)
            complement = set(valves - subset)
            complement.add(startValve)

            subset = valvesForSubset(subset)
            complement = valvesForSubset(complement)

            start = list(filter(lambda v: v.name == "AA", subset))[0]
            bestSubset = maxPressure(subset, start, 26)
            start = list(filter(lambda v: v.name == "AA", complement))[0]
            bestComplement = maxPressure(complement, start, 26)

            curr = bestSubset + bestComplement
            maxRelease = max(maxRelease, curr)
    return maxRelease

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
