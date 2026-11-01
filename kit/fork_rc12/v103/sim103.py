import math, random, os
NR = 200; R0 = 70.0; DR = 9.0
GAP = math.radians(float(os.environ.get('GAPDEG', '34')))
BR = 22.0; T0 = float(os.environ.get('T0', '0.0'))   # rc12: rolling from frame 0
DS = 0.80; BALLR = float(os.environ.get('BALLR', '96'))   # rc12: marble 64 -> 96 (face 4x -> 6x)          # render scale (sim -> screen) and marble radius on screen
def ring_r(k): return R0 + DR * k
def omega(k): return float(os.environ.get('OM', '1.9')) * (1 - float(os.environ.get('OMV', '1')) * k / 260.0) * (1 if (k // int(os.environ.get('ALT', '3'))) % 2 == 0 else -1)
_PJ = [random.Random(k * 7 + 1).uniform(-1, 1) for k in range(260)]
def phase0(k): return k * float(os.environ.get('PH', '0.11')) + float(os.environ.get('JIT', '0.4')) * _PJ[k]
def gap_angle(k, tr): return phase0(k) + omega(k) * tr
def angdiff(a, b): return (a - b + math.pi) % (2 * math.pi) - math.pi
def scale_of(R): return min(1.0, 430.0 / (R + 40))
SPEED_T = 3.0; SPEED_X = float(os.environ.get('SPX', '1.8')); STRONG_T = float(os.environ.get('STRT', '3.0')); SLEEP_T = 1.2
def sim(seed, dur=60, gumt=None, kinds=None, prepos=None):
    """prepos: list of dict(x, y, kind, show) gummies fixed in sim coords, visible from 'show' (rc12: the pickup is seen before it fires)"""
    rnd = random.Random(seed)
    b = dict(x=0.0, y=0.0, vx=math.cos(1.0), vy=math.sin(1.0))
    k = 0; frames = []; events = []; gums = []; combo = 0; last_break = -9; combos = []
    nextgum = list(gumt if gumt is not None else [float(x) for x in os.environ.get('GUMT', '4,8.5,13,17.5,22,26.5,31').split(',')])
    kinds = list(kinds if kinds is not None else os.environ.get('KINDS', 'mush,cre,mel,cre,mush,cre,mel').split(','))
    gi = 0; tr = 0.0; speed_until = -9; strong_until = -9; sleep_until = -9; esc = None; strong_left = 0
    for f in range(int(dur * 30)):
        t = f / 30; dt = 1 / 30
        if k >= NR:
            if esc is None: esc = t; events.append((t, 'escape', 0))
            frames.append(dict(k=k, b=dict(b), gums=[], combo=combo, tr=tr, sp=speed_until, st=strong_until, sl=sleep_until))
            if t > esc + 3.6: break
            continue
        R = ring_r(k); scale = scale_of(R)
        if t >= T0:
            if t >= sleep_until: tr += dt
            if prepos is not None:
                for g in prepos:
                    if not g.get('added') and t >= g['show']: g['added'] = True; gums.append(dict(x=g['x'], y=g['y'], kind=g['kind'], t=t, fixed=True, arm=g['arm']))
            elif nextgum and t >= nextgum[0]:
                nextgum.pop(0)
                # appear on the marble's path, a little ahead, so it grabs it soon after it shows up
                L = float(os.environ.get('AHEAD', '0.30')) * R
                for _try in range(30):
                    gx, gy = b['x'] + b['vx'] * L, b['y'] + b['vy'] * L
                    if math.hypot(gx, gy) < 0.55 * R: break
                    L *= 0.85
                gums.append(dict(x=gx, y=gy, kind=kinds[gi % len(kinds)], t=t)); gi += 1
            spd = float(os.environ.get('SPD', '560')) / scale * (SPEED_X if t < speed_until else 1.0)
            sub = 6
            for _ in range(sub):
                b['x'] += b['vx'] * spd * dt / sub; b['y'] += b['vy'] * spd * dt / sub
                br = BALLR / (DS * scale)
                while k < NR:
                    R = ring_r(k); d = math.hypot(b['x'], b['y'])
                    if d + br < R: break
                    ang = math.atan2(b['y'], b['x'])
                    smash = t < strong_until and strong_left > 0
                    if smash or abs(angdiff(ang, gap_angle(k, tr))) < GAP / 2:
                        isg = abs(angdiff(ang, gap_angle(k, tr))) < GAP / 2
                        if smash and not isg: strong_left -= 1
                        events.append((t, 'break' if isg else 'smash', k)); k += 1
                        if t - last_break < 0.35: combo += 1
                        else:
                            if combo >= 3: combos.append((last_break, combo))
                            combo = 1
                        last_break = t
                        continue
                    nx, ny = b['x'] / d, b['y'] / d
                    dot = b['vx'] * nx + b['vy'] * ny
                    if dot > 0:
                        b['vx'] -= 2 * dot * nx; b['vy'] -= 2 * dot * ny
                        a = math.atan2(b['vy'], b['vx']) + rnd.uniform(-0.12, 0.12); b['vx'], b['vy'] = math.cos(a), math.sin(a)
                        events.append((t, 'bounce', k))
                    b['x'] = nx * (R - br - 0.5); b['y'] = ny * (R - br - 0.5)
                    break
            for g in list(gums):
                if g.get('fixed') and t < g['arm']: continue
                if math.hypot(b['x'] - g['x'], b['y'] - g['y']) < ((BALLR * 0.75) if g.get('fixed') else (BALLR + 40)) / (DS * scale):
                    gums.remove(g); events.append((t, 'gum', g['kind']))
                    if g['kind'] == 'mush': speed_until = t + SPEED_T
                    elif g['kind'] == 'cre': strong_until = t + STRONG_T; strong_left = int(os.environ.get('STRN', '25'))
                    elif g['kind'] == 'mel': sleep_until = t + SLEEP_T
            for g in gums:
                if g.get('fixed'): continue
                if math.hypot(g['x'], g['y']) > ring_r(k) * 0.7: g['x'] *= 0.98; g['y'] *= 0.98
        if t < T0: frames.append(dict(k=k, b=dict(b), gums=[], combo=combo, tr=tr, sp=speed_until, st=-9, sl=sleep_until)); continue
        frames.append(dict(k=k, b=dict(b), gums=[dict(g) for g in gums], combo=combo, tr=tr, sp=speed_until, st=strong_until if strong_left > 0 else -9, sl=sleep_until))
    return frames, events, combos, esc
if __name__ == '__main__':
    import sys
    for s in range(int(sys.argv[1]), int(sys.argv[2])):
        fr, ev, cb, esc = sim(s)
        g = [(round(e[0], 1), e[2]) for e in ev if e[1] == 'gum']
        sm = sum(1 for e in ev if e[1] == 'smash')
        print(s, 'esc', esc and round(esc, 1), 'k', fr[-1]['k'], 'gums', g, 'smash', sm, 'maxcombo', max([c for _, c in cb] + [0]), flush=True)

def place(seed, gumt, kinds, lead=0.7, dur=40):
    """rc12: put gummy i exactly where the marble will be at gumt[i] (given gummies < i), visible from gumt[i]-lead"""
    pre = []
    for i, (tg, kd) in enumerate(zip(gumt, kinds)):
        for g in pre: g.pop('added', None)
        fr, ev, cb, esc = sim(seed, dur, prepos=[dict(g) for g in pre])
        if esc is not None and esc <= tg: break
        f = min(int(round(tg * 30)), len(fr) - 1); bb = fr[f]['b']
        pre.append(dict(x=bb['x'], y=bb['y'], kind=kd, show=tg - lead, arm=tg - 0.12))
    for g in pre: g.pop('added', None)
    fr, ev, cb, esc = sim(seed, dur, prepos=[dict(g) for g in pre])
    return pre, fr, ev, cb, esc
