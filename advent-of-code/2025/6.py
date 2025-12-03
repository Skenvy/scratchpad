# https://adventofcode.com/2025/day/6

ADVENT_DAY=6

# EXPLAIN PART ONE

def parse_input_part_one(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

# EXPLAIN PART TWO

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

part_one_example = parse_input_part_one(f'{ADVENT_DAY}-example-input.txt')
assert part_one_example == "example", f"Failed part one: {part_one_example}"

print(f'XYZ pt1 is {parse_input_part_one(f'{ADVENT_DAY}-input-1.txt')}')

part_two_example = parse_input_part_two(f'{ADVENT_DAY}-example-input.txt')
assert part_two_example == "example", f"Failed part two: {part_two_example}"

print(f'XYZ pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input-2.txt')}')
