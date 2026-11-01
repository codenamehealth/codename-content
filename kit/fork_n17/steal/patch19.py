p='steal_n19.py'; s=open(p).read()
def R(a,b,n=1):
    global s
    assert s.count(a)==n, (a[:90], s.count(a)); s=s.replace(a,b)
i=s.index("V = {'joy': 400"); j=s.index("SLK = 5")
new = r'''V = {'joy': 400, 'cyrus': 440, 'cleo': 390, 'ray': 420}
FRAC = 0.75   # n19: frame 0 = each guide 3/4 of the way home with a gummy (spread out, not a pile-up)
P0 = {n: (PSPOT[n][0] + FRAC * (HOME[n][0] - PSPOT[n][0]), PSPOT[n][1] + FRAC * (HOME[n][1] - PSPOT[n][1])) for n in NAMES}
AC = {n: Actor(n, 0.0, *P0[n]) for n in NAMES}
# frame 0: each holds one gummy (ids 0-3); the blanket keeps ids 4-6; id 7 drops from the sky later
for n in NAMES: AC[n].go(*HOME[n], V[n]).do('drop', n)
# trip 2: Cyrus / Cleo fetch from the blanket; Joy goes later and lingers at the blanket; Rayleigh lifts one from Joy's basket at ~1.5s
for n in ['cyrus', 'cleo']:
    a = AC[n]; a.wait(0.1 if n == 'cyrus' else 0.25).go(*PSPOT[n], V[n]).do('grab', 'pile', 0.15).go(*HOME[n], V[n]).do('drop', n)
S1 = (BASE['joy'][0] - 120, BASE['joy'][1] + 90)
r = AC['ray']; r.until(1.5 - math.hypot(S1[0] - HOME['ray'][0], S1[1] - HOME['ray'][1]) / V['ray']).go(*S1, V['ray'])
T_STEAL1 = r.t; r.do('grab', 'joy', 0.12).go(*HOME['ray'], V['ray']).do('drop', 'ray')
j = AC['joy']; j.until(T_STEAL1 - 0.25 - math.hypot(PSPOT['joy'][0] - HOME['joy'][0], PSPOT['joy'][1] - HOME['joy'][1]) / V['joy']).go(*PSPOT['joy'], V['joy'])
j.do('grab', 'pile', 0.1).until(T_STEAL1 + 0.5).go(*HOME['joy'], V['joy']).do('drop', 'joy')
T_JOYQ = T_STEAL1 + 0.15                 # Joy's '?' right when her gummy goes (she's at the blanket)
T_HUNGRY = max(T_JOYQ + 0.7, max(AC[n].t for n in NAMES) - 0.1)   # the slime gets hungry once
T_FALL = max(max(AC[n].t for n in NAMES) + 0.25, T_HUNGRY + 0.95); G_LAND = T_FALL + 0.53
TOP_Y, LAND_Y = HUD1 + 40, CY + 10
def drop_y(u, top, land, tf=0.53):
    """gravity drop from `top` (at rest) landing on `land` after tf seconds, then two damped bounces (restitution 0.3)."""
    if u < 0: return None
    g = 2 * (land - top) / tf ** 2
    if u < tf: return land - (land - top) * (1 - (u / tf) ** 2)
    u -= tf; v = 0.3 * (2 * (land - top) / tf)
    if u < 2 * v / g: return land - (v * u - 0.5 * g * u * u)
    u -= 2 * v / g; v2 = 0.3 * v
    if u < 2 * v2 / g: return land - (v2 * u - 0.5 * g * u * u)
    return land
def fall_y(t): return drop_y(t - T_FALL, TOP_Y, LAND_Y)
# Joy wins the scramble; Cyrus and Cleo stop short and trudge back; Rayleigh sneaks to Cleo's basket
j.until(G_LAND - 0.1).go(CX, CY - 40, 470); T_JOYGRAB = j.t; j.do('grab', 'sky', 0.15).go(*HOME['joy'], 400).do('drop', 'joy')
for n in ['cyrus', 'cleo']:
    a = AC[n]; a.until(G_LAND - 0.1); tx, ty = PSPOT[n]; a.go(tx + (40 if n == 'cyrus' else 0), ty + (30 if n == 'cleo' else 0), V[n]).until(T_JOYGRAB + 0.45).go(*HOME[n], 240).do('arrive', n)
r.until(G_LAND - 0.1).go(BASE['cleo'][0] - 120, BASE['cleo'][1] + 24, V['ray'])
T_STEAL2 = r.t; r.do('grab', 'cleo', 0.12).go(*HOME['ray'], V['ray']).do('drop', 'ray')
T_RAY3 = r.t
r.wait(0.55).do('grab', 'ray', 0.18).do('grab', 'ray', 0.18).do('grab', 'ray', 0.25)
T_GOFEED = r.t; r.go(*RAYFEED, 330)
T_FEED0 = r.t + 0.15; FEEDS = [T_FEED0 + 0.45 * i for i in range(3)]
r.until(FEEDS[-1] + 0.1)
for k_ in range(3): r.act.append((FEEDS[k_], 'feed', None))
def state(t, ALLX=None):
    pile = [(4, 4), (5, 5), (6, 6)]; bases = {n: [] for n in NAMES}; carry = {n: [i] for i, n in enumerate(NAMES)}; fed = 0
    for (te, n, k, arg) in (ALL if ALLX is None else ALLX):
        if te > t: break
        if k == 'drop' and carry[n]: bases[arg] += carry[n]; carry[n] = []
        elif k == 'grab':
            if arg == 'pile' and pile: carry[n].append(pile.pop()[0])
            elif arg == 'sky': carry[n].append(7)
            elif arg in bases and bases[arg]: carry[n].append(bases[arg].pop())
        elif k == 'feed' and carry[n]: carry[n].pop(); fed += 1
        elif k == 'droppile': pile += [(g_, SLOT[g_]) for g_ in carry[n]]; carry[n] = []
        elif k == 'rainland': pile.append(arg)
        elif k == 'grabslot':
            hit = [e for e in pile if e[1] == arg]
            if hit: pile.remove(hit[0]); carry[n].append(hit[0][0])
    sky = 7 if T_FALL <= t < T_JOYGRAB else None
    return pile, bases, carry, sky, fed
# ---- n19 loop seam: everyone resets to the exact frame-0 state while fresh gummies rain in
T_R = FEEDS[-1] + 0.3
SLOT = {}
_all0 = sorted([(t, n, k, arg) for n, a in AC.items() for (t, k, arg) in a.act], key=lambda e: e[0])
_, BR, _, _, _ = state(T_R, _all0)
RET = [(n, g_) for n in NAMES for g_ in BR[n]]                    # basket gummies each guide carries back
need_pile = {4: gk[4], 5: gk[5], 6: gk[6]}                        # what must stay on the blanket (frame 0)
need_pick = {n: gk[i] for i, n in enumerate(NAMES)}              # what each guide carries at frame 0
want = list(need_pile.values()) + list(need_pick.values())
have = [gk[g_] for _, g_ in RET]
rain_k = list(want)
for k_ in have:
    assert k_ in rain_k, ('returned kind not usable', k_, have, want); rain_k.remove(k_)
RAINIDS = []
for q, k_ in enumerate(rain_k): gid = 8 + q; gk[gid] = k_; RAINIDS.append(gid)
pool = [g_ for _, g_ in RET] + RAINIDS
free_slots = {4: None, 5: None, 6: None}
for sl_, k_ in need_pile.items():
    c = [g_ for g_ in pool if gk[g_] == k_ and g_ not in SLOT]
    c.sort(key=lambda g_: g_ not in RAINIDS)                          # fresh gummies stay on the blanket
    SLOT[c[0]] = sl_
PICKSLOT = {}; nxt = [0, 1, 2, 3, 7]
for n, k_ in need_pick.items():
    c = [g_ for g_ in pool if gk[g_] == k_ and g_ not in SLOT][0]; SLOT[c] = nxt.pop(0); PICKSLOT[n] = SLOT[c]
RAIN = [(T_R + 0.05 + 0.1 * q, gid, SLOT[gid]) for q, gid in enumerate(RAINIDS)]   # (t0, id, slot), falls 0.4s
RTF = 0.4; RSET = 1.78 * RTF
for n in NAMES:
    a = AC[n]; a.until(T_R)
    if n == 'ray': a.go(*PSPOT['ray'], V['ray'])
    else:
        for _ in BR[n]: a.do('grab', n, 0.14)
        a.go(*PSPOT[n], V[n]).do('droppile', n, 0.1)
T_PICK = max([AC[n].t for n in NAMES] + [t0 + RSET for t0, _, _ in RAIN]) + 0.02
for q, n in enumerate(NAMES): AC[n].until(T_PICK + 0.05 * q).do('grabslot', PICKSLOT[n], 0.1)
DEP = {n: FRAC * math.hypot(HOME[n][0] - PSPOT[n][0], HOME[n][1] - PSPOT[n][1]) / V[n] for n in NAMES}
END = max(AC[n].t + DEP[n] for n in NAMES) + 0.02
for n in NAMES: AC[n].until(END - DEP[n]).go(*HOME[n], V[n])        # each passes its frame-0 spot exactly at END
for a in AC.values(): a.until(END + 1)
RAINACT = [(t0 + RSET, 'rain', 'rainland', (gid, sl_)) for t0, gid, sl_ in RAIN]
T_RAIN = RAIN[0][0] if RAIN else T_R
print({n: round(a.t, 2) for n, a in AC.items()}, 'steal1', round(T_STEAL1, 2), 'hungry', round(T_HUNGRY, 2), 'fall', round(T_FALL, 2), 'steal2', round(T_STEAL2, 2), 'ray3', round(T_RAY3, 2), 'feeds', [round(x, 2) for x in FEEDS], 'reset', round(T_R, 2), 'pick', round(T_PICK, 2), 'end', round(END, 2), 'rain', [(gid, gk[gid]) for gid in RAINIDS], 'ret', RET)
ALL = sorted([(t, n, k, arg) for n, a in AC.items() for (t, k, arg) in a.act] + RAINACT, key=lambda e: e[0])
'''
s = s[:i] + new + s[j:]
# pile render by slot
R("""    for gid in pile:
        g = GSM[gk[gid]]; px, py = PILE_POS[gid]; img.alpha_composite(g, (int(CX + px - g.width / 2), int(CY + py - g.height / 2)))""",
"""    for gid, sl_ in pile:
        g = GSM[gk[gid]]; px, py = PILE_POS[sl_]; img.alpha_composite(g, (int(CX + px - g.width / 2), int(CY + py - g.height / 2)))""")
# rain render (only while falling/bouncing, before it joins the pile)
R("""    for (tr, gid) in RAIN:
        ry_ = drop_y(t - tr, HUD1 + 20, CY + PILE_POS[gid][1] + 30, 0.5)
        if ry_ is not None:
            g = GSM[gk[gid]]; img.alpha_composite(g, (int(CX + PILE_POS[gid][0] - g.width / 2), int(ry_ - g.height)))""",
"""    for (tr, gid, sl_) in RAIN:
        if tr <= t < tr + RSET:
            g = GSM[gk[gid]]; land = CY + PILE_POS[sl_][1] + g.height / 2; ry_ = drop_y(t - tr, HUD1 - 40, land, RTF)
            img.alpha_composite(g, (int(CX + PILE_POS[sl_][0] - g.width / 2), int(ry_ - g.height)))""")
# slime: no angry idle frame; happy closed-eye face (PixelLab slime_cands/03) from the first toss on, squash on each bite
R("SLIME = [up(Image.open(q).convert('RGBA'), SLK) for q in sorted(glob.glob(P + '../race/slime_idle_c/*.png'))]",
  "SLIME = [up(Image.open(q).convert('RGBA'), SLK) for q in sorted(glob.glob(P + '../race/slime_idle_c/*.png'))[:8]]   # n19: frame 08 (angry brows) dropped\nHAPPY = up(crop(Image.open(P + '../race/slime_cands/03.png').convert('RGBA')), SLK)   # closed eyes, open mouth")
R("""    if feeds_done and t - feeds_done[-1] < 0.47: sl = SLIMEB[min(len(SLIMEB) - 1, int((t - feeds_done[-1]) * 15))]
    else: sl = SLIME[int(t * 8) % len(SLIME)]
    layer(img, lambda dd: dd.ellipse([SLX - 76, SLY - 14, SLX + 76, SLY + 12], fill=(0, 0, 0, 80)))
    uh = t - T_HUNGRY; jx = int(round(5 * math.sin(uh * 75))) if 0 <= uh < 0.5 else 0   # n18: tummy rumble
    img.alpha_composite(sl, (SLX - sl.width // 2 + jx, SLY - 62 * SLK))""",
"""    layer(img, lambda dd: dd.ellipse([SLX - 76, SLY - 14, SLX + 76, SLY + 12], fill=(0, 0, 0, 80)))
    uh = t - T_HUNGRY; jx = int(round(5 * math.sin(uh * 75))) if 0 <= uh < 0.5 else 0   # n18: tummy rumble
    if t >= FEEDS[0] - 0.32:
        sx_, sy_ = 1.0, 1.0
        if feeds_done and t - feeds_done[-1] < 0.36:       # squash on the bite, then spring back
            u_ = (t - feeds_done[-1]) / 0.36; k_ = math.sin(u_ * math.pi * 2) * (1 - u_)
            sx_, sy_ = 1 + 0.16 * k_, 1 - 0.16 * k_
        hp = HAPPY.resize((int(HAPPY.width * sx_), int(HAPPY.height * sy_)), Image.NEAREST)
        img.alpha_composite(hp, (SLX - hp.width // 2, SLY - hp.height))
    else:
        sl = SLIME[int(t * 8) % len(SLIME)]
        img.alpha_composite(sl, (SLX - sl.width // 2 + jx, SLY - 62 * SLK))""")
R("hy = SLY - 180 - u * 60","hy = SLY - 225 - u * 60")
# sfx: steal swishes only before the reset; rain twinkle
R("    if k == 'grab' and arg in ('joy', 'cleo'): ev.append((te, 'swish'))","    if k == 'grab' and arg in ('joy', 'cleo') and te < T_R: ev.append((te, 'swish'))")
open(p,'w').write(s); print('ok')
