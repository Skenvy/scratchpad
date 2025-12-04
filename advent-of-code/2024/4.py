# https://adventofcode.com/2024/day/4

ADVENT_DAY=4

# Word search! Input is a word search grid! Count unique "XMAS"'s

def solve_part_one(filename):
    words_to_search_for = ['XMAS']
    count_word_instances = 0
    word_search_directions = {
        'UP': [-1, 0],
        'DOWN': [1, 0],
        'LEFT': [0, -1],
        'RIGHT': [0, 1],
        'UP-LEFT': [-1, -1],
        'UP-RIGHT': [-1, 1],
        'DOWN-LEFT': [1, -1],
        'DOWN-RIGHT': [1, 1]
    }
    grid = []
    with open(filename,'r') as lines:
        for line in lines:
            chars = list(line)
            if chars[-1] == '\n':
                del chars[-1]
            grid.append(chars)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            # grid[row][col]
            for word in words_to_search_for:
                if grid[row][col] == word[0]: # start searching in all directions around row,col
                    for [dr,dc] in word_search_directions.values():
                        for char_index, char in enumerate(word):
                            if (row+dr*char_index < 0) or (row+dr*char_index >= len(grid)) or (col+dc*char_index < 0) or (col+dc*char_index >= len(grid[0])):
                                # outside grid boundary before satisfying last character check
                                break
                            if grid[row+dr*char_index][col+dc*char_index] != char:
                                # if the character at this offset for this direction isn't correct, also break
                                break
                        else:
                            # if we didn't break, then the word was valid in this direction
                            count_word_instances += 1
    return count_word_instances

# EXPLAIN PART TWO

def solve_part_two(filename):
    count_word_instances = 0
    grid = []
    with open(filename,'r') as lines:
        for line in lines:
            chars = list(line)
            if chars[-1] == '\n':
                del chars[-1]
            grid.append(chars)
    for row in range(1,len(grid)-1):
        for col in range(1,len(grid[0])-1):
            # This time we are only searching for "MAS" but middle out
            if grid[row][col] == 'A':
                # Cross-Diagonal MAS check
                top_left_to_bottom_right = [grid[row-1][col-1], grid[row+1][col+1]]
                top_left_to_bottom_right.sort()
                top_right_to_bottom_left = [grid[row-1][col+1], grid[row+1][col-1]]
                top_right_to_bottom_left.sort()
                count_word_instances += 1*(top_left_to_bottom_right == ['M','S'])*(top_right_to_bottom_left == ['M','S'])
    return count_word_instances

print(f'Amount of XMAS\'s is {solve_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Amount of X-"MAS"\'s is {solve_part_two(f'{ADVENT_DAY}-input.txt')}')
