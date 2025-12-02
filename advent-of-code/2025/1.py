# https://adventofcode.com/2025/day/1

ADVENT_DAY=1

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

def parse_input_part_one(filename):
    MODULUS = 100
    current_residue = 50
    count_times_residue_is_zero = 0
    with open(filename,'r') as lines:
        for line in lines:
            instruction = line[0]
            assert instruction in ['L', 'R'], f"Unhandled! ${instruction}"
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

# EXPLAIN PART TWO

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

print(f'#(0%100) pt1 is {parse_input_part_one(f'{ADVENT_DAY}-input-1.txt')}')
print(f'XYZ pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input-2.txt')}')
