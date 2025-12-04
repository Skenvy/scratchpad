import os, sys
import time
import functools

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
            print(f"{func.__name__} took {end - start:.6f}s")
    return wrapper
