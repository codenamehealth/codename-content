import sys, os, collections
src = open('r104c.py').read(); src = src[:src.index("if len(sys.argv) > 1 and sys.argv[1] == 'search2':")]
i0 = src.index('def score2'); head, body = src[:i0], src[i0:]
out = []; k = 0; labels = {}
for line in body.split('\n'):
    while 'return None' in line:
        labels[k] = line.strip()[:70]; line = line.replace('return None', f'return FAIL({k})', 1); k += 1
    out.append(line)
src = head + '\n'.join(out)
C = collections.Counter()
def FAIL(i): C[i] += 1; return None
g = {'FAIL': FAIL, '__name__': 'x', '__file__': os.path.abspath('r104c.py')}
sys.argv = ['r104c.py', 'x']
exec(compile(src, 'r104c', 'exec'), g)
N = int(os.environ.get('NS', '2000'))
for s in range(N): g['score2'](s)
for i, c in sorted(C.items()): print(c, labels[i])
