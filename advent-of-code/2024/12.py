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
    plot_evaluated = []
    for _ in range(len(garden_plots)):
        plot_evaluated.append([False]*len(garden_plots[0]))
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
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

print(f'Sum of garden plot contiguity areas mult perimeters is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'XYZ pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
