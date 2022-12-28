#!/usr/bin/env python

import sys

# Return the list of number in SNAFU format.
def parseInput(inputFile):
    fd = open(inputFile, "r")
    lines = fd.readlines()
    fd.close()
    return list(map(lambda l: l.replace("\n", ""), lines))

# Converts a SNAFU digit to its base 10 equivalent.
snafuDigitToBase10 = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}

base10DigitToSnafu = {
    2:  "2",
    1:  "1",
    0:  "0",
    -1: "-",
    -2: "=",
}

# Converts a SNAFU number to decimal
def toDec(sNum):
    digits = list(sNum)
    digits.reverse()
    res = 0
    for i, d in enumerate(digits):
        res += snafuDigitToBase10[d] * 5 ** i
    return res

# Convert a decimal number into SNAFU.
def toSnafu(dNum):
    digits = {}
    i = 0
    # First convert to base 5.
    while dNum > 0:
        d, m = dNum // 5, dNum % 5
        dNum = d
        digits[i] = m
        i += 1

    # Then fixup all the digits that are > 2.
    done = False
    while not done:
        done = True
        # Can't change the size of a dict while iterating, hence everytime we
        # change the dict we restart the process.
        for i, d in digits.items():
            if d > 2:
                digits[i] = digits[i] - 5
                digits[i+1] = digits.get(i+1, 0) + 1
                done = False
                break
    digits = list(digits.items())
    digits.sort(key=lambda i: -i[0])
    return "".join([base10DigitToSnafu[e[1]] for e in digits])

def part1(inputFile):
    nums = parseInput(inputFile)
    return toSnafu(sum([toDec(n) for n in nums]))

def part2(inputFile):
    return 0

if __name__ == "__main__":
    inputFile = sys.argv[1]
    print("Part 1: {}".format(part1(inputFile)))
    print("Part 2: {}".format(part2(inputFile)))
