# https://adventofcode.com/2024/day/1

ADVENT_DAY=1

# Read 2 columns of a text file into two lists, order those lists, and add up
# each indexes difference between the two sorted lists.

def parse_input_part_one(filename):
    with open(filename,'r') as lines:
        sum_of_diffs = 0
        left_list = []
        right_list = []
        for line in lines:
            cols = line.split(' ')
            # There's 3 spaces, so cols will look like ['123', '', '', '456']
            left_list.append(int(cols[0]))
            right_list.append(int(cols[-1]))
        left_list.sort()
        right_list.sort()
        for i in range(len(left_list)):
            sum_of_diffs += abs(left_list[i] - right_list[i])
    return sum_of_diffs

# Now, instead of adding up all the differences, we need to multiply each entry
# in the left list by the amount of times it appears in the right list.

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        sum_of_mults = 0
        left_list = []
        right_list = []
        for line in lines:
            cols = line.split(' ')
            # There's 3 spaces, so cols will look like ['123', '', '', '456']
            left_list.append(int(cols[0]))
            right_list.append(int(cols[-1]))
        left_list.sort()
        right_list.sort()
        # Convert both to map the values to the amount of times they're present
        left_map = {k: sum([1 for j in left_list if j == k]) for k in left_list}
        right_map = {k: sum([1 for j in right_list if j == k]) for k in right_list}
        # Now we can multiple the values in left map, by both the times it's in
        # the left map as well as the right map.
        for left_value, left_count in left_map.items():
            sum_of_mults += left_value * left_count * right_map.get(left_value, 0)
    return sum_of_mults

print(f'Sum of all diffs is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Sum of all mult-freqs is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
