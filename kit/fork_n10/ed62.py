p='phys62.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:70]; s=s.replace(a,b)
rep("CX = 478; FLOOR = 1495;", "CX = 478; FLOOR = 1420;   # review2: pedestal and gummy floor a step behind the guides (they stand in front at y1478-1495, drawn over the pile)\n")
rep("WATCH = {'joy': (152, 1430), 'cyrus': (318, 1445), 'cleo': (648, 1445), 'ray': (800, 1430)}", "WATCH = {'joy': (152, 1478), 'cyrus': (318, 1495), 'cleo': (648, 1495), 'ray': (800, 1478)}")
rep("s.density = 0.001; s.friction = 0.95; s.elasticity = 0.08;", "s.density = 0.001; s.friction = FRIC; s.elasticity = 0.12;")
rep("GRAV = 2600; SUB = 12", "GRAV = 2600; SUB = 12; FRIC = 0.55   # review2: lower friction so the stack breaks into separate gummies (was 0.95: bent like a noodle)")
rep("""            if v > 25 or abs(w) > 0.25 or abs(a) > 0.35: return None""","""            if v > 40 or abs(w) > (0.6 if i >= 5 else 0.25) or abs(a) > 0.35: return None
    # wobble that grows from #5: peak tilt of the stack after each landing rises #5 < #6 < #7
    amp = []
    for i in (4, 5, 6):
        f0, f1 = int(round((land[i] - TD[0]) * FPS)), int(round((TD[i + 1] - TD[0]) * FPS))
        amp.append(max(abs(frames[f][j][2]) for f in range(f0, f1) for j in range(1, i + 1)))
    if not (0.015 <= amp[0] < amp[1] < amp[2] and amp[2] >= 0.04): return None""")
rep("""    return round(gh[0] - land[7], 2), down""","""    # natural scatter, not a neat row: final x spread wide and y not all on one line
    xs = sorted(st[0] for st in fe); ys = [st[1] for st in fe]
    if xs[-1] - xs[0] < 420 or max(ys) - min(ys) < 40: return None
    return round(gh[0] - land[7], 2), down, [round(a_, 3) for a_ in amp]""")
rep("""        lean = rnd.uniform(3.4, 5.6); offs = [0]
        for i in range(1, 8): offs.append(offs[-1] + lean * rnd.uniform(0.6, 1.4))""","""        lean = rnd.uniform(2.0, 7.0); offs = [0]
        for i in range(1, 8): offs.append(offs[-1] + lean * rnd.uniform(-0.6, 1.8))""")
open(p,'w').write(s)
