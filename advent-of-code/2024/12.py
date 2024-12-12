# https://adventofcode.com/2024/day/12

ADVENT_DAY=12

# EXPLAIN PART ONE

def parse_input_part_one(filename):    
    garden_plots = []
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            garden_plots_row = list(line)
            if garden_plots_row[-1] == '\n':
                del garden_plots_row[-1]
            garden_plots.append(garden_plots_row)
    contiguities = []
    # Footgun alert ~ it took me a while to figure out that this was my
    # mistake -- doing this, it treats all lists inside the top level
    # list as the same list.
    # >>> a = [[1,2],[3,4],[5,6]]
    # >>> b = [[False]*len(a[0])]*len(a)
    # >>> b[0][0] = True
    # >>> b
    # [[True, False], [True, False], [True, False]]
    #####################################################################
    # plot_evaluated = [[False]*len(garden_plots[0])]*len(garden_plots) #
    #####################################################################
    plot_evaluated = [[False]*len(garden_plots[0]) for _ in range(len(garden_plots))]
    for x in range(len(garden_plots)):
        for y in range(len(garden_plots[0])):
            if not plot_evaluated[x][y]:
                # Starting a contiguity we haven't parsed over yet
                contiguity_area = 0
                contiguity_perimeter = 0
                plots_to_eval = [(x,y)] # first point in the contiguity
                while plots_to_eval != []:
                    new_plots_to_eval = []
                    for (plot_x,plot_y) in plots_to_eval:
                        if not plot_evaluated[plot_x][plot_y]:
                            plot_evaluated[plot_x][plot_y] = True
                            contiguity_area += 1
                            for adjacent_x, adjacent_y in [(-1,0),(1,0),(0,-1),(0,1)]:
                                if plot_x+adjacent_x < 0 or plot_y+adjacent_y < 0 or plot_x+adjacent_x > len(garden_plots)-1 or plot_y+adjacent_y > len(garden_plots[0])-1:
                                    contiguity_perimeter += 1 # external boundary
                                elif garden_plots[plot_x][plot_y] != garden_plots[plot_x+adjacent_x][plot_y+adjacent_y]:
                                    contiguity_perimeter += 1 # touching a different contiguity
                                elif not plot_evaluated[plot_x+adjacent_x][plot_y+adjacent_y]:
                                    new_plots_to_eval.append((plot_x+adjacent_x,plot_y+adjacent_y))
                    plots_to_eval = new_plots_to_eval.copy()
                contiguities.append([contiguity_area, contiguity_perimeter])
    sum_contiguity_area_x_perimeter = 0
    for contiguity in contiguities:
        sum_contiguity_area_x_perimeter += contiguity[0]*contiguity[1]
    return sum_contiguity_area_x_perimeter

# EXPLAIN PART TWO

def parse_input_part_two(filename):
    garden_plots = []
    with open(filename,'r') as lines:
        for line_index, line in enumerate(lines):
            garden_plots_row = list(line)
            if garden_plots_row[-1] == '\n':
                del garden_plots_row[-1]
            garden_plots.append(garden_plots_row)
    contiguities = []
    plot_evaluated = [[False]*len(garden_plots[0]) for _ in range(len(garden_plots))]
    for x in range(len(garden_plots)):
        for y in range(len(garden_plots[0])):
            if not plot_evaluated[x][y]:
                # Starting a contiguity we haven't parsed over yet
                contiguity_area = 0
                contiguity_perimeter = 0
                borders = {direction:{} for direction in [(-1,0),(1,0),(0,-1),(0,1)]}
                plots_to_eval = [(x,y)] # first point in the contiguity
                while plots_to_eval != []:
                    new_plots_to_eval = []
                    for (plot_x,plot_y) in plots_to_eval:
                        if not plot_evaluated[plot_x][plot_y]:
                            plot_evaluated[plot_x][plot_y] = True
                            contiguity_area += 1
                            for adjacent_x, adjacent_y in [(-1,0),(1,0),(0,-1),(0,1)]:
                                border_found = False
                                if plot_x+adjacent_x < 0 or plot_y+adjacent_y < 0 or plot_x+adjacent_x > len(garden_plots)-1 or plot_y+adjacent_y > len(garden_plots[0])-1:
                                    contiguity_perimeter += 1 # external boundary
                                    border_found = True
                                elif garden_plots[plot_x][plot_y] != garden_plots[plot_x+adjacent_x][plot_y+adjacent_y]:
                                    contiguity_perimeter += 1 # touching a different contiguity
                                    border_found = True
                                elif not plot_evaluated[plot_x+adjacent_x][plot_y+adjacent_y]:
                                    new_plots_to_eval.append((plot_x+adjacent_x,plot_y+adjacent_y))
                                if border_found:
                                    bounding_line = plot_x if adjacent_x != 0 else plot_y # else ~= (adjacent_y != 0)
                                    boundary_post = plot_y if adjacent_x != 0 else plot_x # else ~= (adjacent_y != 0)
                                    borders[(adjacent_x,adjacent_y)][bounding_line] = borders[(adjacent_x,adjacent_y)].get(bounding_line, [])
                                    borders[(adjacent_x,adjacent_y)][bounding_line].append(boundary_post)
                    plots_to_eval = new_plots_to_eval.copy()
                # Check the borders for their own contiguities
                contiguity_borders = 0
                # print(garden_plots[x][y], borders)
                for border in borders.values():
                    for boundary_posts in border.values():
                        boundary_posts.sort()
                        contiguity_borders += 1 # the initial value
                        for pi in range(1,len(boundary_posts)):
                            contiguity_borders += 1*(boundary_posts[pi] > boundary_posts[pi-1]+1)
                contiguities.append([garden_plots[x][y], contiguity_area, contiguity_perimeter, contiguity_borders])
    sum_contiguity_area_x_boundaries = 0
    for contiguity in contiguities:
        sum_contiguity_area_x_boundaries += contiguity[1]*contiguity[3]
        # print(f"Region of plant {contiguity[0]} with area {contiguity[1]} and boundaries {contiguity[3]} for price {contiguity[1]*contiguity[3]}")
    return sum_contiguity_area_x_boundaries

print(f'Sum of garden plot contiguity areas mult perimeters is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Sum of garden plot contiguity areas mult boundaries is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
