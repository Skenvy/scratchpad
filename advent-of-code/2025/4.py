# https://adventofcode.com/2025/day/4

import util
ADVENT_DAY=4
INPUT_FILE_PART_ONE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
INPUT_FILE_PART_TWO=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
_EXAMPLE_INPUT_FILE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-example-input.txt'
example_answer_one = 13
example_answer_two = 43

# Our input is a floorplan / grid map, that shows empty spots, '.', and "Rolls
# of paper" '@'. We need to determine if each '@' is accessible or not, based on
# how many neighbouring '@' it has (each '@' is accessible if it has fewer than
# 4 neighbours in the 8 surrounding plots e.g. Conway's Game of Life rule to die
# from overpopulation is equivalent to the inaccessibility). We must count how
# many '@' are accessible.

@util.stopwatch
def solve_part_one(filename):
    # Fill the map
    map = []
    with open(filename,'r') as lines:
        for line in lines:
            map_row = list(line)
            if map_row[-1] == '\n':
                del map_row[-1]
            map.append(map_row)
    # Filled map
    count_accessible_blobs = 0
    for _row, row in enumerate(map):
        for _col, val in enumerate(row):
            if val == '@':
                adjacent_grids = [
                    (_row+1,_col+0),
                    (_row+1,_col-1),
                    (_row+0,_col-1),
                    (_row-1,_col-1),
                    (_row-1,_col+0),
                    (_row-1,_col+1),
                    (_row+0,_col+1),
                    (_row+1,_col+1),
                ]
                count_adjacent_blobs = 0
                for grid in adjacent_grids:
                    if grid[0] in range(len(map)):
                        if grid[1] in range(len(map[0])):
                            if map[grid[0]][grid[1]] == '@':
                                count_adjacent_blobs += 1
                if count_adjacent_blobs < 4:
                    count_accessible_blobs += 1
    return count_accessible_blobs

# For part 2, we still use the same rule for accessibility, but instead of one
# static count, we must remove accessible '@' and then recheck for accessibility
# until all accessible '@' are removed. Our result is how many were removed.

@util.stopwatch
def solve_part_two(filename):
    # Fill the map
    map = []
    with open(filename,'r') as lines:
        for line in lines:
            map_row = list(line)
            if map_row[-1] == '\n':
                del map_row[-1]
            map.append(map_row)
    # Filled map
    # We don't need to keep track of ones we're going to remove and do the
    # removal async, because if we would remove them, then we can remove them
    # straight away and subsequent line counts will preempt the removals on the
    # next line. This should reduce the amount of times we have to loop the
    # whole grid, and is only possible because we only have on condition on
    # accessibility and it's an upper limit on adjacent neighbours.
    count_removed_blobs = 0
    prior_count_removed_blobs = -1
    # Track if we managed to remove any extra this cycle or if we've finished by
    # going until the prior count equals the current count.
    while prior_count_removed_blobs != count_removed_blobs:
        prior_count_removed_blobs = count_removed_blobs
        for _row, row in enumerate(map):
            for _col, val in enumerate(row):
                if val == '@':
                    adjacent_grids = [
                        (_row+1,_col+0),
                        (_row+1,_col-1),
                        (_row+0,_col-1),
                        (_row-1,_col-1),
                        (_row-1,_col+0),
                        (_row-1,_col+1),
                        (_row+0,_col+1),
                        (_row+1,_col+1),
                    ]
                    count_adjacent_blobs = 0
                    for grid in adjacent_grids:
                        if grid[0] in range(len(map)):
                            if grid[1] in range(len(map[0])):
                                if map[grid[0]][grid[1]] == '@':
                                    count_adjacent_blobs += 1
                    if count_adjacent_blobs < 4:
                        count_removed_blobs += 1
                        map[_row][_col] = '.'
    return count_removed_blobs

util.run_solvers(
    '#Accessible "@"',
    _EXAMPLE_INPUT_FILE,
    solve_part_one,
    example_answer_one,
    INPUT_FILE_PART_ONE,
    solve_part_two,
    example_answer_two,
    INPUT_FILE_PART_TWO,
)
