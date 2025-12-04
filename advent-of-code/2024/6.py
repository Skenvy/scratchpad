# https://adventofcode.com/2024/day/6

ADVENT_DAY=6

# Input is a grid, with empty spaces '.', filled spaces '#', and the starting
# position of an agent '^'. If the agent will turn right every time it hits a
# filled space (on the empty space before the filled space), count how many
# unique empty spaces the agent will pass through before exiting the grid.

def solve_part_one(filename):
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

# Instead of counting unique steps, now, we need to count how many grids on to
# which we could place a single additional obstacle, that would trap in a loop

def solve_part_two(filename):
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
    cx,cy = px,py # "current" position
    map[cx][cy] = 'X'
    # We know from part one there is no original loop, but now we need to make
    # one, so preemptively keep track of loopable positions. Keep track of what
    # grids we have been on, and what direction we were facing.
    ##### This solution tries to find the set that would lock it in a loop that
    # had already been travelled, without trying to create a NEW loop. But there
    # must be places that a NEW loop could be formed from. So it must be exhaust
    # all_walked_grids = []
    # possible_new_colliders = []
    # while True: # check for grid exits and break
    #     # Check edge
    #     if cx+dx==-1 or cy+dy==-1 or cx+dx==len(map) or cy+dy==len(map[0]):
    #         break
    #     # Check previously walked areas
    #     all_walked_grids.append(((cx,cy),(dx,dy)))
    #     (lpdx,lpdy) = directions[(dx,dy)] # loop preemptive direction
    #     if ((cx,cy),(lpdx,lpdy)) in all_walked_grids:
    #         # If we previously walked in the next preemptive direction, then
    #         # changing direction here would put us on an already travelled path
    #         if map[cx+dx][cy+dy] != '#':
    #             possible_new_colliders.append((cx+dx,cy+dy))
    #     while map[cx+dx][cy+dy] == '#':
    #         (dx,dy) = directions[(dx,dy)]
    #     cx,cy=cx+dx,cy+dy # Move
    # return len(set(possible_new_colliders))
    ##### Exhaustive check
    loop_detector = []
    all_walked_grids = []
    while True: # check for loops and grid exits and break
        # Check edge
        all_walked_grids.append((cx,cy))
        if cx+dx==-1 or cy+dy==-1 or cx+dx==len(map) or cy+dy==len(map[0]):
            break # This square was already counted
        (odx,ody) = (dx,dy)
        while map[cx+dx][cy+dy] == '#':
            (dx,dy) = directions[(dx,dy)]
        if (odx,ody) != (dx,dy):
            # We rotated this step, check or add to loop detector
            if ((cx,cy),(dx,dy)) in loop_detector: # we've just hit a loop
                break
            loop_detector.append(((cx,cy),(dx,dy)))
        cx,cy=cx+dx,cy+dy # Move
    del all_walked_grids[0] # can't place an obstruction on the starting loc
    count_possible_new_obstructions = 0
    for (pox,poy) in set(all_walked_grids): # "possible obstruction" x,y
        # Edit the map in place to add an obstacle
        if map[pox][poy] == '#':
            continue # skip if it's already an obstacle
        map[pox][poy] = '#'
        # "Test" this current map to see if we can get stuck in a loop
        tcx,tcy = px,py # "start" position
        (dx, dy) = (-1,0) # current direction
        loop_detector = []
        while True: # check for loops and grid exits and break
            (odx,ody) = (dx,dy)
            # Check edge
            if tcx+dx==-1 or tcy+dy==-1 or tcx+dx==len(map) or tcy+dy==len(map[0]):
                break
            while map[tcx+dx][tcy+dy] == '#':
                (dx,dy) = directions[(dx,dy)]
            if (odx,ody) != (dx,dy):
                # We rotated this step, check or add to loop detector
                if ((tcx,tcy),(dx,dy)) in loop_detector: # we've just hit a loop
                    count_possible_new_obstructions += 1
                    break
                loop_detector.append(((tcx,tcy),(dx,dy)))
            tcx,tcy=tcx+dx,tcy+dy # Move
        # Edit the map in place to remove the test obstacle
        map[pox][poy] = '.'
    return count_possible_new_obstructions

print(f'Amount of unique grids visited is {solve_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Amount of grids where a single obstacle would init a loop is {solve_part_two(f'{ADVENT_DAY}-input.txt')}')
