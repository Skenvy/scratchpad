# https://adventofcode.com/2023/day/1

# Open a text file, read it line by line, seek each line to find the firt and
# last number (if only one number is present, it is _both_ the first and last).
# Add every line's 2 digit number together.

FILENAME = '1-input-1.txt'
with open(FILENAME,'r') as input_list:
    summed_value = 0
    for line in input_list:
        first_digit = ''
        last_digit = ''
        for char in line:
            if char.isdigit():
                first_digit = char
                break
        else:
            raise Exception(f'No digit in line {line}')
        for char in reversed(line):
            if char.isdigit():
                last_digit = char
                break
        summed_value += int(f'{first_digit}{last_digit}')
    print(f'All lines add up to {summed_value}')

# For part 2, we need to also accept the presence of whole english names for
# single digit numbers (sans zero), and if the word comes before or after a
# digit, then the word counts as the digit.

from re import search

FILENAME = '1-input-1.txt'
with open(FILENAME,'r') as input_list:
    summed_value = 0
    for line in input_list:
        # Find the numbers the same way as before, but record positions as well.
        first_digit = ''
        first_loc = 0
        last_digit = ''
        last_loc = len(line)-1
        for loc in range(len(line)):
            if line[loc].isdigit():
                first_loc = loc
                first_digit = line[loc]
                break
        else:
            raise Exception(f'No digit in line {line}')
        for loc in range(len(line)):
            if line[len(line)-1-loc].isdigit():
                last_loc = len(line)-1-loc
                last_digit = line[last_loc]
                break
        # Now we have positions of the first and last "digit", snip the line to
        # the line before and after the first and last digits and scan them.
        num_words_forward = '(one|two|three|four|five|six|seven|eight|nine)'
        num_words_reverse = '(enin|thgie|neves|xis|evif|ruof|eerht|owt|eno)'
        lut = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5,
               'six': 6, 'seven': 7, 'eight': 8, 'nine': 9}
        # The line before the first digit
        word = line[0:first_loc]
        seeker = search(num_words_forward, word)
        word = '' if seeker is None else seeker.group()
        first_digit = lut.get(word, first_digit)
        # The line after the last digit... but in a silly way, because 'first'!
        word = line[last_loc+1:len(line)]
        seeker = search(num_words_reverse, word[::-1])
        word = '' if seeker is None else seeker.group()[::-1]
        last_digit = lut.get(word, last_digit)
        # Now back to adding them as usual.
        summed_value += int(f'{first_digit}{last_digit}')
    print(f'All lines add up to {summed_value}')
