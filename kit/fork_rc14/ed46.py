import sys
p=sys.argv[1]; s=open(p).read()
def R(a,b,c=1):
    global s
    assert s.count(a)==c,(s.count(a),a); s=s.replace(a,b)
R("sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer",
  "sys.path.insert(0, '../../pixellab/safezone'); import hook as _hk\nsys.path.insert(0, SP + 'fork_rc1'); import hook2 as _h2\n_f0 = _hk._fit; _h2._fit = lambda lines, maxw, hi=80, lo=48: _f0(lines, maxw, min(hi, 64), lo)")
R("BY = 604                                     # board top on screen", "BY = 656                                     # board top on screen\nVY0 = 20; VH = 1500 - 656                    # board rows shown: y20-864 (only the grass border is trimmed)\nSPD = 1.15                                   # race plays 15% faster (same sim, same winner) so the finish lands earlier")
R("""HOOK, HB = hook_layer(["WHO'S IN", 'FIRST PLACE?'], accent=1)
CHIP_Y = HB + 6""", """HOOK, HB = _h2.hook_layer2(["WHO'S IN", 'FIRST PLACE?'], accent=1, sub='Pick your racer')
CHIP_Y = HB + 6; CHIP_H = 92
assert CHIP_Y + CHIP_H + 6 <= BY, (HB, BY)""")
R("""POPS = []   # (t0, x, y, text, col, size)
def add_pop(t0, x, y, text, col, size=34):
    POPS.append((t0, x, y, text, col, size))""", """POPS = []   # (t0, x, y, text, col, size, who) - who: racer the stamp follows (None = fixed world point)
def add_pop(t0, x, y, text, col, size=34, who=None):
    POPS.append((t0, x, y, text, col, size, who))""")
R("""        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, POWER[e[3]][0], POWER[e[3]][1], 40)""",
  """        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, POWER[e[3]][0], POWER[e[3]][1], 64, e[2])""")
R("""        s = st0[e[3]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BONK!', (255, 255, 255), 36)""",
  """        s = st0[e[3]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BONK!', (255, 255, 255), 64, e[3])""")
R("""        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BLOCKED!', (110, 230, 90), 32)""",
  """        s = st0[e[2]]; add_pop(t0, s['x'], s['y'] - FOOT - 40, 'BLOCKED!', (110, 230, 90), 60, e[2])""")
R("""add_pop(t0, c_ * C, r_ * C - 90, 'SMASH!', (90, 160, 255), 32)""", """add_pop(t0, c_ * C, r_ * C - 90, 'SMASH!', (90, 160, 255), 60)""")
R("""def pop_items(t, camx):
    act = [p for p in POPS if 0 <= t - p[0] < POP_D]; placed = []; items = []
    for t0, x, y, text, col, size in act:
        u = t - t0; sx = x - camx; sy = y - u * 30
        w = len(text) * size + 20; hh = size + 16
        sx = min(max(sx, 70 + w / 2), 1010 - w / 2)""", """def pop_items(t, camx, st):
    act = [p for p in POPS if 0 <= t - p[0] < POP_D]; placed = []; items = []
    for t0, x, y, text, col, size, who in act:
        if who is not None: x, y = st[who]['x'], st[who]['y'] - FOOT - 70      # rides directly above the racer it applies to
        u = t - t0; sx = x - camx; sy = y - u * 20
        w = len(text) * size + 20; hh = size + 16
        xr = 1018 if BY + sy - VY0 < 1110 else 880
        sx = min(max(sx, 76 + w / 2), xr - w / 2)""")
R("""        sy = max(sy, 30)""", """        sy = max(sy, VY0 + hh / 2 + 6)""")
R("""DUR_RACE = T_WIN + 1.2; T_POD = DUR_RACE; T_LOOP = T_POD + 3.0; DUR = T_LOOP + 0.3; NF = int(round(DUR * FPS))""",
  """T_POD_D = (T_WIN + 1.0) / SPD; PODIUM = 2.5; DUR = T_POD_D + PODIUM; NF = int(round(DUR * FPS))   # ends on the podium; the loop supplies the GO!""")
R("""for e in FX:
    if e[1] == 'pick': ev.append((round(e[0], 3), SFX[e[3]]))
    elif e[1] == 'hit': ev.append((round(e[0], 3), 'punch'))
    elif e[1] == 'block': ev.append((round(e[0], 3), 'boing'))
    elif e[1] == 'smash': ev.append((round(e[0], 3), 'crunch_8bit'))""", """for e in FX:
    td = round(e[0] / SPD, 3)
    if e[1] == 'pick': ev.append((td, SFX[e[3]]))
    elif e[1] == 'hit': ev.append((td, 'punch'))
    elif e[1] == 'block': ev.append((td, 'boing'))
    elif e[1] == 'smash': ev.append((td, 'crunch_8bit'))""")
R("""    t = f / FPS
    loop = t >= T_LOOP
    if loop: t = 0.0; camx = CAM0; rank_pos = {n: float(i) for i, n in enumerate(FR[0][1])}
    fi = int(round(t * FPS))""", """    td = f / FPS; t = td * SPD
    fi = int(round(t * FPS))""")
R("""    if t < T_POD:""", """    if td < T_POD_D:""")
R("""        camx += (target - camx) * 0.12 if t > T_START else 0""", """        camx += (target - camx) * 0.15 if t > T_START else 0""")
R("""ev.append((round(t, 3), 'jump'))""", """ev.append((round(td, 3), 'jump'))""")
R("""            dv = ImageDraw.Draw(view); ctext(dv, x, y - FOOT + 4, str(rk), F(26), RING[n], 5)""",
  """            dv = ImageDraw.Draw(view); ctext(dv, x, max(VY0 + 4, y - FOOT - 24), str(rk), F(52), RING[n], 8)""")
R("""fin_seen.add(n); ev.append((round(t, 3),""", """fin_seen.add(n); ev.append((round(td, 3),""")
R("""        text_layer(view, pop_items(t, camx))""", """        text_layer(view, pop_items(t, camx, st))""")
R("""        img.alpha_composite(view, (0, BY))""", """        img.alpha_composite(view.crop((0, VY0, W, VY0 + VH)), (0, BY))""")
R("""dd.rounded_rectangle([70, CHIP_Y, 1010, CHIP_Y + 100], 18""", """dd.rounded_rectangle([70, CHIP_Y, 1010, CHIP_Y + CHIP_H], 18""")
R("""            tgt = rank.index(n); rank_pos[n] += (tgt - rank_pos[n]) * 0.2""", """            tgt = rank.index(n); rank_pos[n] += (tgt - rank_pos[n]) * 0.6     # swaps snap in ~3 frames
            if abs(tgt - rank_pos[n]) < 0.02: rank_pos[n] = float(tgt)""")
R("""            ctext(d, sx + 44, CHIP_Y + 36, ['1ST', '2ND', '3RD', '4TH'][ri], F(28), (255, 214, 60) if ri == 0 else (230, 230, 230), 5)""",
  """            ctext(d, sx + 52, CHIP_Y + 24, ['1ST', '2ND', '3RD', '4TH'][ri], F(44), (255, 214, 60) if ri == 0 else (230, 230, 230), 6)""")
R("""            sx = 70 + 940 * (rank_pos[n] + 0.5) / 4 - 50; ic = ICS2[n]
            img.alpha_composite(ic, (int(sx - ic.width / 2), CHIP_Y + 8))""", """            sx = 70 + 940 * (rank_pos[n] + 0.5) / 4 - 62; ic = ICS2[n]
            img.alpha_composite(ic, (int(sx - ic.width / 2), CHIP_Y + 2))""")
R("""        if t < 0.7:
            text_layer(img, [(W / 2, BY + 380, 'GO!', 150, (120, 230, 90), 10, int(255 * min(1, (0.7 - t) / 0.3)))])""", """        if td < 0.7:
            text_layer(img, [(W / 2, BY + 340, 'GO!', 150, (120, 230, 90), 10, int(255 * min(1, (0.7 - td) / 0.3)))])""")
R("""        u = t - T_POD; order""", """        t = td; u = td - T_POD_D; order""")
R("""        if u > 0.8: text_layer(img, [(W / 2, HB + 214, 'DID YOU PICK RIGHT?', 40,""", """        if u > 0.8: text_layer(img, [(W / 2, HB + 214, 'DID YOU PICK RIGHT?', 44,""")
R("""wr.close(); json.dump(ev, open('v46_ev.json', 'w'))""", """wr.close(); json.dump({'events': ev}, open('v46_ev.json', 'w'))""")
open(p,'w').write(s); print('ok')
