p='r58.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
# tilted diamond pegs (no perfect balance on a point), same geometry drawn and simulated
rep("    for x in ([255, 445, 635, 825] if j % 2 == 0 else [350, 540, 730]): PEGS.append((X(x), y + DY, 13))",
    "    for x in ([255, 445, 635, 825] if j % 2 == 0 else [350, 540, 730]): PEGS.append((X(x), y + DY, 13))\n_pr = random.Random(58); PEGTILT = [_pr.choice([-1, 1]) * _pr.uniform(0.05, 0.09) for _ in PEGS]   # review4: pegs tilted 3-5 deg so nothing balances on a tip\ndef peg_pts(i, x, y, r):\n    a = PEGTILT[i]; ca, sa = math.cos(a), math.sin(a)\n    return [(x + px * ca - py * sa, y + px * sa + py * ca) for px, py in [(0, -r - 8), (r, 0), (0, r + 8), (-r, 0)]]")
rep("""    for (x, y, r) in PEGS:
        c = pymunk.Poly(sp.static_body, [(x, y - r - 8), (x + r, y), (x, y + r + 8), (x - r, y)]);""", """    for i_, (x, y, r) in enumerate(PEGS):
        c = pymunk.Poly(sp.static_body, peg_pts(i_, x, y, r));""")
rep("""for (x, y_, r) in PEGS:
    pts = [(x, y_ - r - 8), (x + r, y_), (x, y_ + r + 8), (x - r, y_)]""", """for i_, (x, y_, r) in enumerate(PEGS):
    pts = peg_pts(i_, x, y_, r)""")
# chute: walls start below the funnel lips and are wider (no prong tips to balance on)
rep("SEGS.append(((CX - 63, FIN_Y - 10), (CX - 63, JT + 20), 8, 'chute')); SEGS.append(((CX + 63, FIN_Y - 10), (CX + 63, JT + 20), 8, 'chute'))",
    "SEGS.append(((CX - 68, FIN_Y + 12), (CX - 68, JT + 20), 8, 'chute')); SEGS.append(((CX + 68, FIN_Y + 12), (CX + 68, JT + 20), 8, 'chute'))   # review4: 110px inside, tops tucked under the funnel lips")
# seed rules
rep("""    fr, fin, ld, bo = sim(seed, record=False)
    if any(k_[0] == 'kick' for k_ in KLOG): return None""", """    global DBGQ
    DBGQ = []
    fr, fin, ld, bo = sim(seed, record=True)
    if any(k_[0] == 'kick' for k_ in KLOG): return None
    # review4: nothing stays still (<15px over 0.4s) except on the gate or at the bottle; nothing rides a waterwheel >0.3s
    for n in NAMES:
        ride = 0
        for f in range(len(fr)):
            if n in fr[f][3] or fr[f][0][n][1] > FIN_Y - 120: break
            if (f + 1) / FPS > T_GO + 0.15 and f + 12 < len(fr):
                p = fr[f][0][n]
                if all(math.hypot(fr[g][0][n][0] - p[0], fr[g][0][n][1] - p[1]) < 15 for g in range(f, f + 12)): return None
            ride = ride + 1 if DBGQ[f][0][n] < 1.5 else 0
            if ride > 9: return None""")
# halo removed (it extended past the marble and read as overlaps)
rep("        dl.ellipse([x - MR - 8, sy - MR - 8, x + MR + 8, sy + MR + 8], fill=RING[n] + (55,))\n", "")
# podium: drop in from above the top of the frame
rep("""        DROP = 220.0; tf = math.sqrt(2 * DROP / 3000.0)   # review3: each guide drops onto the block (gravity) and lands
        dy_ = -DROP + 0.5 * 3000.0 * min(uu, tf) ** 2""", """        DROP = float(top); tf = math.sqrt(2 * DROP / 5000.0)   # review4: each guide falls from above the top of the frame and lands
        dy_ = -DROP + 0.5 * 5000.0 * min(uu, tf) ** 2""")
rep("NHOLD = int(round(1.8 * FPS))", "NHOLD = int(round(2.0 * FPS))")
# standings hysteresis
rep("    rank = sorted(NAMES, key=lambda n: (fin[n] if n in fin else 1e6 - pos[n][1]))", """    raw = sorted(NAMES, key=lambda n: (fin[n] if n in fin else 1e6 - pos[n][1]))
    global RANK_SHOWN, RANK_PEND
    if f == 0 or RANK_SHOWN is None: RANK_SHOWN, RANK_PEND = raw, (raw, 0)
    if raw != RANK_SHOWN:   # review4: a new order must hold 4 frames before the bar changes (no one-frame flicker)
        RANK_PEND = (raw, RANK_PEND[1] + 1) if RANK_PEND[0] == raw else (raw, 1)
        if RANK_PEND[1] >= 4 or any(n in fin for n in raw[:1]): RANK_SHOWN = raw
    rank = RANK_SHOWN""")
rep("cam = 0.0\ndef SIMF", "cam = 0.0\nRANK_SHOWN = None; RANK_PEND = (None, 0)\ndef SIMF")
open(p,'w').write(s)
