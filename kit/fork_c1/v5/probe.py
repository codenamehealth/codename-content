import sys, os, math, sim
from sim import *
seeds = range(int(sys.argv[1]), int(sys.argv[2]))
tot_hits = 0; deep = 0; worst = 0; nz = 0
for sd in seeds:
    del sim.NUDGE[1:]; sim.NUDGE[0] = 0
    fr, ev, cnt, ld, T = run(sd, record=False, tmax=20)
    tot_hits += len(ev); d = sim.NUDGE[1:]; nz += len(d); deep += sum(1 for x in d if x > 10); worst = max([worst] + d)
print(os.environ.get('HUBH'), os.environ.get('ARM'), os.environ.get('OMEGA'), 'hits/run %.1f' % (tot_hits / len(seeds)), 'nudges', nz, 'deep>10px', deep, 'worst %.0f' % worst, flush=True)
