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

# We could optimise this by inserting our ranges into an ordered list and then
# searching through that ordered list for which range it might be in but that's
# not strictly necessary. If we read in the entire list of 1000 IDs before
# checking them against each of the ranges, we could sort that list and iterate
# over some partially ordered lists of the ranges.

@util.stopwatch
def solve_part_one(filename):
    import bisect
    from functools import cache
    ranges = []
    insort_key = cache(lambda x : x[0])
    IDs = []
    count_in_range_IDs = 0
    with open(filename,'r') as lines:
        for line in lines:
            sline = line.strip()
            if sline == '':
                continue # skip the empty line
            # _IDs needs to be __hash__'able by insort so tuple instead of list
            _IDs = tuple([int(x) for x in sline.split('-')])
            assert len(_IDs) <=2, f"Split line {line.strip()} had too many IDs"
            if len(_IDs) == 2:
                # Reading in a range
                bisect.insort(ranges, (min(_IDs), _IDs), key=insort_key)
            else:
                # Reading in an ID
                bisect.insort(IDs, _IDs[0])
    # Now we should have a sorted list of IDs and a sorted list of ranges.
    _l = 0 # low index
    for id in IDs:
        # print(f'Evaluating ID: {id}')
        # If this ID is lower than the current low range boundary, skip this ID
        if id < ranges[_l][0]:
            # print(f'  Skip ID:{id}, below lowest range {ranges[_l][1]}')
            continue
        # We should now have at least ranges[_l][1][0] <= id -- If the range
        # was short and we ALREADY have ranges[_l][1][1] < id -- then
        # increment the range iterator forwards.
        while ranges[_l][1][1] < id:
            # print(f'  Skip RANGE:{ranges[_l][1]}, below currnet ID:{id}')
            _l += 1
            if _l == len(ranges):
                break # breaks the while
        # Check it again to break the for if we've hit the end
        if _l == len(ranges):
            break
        # We also can't be sure that we ended up on a range that the id isn't
        # now less than again, so sandwich the range incrementer with another
        # continuer if the id is once again below the next range.
        if id < ranges[_l][0]:
            # print(f'  Skip ID:{id}, below lowest range {ranges[_l][1]}')
            continue
        # If we didn't skip any of the preceding steps, then the ID is in range
        # print(f'  Counting ID:{id} in RANGE:{ranges[_l][1]}')
        count_in_range_IDs += 1
    return count_in_range_IDs

# For part two, we don't care about the list of individual IDs. We need to take
# all the ranges, and find the unique amount of integers in all of the ranges
# combined. e.g. range 1-3 and range 5-7 would be "6" ~= |{1,2,3,5,6,7}|

@util.stopwatch
def solve_part_two(filename):
    import bisect
    from functools import cache
    ranges = []
    insort_key = cache(lambda x : x[0])
    count_all_range_IDs = 0
    with open(filename,'r') as lines:
        for line in lines:
            sline = line.strip()
            if sline == '':
                break # skip the empty line, _and_ all the IDs after it.
            # _IDs needs to be __hash__'able by insort so tuple instead of list
            _IDs = tuple([int(x) for x in sline.split('-')])
            assert len(_IDs) ==2, f"Split line {line.strip()} was not two IDs"
            if len(_IDs) == 2:
                # Reading in a range
                bisect.insort(ranges, (min(_IDs), _IDs), key=insort_key)
            # We don't else this because we don't care about reading IDs here.
    # Now we should have a sorted list of ranges.
    # print(f'Evaluating RANGE:{ranges[0][1]}')
    # print(f'  START windowing a new current range {ranges[0][1]}')
    window_low = ranges[0][1][0]
    window_high = ranges[0][1][1]
    del ranges[0]
    final_range_was_already_extended = False
    for _ri, _range in enumerate(ranges):
        # print(f'Evaluating RANGE:{_range[1]}')
        this_low = _range[1][0]
        this_high = _range[1][1]
        # We are now either adding subsequent ranges to the current window range
        # or counting the size of the current range and then terminating it.
        # If "this" range's low is lower than the "current" range high, we're in
        # a range that overlaps with the current range, so extend the current..
        if this_low <= window_high:
            # It's possible ranges, which we've ordered by lowest value, are out
            # of order with regards to highest values, so take a max.
            # print(f'  EXTEND ({window_low}, {window_high}) with {_range[1]}')
            window_high = max(window_high, this_high)
            # If we extended the current range, keep going until we can't, but
            # also don't keep going if it was the final range...
            if _ri+1 < len(ranges):
                continue
            else:
                final_range_was_already_extended = True
        # We are now counting the current range after all possible extensions,
        # and then terminating it, and starting the next window from this one.
        # print(f'  TERMINATE ({window_low}, {window_high})')
        count_all_range_IDs += (window_high-window_low)+1
        # If we are on the final range, and it did not overlap a prior range, it
        # means the prior range, or set of extended ranges, would've terminated
        # and we would have just started a new window on the non-overlapping
        # final range. We need a way to know if we are on the final range, and
        # if it did not overlap the prior range / set-of-ranges.
        if _ri == len(ranges)-1: # then we're on the final range
            # We still need to know whether or not "this" (final) range
            # overlapped with the window or was non-overlapping. There's a lot
            # of ways to treat this using tricks of the "this" high and the
            # window high, but there's too many traps so just use a flag.
            if not final_range_was_already_extended:
                # print(f' Evaluating FINAL RANGE: ({this_low}, {this_high})')
                count_all_range_IDs += (this_high-this_low)+1
        else:
            # If we aren't on the final range and we terminated the previous
            # window, then start the next window to continue in the next loop.
            # print(f'  START windowing a new current range {_range[1]}')
            window_low = this_low
            window_high = this_high
    return count_all_range_IDs

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
