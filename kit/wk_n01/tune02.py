import sys, json, random, os
N_IT = int(sys.argv[1]); sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
base = json.load(open(os.environ.get('BASE', 'ovr_a.json')))
rnd = random.Random(int(os.environ.get('RS', '1'))); CNT = {}
for it in range(N_IT):
    c = json.loads(json.dumps(base))
    c['cleo'][0][0] = rnd.uniform(1500, 2500); c['cleo'][1][0] = c['cleo'][0][0] + 150; c['cleo'][2][0] = rnd.uniform(c['cleo'][1][0] + 600, 3600)
    c['cleo'][2][1] = rnd.choice(['crate', 'slime'])
    c['joy'][1][0] = rnd.uniform(1500, 2400); c['joy'][2][0] = rnd.uniform(c['joy'][1][0] + 600, 3600)
    c['cyrus'][0][0] = rnd.uniform(600, 1200); c['cyrus'][1][0] = rnd.uniform(1500, 2300); c['cyrus'][2][0] = rnd.uniform(c['cyrus'][1][0] + 600, 3600)
    c['ray'][0][0] = rnd.uniform(900, 1300); c['ray'][1][0] = rnd.uniform(1700, 2700); c['ray'][2][0] = rnd.uniform(2700, 3400)
    globals()['OVR'] = c; globals()['SA'] = rnd.uniform(240, 330); globals()['SB'] = rnd.uniform(0.5, 4)
    r = score_r(2234)
    if isinstance(r, str):
        CNT[r] = CNT.get(r, 0) + 1
        if False:
            json.dump({'c': c, 'SA': SA, 'SB': SB}, open('r8_%d.json' % CNT[r], 'w'))
            st_, fr_, ev_, *_ = sim(2234, 18); print('R8', [(round(e[0],2), e[1], e[2], e[3] if len(e)>3 and isinstance(e[3], str) else '') for e in ev_ if e[1] in ('pick','smash','block','caught')], [(g, round(st_[g]['done'],1)) for g in G if st_[g]['done']])
    else: print(round(SA, 1), round(SB, 2), json.dumps(c), r, flush=True)
print(CNT)
