#!/usr/bin/env python

import sys
import re
import copy
import cProfile

# Represents the cost of buying a robot in number of ore, clay and obsi
class Cost:
    def __init__(self, ore, clay, obsidian):
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian

    def __repr__(self):
        return str((self.ore, self.clay, self.obsidian))

class Blueprint:
    def __init__(self, oreRobotCost, clayRobotCost, obsidianRobotCost, geodeRobotCost):
        self.oreRobotCost      = oreRobotCost
        self.clayRobotCost     = clayRobotCost
        self.obsidianRobotCost = obsidianRobotCost
        self.geodeRobotCost    = geodeRobotCost

    # Compute the maximum number of geodes that can be opened in INIT_TIME
    # minutes.
    def maxOpenedGeodes(self, INIT_TIME):
        # Represent a state node.
        class State:
            def __init__(self):
                self.remainingTime = INIT_TIME
                self.availOre = 0
                self.availClay = 0
                self.availObsidian = 0
                self.availGeode = 0
                self.numOreRobots = 1
                self.numClayRobots = 0
                self.numObsidianRobots = 0
                self.numGeodeRobots = 0

            def __repr__(self):
                r ="  remainingTime     = {}\n".format(self.remainingTime)+\
                   "  availOre          = {}\n".format(self.availOre)+\
                   "  availClay         = {}\n".format(self.availClay)+\
                   "  availObsidian     = {}\n".format(self.availObsidian)+\
                   "  availGeode        = {}\n".format(self.availGeode)+\
                   "  numOreRobots      = {}\n".format(self.numOreRobots)+\
                   "  numClayRobots     = {}\n".format(self.numClayRobots)+\
                   "  numObsidianRobots = {}\n".format(self.numObsidianRobots)+\
                   "  numGeodeRobots    = {}\n".format(self.numGeodeRobots)
                return r

            def __hash__(self):
                return hash((self.remainingTime, \
                             self.availOre, \
                             self.availClay, \
                             self.availObsidian, \
                             self.availGeode, \
                             self.numOreRobots, \
                             self.numClayRobots, \
                             self.numObsidianRobots, \
                             self.numGeodeRobots))

            def __eq__(self, other):
                return self.remainingTime     == other.remainingTime and \
                       self.availOre          == other.availOre and \
                       self.availClay         == other.availClay and \
                       self.availObsidian     == other.availObsidian and \
                       self.availGeode        == other.availGeode and \
                       self.numOreRobots      == other.numOreRobots and \
                       self.numClayRobots     == other.numClayRobots and \
                       self.numObsidianRobots == other.numObsidianRobots and \
                       self.numGeodeRobots    == other.numGeodeRobots

            # Compute the set of possible next states from this state.
            def nextStates(self, bp):
                maxOreRobots = max(bp.oreRobotCost.ore, \
                                   bp.clayRobotCost.ore,\
                                   bp.obsidianRobotCost.ore, \
                                   bp.geodeRobotCost.ore)
                maxClayRobots = max(bp.oreRobotCost.clay, \
                                    bp.clayRobotCost.clay,\
                                    bp.obsidianRobotCost.clay, \
                                    bp.geodeRobotCost.clay)
                maxObsiRobots = max(bp.oreRobotCost.obsidian, \
                                    bp.clayRobotCost.obsidian,\
                                    bp.obsidianRobotCost.obsidian, \
                                    bp.geodeRobotCost.obsidian)

                nextStateTemplate = copy.copy(self)
                # Next state will be at t = time - 1
                nextStateTemplate.remainingTime -= 1
                # Account for income from each robot for the next state.
                nextStateTemplate.availOre += self.numOreRobots
                nextStateTemplate.availClay += self.numClayRobots
                nextStateTemplate.availObsidian += self.numObsidianRobots
                nextStateTemplate.availGeode += self.numGeodeRobots

                # We can always do nothing.
                n = [nextStateTemplate]

                # Check if we can buy a robot in the next state. Note that
                # robots are bought at the beginning of a minute/state.
                # Therefore, resources collected at minute t cannot be used to
                # buy a robot at minute t. This is why the canAfford() check is
                # made on the current state, and the buy() on the next state.
                # Additionally, we only buy a robot if its going to have time to
                # do useful work.
                if self.remainingTime > 1:
                    # Heuristic: If we can buy a geode robot then buy it and
                    # don't look into any other state. The rationale is that we
                    # want to buy geode robots as early as possible to maximize
                    # the rate of geodes opened.
                    if self.canAfford(bp.geodeRobotCost):
                        newState = nextStateTemplate.buy(bp.geodeRobotCost)
                        newState.numGeodeRobots += 1
                        n = [newState]
                    else:
                        if self.canAfford(bp.obsidianRobotCost) and \
                           self.numObsidianRobots < maxObsiRobots:
                            newState = nextStateTemplate.buy(bp.obsidianRobotCost)
                            newState.numObsidianRobots += 1
                            n.append(newState)
                        if self.canAfford(bp.clayRobotCost) and \
                           self.numClayRobots < maxClayRobots:
                            newState = nextStateTemplate.buy(bp.clayRobotCost)
                            newState.numClayRobots += 1
                            n.append(newState)
                        if self.canAfford(bp.oreRobotCost) and \
                           self.numOreRobots < maxOreRobots:
                            newState = nextStateTemplate.buy(bp.oreRobotCost)
                            newState.numOreRobots += 1
                            n.append(newState)
                return n

            # Check if this state can afford a robot.
            def canAfford(self, robotCost):
                return robotCost.ore <= self.availOre and \
                       robotCost.clay <= self.availClay and \
                       robotCost.obsidian <= self.availObsidian

            # Return a copy of this state after buying a robot.
            def buy(self, robotCost):
                assert self.canAfford(robotCost)
                newState = State()
                newState.remainingTime       = self.remainingTime  
                newState.availOre            = self.availOre - robotCost.ore
                newState.availClay           = self.availClay - robotCost.clay
                newState.availObsidian       = self.availObsidian - robotCost.obsidian
                newState.availGeode          = self.availGeode  
                newState.numOreRobots        = self.numOreRobots  
                newState.numClayRobots       = self.numClayRobots  
                newState.numObsidianRobots   = self.numObsidianRobots  
                newState.numGeodeRobots      = self.numGeodeRobots  
                return newState

            # Check if this current state can beat the number of opened geodes
            # `numGeodes` by the time remainingTime becomes 0.
            def canBeatByTimeout(self, numGeodes):
                # Best case scenario, we create a new geode robot at every
                # minute until the end, including this very minute
                m = self.remainingTime - 1
                best = m * (m + 1) / 2
                # Also take into account the current number of geodes opened and
                # the number of geode robot currently available.
                best += self.numGeodeRobots * self.remainingTime + self.availGeode
                return best >= numGeodes

        startState = State()
        S = [startState]
        visited = set()
        maxOpenedGeodes = 0

        while len(S) > 0:
            curr = S.pop(0)
            
            if curr in visited:
                continue
            else:
                visited.add(copy.copy(curr))

            if curr.remainingTime == 0:
                # This is a goal node, check against the known
                # maxOpenedGeodes.
                maxOpenedGeodes = max(maxOpenedGeodes, curr.availGeode)
                continue

            if not curr.canBeatByTimeout(maxOpenedGeodes):
                # This state cannot possibly beat the current known
                # maxOpenedGeodes by the time it runs out of time. Just
                # prune it, this saves computation.
                continue

            possibleNextStates = curr.nextStates(self)
            for s in possibleNextStates:
                S.insert(0,s)

        return maxOpenedGeodes


def parseInput(inputFile):
    fd = open(inputFile, "r")
    blueprints = []
    for l in fd.readlines():
        nums = list(map(lambda n: int(n), re.findall("[0-9]+", l)))
        oreRCost = Cost(nums[1], 0, 0)
        clayRCost = Cost(nums[2], 0, 0)
        obsiRCost = Cost(nums[3], nums[4], 0)
        geoRCost = Cost(nums[5], 0, nums[6])
        blueprints.append(Blueprint(oreRCost, clayRCost, obsiRCost, geoRCost))
    fd.close()
    return blueprints

def part1(inputFile):
    blueprints = parseInput(inputFile)
    res = 0
    for i, b in enumerate(blueprints):
        m = b.maxOpenedGeodes(24)
        qlvl = (i + 1) * m
        print("BP {} quality level = {}".format(i, qlvl))
        res += qlvl
    return res

def part2(inputFile):
    blueprints = parseInput(inputFile)
    res = 1
    for i, b in enumerate(blueprints[:3]):
        m = b.maxOpenedGeodes(32)
        print("BP {} quality level = {}".format(i+1, m))
        res *= m
    return res

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
