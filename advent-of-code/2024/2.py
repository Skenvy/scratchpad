# https://adventofcode.com/2024/day/2

ADVENT_DAY=2

# Check each line of a file to see if the numbers in a line are all either only
# increasing, or only decreasing, and by no more than 3 at a time. Count the
# amount of lines that meet this criteria

def parse_input_part_one(filename):
    with open(filename,'r') as lines:
        num_of_safe_reps = 0
        for line in lines:
            is_level_safe = True
            nums = [int(x) for x in line.split(' ')]
            # If the first two numbers are the same, it's not safe. If they are
            # different, then we know if the line should be all incr or decr.
            if nums[1] == nums[0]:
                continue
            increasing = nums[1] > nums[0]
            for i in range(1, len(nums)):
                is_level_safe &= nums[i-1*(not increasing)] - nums[i-1*increasing] <= 3
                is_level_safe &= nums[i-1*(not increasing)] - nums[i-1*increasing] >= 1
                if not is_level_safe:
                    break
            if is_level_safe:
                num_of_safe_reps += 1
    return num_of_safe_reps

# The same as before, except each line is allowed to have at most one bad value
# that removing from an unsafe line can make it a safe line.

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        num_of_safe_reps = 0
        for line in lines:
            nums = [int(x) for x in line.split(' ')]
            # If a line has only one or two numbers, it's valid, because any
            # bad value in two numbers is also just "one number"
            if len(nums) <= 2:
                num_of_safe_reps += 1
                continue
            # There are more optimised ways of doing this, but we would need to
            # handle lists of 3 values as a special case, because they aren't
            # automatically valid like lists of one or two, but we can't be sure
            # of the increasing or decreasing status without 4 values, i.e. test
            # the differences between nums[0] and [1], [1] and [2], [2] and [3].
            # {[0] and [1], [1] and [2]} would only be good if the bad value was
            # not one of the first 3 values. Instead, test the whole list.
            increase_eval = [nums[i]>nums[i-1] for i in range(1, len(nums))]
            if increase_eval in [[True]*(len(nums)-1), [False]*(len(nums)-1)]:
                increasing = nums[1] > nums[0] # monotonic
            else:
                # if only one is different from the rest, remove that value
                truths = [i for i,x in enumerate(increase_eval) if x]
                falses = [i for i,x in enumerate(increase_eval) if not x]
                if len(falses) > 1 and len(truths) > 1:
                    # increase_eval must be either all truths or all falses, or
                    # allow for only one bad value. If both truths and falses
                    # are more than 1, then too many bad values.
                    continue
                else:
                    increasing = len(truths) > 1
            # We now know if the whole list should be increasing or decreasing.
            # It doesn't matter than increase_eval only checked > and not >=
            # because we only wanted to know if it was semi-monotonic or not.
            might_be_safe_level = True
            possible_bad_Is = []
            for i in range(1, len(nums)):
                might_be_safe_level &= nums[i-1*(not increasing)] - nums[i-1*increasing] <= 3
                might_be_safe_level &= nums[i-1*(not increasing)] - nums[i-1*increasing] >= 1
                if not might_be_safe_level:
                    possible_bad_Is.append(i)
                might_be_safe_level = True
            if len(possible_bad_Is) == 0: # is_level_safe
                num_of_safe_reps += 1
                continue
            # Else, check what bad indexes we might be able to remove. At most
            # two adjacent indexes might have been off, and their common value
            # can be removed. If more than 2 indexes were off, it's all off.
            if len(possible_bad_Is) > 2:
                continue
            assert len(possible_bad_Is) != 0, "If there were not bad I's, should have been safe."
            # index "i" uses values "i-1" and "i". If only index is "1" then the
            # bad value is index 0. If index "a" and "a+1" are off, then their
            # shared value of index i is the bad value. If index "len(nums)" is
            # the only index, then bad value is index len(nums). It is also
            # possible that only one index was served in this list, that is not
            # 1 or len(nums). Say a list 1 2 3 4 3 5 6 7 -- only the 3 after the
            # 4 is out of place, and this would make possible_bad_Is = [4]
            possible_bad_value_indexes = []
            if len(possible_bad_Is) == 2:
                if possible_bad_Is[0] != possible_bad_Is[1]-1:
                    # two bad indexes that weren't adjacent isn't allowed
                    continue
                else:
                    possible_bad_value_indexes = [possible_bad_Is[0]]
            else:
                # len(possible_bad_Is) == 1
                possible_bad_value_indexes = [possible_bad_Is[0]-1, possible_bad_Is[0]]
            for possible_bad_value_index in possible_bad_value_indexes:
                is_level_safe = True
                sanitised_nums = nums.copy()
                del sanitised_nums[possible_bad_value_index]
                for i in range(1, len(sanitised_nums)):
                    is_level_safe &= sanitised_nums[i-1*(not increasing)] - sanitised_nums[i-1*increasing] <= 3
                    is_level_safe &= sanitised_nums[i-1*(not increasing)] - sanitised_nums[i-1*increasing] >= 1
                    if not is_level_safe:
                        break
                if is_level_safe:
                    num_of_safe_reps += 1
                    break
            if not is_level_safe:
                print(nums, possible_bad_Is, possible_bad_value_indexes)
    return num_of_safe_reps

print(f'Number of safe reports no bad values is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Number of safe reports allow one bad value is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
