import sys
sys.argv = ['n01.py', 'x']
src = open('n01.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
st, fr, ev, obs, lanes, ld = sim(2234, 18)
print(lanes)
for g in G: print(g, [(round(o[0]), o[1], o[3]) for o in obs[g]])
