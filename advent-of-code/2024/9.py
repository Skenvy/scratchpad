# https://adventofcode.com/2024/day/9

ADVENT_DAY=9

# Input is a string of numbers, each consective number alternates between
# describing the size of a file, or the size of free space, in chunks.

def parse_input_part_one(filename):
    disk_map = []
    with open(filename,'r') as lines:
        for line in lines:
            digits_in_line = list(line)
            if digits_in_line[-1] == '\n':
                del digits_in_line[-1]
            disk_map.extend([int(q) for q in digits_in_line])
    # Convert disk map to chunks
    chunks = []
    describe_file = True
    filename_index = 0
    for descriptor in disk_map:
        if describe_file:
            chunks.extend([filename_index]*descriptor)
            filename_index += 1
        else:
            chunks.extend([None]*descriptor)
        describe_file = not describe_file
    # Convert chunks to fragmented chunks
    reverse_search_init = len(chunks)-1
    for forward_search_index in range(len(chunks)):
        if forward_search_index >= reverse_search_init:
            break
        if chunks[forward_search_index] == None:
            for reverse_search_index in range(reverse_search_init, 0, -1):
                if chunks[reverse_search_index] != None:
                    chunks[forward_search_index] = chunks[reverse_search_index]
                    chunks[reverse_search_index] = None
                    reverse_search_init = reverse_search_index-1
                    break
    # Now we have fragmented chunks
    checksum = sum([p*v for p,v in enumerate(chunks) if v != None])
    return checksum

# EXPLAIN PART TWO

def parse_input_part_two(filename):
    with open(filename,'r') as lines:
        for line in lines:
            pass # do something with each line
    return 'TODO'

print(f'Checksum of fragmented chunks is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
# print(f'XYZ pt2 is {parse_input_part_two(f'{ADVENT_DAY}-input-2.txt')}')
