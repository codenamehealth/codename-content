import os, sys
sys.argv = ['r15.py', 'search', '0', '0']
src = open('r15.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    rc, fr, gt, sv = sim(seed)
    print(seed, 'out', {n: (round(s['out'],1) if s['out'] else None, round(s['caught'],1) if s['caught'] else None) for n, s in rc.items()}, 'gum', gt and (gt[0], round(gt[1],1), rc[gt[0]]['behind']), 'shoves', [(x[0], x[1][:2]+'>'+x[2][:2]) for x in sv])
