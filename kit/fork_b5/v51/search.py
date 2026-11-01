import sys
from sim51 import *
for s in range(int(sys.argv[1]), int(sys.argv[2])):
    r = score(s)
    if r: print(s, r, flush=True)
