# https://adventofcode.com/2024/day/5

ADVENT_DAY=5

# Input in two sections. First set of lines read as "X|Y" which implies a rule
# that in the second set of lines, "X" must come before "Y". Keep valid lines
# in the second set of lines that adhere to all rules in first set of lines,
# then iterate over valid lines and add up the middle number from each.

def solve_part_one(filename):
    rules = {}
    sum_middle_valid_lines = 0
    with open(filename,'r') as lines:
        for line in lines:
            if '|' in line:
                # Reading a rule.
                [x,y] = line.split('|')
                _rule = rules.get(int(x), [])
                _rule.append(int(y))
                rules[int(x)] = _rule
                # each rule "x" is a list of "y"'s that must be after it.
            elif ',' in line:
                # Reading a pages line.
                pages = [int(z) for z in line.split(',')]
                prior_pages = []
                for page in pages:
                    if list(set(prior_pages) & set(rules.get(page, []))) == []:
                        # If the intersection of rules about pages that must be
                        # AFTER this current page, and the set of previous pages
                        # is empty, then no rule violation, still a valid line
                        prior_pages.append(page)
                    else:
                        break
                else:
                    # If we didn't break, the line was valid.
                    # Middle page is length "//2"
                    sum_middle_valid_lines += pages[len(pages)//2]
    return sum_middle_valid_lines

# Do the above, but, keep a list of all the lines that weren't valid, i.e. they
# broke one of the rules. Fix those lines so they adhere to the rules, then of
# the fixed lines, again, sum up their middle values.

def solve_part_two(filename):
    rules = {}
    sum_middle_invalid_lines = 0
    with open(filename,'r') as lines:
        for line in lines:
            if '|' in line:
                # Reading a rule.
                [x,y] = line.split('|')
                _rule = rules.get(int(x), [])
                _rule.append(int(y))
                rules[int(x)] = _rule
                # each rule "x" is a list of "y"'s that must be after it.
            elif ',' in line:
                # Reading a pages line.
                pages = [int(z) for z in line.split(',')]
                prior_pages = []
                invalid_line_to_fix = False
                for page in pages:
                    if list(set(prior_pages) & set(rules.get(page, []))) == []:
                        # If the intersection of rules about pages that must be
                        # AFTER this current page, and the set of previous pages
                        # is empty, then no rule violation, still a valid line
                        prior_pages.append(page)
                    else:
                        # If intersection NOT empty, invalid line TO FIX
                        invalid_line_to_fix = True
                        break
                if invalid_line_to_fix:
                    # Fix the line and then sum up its middle values
                    # Is there only one unique corrected ordering? Hope so.
                    assert len(pages) == len(set(pages)), f"FOUND BAD ROW {pages}"
                    rules_here = {x:rules[x] for x in pages}
                    new_pages = []
                    while len(rules_here) > 0:
                        precluding_values = []
                        for y in rules_here.values():
                            precluding_values.extend(y)
                        x_added_this_round = []
                        for x in rules_here.keys():
                            if x not in precluding_values:
                                new_pages.append(x)
                                x_added_this_round.append(x)
                        for x in x_added_this_round:
                            del rules_here[x]
                    # new_pages should be valid now
                    sum_middle_invalid_lines += new_pages[len(new_pages)//2]
    return sum_middle_invalid_lines

print(f'Sum of middle values in valid lines is {solve_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Sum of middle values in invalid lines after fixing is {solve_part_two(f'{ADVENT_DAY}-input.txt')}')
