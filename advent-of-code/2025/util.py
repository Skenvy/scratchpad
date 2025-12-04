import os, sys
import time
import functools
from collections.abc import Callable

# This util is adjacent to the files that import it..
AOC_YEAR_DIR = os.path.dirname(os.path.realpath(__file__))

def stopwatch(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.perf_counter()
            filename = args[0][len(AOC_YEAR_DIR)+1:]
            print(f"{func.__name__}({filename}) took {end - start:.6f}s")
    return wrapper

# Just a neat way to run this lengthy chunk the same way.
def run_solvers(
    puzzle_description: str,
    _EXAMPLE_INPUT_FILE: str,
    solve_part_one: Callable[[str], any],
    example_answer_one: any,
    INPUT_FILE_PART_ONE: str,
    solve_part_two: Callable[[str], any],
    example_answer_two: any,
    INPUT_FILE_PART_TWO: str,
):
    example_one = solve_part_one(_EXAMPLE_INPUT_FILE)
    assert example_one == example_answer_one, f"Failed part one: {example_one}"
    print(f'{puzzle_description} pt1 is {solve_part_one(INPUT_FILE_PART_ONE)}')
    example_two = solve_part_two(_EXAMPLE_INPUT_FILE)
    assert example_two == example_answer_two, f"Failed part two: {example_two}"
    print(f'{puzzle_description} pt2 is {solve_part_two(INPUT_FILE_PART_TWO)}')
