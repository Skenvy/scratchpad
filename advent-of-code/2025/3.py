# https://adventofcode.com/2025/day/3

import util
ADVENT_DAY=3
INPUT_FILE_PART_ONE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
INPUT_FILE_PART_TWO=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
_EXAMPLE_INPUT_FILE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-example-input.txt'
example_answer_one = 357
example_answer_two = 3121910778619

# Our input is a set of lines which are each lists of single digit values, from
# 1 to 9. E.g. a row could be "123456789" which would be 9 seperate values that
# we'd treat as ['1', '2', '3', '4', '5', '6', '7', '8', '9']. Each line is a
# "battery bank" in this example, and the digits are each battery's rating. We
# must find which two batteries in each row (line) we can turn on to achieve the
# maximum power for that row, where the resulting power is if the digits, in the
# order they are in the row, were the two digits of one two-digit number. E.g.
# if we turned on batteries "6" and "7" in our row, the row's power delivered
# would be "67". We need to find the maximum power for each row and sum them up.

@util.stopwatch
def solve_part_one(filename):
    joltage_sum = 0
    with open(filename,'r') as lines:
        for line in lines:
            # strip the newlines lol
            cline = line.strip()
            # If we call .split('~') on some string, if the character is not
            # present, we'll get back a list with one single entry in it, the
            # original input. If we get back more than a single item list, then
            # everything in all the entries besides the first one are values
            # that appear after the first instance of the character we split on.
            for _1st in range(9,0,-1): # e.g. 9, then 8, then ..., then 1.
                # Try splitting on what we want to test for the 1st digit
                scline = cline.split(f'{_1st}')
                # If there's only one entry then the char isn't in the line.
                # If the 2nd entry in the list is empty and we only have two
                # entries, it means "_1st" was only found in the last char of
                # the line, so it can't be our "_1st"!
                if len(scline) == 1 or (len(scline) == 2 and scline[1] == ''):
                    continue
                # If the char WAS in the line, rebuild the line after the char's
                # first appearance... join everything in the list besides the
                # first item on the char we just split on.
                post_1st_1st = f'{_1st}'.join(scline[1:])
                __2nd = 0
                for _2nd in range(9,0,-1): # e.g. 9, then ..., then 1.
                    split_post_1st_1st = post_1st_1st.split(f'{_2nd}')
                    if len(split_post_1st_1st) > 1:
                        # the _2nd digit exists and we want to use it!
                        __2nd = _2nd
                        break
                row_joltage = _1st*10 + __2nd
                assert __2nd != 0, "Whoops, didn't already avoid this?"
                # print(f'Adding row joltage {row_joltage}')
                joltage_sum += row_joltage
                break
    return joltage_sum

# The same as part one, except instead of finding the maximum possible joltage
# for each row by combining only "two" batteries in order, we now have to turn
# on 12 batteries in each row and find the maximum possible joltage for 12 being
# turned on!

# This is clearly the point in this year's calendar where optimisations become
# a requirement, because for part one, we had a "100 choose 2" problem where,
# unoptimised, we would have had 4950 cases to test. In part two, we're living
# on the edge with "100 choose 12", or... 1,050,421,051,106,700 cases... so
# optimisations for this are strictly required.

@util.stopwatch
def solve_part_two(filename):
    joltage_sum = 0
    # Create a recursive function we can call as part of this, where we give it
    # the "subsequent line segment", "subline", which is the rest of the line
    # after the first instance of whatever character it was previously split on.
    # When we call it the first time we give it the amount of digits we want to
    # use out of the whole line.
    def line_joltage(subline, digits):
        # Both the terminal and non terminal case use the same range 9 to 1.
        if digits <= 1:
            for _nth in range(9,0,-1):
                split_subline = subline.split(f'{_nth}')
                if len(split_subline) > 1:
                    # the _nth digit exists and we want to use it because it's
                    # the first highest value we found.
                    # print(f'[Call:{digits}] Return from attempt at {_nth}')
                    return _nth
                # print(f'[Call:{digits}] Continue from attempt at {_nth}')
        else:
            for _nth in range(9,0,-1):
                spline = subline.split(f'{_nth}') # "Sp[li](t sub)[li]ne"
                # Two cases would lead to us skipping this _nth value. If there
                # is only one value in the list, then the value didn't exist in
                # the line so we necessarily skip it. At the same time, if there
                # are more than two entries, we also need to make sure there are
                # enough digits left in the rest of the subline after the first
                # instance of the current _nth we just split on! The number of
                # digits used, as an input, is the length of the string that
                # the current call must return. So we need at least "that value
                # minus one" many digits left in the sub-sub-line, or we wont be
                # able to return a value that uses the input many digits.
                subsubline = f'{_nth}'.join(spline[1:])
                if len(spline) == 1 or len(subsubline) < (digits-1):
                    # print(f'[Call:{digits}] Continue from attempt at {_nth}')
                    continue
                # If we didn't continue, then we can use the current _nth and
                # recurse on the remaining subline.
                # print(f'[Call:{digits}] Return from attempt at {_nth}')
                return (10**(digits-1))*_nth + line_joltage(subsubline,digits-1)
    with open(filename,'r') as lines:
        for line in lines:
            # print(line.strip())
            res = line_joltage(line.strip(), 12)
            # print(f'  Result: Added {res}')
            joltage_sum += res
    return joltage_sum

util.run_solvers(
    'Sum joltage',
    _EXAMPLE_INPUT_FILE,
    solve_part_one,
    example_answer_one,
    INPUT_FILE_PART_ONE,
    solve_part_two,
    example_answer_two,
    INPUT_FILE_PART_TWO,
)
