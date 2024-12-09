# https://adventofcode.com/2023/day/2

# Open a text file whose lines look like; (X game number, Z colour number, Y colour count)
# """Game <int:X>: <";" joined by>{<"," joined by>["<int:Y> <string:Z>"]}"""
# For example "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"

from re import search

def parse_input(filename):
    parsed_state = {}
    with open(filename,'r') as lines:
        for line in lines:
            seeker = search('^Game \d+:', line)
            if seeker is None:
                continue
            else:
                game_id = int(search('\d+', seeker.group()).group())
                parsed_state[game_id] = {}
                rounds = line.replace(f'Game {game_id}:', '').split(';')
                for round in rounds:
                    count_colours = round.split(',')
                    for count_colour in count_colours:
                        [count, colour] = count_colour.strip().split(' ')
                        if parsed_state[game_id].get(colour) is None:
                            parsed_state[game_id][colour] = [int(count)]
                        else: 
                            parsed_state[game_id][colour].append(int(count))
    # parsed_state is now {<game_id>: {<colour>: [<counts...>], ...}, ...}
    return parsed_state

FILENAME = '2-input-2.txt'

games = parse_input(FILENAME)

# Parse these lines to determine which games would have been possible if the bag
# had been loaded with 12 red cubes, 13 green cubes, and 14 blue cubes.
# Sum up the game IDs for the possible games.

colours_max = {'red': 12, 'green': 13, 'blue': 14}
game_sum = 0
for (game_id, game) in games.items():
    for (colour, cmax) in colours_max.items():
        if max(game.get(colour, [0])) > cmax:
            break
    else:
        game_sum += game_id

print(f'Sum of all games with limits on RGBs is {game_sum}')

# what is the fewest number of cubes of each color that could have been in the
# bag to make the game possible? Find these fewests, then for each game multiply
# the fewest RGB together, and sum up all these multiples.

sum_of_mult_sets = 0
for game in games.values():
    product = 1
    for count in game.values():
        product *= max(count)
    sum_of_mult_sets += product

print(f'Sum of all games\' mult-sets is {sum_of_mult_sets}')
