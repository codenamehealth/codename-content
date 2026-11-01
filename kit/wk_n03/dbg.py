import sys
sd = int(sys.argv[1]); sys.argv = ['n03.py', 'x']
src = open('n03.py').read().split("if len(sys.argv) > 1 and sys.argv[1] == 'search':")[0]
exec(src)
B, fr, ev, gum, hits = sim(sd)
for f in range(0, len(fr), 15):
    st, front = fr[f]
    row = []
    for g in G:
        x, y, vx, vy, ca, do = st[g][:6]
        r, c = cell_of(x, y); row.append(f"{g[:2]} d{DEXIT.get((r,c),-1):2d} s{DSRC.get((r,c),-1):2d} v{int(math.hypot(vx,vy)):3d}{'X' if ca else ''}")
    print(f"{f/30:5.1f} F{front:5.1f} ", ' | '.join(row))
