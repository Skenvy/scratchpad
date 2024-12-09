# https://adventofcode.com/2024/day/3

ADVENT_DAY=3

# Parse a text file for instances of "mul(A,B)" with A and B being numbers.
# Add up each result of the valid mul's

from re import findall, match

def parse_input_part_one(filename):
    with open(filename,'r') as lines:
        sum_of_muls = 0
        for line in lines:
            muls = findall(r'mul\(\d+,\d+\)', line)
            for mul in muls:
                nums = [int(x) for x in mul[4:-1].split(',')]
                sum_of_muls += nums[0]*nums[1]
    return sum_of_muls

# We now need to also check for "do()" and "don't()" and respect them. Look on
# regexr and see that "(mul\(\d+,\d+\)|do\(\)|don't\(\))" finds what we expect
# in "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def parse_input_part_two(filename):
    do = True
    with open(filename,'r') as lines:
        sum_of_muls = 0
        for line in lines:
            muls = findall(r'(mul\(\d+,\d+\)|do\(\)|don\'t\(\))', line)
            for mul in muls:
                if match(r'mul\(\d+,\d+\)', mul):
                    if do:
                        nums = [int(x) for x in mul[4:-1].split(',')]
                        sum_of_muls += nums[0]*nums[1]
                else:
                    # it's either "do()" or "don't()"
                    do = mul == "do()"
    return sum_of_muls

print(f'Sum of all muls is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Sum of all muls with DO and DONT is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
