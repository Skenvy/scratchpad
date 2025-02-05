# https://www.reddit.com/r/Collatz/comments/1i7nb7q/third_weekly_collatz_path_length_competition/

BITS_THIS_WEEK = 256
# Samples to try should actually be "half" how many you want because it will try one less and one more than the magic numbers
SAMPLES_TO_TRY = 5000
# Maximum stopping time to check for each before giving up
MST=10000
# The post includes a baseline stopping time to beat (here as the total stopping time)
ST2B = 3035

BIT_MIN = 2**(BITS_THIS_WEEK - 1)
BIT_MAX = 2*BIT_MIN - 1

MAGIC_BASE = 576460752303423488
MAGIC_ADD = 27

def magic(n):
    return MAGIC_ADD+MAGIC_BASE*n

# Get the first and last "n" such that magic(n) will be between BIT_MIN and BIT_MAX
_REM = BIT_MIN % MAGIC_BASE
FIRST_VAL = BIT_MIN - _REM + MAGIC_BASE
FIRST_INDEX = FIRST_VAL // MAGIC_BASE

_REM = BIT_MAX % MAGIC_BASE
LAST_VAL = BIT_MAX - _REM - (_REM<MAGIC_ADD)*MAGIC_BASE
LAST_INDEX = LAST_VAL // MAGIC_BASE

print(f'Bits this week are {BITS_THIS_WEEK} -- range is')
print(f'FROM: {BIT_MIN}')
print(f'TO:   {BIT_MAX}')
print(f'Indexing from {FIRST_INDEX} to {LAST_INDEX}')

from math import ceil as roof

# To take "SAMPLES_TO_TRY"*2 samples, walk out of range
i = FIRST_INDEX # index
u = (LAST_INDEX - FIRST_INDEX)/SAMPLES_TO_TRY # update
ui = 0 # update's iteration

from collatz import stopping_time

l = {}
while i < LAST_INDEX+1:
    _m = magic(i)
    _ml = _m - 1
    _mh = _m + 1
    l[_ml] = stopping_time(_ml, total_stopping_time=True, max_stopping_time=MST) or -1
    l[_mh] = stopping_time(_mh, total_stopping_time=True, max_stopping_time=MST) or -1
    ui += 1
    i = FIRST_INDEX + roof(u*ui)

sl = {k:v for k,v in sorted(l.items(), key=lambda item: item[1])}
for (k,v) in sl.items():
    print(f'{"BEATS THE ST2B"*(v>ST2B)+"LESS THAN ST2B"*(v<=ST2B)}: NUMBER {k} HAS STOPPING TIME {v}')

print()
print(f'Checked a total of {len(sl)} numbers')

