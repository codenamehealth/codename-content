import sys
sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
for seed in range(1,6):
    st, fr, ev, obs, lanes, ld = sim(seed, 18)
    print(seed, [(round(o[0]), o[1], o[3]) for o in obs['cleo']], [(round(e[0],2), e[1]) for e in ev if e[2]=='cleo' and e[1] in ('pick','smash','satk','atk','hit','caught','hop')])
