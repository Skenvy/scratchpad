# https://adventofcode.com/2024/day/6

ADVENT_DAY=6

# Input is a grid, with empty spaces '.', filled spaces '#', and the starting
# position of an agent '^'. If the agent will turn right every time it hits a
# filled space (on the empty space before the filled space), count how many
# unique empty spaces the agent will pass through before exiting the grid.

def parse_input_part_one(filename):
    # Fill the map
    map = []
    px, py = -1, -1 # "player x, player y"
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            map_row = list(line)
            if map_row[-1] == '\n':
                del map_row[-1]
            map.append(map_row)
            if '^' in map_row:
                px = line_index
                py = map_row.index('^')
    # Filled map
    # Could be more optimised to only parse a list of blocking spaces, but eh
    # we only ever rotate clockwise so just map each direction to the next
    directions = {
        (-1,0):(0,1), # up turns to right
        (0,1):(1,0), # right turns to down
        (1,0):(0,-1), # down turns to left
        (0,-1):(-1,0), # left turns to up
    }
    (dx, dy) = (-1,0) # current direction
    # Now start movement
    count_unique_steps = 1 # First square we start on
    count_nonunique_steps = 0
    cx,cy = px,py # "current" position
    map[cx][cy] = 'X'
    loop_detector = []
    while True: # check for loops and grid exits and break
        (odx,ody) = (dx,dy)
        # Check edge
        if cx+dx==-1 or cy+dy==-1 or cx+dx==len(map) or cy+dy==len(map[0]):
            break # This square was already counted
        while map[cx+dx][cy+dy] == '#':
            (dx,dy) = directions[(dx,dy)]
        if (odx,ody) != (dx,dy):
            # We rotated this step, check or add to loop detector
            if ((cx,cy),(dx,dy)) in loop_detector: # we've just hit a loop
                break
            loop_detector.append(((cx,cy),(dx,dy)))
        cx,cy=cx+dx,cy+dy # Move
        # Set and count movement
        count_unique_steps += 1*(map[cx][cy] == '.')
        count_nonunique_steps += 1*(map[cx][cy] == 'X')
        map[cx][cy] = 'X'
    # for row in map:
    #     print(''.join(row))
    # print(f"Exited map on ({cx},{cy}), {count_unique_steps} UNIQUE, {count_nonunique_steps} NONUNIQUE")
    return count_unique_steps

# EXPLAIN PART TWO

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

print(f'Amount of unique grids visited is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'XYZ pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
