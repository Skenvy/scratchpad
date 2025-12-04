# https://adventofcode.com/2025/day/1

import util
ADVENT_DAY=1
INPUT_FILE_PART_ONE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
INPUT_FILE_PART_TWO=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-input.txt'
_EXAMPLE_INPUT_FILE=f'{util.AOC_YEAR_DIR}/{ADVENT_DAY}-example-input.txt'

# We have a list of instructions, one per line, that are either "L<number>" or
# "R<number>". The instructions are whether we need to modulo add or module
# subtract from our current value. We start with a value of 50 mod 100, and must
# follow the L (subtract) and R (add) rules in order. As we're following them,
# we must count how many times the "current value" is 0 mod 100. The values in
# the instructions are never negative (e.g. we don't get some "L-X" that would
# otherwise be equivalent of an "RX") but they can be larger than the modulus.

# An important piece of consideration doing this in _any_ language is how that
# language handles negative modulo wrapping. You'd hope that modulo of negative
# numbers, at least with a positive modulus, would behave well, e.g. -3%10 = 7
# See https://en.wikipedia.org/wiki/Modulo#In_programming_languages for more.
# In python, the % does what we want. But this is something to be aware of..

@util.stopwatch
def parse_input_part_one(filename):
    MODULUS = 100
    current_residue = 50
    count_times_residue_is_zero = 0
    with open(filename,'r') as lines:
        for line in lines:
            instruction = line[0]
            # assert instruction in ['L', 'R'], f"Unhandled! ${instruction}"
            # We would generally get the value as everything after the first
            # char by doing this...
            number_chars = line[1:]
            # line_value = int(number_chars)
            # But because we know the modulus is 100, we can say we only care
            # about the last two number chars in the string, because anything
            # else will just get lost in the modulo... so say range "-2:"
            # _except_... each line comes with an end '\n' newline that can be
            # seen by printing the repr(line). So range to get the last two
            # digits, _including_ the newline is "-3:"
            line_value = int(number_chars[-3:])
            # The numbers in the list are only ever positive. If the instruction
            # was an 'L' and we need to subtract just invert the value.
            line_value = -line_value if instruction == 'L' else line_value
            # Now we can do the same thing for both L and R.
            current_residue = (current_residue + line_value) % MODULUS
            count_times_residue_is_zero += (1 if current_residue == 0 else 0)
    return count_times_residue_is_zero

# For part 2, instead of only counting the instances that the residue is 0 at
# the end of a rotation (each L/R instruction), we must count every instance
# during the rotations as well! e.g. if we had a current residue of 1, and got
# an L2 line, we'd end up with a current residue of 99, but we'd have to count
# the 0 that was passed over during the rotation from 1 down to 99.

@util.stopwatch
def parse_input_part_two(filename):
    MODULUS = 100
    current_residue = 50
    count_times_residue_is_zero = 0
    count_times_dial_passes_zero = 0
    with open(filename,'r') as lines:
        for line in lines:
            instruction = line[0]
            # assert instruction in ['L', 'R'], f"Unhandled! ${instruction}"
            number_chars = line[1:]
            # We can still use the trick of taking the range "-3:" for the sub
            # hundred value, and the range ":-3" for the above hundreds value.
            line_value = int(number_chars[-3:]) # line_value ~= sub hundred val
            # An LXYZ / RXYZ where YZ are single digits each and X is any number
            # of digits, will contribute the X value directly to the number of
            # times the 0 is passed over by rotating the dial. So we can take X
            # and just add it to our count then handle the sub hundred part.
            # But incase our line doesn't have hundreds, prepend with a 0, or
            # int('') on an empty string will ValueError.
            count_times_dial_passes_zero += int(f'0{number_chars[:-3]}')
            # Now we can handle the sub-hundred value. At this point though, we
            # have our current_residue and a line_value both as base residues,
            # e.g. 0 <= current_residue, line_value < 100 -- so no matter if we
            # add or subtract the line_value from our current_residue, the
            # result will be >= -99 and <= 198. Do our regular L invert..
            line_value = -line_value if instruction == 'L' else line_value
            # And test if we passed over 0 or not by seeing if we're still in
            # a base residue or a non-base residue. We must be careful to de-
            # duplicate how we count '0' and '100' cases. If the next residue is
            # 0 or 100, then the final addition will count it. 0 is in the
            # range(100), but 100 is not. We need to use range(101) to get both!
            next_residue = current_residue + line_value
            # Whoops!!! We _also_ need to specifically handle when our _current_
            # residue is 0, because an L instruction on a _current_ residue of 0
            # will end up with a negative next_residue and trigger our dial pass
            # count increment, despite that it didn't dial pass over 0.
            if next_residue not in range(101) and current_residue != 0:
                count_times_dial_passes_zero += 1
            # Do our regular next current residue and end count...
            current_residue = next_residue % MODULUS
            count_times_residue_is_zero += (1 if current_residue == 0 else 0)
    return count_times_residue_is_zero+count_times_dial_passes_zero

print(f'#(0%100) pt1 is {parse_input_part_one(INPUT_FILE_PART_ONE)}')
print(f'#(0%100) pt2 is {parse_input_part_two(INPUT_FILE_PART_TWO)}')
