# https://adventofcode.com/2024/day/11

ADVENT_DAY=11

# EXPLAIN PART ONE

def parse_input_part_one(filename):
    nums = []
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            digits_in_line = line.split(' ')
            if digits_in_line[-1] == '\n':
                del digits_in_line[-1]
            nums.extend([int(q) for q in digits_in_line])
    # Blink 25 times
    for _ in range(25):
        new_nums = []
        for num in nums:
            if num == 0:
                new_nums.append(1)
            elif len(f'{num}') % 2 == 0:
                new_nums.append(int(f'{num}'[:len(f'{num}')//2]))
                new_nums.append(int(f'{num}'[len(f'{num}')//2:]))
            else:
                new_nums.append(num*2024)
        nums = new_nums.copy()
    return len(nums)

# EXPLAIN PART TWO

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            pass # do something with each line
    return 'TODO'

print(f'XYZ pt1 is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'XYZ pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
