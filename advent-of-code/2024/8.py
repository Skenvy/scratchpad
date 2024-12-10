# https://adventofcode.com/2024/day/8

ADVENT_DAY=8

# The input is a grid of empty spaces '.' and filled spaces (many symbols).
# For each symbol present, the collection of spaces that contain that symbol
# are used to determine "antinodes", locations in the grid (whether they be in
# empty space, overlapping a symbol, or overlapping another antinode) that must
# be counted, to get the count of all UNIQUE locations that are an antinode.

def parse_input_part_one(filename):
    all_symbol_locations = {}
    map = []
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            map_row = list(line)
            if map_row[-1] == '\n':
                del map_row[-1]
            map.append(map_row)
            for col_index, col_val in enumerate(map_row):
                if col_val != '.':
                    all_symbol_locations[col_val] = all_symbol_locations.get(col_val, [])
                    all_symbol_locations[col_val].append((line_index, col_index))
    # Get all antinode locations from each pair of locations for each symbol
    antinode_locations = []
    for symbol, symbol_locations in all_symbol_locations.items():
        # Get each set of "pair locations" i.e. each set of 2 locations.
        symbol_pair_locations = []
        for k in range(len(symbol_locations)-1):
            for j in range(k+1,len(symbol_locations)):
                symbol_pair_locations.append((symbol_locations[k], symbol_locations[j]))
        for spl in symbol_pair_locations:
            # Calculate this pair's antinodes.
            dx, dy = spl[0][0] - spl[1][0], spl[0][1] - spl[1][1]
            possible_antinodes = [(spl[0][0]+dx, spl[0][1]+dy), (spl[1][0]-dx, spl[1][1]-dy)]
            for (pax,pay) in possible_antinodes:
                if not (pax<0 or pax>=len(map) or pay<0 or pay>=len(map[0])):
                    antinode_locations.append((pax,pay)) # add loc if within map
    return len(set(antinode_locations))

# EXPLAIN PART TWO

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

print(f'Amount of unique antinode locations is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'XYZ pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
