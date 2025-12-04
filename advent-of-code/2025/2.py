# https://adventofcode.com/2025/day/2

ADVENT_DAY=2

# The input is a list of ranges. A comma seperated list of ranges, two IDs
# split by hyphens. We need to iterate through the ranges, and then for each
# range, iterate over the numbers in that range, and find all instances of
# numbers with a repeated sequence. Or, that are specifically exactly a sequence
# repeated twice. E.g. 123123 is one we need to account for, but 1231234 isn't?

# We need to find all these instances of doubled-up-sequence-numbers in each of
# the ranges (ranges of "IDs" and the double-ups are "Invalid IDs"), and add
# them all together to get the answer for part one.

def solve_part_one(filename):
    rngs = []
    sum_IDs = 0
    with open(filename,'r') as lines:
        for line in lines:
            # rngs += [[int(x) for x in r.split('-')] for r in line.split(',')]
            # Hold off on converting them to ints for now...
            # rngs += [r.split('-') for r in line.split(',')]
            # Buuuuut... we need to strip the newline from the last value..
            rngs += [[x.strip() for x in r.split('-')] for r in line.split(',')]
    # Now we've got some [['1','2'], ['3','4'], ...] from our "1-2,3-4,..."
    for rng in rngs:
        # Only ranges on even lengthed integers are relevant
        # Extract from each range the valid, even lengthed, ranges to test
        valid_ranges = []
        # We could replace this if else with only the else case because it does
        # handle all cases the same, but we keep the if to be illustrative.
        if len(rng[0]) == len(rng[1]):
            if len(rng[0]) % 2 == 1:
                # if both the first and last value in a range are the same, odd,
                # length, then we can just skip that range entirely.
                continue
            # Alternatively if they're both the same even length, then that's
            # the whole valid range...
            valid_ranges = [rng]
        else:
            # Our lowest valid range starts either from an even lengthed lowest
            # rng ID, or from the even lengthed next highest power of 10. E.g.
            # if len(rng[0]) is odd, then 10**len(rng[0]) will be the next even
            # lengthed power of 10. Our _highest_ valid range ends on either an
            # even lengthed highest rng ID, or on the lower power of 10 minus 1.
            # E.g. 10**(len(rng[1])-1)-1 will be an even length of 9's one char
            # shorter than the length of rng[1].
            # So, our minimum and maximum boundaries to this global range are...
            vmin = rng[0] if len(rng[0])%2 == 0 else f"{10**len(rng[0])}"
            vmax = rng[1] if len(rng[1])%2 == 0 else f"{10**(len(rng[1])-1)-1}"
            # for even lengths in the lengths of the range IDs
            for even_length in range(len(vmin), len(vmax)+1, 2):
                # Determine this sub range's local min and max.
                sub_range_min = max(10**(even_length-1), int(vmin))
                sub_range_max = min(10**(even_length)-1, int(vmax))
                valid_ranges += [[sub_range_min, sub_range_max]]
        # We now have a set of "valid ranges", sub ranges of the input ranges
        # which are only the components of them that are ranges on even length
        # integers. So we now iterates the valid ranges for each range. It's
        # worth noting that, for our inputs, all our ranges end up with only
        # one valid range each, so we could unpack that and just iterate the
        # first (and only) entry in each, but this might not be universal..
        for valid_range in valid_ranges:
            # print(f"For valid range {valid_range} of range {rng}")
            # for each valid range we have our minimum ID and our maximum ID. We
            # can avoid iterating through the IDs and testing them by observing
            # that we can just figure it out with no need to iterate.. E.g. say
            # we have a range 1234 to 9876. We can already see intuitively that
            # each of the 1313, 1414, .., 9797 will be valid repeated sequences.
            # We need to add these to the sum_IDs. For this and the next part,
            # we split both our min and max IDs for this particular range into
            # the first half and the second half of the string of each of them.
            vmin = f"{valid_range[0]}"
            vmin_1st = vmin[:len(vmin)//2]
            vmin_2nd = vmin[len(vmin)//2:]
            vmax = f"{valid_range[1]}"
            vmax_1st = vmax[:len(vmax)//2]
            vmax_2nd = vmax[len(vmax)//2:]
            # Do our e.g. 1313, 1414, .., 9797 iteration. Only do this if we
            # know that there will be a wide enough gap..
            if int(vmin_1st)+1 < int(vmax_1st):
                for sequence in range(int(vmin_1st)+1, int(vmax_1st)):
                    sum_IDs += int(f"{sequence}{sequence}")
                    # print(f"  Add MID repeated sequence {sequence}{sequence}")
            # Now we handle the possibility of the f"{vmin_1st}{vmin_1st}" and
            # f"{vmax_1st}{vmax_1st}" numbers in this range. Our minimum's 2nd
            # half has to be less than or equal to its 1st half, and the max's
            # 2nd half has to be greater than or equal to its 1st half.
            if vmin_1st != vmax_1st:
                if int(vmin_2nd) <= int(vmin_1st):
                    sum_IDs += int(f"{vmin_1st}{vmin_1st}")
                    # print(f"  Add MIN repeated sequence {vmin_1st}{vmin_1st}")
                if int(vmax_2nd) >= int(vmax_1st):
                    sum_IDs += int(f"{vmax_1st}{vmax_1st}")
                    # print(f"  Add MAX repeated sequence {vmax_1st}{vmax_1st}")
            else:
                # If the 1st half of both our min and max IDs is the same, we
                # instead need to check if that value falls inside the range of
                # both of the 2nd halves... (also both 1st's are the same then
                # the ordering of min and max is preserved to the 2nd's too).
                if int(vmin_1st) in range(int(vmin_2nd),int(vmax_2nd)+1):
                    sum_IDs += int(f"{vmin_1st}{vmin_1st}")
                    # print(f"  Add DIM repeated sequence {vmin_1st}{vmin_1st}")
    return sum_IDs

# Ok, so.. we made a LOT of optimisation choices in part one given the knowledge
# that only numbers that were "exactly one sequence repeated twice" were ones we
# needs to add to our total.. and pretty much none of them apply to part two..
# In part two, we are still limited to numbers that are only exactly repeated
# sequences, but they can repeat any amount of times >= 2. So all our tricks to
# split numbers in half and treat all the special cases are irrelevant here lol.

# So we have to basically go back to scratch for part two.

def solve_part_two(filename):
    rngs = []
    sum_IDs = 0
    with open(filename,'r') as lines:
        for line in lines:
            rngs += [[x.strip() for x in r.split('-')] for r in line.split(',')]
    for rng in rngs:
        # Break ranges up into contiguities of "same lengthed integers"
        for l in range(len(rng[0]), len(rng[1])+1): # l ~ length
            # Figure out the current min and current max
            cmin = rng[0] if l == len(rng[0]) else f"{10**len(rng[0])}"
            cmax = rng[1] if l == len(rng[1]) else f"{10**(len(rng[1])-1)-1}"
            # Do a very basic test for integers that exactly divide the length
            divs = [x for x in range(1, l//2+1) if l//x == l/x]
            # Now we can segment the current length integers into "div" lengths
            # print(f"Range {rng}: Curr [{cmin},{cmax}] len {l} divs {divs}")
            _range = range(int(cmin), int(cmax)+1)
            for div in divs:
                for sequence in range(int(cmin[:div]), int(cmax[:div])+1):
                    # Trap it if it's _already_ a repeated sequence!
                    already_repeated = False
                    for dd in [x for x in divs if div//x == div/x and x != div]:
                        # "dd" are the dividers of "div"
                        if int((f"{sequence}"[:dd])*(div//dd)) == sequence:
                            already_repeated = True
                            break
                    repeated_sequence = int(f"{sequence}"*(l//div))
                    if repeated_sequence in _range and not already_repeated:
                        sum_IDs += repeated_sequence
                        # print(f"    Adding {repeated_sequence} to the sum")
    return sum_IDs

part_one_example = solve_part_one(f'{ADVENT_DAY}-example-input.txt')
assert part_one_example == 1227775554, f"Failed part one: {part_one_example}"

print(f'Sum "IDs" pt1 is {solve_part_one(f'{ADVENT_DAY}-input.txt')}')

part_two_example = solve_part_two(f'{ADVENT_DAY}-example-input.txt')
assert part_two_example == 4174379265, f"Failed part two: {part_two_example}"

print(f'Sum "IDs" pt2 is {solve_part_two(f'{ADVENT_DAY}-input.txt')}')
