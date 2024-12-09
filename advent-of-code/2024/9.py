# https://adventofcode.com/2024/day/9

ADVENT_DAY=9

# Input is a string of numbers, each consective number alternates between
# describing the size of a file, or the size of free space, in chunks. Get the
# "chunks" descriptive map, which alternates between being "empty" for free
# space, or filled with the filename-index that increases for each subsequent
# file encountered. Once the chunk map is done, fully fragment, starting from
# the end-most chunk, and moving it to the start-most free space. Then get the
# checksum for the fully fragmented chunks by summing the multiples of each
# chunk's value (what its filename-index value was) by its new location.

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

# The same as before, except instead of fully fragmenting by moving only chunks
# at a time, try and move whole files (all of the chunks in a single file) one
# file at a time, starting from the end and decreasing. If a file can't be moved
# to earlier in the chunks the first pass over, it doesn't get moved, even if
# space later opens up after moving lower chunks.

def parse_input_part_two(filename):
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
    # Iterating downwards in files and upwards in free space to compact.
    # Is the last element a file, or free space? Figure out last file index.
    # If length disk map mod 2 is 0 then last spot free then 2nd last spot file.
    first_last_file = -1 - 1*(len(disk_map) % 2 == 0)
    # Now iterate downwards in files, and for each, only once, check free spaces
    for file_space_index, file_space_size in enumerate(disk_map[first_last_file:0:-2]):
        for free_space_index, free_space_size in enumerate(disk_map[1::2]):
            if free_space_size >= file_space_size:
                # Move this file into this free space.
                # disk_map[:1+free_space_index*2] represents all slots up to now
                # disk_map[:first_last_file-file_space_index*2] all up to file
                insert_start = sum(disk_map[:1+free_space_index*2])
                file_start = sum(disk_map[:first_last_file-file_space_index*2])
                if insert_start >= file_start:
                    break
                for k in range(file_space_size):
                    chunks[insert_start+k] = chunks[file_start+k]
                    chunks[file_start+k] = None
                # Now, we need to change this free_space_index; to subtract
                # file_space_size and add file_space_size to file_space_index
                # that is prior to that "previous free space chunk."
                disk_map[free_space_index*2] += file_space_size
                disk_map[1+free_space_index*2] -= file_space_size
                break # break the free space search after moving this file.
    # Now we have compacted chunks
    checksum = sum([p*v for p,v in enumerate(chunks) if v != None])
    return checksum

print(f'Checksum of fragmented chunks is {parse_input_part_one(f'{ADVENT_DAY}-input.txt')}')
print(f'Checksum of compacted chunks is {parse_input_part_two(f'{ADVENT_DAY}-input.txt')}')
