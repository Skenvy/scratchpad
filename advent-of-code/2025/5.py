# https://adventofcode.com/2025/day/5

import util
ADVENT_DAY=5
INPUT_FILE_PART_ONE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
INPUT_FILE_PART_TWO=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
_EXAMPLE_INPUT_FILE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-example-input.txt'
example_answer_one = 3
example_answer_two = 14

# Our input is in 2 parts.. first we have a collection of ID ranges e.g. "X-Y",
# followed by a blank line and then the 2nd part of the input, a collection of
# singular IDs. We need to count how many of the singular IDs are inside any of
# the ranges, which are inclusive. E.g. "1" would be "fresh" and thus counted
# because it's in range "1-3". In our actual input we have near to 1000ish IDs
# to check against almost 200 ranges.

@util.stopwatch
def solve_part_one(filename):
    ranges = []
    count_in_range_IDs = 0
    with open(filename,'r') as lines:
        for line in lines:
            sline = line.strip()
            if sline == '':
                continue # skip the empty line
            IDs = [int(x) for x in sline.split('-')]
            assert len(IDs) <=2, f"Split line {line.strip()} had too many IDs"
            if len(IDs) == 2:
                # Reading in a range
                ranges += [range(min(IDs), max(IDs)+1)]
            else:
                # Reading in an ID
                # If we are already reading the IDs then we've finished reading
                # all the ranges so we can go ahead and count them here.
                for _range in ranges:
                    if IDs[0] in _range:
                        count_in_range_IDs += 1
                        break
    return count_in_range_IDs

# EXPLAIN PART TWO

@util.stopwatch
def solve_part_two(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

util.run_solvers(
    '#IDs-in-range',
    _EXAMPLE_INPUT_FILE,
    solve_part_one,
    example_answer_one,
    INPUT_FILE_PART_ONE,
    solve_part_two,
    example_answer_two,
    INPUT_FILE_PART_TWO,
)
