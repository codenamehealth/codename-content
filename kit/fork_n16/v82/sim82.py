# #82 physics (fork_n16, Oct 29 notes2): fixed-timestep rigid-ball sim with gravity inside a ring of AABB bricks.
# Every brick collider is the exact pixel rect of the brick sprite as drawn. Ball = circle RB.
# Rule: every bounce event (a wall contact; reflections <0.06s apart are one contact) queues exactly one new brick
# on top of the stack of the bin it hit; the brick appears the first substep the ball is clear of its rect.
import math, random, os, sys, json
import numpy as np
from PIL import Image
FPS = 30; NS = 24; DT = 1.0 / FPS / NS
CX, CY = 478, 1068; R0 = 360; NB = 60; BH = 28; RB = 64
G = float(os.environ.get('G', '1250'))
SPD0 = float(os.environ.get('SP', '1050'))
GA = math.radians(float(os.environ.get('GA', '35')))        # exit corridor axis (screen angle, y down; 0 = right)
CW = RB + float(os.environ.get('CWX', '14'))                                                   # corridor half width
RMIN = 110                                                     # stacks never grow inside this radius
BOOST = float(os.environ.get('BOOST', '1.006')); VMAX = float(os.environ.get('VMAX', '1800'))
MERGE = 0.06
SPD_GUM = float(os.environ.get('SG', '1.12'))
SB = os.path.dirname(os.path.abspath(__file__))
BW, BHh = 32, 33   # brick sprite size after crop + 1.25x (checked in render)
AX, AY = math.cos(GA), math.sin(GA)

PAR = math.radians(float(os.environ.get('PAR', '25')))   # bins this close to the exit axis stack parallel to it (tunnel walls)
def stack_dir(b):
    am = math.radians(b * 6 + 3); da = abs((am - GA + math.pi) % (2 * math.pi) - math.pi)
    return (AX, AY) if da < PAR else (math.cos(am), math.sin(am))
def brick_rect(b, k):
    am = math.radians(b * 6 + 3); ux, uy = stack_dir(b)
    bx, by = CX + R0 * math.cos(am) - k * BH * ux, CY + R0 * math.sin(am) - k * BH * uy
    r = math.hypot(bx - CX, by - CY)
    x0, y0 = int(bx - BW / 2), int(by - BHh / 2)
    return (x0, y0, x0 + BW, y0 + BHh), r

def in_corridor(rect):
    x0, y0, x1, y1 = rect; sides = set(); hit = False
    for px, py in ((x0, y0), (x1, y0), (x0, y1), (x1, y1), ((x0 + x1) / 2, (y0 + y1) / 2)):
        dx, dy = px - CX, py - CY; al = dx * AX + dy * AY; pe = -dx * AY + dy * AX
        if al > 0:
            if abs(pe) < CW: hit = True
            sides.add(pe > 0)
    return hit or len(sides) == 2 and all(((p[0] - CX) * AX + (p[1] - CY) * AY) > 0 for p in ((x0, y0), (x1, y1)))

GAPB = set(b for b in range(NB) if in_corridor(brick_rect(b, 0)[0]))
KMAX = {}
for b in range(NB):
    k = 0
    while True:
        rect, r = brick_rect(b, k + 1)
        cx_, cy_ = (rect[0] + rect[2]) / 2 - CX, (rect[1] + rect[3]) / 2 - CY
        if r < RMIN or in_corridor(rect) or (stack_dir(b) == (AX, AY) and cx_ * AX + cy_ * AY < 60): break
        k += 1
    KMAX[b] = k

def sim(seed, dur=22.0, post=3.0, gums_on=True):
    rnd = random.Random(seed)
    x, y = CX + rnd.uniform(-40, 40), CY + rnd.uniform(-80, 0)
    a = rnd.uniform(0, 2 * math.pi); vx, vy = math.cos(a) * SPD0, math.sin(a) * SPD0
    init = (x, y, vx, vy)
    bricks = []   # dict(b, k, rect, t_spawn)
    for b in range(NB):
        if b not in GAPB: bricks.append(dict(b=b, k=0, rect=brick_rect(b, 0)[0], t=-1.0))
    def arrays():
        R = np.array([br['rect'] for br in bricks], float); return R[:, 0], R[:, 1], R[:, 2], R[:, 3]
    X0, Y0, X1, Y1 = arrays()
    hq = {b: 0 for b in range(NB)}           # queued height per bin
    pending = []                             # dict(b,k,rect,t_hit,ev)
    events = []                              # bounce events: dict(t, b, brick_index, spawn_t)
    refl = []                                # every reflection (t, brick idx)
    last_refl = -9.0
    frames = []; esc = None; fail = None; post_contacts = 0
    gums = []; spawn_t = 2.0; boost_t = -9
    nsteps = int((dur + post) * FPS) * NS
    for step in range(nsteps):
        t = step * DT
        if esc is not None and t > esc + post: break
        if esc is None and t > dur: fail = 'noescape'; break
        vy += G * DT; x += vx * DT; y += vy * DT
        for it in range(4):
            qx = np.clip(x, X0, X1); qy = np.clip(y, Y0, Y1); d2 = (x - qx) ** 2 + (y - qy) ** 2
            j = int(np.argmin(d2))
            if d2[j] >= RB * RB: break
            d = math.sqrt(d2[j])
            if d < 1e-6: fail = 'inside'; break
            nx, ny = (x - qx[j]) / d, (y - qy[j]) / d
            x += nx * (RB - d); y += ny * (RB - d)
            vn = vx * nx + vy * ny
            if vn < 0:
                vx -= 2 * vn * nx; vy -= 2 * vn * ny
                refl.append((t, j))
                if esc is not None: post_contacts += 1
                elif t - last_refl > MERGE:
                    sp = math.hypot(vx, vy); ns = min(VMAX, sp * BOOST); vx, vy = vx / sp * ns, vy / sp * ns
                    b = bricks[j]['b']; k = hq[b] + 1
                    if k > KMAX[b]: fail = 'cap%d' % b; break
                    hq[b] = k
                    ev = dict(t=t, b=b, j=j, k=k, spawn_t=None); events.append(ev)
                    pending.append(dict(b=b, k=k, rect=brick_rect(b, k)[0], ev=ev))
                last_refl = t
        if fail: break
        # spawn queued bricks once the ball is clear of their rect (same bin: in order)
        if pending:
            done = []
            for p in pending:
                if any(q['b'] == p['b'] and q['k'] < p['k'] for q in pending if q not in done and q is not p): continue
                x0, y0, x1, y1 = p['rect']; qx = min(max(x, x0), x1); qy = min(max(y, y0), y1)
                if (x - qx) ** 2 + (y - qy) ** 2 > (RB + 1) ** 2:
                    bricks.append(dict(b=p['b'], k=p['k'], rect=p['rect'], t=t)); p['ev']['spawn_t'] = t; done.append(p)
            if done:
                pending = [p for p in pending if p not in done]; X0, Y0, X1, Y1 = arrays()
        # gummies (mushroom SPEED): impulse on pickup
        if esc is None and gums_on:
            if t >= spawn_t and len(gums) < 5:
                for _ in range(30):
                    gr = rnd.uniform(40, 170); ga = rnd.uniform(0, 2 * math.pi)
                    gx, gy = CX + gr * math.cos(ga), CY + gr * math.sin(ga)
                    if math.hypot(gx - x, gy - y) > RB + 120: break
                gums.append(dict(x=gx, y=gy, t=t, got=None)); spawn_t = t + 2.6
            for g in gums:
                if g['got'] is None and math.hypot(g['x'] - x, g['y'] - y) < RB + 18:
                    g['got'] = t; sp = math.hypot(vx, vy); ns = min(VMAX, sp * SPD_GUM); vx, vy = vx / sp * ns, vy / sp * ns
        # escape: fully past the ring along the corridor
        if esc is None:
            dx, dy = x - CX, y - CY; al = dx * AX + dy * AY
            if al > R0 + 24 + RB: esc = t; esc_state = (x, y, vx, vy); pending_at_esc = len(pending)
        if step % NS == NS - 1: frames.append((x, y, vx, vy))
    if fail is None and esc is None: fail = 'noescape'
    res = dict(seed=seed, fail=fail, esc=esc, frames=frames, events=events, refl=len(refl), gums=gums, init=init,
               bricks=[(br['b'], br['k'], br['rect'], br['t']) for br in bricks], post_contacts=post_contacts)
    if esc is not None:
        res['esc_state'] = esc_state; res['pending_at_esc'] = pending_at_esc
    return res

def trajectory(res, T=3.0):
    """ballistic path after escape (identical integrator), for king placement"""
    x, y, vx, vy = res['esc_state']; out = []
    for i in range(int(T / DT)):
        vy += G * DT; x += vx * DT; y += vy * DT; out.append((i * DT, x, y, vx, vy))
    return out

XMAXK = float(os.environ.get('XMAXK', '2500'))
K = 7; MOUTH = (75, 88); KBASE = 156
def place_king(res):
    """mouth centre on the descending path; king body right of the play view (x>1085 at zoom 1);
    mouth height must put the king's base on the temple floor for some bg offset OY in [-480, -300]"""
    best = None
    for (tt, x, y, vx, vy) in trajectory(res):
        if vy <= 0 or x < 1425 or x > XMAXK: continue
        if 1424 <= y <= 1744:
            kx = x - (MOUTH[0] - 80) * K; base = y + (KBASE - MOUTH[1]) * K
            cand = (abs(y - 1580) + abs(x - 1500), tt, x, y, kx, base)
            if best is None or cand < best: best = cand
    return best

if __name__ == '__main__' and sys.argv[1] == 'search':
    print('GAPB', sorted(GAPB), 'KMAX', [KMAX[b] for b in range(NB)], flush=True)
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        r = sim(s)
        if r['fail']: continue
        ne = len(r['events']); ng = sum(1 for g in r['gums'] if g['got'])
        miss = sum(1 for e in r['events'] if e['spawn_t'] is None)
        kp = place_king(r)
        if 11.5 < r['esc'] < 16 and ne >= 30 and kp and r['post_contacts'] == 0 and miss == 0:
            print(s, round(r['esc'], 2), ne, ng, 'king', [round(v) for v in kp[1:]], 'maxh', max(b[1] for b in r['bricks']), flush=True)
