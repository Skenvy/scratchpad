# https://adventofcode.com/2025/day/3

ADVENT_DAY=3

# Our input is a set of lines which are each lists of single digit values, from
# 1 to 9. E.g. a row could be "123456789" which would be 9 seperate values that
# we'd treat as ['1', '2', '3', '4', '5', '6', '7', '8', '9']. Each line is a
# "battery bank" in this example, and the digits are each battery's rating. We
# must find which two batteries in each row (line) we can turn on to achieve the
# maximum power for that row, where the resulting power is if the digits, in the
# order they are in the row, were the two digits of one two-digit number. E.g.
# if we turned on batteries "6" and "7" in our row, the row's power delivered
# would be "67". We need to find the maximum power for each row and sum them up.

def parse_input_part_one(filename):
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

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

part_one_example = parse_input_part_one(f'{ADVENT_DAY}-example-input.txt')
assert part_one_example == 357, f"Failed part one: {part_one_example}"

print(f'Sum joltage pt1 is {parse_input_part_one(f'{ADVENT_DAY}-input-1.txt')}')

part_two_example = parse_input_part_two(f'{ADVENT_DAY}-example-input.txt')
assert part_two_example == 3121910778619, f"Failed part two: {part_two_example}"

print(f'Sum joltage pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input-2.txt')}')
