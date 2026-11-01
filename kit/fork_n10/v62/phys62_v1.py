# #62 tower physics (Oct 29 n10): every gummy is a rigid body from the moment it spawns; it falls, lands, settles and the
# tower topples under gravity and contact only (no scripted rest positions, no sway curve, no sweep).
import sys, os, math, random, json
SPD = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SPD + 'fork1'); from common import *
sys.path.insert(0, SPD + 'fork_rc3'); from rc3 import acv_gummy_strong
import numpy as np, pymunk
GK = 3
SEQ = ['acv', 'cre', 'mush', 'mel', 'cre', 'acv', 'mush', 'mel']
SPR = {k: crop(gummy(k, GK)) for k in set(SEQ)}; SPR['acv'] = crop(up(acv_gummy_strong(), GK))
PED = up(crop(Image.open(SPD + 'fork2/pedestal/00.png').convert('RGBA')), 3)
CX = 478; FLOOR = 1495; PTOP = FLOOR - PED.height + 4 * 3
TD = [-0.3 + sum([0, 1.05, 0.95, 1.05, 0.9, 1.0, 0.85, 0.95][:i + 1]) for i in range(len(SEQ))]
GRAV = 2600; SUB = 12
def hull(img):
    a = np.array(img)[:, :, 3] > 0; wmax = a.sum(1).max(); pts = []
    rows = [y for y in range(a.shape[0]) if a[y].sum() >= 0.45 * wmax]     # body rows only (drops the apple stem / leaf)
    for y in range(rows[0], a.shape[0]):
        xs = np.where(a[y])[0]
        if len(xs): pts += [(xs[0], y), (xs[-1] + 1, y), (xs[0], y + 1), (xs[-1] + 1, y + 1)]
    return [(x - img.width / 2, y - img.height / 2) for x, y in pts]
HULL = {k: hull(v) for k, v in SPR.items()}
WATCH = {'joy': (152, 1430), 'cyrus': (318, 1445), 'cleo': (648, 1445), 'ray': (800, 1430)}
def _watch_poly(g, wx, wy):
    fr = idle(g, 4)[0]; a = np.array(fr)[:, :, 3] > 0; pts = []
    for y in range(0, a.shape[0], 4):
        xs = np.where(a[y])[0]
        if len(xs): pts += [(wx - fr.width / 2 + xs[0] + 6, wy - 78 * 4 + y), (wx - fr.width / 2 + xs[-1] - 6, wy - 78 * 4 + y)]
    return pts
WATCH_POLYS = []   # n10 final: watchers stand a step behind the gummy floor line (feet y1430-1445 vs floor 1495), so falling gummies pass in front of them, not through them
def sim(offs, spawn_y, dur, record=True):
    sp = pymunk.Space(); sp.gravity = (0, GRAV); sp.iterations = 40
    g = pymunk.Segment(sp.static_body, (-400, FLOOR), (1480, FLOOR), 2); g.friction = 0.9; g.elasticity = 0.1; g.collision_type = 9
    pw = PED.width
    ped = pymunk.Poly(sp.static_body, [(CX - pw / 2 + 6, PTOP), (CX + pw / 2 - 6, PTOP), (CX + pw / 2 - 6, FLOOR), (CX - pw / 2 + 6, FLOOR)]); ped.friction = 0.9; ped.elasticity = 0.05
    sp.add(g, ped)
    for x in (-400, 1480):    # far off-frame (no invisible walls on screen)
        wl = pymunk.Segment(sp.static_body, (x, -2000), (x, FLOOR), 6); wl.friction = 0.6; wl.elasticity = 0.2; sp.add(wl)
    for poly in WATCH_POLYS:  # the watching guides are solid: falling gummies bounce off them instead of passing through
        wp = pymunk.Poly(sp.static_body, poly); wp.friction = 0.7; wp.elasticity = 0.15; sp.add(wp)
    bodies = [None] * len(SEQ); land = [None] * len(SEQ); ground_hit = [None]
    t = TD[0]; dt = 1 / (FPS * SUB); frames = []
    first_contact = {}
    nf = int(round((dur - TD[0]) * FPS))
    for f in range(nf):
        t = TD[0] + f / FPS
        for i, td in enumerate(TD):
            if bodies[i] is None and t >= td - 1e-9:
                b = pymunk.Body(); b.position = (CX + offs[i], spawn_y + SPR[SEQ[i]].height / 2); b.angle = 0
                s = pymunk.Poly(b, HULL[SEQ[i]]); s.density = 0.001; s.friction = 0.95; s.elasticity = 0.08; s.collision_type = i + 1
                sp.add(b, s); bodies[i] = b
        for _ in range(SUB):
            sp.step(dt)
        # first contact of each gummy (landing) and first gummy on the ground
        for i, b in enumerate(bodies):
            if b is None: continue
            if land[i] is None:
                for sh in b.shapes:
                    pass
                cps = []
                b.each_arbiter(lambda arb: cps.append(arb))
                if cps: land[i] = t + 1 / FPS
            if ground_hit[0] is None and b.position.y > PTOP + 10: ground_hit[0] = (t + 1 / FPS, i)
        if record: frames.append([(b.position.x, b.position.y, b.angle, b.velocity.length, b.angular_velocity) if b else None for b in bodies])
    return frames, land, ground_hit[0]
def check(frames, land, gh):
    if gh is None or any(l is None for l in land): return None
    if gh[0] < land[7]: return None                       # nothing falls before #8 lands
    if gh[0] - land[7] > 1.6: return None                  # #8 tips it, promptly
    # before every new drop (and before #8 lands) the tower is settled and upright
    for i in range(1, 8):
        fi = int(round((TD[i] - 0.02 - TD[0]) * FPS))
        st = frames[fi]
        for j in range(i):
            x, y, a, v, w = st[j]
            if v > 25 or abs(w) > 0.25 or abs(a) > 0.35: return None
    # the tower itself goes over (not just #8 sliding off): at least 5 gummies end on the ground, and #8 was resting on the
    # stack for a moment first (it lands, the stack starts to lean, then everything goes)
    fe = frames[-1]; down = sum(1 for st in fe if st and st[1] > PTOP)
    if down < 5: return None
    if gh[1] == 7: return None                            # #8 sliding off alone is not a topple
    f8 = int(round((land[7] + 0.25 - TD[0]) * FPS)); x8, y8 = frames[f8][7][:2]
    if y8 > PTOP - 300: return None
    return round(gh[0] - land[7], 2), down
if __name__ == '__main__':
    HB = 454
    best = None; rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    for it in range(int(sys.argv[2]) if len(sys.argv) > 2 else 200):
        lean = rnd.uniform(3.4, 5.6); offs = [0]
        for i in range(1, 8): offs.append(offs[-1] + lean * rnd.uniform(0.6, 1.4))
        offs[7] = offs[6] + rnd.uniform(8, 32)
        offs = [round(o, 1) for o in offs]   # exact values that get printed (the topple is sensitive to sub-pixel offsets)
        fr, land, gh = sim(offs, HB + 20, TD[7] + 2.5)
        c = check(fr, land, gh)
        if c is not None:
            print('OK', it, [round(o, 1) for o in offs], 'land', [round(l, 2) for l in land], 'tip', gh, c, flush=True)
