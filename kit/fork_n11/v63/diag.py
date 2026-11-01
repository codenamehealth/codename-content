import sys, os, collections
sys.argv = ['r63.py', 'search', '0', '0']
g = {'__name__': '__main__', '__file__': os.path.abspath('r63.py')}
os.chdir(os.path.dirname(os.path.abspath('r63.py')))
try: exec(open('r63.py').read(), g)
except SystemExit: pass
G = g['G']; C = collections.Counter(); rows = []
for seed in range(int(os.environ.get('A', 1)), int(os.environ.get('B', 200))):
    st, fr, ev, obs, lanes, ld = g['sim'](seed, 18)
    done = [x for x in G if st[x]['done'] is not None]; caught = sorted(st[x]['caught'] for x in G if st[x]['caught'] is not None)
    key = (len(done), len(caught), done[0] if done else None)
    C[key] += 1
    if len(done) == 1 and done[0] == 'joy': rows.append((seed, round(st['joy']['done'], 1), [round(c, 1) for c in caught]))
print(C.most_common(10)); print(rows[:20])
