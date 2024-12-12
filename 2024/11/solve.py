#!/bin/python3

import sys

ORIG_STONES = list(
    map(lambda s: int(s),
        open(sys.argv[1], "r").readline().replace("\n", "").split(" ")))

# Given a list of stones, apply the rules once and all the stones.
# @param stones: The list of stones.
# @return: A new list containing the state of the stones after applying the
# rules, i.e. after the blink.
def apply_rules(stones):
    res = []
    for s in stones:
        if s == 0:
            # If the stone is engraved with the number 0, it is replaced by a
            # stone engraved with the number 1.
            res.append(1)
        elif len(str(s)) % 2 == 0:
            # If the stone is engraved with a number that has an even number of
            # digits, it is replaced by two stones. The left half of the digits
            # are engraved on the new left stone, and the right half of the
            # digits are engraved on the new right stone. (The new numbers don't
            # keep extra leading zeroes: 1000 would become stones 10 and 0.)
            strrep = str(s)
            left = int(strrep[:len(strrep)//2])
            right = int(strrep[len(strrep)//2:])
            res.append(left)
            res.append(right)
        else:
            # If none of the other rules apply, the stone is replaced by a new
            # stone; the old stone's number multiplied by 2024 is engraved on
            # the new stone.
            res.append(s * 2024)
    return res

stones = ORIG_STONES
for i in range(25):
    stones = apply_rules(stones)

part1 = len(stones)
print(f"Part 1: {part1}")

# If f give len of array after N iterations, then
#   f(a1 a2 a3, N) = f(a1, N) + f(a2, N) + f(a3, N)
# We can then use a cache to save the value of f(a, N) for all arrays of len 1
# (i.e. for individual stones).
cache = {}
def f(a, N):
    if N == 0:
        return len(a)
    elif len(a) == 1:
        res = []
        s = a[0]
        key = (s, N)
        if key in cache.keys():
            return cache[key]
        if s == 0:
            # If the stone is engraved with the number 0, it is replaced by a
            # stone engraved with the number 1.
            res.append(1)
        elif len(str(s)) % 2 == 0:
            # If the stone is engraved with a number that has an even number of
            # digits, it is replaced by two stones. The left half of the digits
            # are engraved on the new left stone, and the right half of the
            # digits are engraved on the new right stone. (The new numbers don't
            # keep extra leading zeroes: 1000 would become stones 10 and 0.)
            strrep = str(s)
            left = int(strrep[:len(strrep)//2])
            right = int(strrep[len(strrep)//2:])
            res.append(left)
            res.append(right)
        else:
            # If none of the other rules apply, the stone is replaced by a new
            # stone; the old stone's number multiplied by 2024 is engraved on
            # the new stone.
            res.append(s * 2024)
        res = f(res, N - 1)
        cache[key] = res
        return res
    else:
        res = 0
        for e in a:
            res += f([e], N)
        return res

stones = ORIG_STONES

part2 = f(stones, 75)
print(f"Part 2: {part2}")
