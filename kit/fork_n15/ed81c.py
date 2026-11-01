p='r81.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("def passable(r, c): return 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] != '#' and MAP[r][c] != 'o'",
  "SMASHED = set()   # n15c: lamps smashed by a STRENGTH strike become floor\ndef passable(r, c): return 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] != '#' and (MAP[r][c] != 'o' or (r, c) in SMASHED)")
R("""    r, c = int(y // C), int(x // C); return 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] == 'o'""",
  """    r, c = int(y // C), int(x // C); return 0 <= r < ROWS and 0 <= c < COLS and MAP[r][c] == 'o' and (r, c) not in SMASHED""")
R("SPOTS = [((9, 9), 'acv') if ACVR else ((9, 3), 'acv'), ((12, 9), 'mush'), ((16, 3), 'mel'), ((9, 3), 'cre') if ACVR else ((9, 9), 'cre')]",
  "SPOTS = [((9, 9), 'acv') if ACVR else ((9, 3), 'acv'), ((12, 9), 'mush'), ((16, 3), 'mel'), ((5, 2), 'cre') if ACVR else ((9, 9), 'cre')]   # n15c: STRENGTH sits just above the left-lane lamp it smashes")
R("shield=False, sleep=-9.0, dist0=0.0, ate=False)", "shield=False, sleep=-9.0, dist0=0.0, ate=False, smash=None, atk=-9.0, struck=True, face=1)")
R("    taken = {}; frames = []; front = 0.0; bursts = []; pops = []; ssleep = -9.0", "    SMASHED.clear(); smashes = []\n    taken = {}; frames = []; front = 0.0; bursts = []; pops = []; ssleep = -9.0")
R("""            sliding = t - s['slide'] < SL or (s['slide'] > 0 and pillar_at(s['x'], s['y']))""", """            sliding = t - s['slide'] < SL or (s['slide'] > 0 and pillar_at(s['x'], s['y']))
            planted = 0 <= t - s['atk'] < ATK_LEN   # n15c: STRENGTH planted strike on a lamp
            if planted:
                s['vx'] = s['vy'] = 0.0
                if not s['struck'] and t - s['atk'] >= ATK_WIND:
                    s['struck'] = True; SMASHED.add(s['smash']); smashes.append((t, n, s['smash'], s['face'])); front = max(0.0, front - PUSH); s['smash'] = None""")
R("""            if sliding:
                sp *= 1.2; s['vx'] += (s['sdx'] * sp - s['vx']) * 0.3; s['vy'] += (s['sdy'] * sp - s['vy']) * 0.3
            else:""", """            if planted: pass
            elif s['smash'] is not None:   # walk to the lamp's side, plant, strike
                lr, lc = s['smash']; lx, ly = lc * C + C / 2, lr * C + 44
                px_, py_ = lx + s['face'] * -72, ly
                ddx_, ddy_ = px_ - s['x'], py_ - s['y']; dl = math.hypot(ddx_, ddy_)
                if dl < 12: s['atk'] = t; s['struck'] = False; s['vx'] = s['vy'] = 0.0
                else:
                    spd_ = min(sp, dl * 6); s['vx'] += (ddx_ / dl * spd_ - s['vx']) * 0.25; s['vy'] += (ddy_ / dl * spd_ - s['vy']) * 0.25
            elif sliding:
                sp *= 1.2; s['vx'] += (s['sdx'] * sp - s['vx']) * 0.3; s['vy'] += (s['sdy'] * sp - s['vy']) * 0.3
            else:""")
R("""                    push = (sep - dd) / 2 * (0.25 if shp else 1.0); s['x'] += ddx / dd * push * 0.8; s['y'] += ddy / dd * push * (0.8 if shp else 0.5)""",
"""                    push = (sep - dd) / 2 * (0.25 if shp else 1.0); pxu, pyu = ddx / dd, ddy / dd
                    vv = math.hypot(s['vx'], s['vy'])
                    if shp and vv > 1:   # n15c: the bubble deflects a runner sideways, never holds them back
                        vxu, vyu = s['vx'] / vv, s['vy'] / vv; dp = pxu * vxu + pyu * vyu
                        if dp < 0: pxu, pyu = pxu - dp * vxu, pyu - dp * vyu
                    s['x'] += pxu * push * 0.8; s['y'] += pyu * push * (0.8 if shp else 0.5)""")
R("""                    elif kind == 'cre': front = max(0.0, front - PUSH)      # STRONG: punches the shadow back""",
"""                    elif kind == 'cre':   # n15c STRENGTH: plants by the nearest lamp below and smashes it (the blast pushes the shadow back)
                        lm = [(lr, lc) for (lr, lc) in LAMPS if (lr, lc) not in SMASHED and 0 <= lr * C + 44 - s['y'] < 2.5 * C and abs(lc * C + C / 2 - s['x']) < 2 * C]
                        if lm:
                            s['smash'] = min(lm, key=lambda q: math.hypot(q[1] * C + C / 2 - s['x'], q[0] * C + 44 - s['y']))
                            s['face'] = 1 if s['x'] < s['smash'][1] * C + C / 2 else -1
                        else: front = max(0.0, front - PUSH)""")
R("sleep=s['sleep']) for n, s in racers.items()}, front, dict(taken), ssleep))", "sleep=s['sleep'], atk=s['atk'], face=s['face']) for n, s in racers.items()}, front, dict(taken), ssleep))")
R("    return racers, frames, bursts, pops\n", "    sim.smashes = smashes\n    return racers, frames, bursts, pops\n")
R("PUSH = 9.0; BT, BK", "ATK_WIND, ATK_LEN = 0.42, 1.0; PUSH = 9.0; BT, BK")
open(p,'w').write(s)
