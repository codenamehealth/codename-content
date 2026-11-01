p='phys62.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
rep("CX = 478; FLOOR = 1420;", "CX = 478; FLOOR = 1495;")
rep("GRAV = 2600; SUB = 12; FRIC = 0.55", "GRAV = 2600; SUB = 12; FRIC = 0.45")
rep("WATCH_POLYS = []   #", """def _watch_slabs(g, wx, wy):
    # the guides are solid: stepped slabs that follow the union of Syeda's panic frames (they panic from the tip to the end)
    frs = seq(PL + f'maze/anim/{g}_panic', 4, 1); a = np.zeros((frs[0].height, frs[0].width), bool)
    for fr in frs: a |= np.array(fr)[:, :, 3] > 0
    out = []
    for y0 in range(0, a.shape[0], 16):
        cols = np.where(a[y0:y0 + 16].any(0))[0]
        if len(cols) == 0: continue
        x0, x1 = wx - frs[0].width / 2 + cols[0] + 4, wx - frs[0].width / 2 + cols[-1] - 3
        Y0, Y1 = wy - 78 * 4 + y0, min(wy - 78 * 4 + y0 + 16, wy)
        if x1 - x0 > 6 and Y1 > Y0: out.append([(x0, Y0), (x1, Y0), (x1, Y1), (x0, Y1)])
    return out
WATCH_POLYS = [pl for g, p in WATCH.items() for pl in _watch_slabs(g, *p)]
_unused = []   #""")
open(p,'w').write(s)
p='r62.py'; s=open(p).read()
rep("""    for s, p in sprites: img.alpha_composite(s, p)     # review2: the pile lands a step behind the guides (they are drawn in front)
""", "")
rep("""        img.alpha_composite(fr, (int(wx - fr.width / 2), int(wy - 78 * 4)))
""", """        img.alpha_composite(fr, (int(wx - fr.width / 2), int(wy - 78 * 4)))
    for s, p in sprites: img.alpha_composite(s, p)     # review2: gummies collide with the guides (solid slabs from their panic frames)
""")
rep("T_TIMBER + 0.2 < t < T_TIMBER + 2.2 else", "t > T_TIMBER + 0.2 else")
open(p,'w').write(s)
