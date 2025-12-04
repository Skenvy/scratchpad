# https://adventofcode.com/2024/day/11

ADVENT_DAY=11

# A set of numbers. There are some rules for how they get updated per iteration.
# Calculate how many numbers there are at the end of X iterations. Both problems
# for today are doing the exact same thing, just to different X's. The solution
# for part one is the "naive" approach of just updating the numbers in place.

def solve_part_one(filename):
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
            elif len(str(num)) % 2 == 0:
                new_nums.append(int(str(num)[:len(str(num))//2]))
                new_nums.append(int(str(num)[len(str(num))//2:]))
            else:
                new_nums.append(num*2024)
        nums = new_nums.copy()
    return len(nums)

# Part 2 hits a wall of being resource exhaustive following the naive approach.
# It needs some optimisations. Although the text of the problem statement says
# several times in bold font something about ordering or staying in line, being
# in order is irrelevant to how the numbers evolve each iteration. There's a few
# rules to apply to each number each iteration, but they only act on each number
# individually independent of the surrounding numbers. So, rather than caring
# about order, do away with order; bucket the numbers and act on the buckets!
# Do this by acting on the "amount" of times "number X" appears, rather than
# just on the "number X" done "amount" times.

def solve_part_two(filename):
    # Read in the numbers
    nums = []
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            digits_in_line = line.split(' ')
            if digits_in_line[-1] == '\n':
                del digits_in_line[-1]
            nums.extend([int(q) for q in digits_in_line])
    # Define the transform rules
    def transform_number(num):
        num_len = len(str(num))
        if num == 0:
            return [1]
        elif num_len % 2 == 0:
            return [num//10**(num_len//2), num%10**(num_len//2)]
        else:
            return [num*2024]
    _CACHE_TRANSFORM = {}
    def cache_transform_number(num):
        if num not in _CACHE_TRANSFORM.keys():
            _CACHE_TRANSFORM[num] = transform_number(num)
        return _CACHE_TRANSFORM[num]
    # Blink 75 times
    bucketed_nums = {num:1 for num in nums}
    stable_cache_reached = False
    for i in range(75):
        new_bucketed_nums = {}
        for num, amount in bucketed_nums.items():
            for new_num in cache_transform_number(num):
                new_bucketed_nums[new_num] = new_bucketed_nums.get(new_num, 0)
                new_bucketed_nums[new_num] += amount
        # To get a sense of how much the cache sped up this, compared to the
        # very large amount of numbers we'd otherwise be acting on, use this
        # to see how many numbers you're "actually" caring about. After this
        # point, no new keys will be added.
        if set(new_bucketed_nums.keys()) == set(bucketed_nums.keys()) and not stable_cache_reached:
            print(f"Took {i+1} iterations to reach stable cache, with {len(bucketed_nums.keys())} many values cached")
            # Took 90 iterations to reach stable cache, with 3811 many values cached < for my input
            stable_cache_reached = True
        bucketed_nums = new_bucketed_nums.copy()
    return sum(bucketed_nums.values())

print(f'Amount of stones after 25 iterations is {solve_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Amount of stones after 75 iterations is {solve_part_two(f'{ADVENT_DAY}-input.txt')}')
