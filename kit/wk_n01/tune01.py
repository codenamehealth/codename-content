import sys, json, random, itertools
N_IT = int(sys.argv[1]); sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
base = {'joy': [[903, 'slime', None], [1970, 'slime', 'acv'], [3046, 'crate', None]],
        'cleo': [[884, 'crate', None], [1856, 'slime', 'cre'], [2006, 'crate', None], [2977, 'crate', None]],
        'cyrus': [[657, 'crate', None], [1779, 'slime', 'mush'], [2618, 'crate', None]],
        'ray': [[1099, 'slime', 'mel'], [2347, 'crate', None], [3200, 'slime', None]]}
rnd = random.Random(int(__import__('os').environ.get('RS','1'))); best = []; CNT = {}
for it in range(N_IT):
    c = json.loads(json.dumps(base))
    c['joy'][0][0] = rnd.uniform(800, 1000)
    c['joy'][1][0] = rnd.uniform(1250, 1700); c['joy'][2][0] = rnd.uniform(c['joy'][1][0] + 700, 3300)
    if rnd.random() < 0.5: c['joy'][2][1] = 'slime'
    c['cleo'][0][0] = rnd.uniform(600, 1000); c['cleo'][1][0] = rnd.uniform(1500, 2300); c['cleo'][2][0] = c['cleo'][1][0] + 150; c['cleo'][3][0] = rnd.uniform(c['cleo'][2][0] + 700, 3400)
    if rnd.random() < 0.5: c['cleo'][3][1] = 'slime'
    c['ray'][2][0] = rnd.uniform(2900, 3500); c['ray'][1][0] = rnd.uniform(1900, 2600)
    c['cyrus'][2][0] = rnd.uniform(2400, 3300)
    globals()['OVR'] = c
    globals()['SA'] = rnd.uniform(300, 360); globals()['SB'] = rnd.uniform(0.5, 4)
    r = score_r(2234)
    if isinstance(r, str): CNT[r] = CNT.get(r, 0) + 1
    else: print(round(SA, 1), round(SB, 2), json.dumps(c), r, flush=True)
print(CNT)
