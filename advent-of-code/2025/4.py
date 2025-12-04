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
    count_removed_blobs = 0
    count_accessible_blobs = -1
    while count_accessible_blobs != 0:
        count_accessible_blobs = 0
        removals = []
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
                        removals += [(_row, _col)]
        for (_row, _col) in removals:
            map[_row][_col] = '.'
        count_removed_blobs += len(removals)
    return count_removed_blobs

util.run_solvers(
    'Example puzzle description',
    _EXAMPLE_INPUT_FILE,
    solve_part_one,
    example_answer_one,
    INPUT_FILE_PART_ONE,
    solve_part_two,
    example_answer_two,
    INPUT_FILE_PART_TWO,
)
