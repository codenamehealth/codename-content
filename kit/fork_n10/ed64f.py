p='r64.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
rep("if not (0.5 <= (j - popped) / FPS <= 1.1): return None   # review2: a visible ~0.6s arc into his hands",
    "if not (0.2 <= (j - popped) / FPS <= 1.1): return None   # the arc is shown in slow motion (TMAP), so short real flights read")
rep('''    j = int(round((t - t0) * FPS)) - 1
    if j < 0:   # the spawn frame: one step back along the first frame's motion (no one-frame stall at spawn)
        x, y, vx, vy = path[0]; return (x - vx / FPS, y - vy / FPS + 0.5 * GRAV / FPS ** 2, vx, vy - GRAV / FPS)
    return path[min(j, len(path) - 1)]''', '''    u = (t - t0) * FPS - 1; j = math.floor(u + 1e-9); fr_ = u - j
    def st(k):
        if k < 0:   # spawn: one step back along the first frame's motion (no one-frame stall at spawn)
            x, y, vx, vy = path[0]; return (x - vx / FPS, y - vy / FPS + 0.5 * GRAV / FPS ** 2, vx, vy - GRAV / FPS)
        return path[min(k, len(path) - 1)]
    a, b = st(j), st(j + 1)
    if fr_ < 1e-6: return a
    return tuple(a[q] + (b[q] - a[q]) * fr_ for q in range(4))   # slow-motion frames sit between sim frames''')
rep('''N = int(round(END * FPS))
''', '''# review2: the escape-to-catch plays at 0.4x so the gummy's real arc into his hands is readable
SLO0, SLO1, SLOW = T_ESC - 0.15, T_CATCH + 0.05, 0.4
TMAP = []; _st = 0.0
while _st < END - 1e-9:
    TMAP.append(_st); _st += (SLOW if SLO0 <= _st < SLO1 else 1.0) / FPS
N = len(TMAP)
def out_t(simt):
    for i_, v_ in enumerate(TMAP):
        if v_ >= simt - 1e-9: return i_ / FPS
    return N / FPS
''')
rep("def frame(f):\n    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()", "def frame(f):\n    t = TMAP[f]; img = BG[int(t * 6) % len(BG)].copy()")
rep("w.close(); json.dump({'events': sorted(ev)}, open('v64_ev.json', 'w'))", "w.close(); json.dump({'events': sorted((round(out_t(tt), 3), nm) for tt, nm in ev)}, open('v64_ev.json', 'w'))")
open(p,'w').write(s)
