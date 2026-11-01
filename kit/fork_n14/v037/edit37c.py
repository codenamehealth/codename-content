p = 'r37.py'; s = open(p).read()
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:70]); s = s.replace(a, b)
# ---- hooks
rep("HOOK, HB = hook_fade(['Can you spot', 'the cheater?'], accent=1, color=(255, 214, 60))",
    "HOOK, HB = hook_fade(['Can you spot', 'the cheater?'], accent=1, color=(255, 214, 60)); HOOK2, _ = hook_fade(['Did you', 'catch it?'], accent=1, color=(255, 214, 60))   # review2: swaps in at the reveal")
# ---- per-lane display offset so every swimmer's head meets the finish wall (sim unchanged)
rep("""    if s <= LEN: return XLD + s * KD, 1
    return XRD - (s - LEN) * KD, -1""",
"""    if s <= LEN: return XLD + s * KD + LOFF.get(n, 0), 1
    return XRD - (s - LEN) * KD + LOFF.get(n, 0), -1""")
rep("def xpos(s):", "LOFF = {}\ndef xpos(s, n=None):")
rep("GHOST = {}\ndef swimmer(", """WALL = XLD - SWIM['cleo'][0].width // 2      # review2: start/finish wall face (x=132): heads touch it at the finish, feet push off it at the start
LOFF.update({n_: SWIM[n_][0].width // 2 - SWIM['cleo'][0].width // 2 for n_ in NAMES})
GHOST = {}
def swimmer(""")
rep("""    x, d = xpos(s); i = NAMES.index(n); y = LANEY[i]
    fr = SWIM[n][int(t * 10) % len(SWIM[n])] if moving else SWIM[n][0]""",
"""    x, d = xpos(s, n); i = NAMES.index(n); y = LANEY[i]
    fr = SWIM[n][int(t * 10) % len(SWIM[n])] if moving else SWIM[n][0]""")
rep("""    i = NAMES.index(n); st0 = FR[min(int(round(t0 * FPS)), len(FR) - 1)][n]; x, d = xpos(st0['s']); sw = SWIM[n][0].width""",
    """    i = NAMES.index(n); st0 = FR[min(int(round(t0 * FPS)), len(FR) - 1)][n]; x, d = xpos(st0['s'], n); sw = SWIM[n][0].width""")
rep("""            gx, _ = xpos(r['gs']); gy = LANEY[NAMES.index(n)]""", """            gx, _ = xpos(r['gs'], n); gy = LANEY[NAMES.index(n)]""")
rep("""                    x_, _ = xpos(r['s']); burst(img""", """                    x_, _ = xpos(r['s'], n); burst(img""")
rep("""            x, _ = xpos(r['s']); shield_pop(""", """            x, _ = xpos(r['s'], n); shield_pop(""")
rep("""            x, _ = xpos(st[e[2]]['s']); bonk_burst(""", """            x, _ = xpos(st[e[2]]['s'], e[2]); bonk_burst(""")
# STRENGTH! clears the moment she slams (before the BONK!s land)
rep("""    STAMPS.append([t0, i, text, col, cx, cy, t0 + 1.15])""",
    """    STAMPS.append([t0, i, text, col, cx, cy, t0 + (HIT_T if text == POWER['cre'][0] else 1.15)])   # review2: STRENGTH! gone before the BONK!s""")
# slime never inside the wall at the start
rep("""    cx = x - side * (sw * 0.5 - 35 + 24 * REV['rise'])""",
    """    cx = x - side * (sw * 0.5 - 35 + 24 * REV['rise'])
    if side > 0: cx = max(cx, WALL + fr.width / 2 + 4)""")
# ---- the wall/deck, lane ropes end at the wall, icons sit on the deck
rep("""for i in range(0, NL + 1):
    y = LY0 + LH * i
    for k, x in enumerate(range(PX0 + 4, PX1 - 20, BUOY.width + 4)):""",
"""WALLX = 132
DECK = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _dd = ImageDraw.Draw(DECK)
_dd.rectangle([WALLX, PY0, WALLX + 12, PY1], fill=(20, 70, 130, 150))                        # wall shadow on the water
for _x in range(WALLX - STONE.width + 4, -STONE.width, -(STONE.width - 4)):
    for _y in range(PY0 - 10, PY1 + STONE.height, STONE.height - 4): DECK.alpha_composite(STONE, (_x, _y))
_dd.rectangle([WALLX - 6, PY0, WALLX + 2, PY1], fill=(235, 225, 200, 255))                      # wall edge
for i in range(0, NL + 1):
    y = LY0 + LH * i
    for k, x in enumerate(range(WALLX + 4, PX1 - 20, BUOY.width + 4)):""")
rep("""    img.alpha_composite(water_layer(t_anim)); img.alpha_composite(FRAME)""",
    """    img.alpha_composite(water_layer(t_anim)); img.alpha_composite(FRAME); img.alpha_composite(DECK)""")
rep("""        if t_sim < T_F: img.alpha_composite(ICON[n], (74, int(LANEY[i] - LH / 2 + 2)))""",
    """        if not FROZEN[0]: img.alpha_composite(ICON[n], (WALLX - 76, int(LANEY[i] - LH / 2 + 2)))   # on the deck""")
rep("OPEN = []\ndef scene(", "OPEN = []; FROZEN = [False]\ndef scene(")
# touch splashes at the wall
rep("""    for e in FX:
        if e[1] == 'bonk' and 0 <= t_sim - e[0] < 0.3:""",
"""    for n in NAMES:
        fn_ = st[n]['fin']
        if fn_ is not None and 0 <= t_sim - fn_ < 0.35: burst(img, WALLX + 18, LANEY[NAMES.index(n)] + 4, (t_sim - fn_) / 0.35, (235, 250, 255), n=10, r0=20, r1=120)
    for e in FX:
        if e[1] == 'bonk' and 0 <= t_sim - e[0] < 0.3:""")
# ---- the slam: splash column at the chop + two splash waves rolling into the lanes above and below; BONK! when they arrive
rep("""        if e[1] == 'wave' and 0 <= u < 0.45:
            x, _ = xpos(FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]['s']); y = LANEY[NAMES.index(e[2])]; q = u / 0.45
            layer(img, lambda dd, x=x, y=y, q=q: [dd.ellipse([x - 60 - 90 * q, y - 30 - LH * 1.1 * q, x + 60 + 90 * q, y + 30 + LH * 1.1 * q], outline=(150, 200, 255, int(240 * (1 - q))), width=12 - 4 * k_) for k_ in range(2)])""",
"""        if e[1] == 'wave' and 0 <= u < WAVE_T + 0.3:
            sw_ = FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]; x, d_ = xpos(sw_['s'], e[2]); i_ = NAMES.index(e[2]); y = LANEY[i_]
            fx_ = x + d_ * 70
            if u < 0.45:   # splash column where the blade hits the water
                rr = random.Random(5); q = u / 0.45
                def col(dd, q=q, rr=rr):
                    for k_ in range(26):
                        vx = rr.uniform(-260, 260); vy = rr.uniform(-900, -420); sz = rr.choice([8, 10, 14])
                        px = fx_ + vx * q * 0.45; py = y + vy * q * 0.45 + 0.5 * 2600 * (q * 0.45) ** 2
                        dd.rectangle([px, py, px + sz, py + sz], fill=(235, 250, 255, int(255 * (1 - q ** 2))))
                layer(img, col)
            for j_ in (i_ - 1, i_ + 1):
                if not 0 <= j_ < NL: continue
                ty = LANEY[j_]; q = min(1.0, u / WAVE_T); yy = y + (ty - y) * q; sgn = 1 if ty > y else -1
                a_ = 255 if u < WAVE_T else int(255 * max(0, 1 - (u - WAVE_T) / 0.3)); wid = 230 + 90 * q + (120 * (u - WAVE_T) / 0.3 if u > WAVE_T else 0)
                def crest(dd, yy=yy, sgn=sgn, a_=a_, wid=wid):
                    for k_ in range(-int(wid), int(wid), 12):
                        h_ = 26 * (1 - (k_ / wid) ** 2)
                        y0_ = yy - sgn * h_
                        dd.rectangle([fx_ + k_, y0_ - 10, fx_ + k_ + 11, y0_ + 10], fill=(150, 210, 255, int(a_ * 0.85)))
                        dd.rectangle([fx_ + k_, y0_ + sgn * 8 - 5, fx_ + k_ + 11, y0_ + sgn * 8 + 5], fill=(245, 252, 255, a_))
                        if (k_ // 12) % 3 == 0: dd.rectangle([fx_ + k_ + 2, y0_ + sgn * 24, fx_ + k_ + 9, y0_ + sgn * 31], fill=(245, 252, 255, int(a_ * 0.7)))
                layer(img, crest)""")
rep("SHOVE_T = float(os.environ.get('SHT', '1.0')); HIT_T = 0.4",
    "SHOVE_T = float(os.environ.get('SHT', '1.0')); HIT_T = 0.4; WAVE_T = 0.15 + 1 / 30   # wave reaches the next lane when the BONK lands")
# ---- time map: slow-mo around the slam, slow into the wall, short touch run after Cleo's touch
rep("""TMAP = []; ts = 0.0; tv = 0.0
while ts < T_F - 1e-9:
    TMAP.append(ts); rate = qrate(ts) if ts < A_SPR else 1 + (R_SPR - 1) * min(1, (ts - A_SPR) / 0.5); ts = min(T_F, ts + rate / FPS); tv += 1 / FPS""",
"""T_SLAM = [e[0] for e in FX if e[1] == 'wave'][0]
SLOW = (T_SLAM - 0.25, T_SLAM + 0.3)      # review2: the slam and the waves play at 0.5x so they read
def srate(ts):
    a, b = SLOW
    if not (a - 0.1 <= ts <= b + 0.1): return 1.0
    w = min(1, (ts - a + 0.1) / 0.1, (b + 0.1 - ts) / 0.1); return 1 - 0.5 * max(0, w)
def frate(ts):        # ease from the 1.6x sprint down to 0.75x for the last 0.3s so the touch reads
    return 1.0 if ts < T_F - 0.45 else max(0.0, min(1, (ts - (T_F - 0.45)) / 0.2))
TMAP = []; ts = 0.0; tv = 0.0
while ts < T_F - 1e-9:
    TMAP.append(ts)
    rate = qrate(ts) * srate(ts) if ts < A_SPR else 1 + (R_SPR - 1) * min(1, (ts - A_SPR) / 0.5)
    rate = rate + (0.75 - rate) * frate(ts)
    ts = min(T_F, ts + rate / FPS); tv += 1 / FPS
T_SEC = FINS[1][0]                          # Cyrus touches 0.1s later: keep rolling (0.75x) until just after, then the photo of Cleo's touch
TOUCH = []; ts = T_F
while ts < T_SEC + 0.07: ts += 0.75 / FPS; TOUCH.append(ts)""")
rep("""NRACE = len(TMAP); T_FV = NRACE / FPS""", """NRACE = len(TMAP); NT = len(TOUCH); T_FV = (NRACE + NT) / FPS""")
rep("""P_ZOOM, P_WIN, P_SLIDE0, P_SLIDE1, P_RISE0, P_RISE1, P_HEART, P_END = 0.35, 0.75, 1.2, 1.8, 1.85, 2.2, 2.15, float(os.environ.get('PEND', '3.5'))""",
    """P_ZOOM, P_WIN, P_SLIDE0, P_SLIDE1, P_RISE0, P_RISE1, P_HEART, P_END = 0.3, 0.45, 0.6, 1.0, 1.0, 1.3, 1.2, float(os.environ.get('PEND', '2.45'))   # review2: heart ~1s sooner
P_HOOK2 = 1.1""")
rep("""    frozen = f >= NRACE
    t_sim = TMAP[f] if not frozen else T_F""",
"""    frozen = f >= NRACE + NT; FROZEN[0] = frozen
    t_sim = TMAP[f] if f < NRACE else (TOUCH[f - NRACE] if not frozen else T_F)""")
rep("""    img.alpha_composite(HOOK)
    if STILLS:""", """    img.alpha_composite(HOOK2 if (frozen and u >= P_HOOK2) else HOOK)
    if STILLS:""")
rep("""    if f < 9: OPEN.append(img.copy())\n""", "")
rep("""for im_ in OPEN: W_.write(im_)          # loop: cut back to the opening\n""", "# review2: no copied opening frames at the end; the reveal cuts straight to frame 0\n")
# slam sfx: impact thud at the chop (sword_swish already on the swing)
rep("""        if e[3] == 'cre': ev.append((round(s2v(e[0] + HIT_T - 0.12), 3), 'sword_swish'))""",
    """        if e[3] == 'cre': ev.append((round(s2v(e[0] + HIT_T - 0.12), 3), 'sword_swish')); ev.append((round(s2v(e[0] + HIT_T), 3), 'stomp_8bit'))""")
open(p, 'w').write(s); print('ok')
