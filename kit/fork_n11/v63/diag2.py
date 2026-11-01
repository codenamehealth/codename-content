import sys, os
sys.argv = ['r63.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r63.py')}
try: exec(open('r63.py').read(), g)
except SystemExit: pass
G = g['G']; FPS = g['FPS']
for seed in [int(x) for x in os.environ['SEEDS'].split(',')]:
    st, fr, ev, obs, lanes, ld = g['sim'](seed, 18)
    tw = st['joy']['done']; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    picks = [(round(e[0],1), e[2], e[3]) for e in ev if e[1] == 'pick' and e[0] < tw]
    jb = [round(e[0],1) for e in ev if e[1] == 'block' and e[2] == 'joy']
    sw = [(round(e[0],1), e[3]) for e in ev if e[1] == 'sleepwave']
    nsm = sum(e[1] == 'smash' for e in ev); natk = sum(e[1] == 'atk' for e in ev)
    gap = max(max(f[0][x]['x'] for x in G if f[0][x]['caught'] is None) - f[1] for f in fr[int(1.5 * FPS):int(tw * FPS)])
    print(seed, round(tw,1), [round(c,1) for c in caught], 'leaders', len(ld), 'picks', picks, 'joyblock', jb, 'sw', sw, 'smash', nsm, 'atk', natk, 'gap', round(gap))
