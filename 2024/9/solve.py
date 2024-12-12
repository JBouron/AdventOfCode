#!/bin/python3

import sys

fd = open(sys.argv[1], "r")
line = list(fd.readline().replace("\n", ""))
m = list(map(lambda c: int(c), line))

# Sanity check: No file has a size of 0 blocks. This is not mentioned in the
# problem statement but this seems required?
assert 0 not in [m[i] for i in range(0, len(m), 2)]

i, j = 0, len(m)-1

# We can ignore any sequence of free block after the last file in the disk map.
if j % 2:
    j -= 1

part1 = 0
output_block_pos = 0

while i <= j:
    if i % 2:
        # i is pointing to some blocks of free space, move blocks from the file
        # pointed by j (moving j if the file is too small) to the free space
        # pointed by i.
        num_free_blocks = m[i]
        while num_free_blocks:
            # Sanity check: j points to a file at this point.
            assert j % 2 == 0
            fileid = j // 2
            num_blocks = m[j]
            assert num_blocks > 0
            # Move one block from file j to the empty space.
            # TODO: This could be optimized.
            num_free_blocks -= 1
            part1 += output_block_pos * fileid
            output_block_pos += 1
            m[j] = m[j] - 1
            if num_blocks == 1:
                # We moved all the blocks from file j. Move to the file
                # immediately preceding it.
                j -= 2
        # Move the left pointer to the next file.
        i += 1
    else:
        # i is pointing to some blocks of a file, the resulting map after all
        # moves will have the same content for those blocks, we only need to
        # update the result.
        fileid = i // 2
        num_blocks = m[i]
        # This could be optimized ...
        for n in range(num_blocks):
            part1 += output_block_pos * fileid
            output_block_pos += 1
        # Move to the next (free) block.
        i += 1

print(f"Part 1: {part1}")
