import sys, os, collections
sys.argv = ['r56.py', 'search', '0', '0']
g = {'__name__': '__main__'}
try: exec(open('r56.py').read(), g)
except SystemExit: pass
os.chdir(os.path.dirname(os.path.abspath('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n11/v56/r56.py')))
C = collections.Counter(); NAMES = g['NAMES']
for seed in range(int(os.environ['A']), int(os.environ['B'])):
    fr, ev, obs, ld, fin, mc = g['sim'](seed)
    if any(v is None for v in fin.values()): C['nofin'] += 1; continue
    order = sorted(NAMES, key=lambda n: fin[n]); C['win_' + order[0]] += 1
    C['shove%d' % sum(e[1] == 'shove' for e in ev)] += 1
    cre = [e[2] for e in ev if e[1] == 'pick' and e[3] == 'cre']; C['cre_' + (cre[0] if cre else 'none')] += 1
    C['tw_ok'] += 9.6 < fin[order[0]] < 11.8
print(C)
