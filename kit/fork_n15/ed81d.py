p='r81.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a, s.count(a)); s=s.replace(a,b)
R("SRUNL = {g: [fl(f) for f in v] for g, v in SRUN.items()};", """ATK = {g: seq(SP0 + f'pixellab/race/{g}_atk', 2, 0) for g in NAMES}      # n15c: Syeda/PixelLab attack frames (same sets as #89)
ATKL = {g: [f.transpose(Image.FLIP_LEFT_RIGHT) for f in v] for g, v in ATK.items()}
BCX = {'joy': 34.5, 'cyrus': 29.0, 'cleo': 31.0, 'ray': 29.5}
def atk_frame(a):
    if a < 0.42: return 0 if a < 0.21 else 1
    if a < 0.72: return 2 + min(5, int((a - 0.42) / 0.3 * 6))
    return 8 + min(4, int((a - 0.72) / 0.28 * 5))
SRUNL = {g: [fl(f) for f in v] for g, v in SRUN.items()};""")
R("SHAKE = [tb for (tb, n, bx, by, kind) in BURSTS if kind == 'cre']", "SMASHES = list(sim.smashes); SMASH_AT = {q[2]: q[0] for q in SMASHES}\nSHAKE = [q[0] for q in SMASHES] or [tb for (tb, n, bx, by, kind) in BURSTS if kind == 'cre']")
R("TW = float(os.environ.get('TW', '2.6'))", "TW = float(os.environ.get('TW', '3.1'))")
R("U_SURGE0, U_SURGE1, U_HAPPY = 0.35, 1.1, 1.85", "U_SURGE0, U_SURGE1, U_HAPPY = 0.25, 0.85, 1.5   # n15c: payoff 0.35s sooner, line held 1.6s")
R("U_CURL0, U_CURL1, U_EYES = 1.1, 1.6, 1.3", "U_CURL0, U_CURL1, U_EYES = 0.85, 1.3, 1.0")
R("elif 1.58 <= UT < 1.70:", "elif U_EYES + 0.25 <= UT < U_EYES + 0.36:")
R("    cx, cy = fx + (cx1 - fx) * k, (fy - 60) + (cy1 - fy + 60) * k\n    rx, ry = 320 + (195 - 320) * k, 200 + (115 - 200) * k",
  "    sx0_, sy0_ = fx + BSIDE * 235, fy - 40   # n15c: forms beside the fire, never over the winner\n    cx, cy = sx0_ + (cx1 - sx0_) * k, sy0_ + (cy1 - sy0_) * k\n    rx, ry = 230 + (195 - 230) * k, 150 + (115 - 150) * k")
# DF: surge stops two rows above the fire
a = s.index("DF = max(DSL[EX_R * FINE + 1"); b = s.index("\n", a)
s = s[:a] + "DF = float(DSL[(EX_R - 2) * FINE + 2, EX_C[1] * FINE + 2]) + 0.5   # n15c: the surge stops two rows short of the fire (never rings the winner)" + s[b:]
# visual front recoil from the smash
R("    front = max(front, FRONT0 + 1.6 * (t - V0))", "    front = max(front, FRONT0 + 1.6 * (t - V0) - sum(PUSH * sm((t - q[0]) / 0.3) for q in SMASHES))")
# lamps: smashed ones gone, shatter burst
R("""    for (r, c) in LAMPS:
        lx, ly = c * C + C / 2, r * C + C - 6""", """    for (r, c) in LAMPS:
        lx, ly = c * C + C / 2, r * C + C - 6
        if (r, c) in SMASH_AT and t >= SMASH_AT[(r, c)]:   # n15c: smashed by STRENGTH: shards + flash, then gone
            u = t - SMASH_AT[(r, c)]
            if u < 0.6:
                layer(b, lambda dd, lx=lx, ly=ly, u=u: (dd.ellipse([lx - 40 - 160 * u, ly - 70 - 100 * u, lx + 40 + 160 * u, ly + 10 + 40 * u], fill=(255, 230, 160, int(160 * (1 - u / 0.6)))),
                    [dd.rectangle([lx + math.cos(j * 0.698) * (20 + 260 * u) - 6, ly - 60 + math.sin(j * 0.698) * (20 + 180 * u) + 400 * u * u - 6, lx + math.cos(j * 0.698) * (20 + 260 * u) + 6, ly - 60 + math.sin(j * 0.698) * (20 + 180 * u) + 400 * u * u + 6], fill=((255, 200, 110) if j % 2 else (90, 90, 110)) + (int(255 * (1 - u / 0.6)),)) for j in range(9)]))
            continue""")
# planted attack sprite
R("""        elif t < T_START or t < s['sleep']: spr = STAND[n]
        elif s['sliding']:""", """        elif t < T_START or t < s['sleep']: spr = STAND[n]
        elif 0 <= t - s['atk'] < ATK_LEN:   # n15c: planted STRENGTH strike (attack frames)
            fi_ = atk_frame(t - s['atk'])
            spr = None; aspr = ATK[n][fi_] if s['face'] > 0 else ATKL[n][fi_]; aox = BCX[n] * SS if s['face'] > 0 else (128 - BCX[n]) * SS
            if t - s['atk'] < 0.2: layer(b, lambda dd: [dd.ellipse([x + q * 30 - 14, y - 8, x + q * 30 + 14, y + 6], fill=(240, 245, 255, int(170 * (1 - (t - s['atk']) / 0.2)))) for q in (-1, 1)])
        elif s['sliding']:""")
R("""        b.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['shield'] and not s['caught']:""", """        if spr is None: b.alpha_composite(aspr, (int(x - aox), int(y - 104 * SS)))
        else: b.alpha_composite(spr, (int(x - spr.width / 2), int(y - FOOT)))
        if s['shield'] and not s['caught']:""")
R("""        if boosted and not s['caught']:
            ghosts[n] = (ghosts[n] + [(spr, x, y)])[-5:]""", """        if boosted and not s['caught'] and spr is not None:
            ghosts[n] = (ghosts[n] + [(spr, x, y)])[-5:]""")
R("""            if kind == 'cre':   # STRONG: red/orange impact burst (spikes), punches the shadow back""", """            if kind == 'cre' and SMASHES: pass   # n15c: the burst plays at the smash instead
            elif kind == 'cre':   # STRONG: red/orange impact burst (spikes), punches the shadow back""")
R("""            if kind == 'cre': events.append((round(tb + 0.05, 3), 'punch'))""", """            if kind == 'cre' and not SMASHES: events.append((round(tb + 0.05, 3), 'punch'))
    for (ts_, n_, lrc, fc_) in SMASHES:   # n15c: STRENGTH impact on the lamp: orange spikes + punch + crunch
        u = t - ts_; bx, by = lrc[1] * C + C / 2, lrc[0] * C + C - 6
        if 0 <= u < 0.5:
            rad = 50 + 260 * u; al = int(240 * (1 - u / 0.5)); col = PW['cre'][1]
            layer(b, lambda dd: [dd.line([bx + math.cos(a_) * rad * 0.45, by - 70 + math.sin(a_) * rad * 0.45, bx + math.cos(a_) * rad, by - 70 + math.sin(a_) * rad], fill=col + (al,), width=12) for a_ in [k_ * 0.785 + 0.39 for k_ in range(8)]])
        if abs(t - ts_) < 0.5 / FPS: events += [(round(ts_, 3), 'punch'), (round(ts_ + 0.03, 3), 'crunch_8bit')]""")
# text: hard cut
R("""        a_ = min(1.0, (UT - U_HAPPY) / 0.15)
        if a_ < 1: img.alpha_composite(Image.blend(HOOK, HOOK_END, a_))
        else: img.alpha_composite(HOOK_END)""", """        img.alpha_composite(HOOK_END)   # n15c: hard cut, the two lines never stack""")
open(p,'w').write(s)
