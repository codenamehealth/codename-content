import os, sys
sys.argv = ['r81.py', 'none']
src = open('r81.py').read().split("if sys.argv[1] == 'search':")[0]
exec(src)
rc, fr, bu, po = sim(0)
for f in range(88, 118, 3):
    st, front, tk, ss = fr[f]
    print(round(f/30,2), round(front,1), {n: (int(v['x']), int(v['y']), round(float(DSL[cell_of(v['x'], v['y'])]),1), v['caught']) for n, v in st.items()})
