p='r62.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
rep("T_END = GH[0] + 2.4; N = int(round(T_END * FPS))", """# review2: end = pile at rest + 1.0s hold
T_REST = GH[0]
for f in range(int(round((GH[0] - TD[0]) * FPS)), len(FR_)):
    if all(st is None or st[3] < 15 for st in FR_[f]): T_REST = TD[0] + (f + 1) / FPS; break
T_END = T_REST + 1.0; N = int(round(T_END * FPS))
# review2: growing wobble from #5. Rigid stacking settles dead still, so the gummies' softness is rendered as a damped
# shear of the column that starts at zero on each landing (#5 4px, #6 7px, #7 10px at the top) and fades before the real tip.
WOB = [(LAND[4], 4.0), (LAND[5], 7.0), (LAND[6], 10.0), (LAND[7], 12.0)]
def shear(t):
    v = 0.0
    for tl, A in WOB:
        if t > tl: v += A * math.sin(2 * math.pi * 2.2 * (t - tl)) * math.exp(-(t - tl) / 0.7)
    if t > LAND[7]: v *= max(0.0, 1 - (t - LAND[7]) / 0.35)   # handed over to the real physics before the stack tips
    return v""")
rep("""    for i, k in enumerate(SEQ):
        if st[i] is None: continue
        x, y, ang = st[i][:3]; s = SPR[k].rotate""","""    sh = shear(t)
    for i, k in enumerate(SEQ):
        if st[i] is None: continue
        x, y, ang = st[i][:3]
        if sh and y < PTOP: x += sh * min(1.0, (PTOP - y) / 640)
        s = SPR[k].rotate""")
rep("""    for g, (wx, wy) in sorted(WATCH.items(), key=lambda kv: kv[1][1]):
        fr = PAN""","""    for s, p in sprites: img.alpha_composite(s, p)     # review2: the pile lands a step behind the guides (they are drawn in front)
    for g, (wx, wy) in sorted(WATCH.items(), key=lambda kv: kv[1][1]):
        fr = PAN""")
rep("""    for s, p in sprites: img.alpha_composite(s, p)     # gummies in front of the watchers (the pile lands at their feet)\n""", "")
rep("T_TIMBER + 0.2 < t < T_TIMBER + 2.4 else", "T_TIMBER + 0.2 < t < T_TIMBER + 2.2 else")
open(p,'w').write(s)
