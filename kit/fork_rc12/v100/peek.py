import sys, runpy
src = open('r100.py').read().split("SEED = int(sys.argv[1])")[0]
g = {}; sys.argv = ['x']; exec(compile(src, 'r100', 'exec'), g)
for s in [int(x) for x in sys.argv_[1:]] if False else []: pass
