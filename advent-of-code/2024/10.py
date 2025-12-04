# https://adventofcode.com/2024/day/10

ADVENT_DAY=10

# Input is a top-down topography. 0 lowest height 9 max height. Trailheads are 0
# Find the sum of all "scores" of trailheads, where a score is the amount of 9's
# "reachable" from a single trailhead, and it is reachable if it can connect
# through 012456789, only in cardinals not diagonally.

def solve_part_one(filename):
    map = []
    trailheads = {}
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            map_row = list(line)
            if map_row[-1] == '\n':
                del map_row[-1]
            map.append([int(x) for x in map_row])
            if '0' in map_row:
                for digit_index, digit in enumerate(map_row):
                    if digit == '0':
                        trailheads[(line_index,digit_index)] = 0
    # trailhead keys known. find each trailhead score
    valid_path_directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for trailhead in trailheads.keys():
        path_locs = [trailhead]
        for next_path_height in range(1,10):
            new_path_locs = []
            for (plx,ply) in path_locs:
                for (vpx,vpy) in valid_path_directions:
                    if plx+vpx==-1 or ply+vpy==-1 or plx+vpx==len(map) or ply+vpy==len(map[0]):
                        continue
                    if map[plx+vpx][ply+vpy] == next_path_height:
                        new_path_locs.append((plx+vpx,ply+vpy))
            path_locs = new_path_locs.copy()
        trailheads[trailhead] = len(set(path_locs))
    return sum(trailheads.values())

# Instead of the trailhead score being the amount of reachable 9's it's now the
# amount of paths that exist to any reachable 9.

def solve_part_two(filename):
    map = []
    trailheads = {}
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            map_row = list(line)
            if map_row[-1] == '\n':
                del map_row[-1]
            map.append([int(x) for x in map_row])
            if '0' in map_row:
                for digit_index, digit in enumerate(map_row):
                    if digit == '0':
                        trailheads[(line_index,digit_index)] = 0
    # trailhead keys known. find each trailhead score
    valid_path_directions = [(1,0), (-1,0), (0,1), (0,-1)]
    for trailhead in trailheads.keys():
        path_locs = [trailhead]
        for next_path_height in range(1,10):
            new_path_locs = []
            for path_loc in path_locs:
                plx, ply = path_loc[-2], path_loc[-1]
                for (vpx,vpy) in valid_path_directions:
                    if plx+vpx==-1 or ply+vpy==-1 or plx+vpx==len(map) or ply+vpy==len(map[0]):
                        continue
                    if map[plx+vpx][ply+vpy] == next_path_height:
                        new_path_locs.append(path_loc + (plx+vpx,ply+vpy))
            path_locs = new_path_locs.copy()
        trailheads[trailhead] = len(set(path_locs))
    return sum(trailheads.values())

print(f'Sum of trailhead scores (reachable peaks) is {solve_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Sum of trailhead scores (traversable paths) is {solve_part_two(f'{ADVENT_DAY}-input.txt')}')
