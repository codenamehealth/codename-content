p='r85.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("GSCHED = [1.0, 3.4, 5.8, 8.2]   # n15: match cut to 10.5s, one gummy every 2.4s",
  "GSCHED = [float(x) for x in os.environ.get('GS', '1.0,3.6,6.4').split(',')]   # n15b: three gummies in the match (no SLEEP: the only Zzz is the payoff)\nATK_WIND, ATK_LEN = 0.42, 1.0; IMP0 = float(os.environ.get('IMP', '820')); FRIC = 2.6")
R("ag[n] = dict(x=sx, y=sy + 40, vx=0.0, vy=0.0, tgt=None, spd=rnd.uniform(240, 270) * SPK, oc=-9, dist=0.0, ph=rnd.uniform(0, 6.3), greed=rnd.uniform(0.6, 1.4), fast=-9.0, sleep=-9.0, shield=-9.0)",
  "ag[n] = dict(x=sx, y=sy + 40, vx=0.0, vy=0.0, tgt=None, spd=rnd.uniform(240, 270) * SPK, oc=-9, dist=0.0, ph=rnd.uniform(0, 6.3), greed=rnd.uniform(0.6, 1.4), fast=-9.0, sleep=-9.0, shield=-9.0,\n                     strong=-9.0, atk=-9.0, struck=True, avic=None, face=1, stun=-9.0, hit=-9.0)")
R("gum = None; gsched = GSCHED; kinds = rnd.sample(['mush', 'acv', 'mel', 'cre'], 4); gi_ = 0   # n15: each power once",
  "gum = None; gsched = GSCHED; kinds = [rnd.choice(['mush', 'cre'])]; kinds += rnd.sample([k for k in ['mush', 'cre', 'acv'] if k != kinds[0]], 2); gi_ = 0   # n15b: each power once, the opener is SPEED or STRENGTH")
R("""            for n, s in ag.items():
                if tt < s['sleep']: s['vx'] *= 0.5; s['vy'] *= 0.5; continue   # melatonin: asleep, stopped""",
"""            for n, s in ag.items():
                if tt - s['stun'] < 0.6:   # knocked back by a STRENGTH strike: slides, deck friction
                    k_ = math.exp(-FRIC * dt); s['vx'] *= k_; s['vy'] *= k_; s['x'] += s['vx'] * dt; s['y'] += s['vy'] * dt; s['tgt'] = None
                    while not inside(s['x'], s['y']): s['x'] += (CX - s['x']) * 0.05; s['y'] += (CY - s['y']) * 0.05
                    continue
                if 0 <= tt - s['atk'] < ATK_LEN:   # planted: wind-up, strike, recover
                    s['vx'] *= 0.5; s['vy'] *= 0.5
                    if not s['struck'] and tt - s['atk'] >= ATK_WIND:
                        s['struck'] = True; o = ag[s['avic']]; dx, dy = o['x'] - s['x'], o['y'] - s['y']
                        if 0 < dx * s['face'] < 250 and abs(dy) < 120:
                            if tt - o['shield'] < 6.0: o['shield'] = -9.0; events.append((t, 'block', s['avic'], n))
                            else:
                                L = math.hypot(dx, dy) or 1; ux, uy = 0.75 * s['face'] + 0.25 * dx / L, 0.25 * dy / L; U = math.hypot(ux, uy)
                                o['vx'], o['vy'] = ux / U * IMP0, uy / U * IMP0; o['stun'] = tt; o['hit'] = tt
                                ci = min(range(NP), key=lambda i: math.hypot(PY[i][0] - o['x'], PY[i][1] - o['y']))
                                flip = ci if math.hypot(PY[ci][0] - o['x'], PY[ci][1] - o['y']) < 110 and own[ci] != n else None
                                if flip is not None: own[flip] = n; prog[flip] = 0.0; capper[flip] = None   # the crystal flips to the striker
                                for i_ in range(NP):
                                    if capper[i_] == s['avic']: prog[i_] = 0.0; capper[i_] = None
                                events.append((t, 'shove', n, s['avic'], flip))
                        else: events.append((t, 'whiff', n, s['avic']))
                        s['strong'] = -9.0
                    s['x'] += s['vx'] * dt; s['y'] += s['vy'] * dt
                    continue
                if 0 <= tt - s['strong'] < 4.0:   # STRENGTH: go after the nearest guide standing on a crystal, plant on the inner side, strike
                    vs = [m for m in NAMES if m != n and tt - ag[m]['stun'] >= 0.6]
                    def oncr(m): return min(math.hypot(px - ag[m]['x'], py - ag[m]['y']) for px, py in PY) < 90
                    vs.sort(key=lambda m: (not oncr(m), math.hypot(ag[m]['x'] - s['x'], ag[m]['y'] - s['y'])))
                    v = vs[0]; o = ag[v]; side = -1 if o['x'] >= CX else 1
                    tx, ty = o['x'] + side * 150, o['y']
                    if abs(o['x'] - s['x']) > 60 and abs(o['x'] - s['x']) < 200 and abs(o['y'] - s['y']) < 70:
                        s['atk'] = tt; s['struck'] = False; s['avic'] = v; s['face'] = 1 if o['x'] > s['x'] else -1; s['vx'] *= 0.3; s['vy'] *= 0.3
                        events.append((t, 'wind', n, v)); continue
                    dx, dy = tx - s['x'], ty - s['y']; L = math.hypot(dx, dy) or 1; sp = s['spd'] * 1.15
                    if L < 40: sp *= L / 40
                    s['vx'] += (dx / L * sp - s['vx']) * 0.15; s['vy'] += (dy / L * sp - s['vy']) * 0.15
                    nx, ny = s['x'] + s['vx'] * dt, s['y'] + s['vy'] * dt
                    if inside(nx, ny): s['dist'] += math.hypot(nx - s['x'], ny - s['y']); s['x'], s['y'] = nx, ny
                    continue""")
R("""                    elif k in ('cre', 'mel'):
                        for m, o in ag.items():""", """                    elif k == 'cre': s['strong'] = tt                             # STRENGTH: one planted strike
                    elif k == 'mel':
                        for m, o in ag.items():""")
R("near = [n for n in NAMES if math.hypot(ag[n]['x'] - px, ag[n]['y'] - py) < 80 and tt >= ag[n]['sleep']]",
  "near = [n for n in NAMES if math.hypot(ag[n]['x'] - px, ag[n]['y'] - py) < 80 and tt >= ag[n]['sleep'] and tt - ag[n]['stun'] >= 0.6]")
R("frames.append(dict(ag={n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], dist=s['dist'], fast=s['fast'], sleep=s['sleep'], shield=s['shield']) for n, s in ag.items()},",
  "frames.append(dict(ag={n: dict(x=s['x'], y=s['y'], vx=s['vx'], vy=s['vy'], dist=s['dist'], fast=s['fast'], sleep=s['sleep'], shield=s['shield'], strong=s['strong'], atk=s['atk'], face=s['face'], stun=s['stun'], hit=s['hit']) for n, s in ag.items()},")
R("""    ks = [e[3] for e in ev if e[1] == 'gum']
    if len(set(ks)) < 4: return None""", """    gm = [(e[2], e[3]) for e in ev if e[1] == 'gum']
    if len(gm) != 3 or len(set(n for n, k in gm)) != 3: return None   # each power once, three different guides
    shv = [e for e in ev if e[1] == 'shove']
    if len(shv) != 1 or shv[0][4] is None: return None   # the STRENGTH strike lands on someone on a crystal and flips it""")
R("[(round(e[0], 1), e[1], e[2]) for e in ev if e[1] in ('block', 'shove', 'lead')]", "[(round(e[0], 1), e[1], e[2]) for e in ev if e[1] in ('block', 'shove', 'lead', 'whiff')]")
open(p,'w').write(s)
