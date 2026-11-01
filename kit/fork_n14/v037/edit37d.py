p = 'r37.py'; s = open(p).read()
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, (s.count(a), a[:70]); s = s.replace(a, b)
# ---- review3: per-lane display mapping between two walls: feet on the start wall (x=132), head touches the far wall (x=880) at the turn,
#      head touches the start wall at the finish (sim unchanged)
rep("""def xpos(s, n=None):
    if s <= LEN: return XLD + s * KD + LOFF.get(n, 0), 1
    return XRD - (s - LEN) * KD + LOFF.get(n, 0), -1""",
"""WALL_R = 880
def xpos(s, n=None):
    n = n or 'cleo'; hw = SWIM[n][0].width / 2; x0 = WALLX + hw; x1 = WALL_R - hw; k_ = (x1 - x0) / LEN
    if s <= LEN: return x0 + s * k_, 1
    return x1 - (s - LEN) * k_, -1""")
rep("""LOFF.update({n_: SWIM[n_][0].width // 2 - SWIM['cleo'][0].width // 2 for n_ in NAMES})\n""", "")
# far wall / deck on the right, ropes end at it
rep("""_dd.rectangle([WALLX - 6, PY0, WALLX + 2, PY1], fill=(235, 225, 200, 255))                      # wall edge""",
"""_dd.rectangle([WALLX - 6, PY0, WALLX + 2, PY1], fill=(235, 225, 200, 255))                      # wall edge
_WR = 880                                                                                       # review3: far (turn) wall
_dd.rectangle([_WR - 12, PY0, _WR, PY1], fill=(20, 70, 130, 150))
for _x in range(_WR - 4, W + STONE.width, STONE.width - 4):
    for _y in range(PY0 - 10, PY1 + STONE.height, STONE.height - 4): DECK.alpha_composite(STONE.transpose(Image.FLIP_LEFT_RIGHT), (_x, _y))
_dd.rectangle([_WR - 2, PY0, _WR + 6, PY1], fill=(235, 225, 200, 255))""")
rep("""    for k, x in enumerate(range(WALLX + 4, PX1 - 20, BUOY.width + 4)):""",
    """    for k, x in enumerate(range(WALLX + 4, 880 - BUOY.width, BUOY.width + 4)):""")
# splash where each swimmer touches the far wall and turns
rep("""        fn_ = st[n]['fin']""", """        tt_ = TTURN.get(n)
        if tt_ is not None and 0 <= t_sim - tt_ < 0.35: burst(img, WALL_R - 18, LANEY[NAMES.index(n)] + 4, (t_sim - tt_) / 0.35, (235, 250, 255), n=10, r0=20, r1=120)
        fn_ = st[n]['fin']""")
rep("CI = NAMES.index('cleo')", """CI = NAMES.index('cleo')
TTURN = {n_: next((k_ / FPS for k_, st_ in enumerate(FR) if st_[n_]['s'] >= LEN), None) for n_ in NAMES}""")
# slime follows Cleo's own mapping
rep("""    s_ = st['cleo']['s']; x, d = xpos(s_); y = LANEY[CI]""", """    s_ = st['cleo']['s']; x, d = xpos(s_, 'cleo'); y = LANEY[CI]""")
rep("""            x, _ = xpos(FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]['s']); y = LANEY[NAMES.index(e[2])]""",
    """            x, _ = xpos(FR[min(int(e[0] * FPS), len(FR) - 1)][e[2]]['s'], e[2]); y = LANEY[NAMES.index(e[2])]""")
# ---- review3: gummies sit exactly where the swimmer's leading edge first reaches them at the power's fire time; a return-leg gummy
#      (Cleo's) floats up out of the water after she has turned, so she never swims through it on the way out; pop on contact
rep("""    # gummies
    for n in NAMES:
        r = st[n]
        if r['boost'] is None:
            gx, _ = xpos(r['gs'], n); gy = LANEY[NAMES.index(n)]; bob = int(5 * math.sin(t_anim * 4 + gx))
            g = up(gummy_src(GK[n]), 4)
            layer(img, lambda d, gx=gx, gy=gy: d.ellipse([gx - 44, gy - 24, gx + 44, gy + 24], fill=(255, 255, 255, 60)))
            img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2 - 14 + bob)))""",
"""    # gummies
    for n in NAMES:
        if n not in GPOS: continue
        tp_, gx, sp_t, gcol = GPOS[n]; gy = LANEY[NAMES.index(n)]
        if t_sim < tp_ and t_sim >= sp_t:
            g = GIMG[n]; rise = min(1.0, (t_sim - sp_t) / 0.35) if sp_t > 0 else 1.0; bob = int(5 * math.sin(t_anim * 4 + gx)) * rise
            if sp_t > 0 and t_sim - sp_t < 0.5:   # surfacing ripple
                q_ = (t_sim - sp_t) / 0.5; layer(img, lambda d, gx=gx, gy=gy, q_=q_: d.ellipse([gx - 50 - 70 * q_, gy - 10 - 16 * q_, gx + 50 + 70 * q_, gy + 26 + 16 * q_], outline=(235, 250, 255, int(220 * (1 - q_))), width=6))
            layer(img, lambda d, gx=gx, gy=gy, rise=rise: d.ellipse([gx - 44, gy - 24, gx + 44, gy + 24], fill=(255, 255, 255, int(60 * rise))))
            gg = g if rise >= 1 else g.copy()
            if rise < 1: gg.putalpha(g.getchannel('A').point(lambda p_, rise=rise: int(p_ * (0.35 + 0.65 * rise))))
            img.alpha_composite(gg, (int(gx - g.width / 2), int(gy - g.height / 2 - 14 + bob + (1 - rise) * 40)))
        elif 0 <= t_sim - tp_ < 0.3:          # pop on contact
            burst(img, gx, gy - 14, (t_sim - tp_) / 0.3, gcol, n=10, r0=20, r1=110)""")
rep("""def draw_slime(img, st, t_sim, t_anim):""", """GIMG = {n_: up(gummy_src(GK[n_]), 4) for n_ in NAMES}
GCOL = {'acv': (255, 120, 110), 'mush': (180, 110, 70), 'mel': (255, 170, 120), 'cre': (255, 130, 180)}
GPOS = {}
for e_ in FX:
    if e_[1] != 'pick': continue
    n_, tp_ = e_[2], e_[0]; sp_ = FR[min(int(round(tp_ * FPS)), len(FR) - 1)][n_]['s']
    x_, d_ = xpos(sp_, n_); hw_ = SWIM[n_][0].width / 2; gx_ = x_ + d_ * (hw_ + GIMG[n_].width / 2 - 6)
    spawn_ = 0.0
    if sp_ > LEN:   # picked on the way back: it floats up after she has turned (and after any sleep), ~1s before she reaches it
        spawn_ = max(TTURN[n_] + 0.3, tp_ - 0.9, max([e2[0] + SLEEP_T for e2 in FX if e2[1] == 'sleep' and e2[0] < tp_] + [0]) + 0.1)
    GPOS[n_] = (tp_, gx_, spawn_, GCOL[GK[n_]])
print('gummies', {k_: (round(v_[0], 2), int(v_[1]), round(v_[2], 2)) for k_, v_ in GPOS.items()})
def draw_slime(img, st, t_sim, t_anim):""")
# ---- speed lines off while asleep
rep("""        fx = dict(shove=shv, speed=b is not None and k == 'mush' and 0 <= t_sim - b < SPEED_T,""",
    """        fx = dict(shove=shv, speed=b is not None and k == 'mush' and 0 <= t_sim - b < SPEED_T and t_sim >= r['sleep'],""")
# ---- photo finish: all four lanes (z 1.1), box under a dark strip that carries PHOTO FINISH! / CLEO WINS!
rep("""        ys = [LANEY[NAMES.index(win)], LANEY[NAMES.index(second)]]; cyA = (ys[0] + ys[1]) / 2
        BX0, BY0, BX1, BY1 = 0, int(LY0 - 40), W, 1500; bw, bh = BX1 - BX0, BY1 - BY0""",
"""        ZP = 1.1; BX0, BY0, BX1 = 0, 528, W; BY1 = BY0 + int((LY1 - LY0 + 10) * ZP); bw, bh = BX1 - BX0, BY1 - BY0   # review3: all four lanes""")
rep("""        z = (1 + 0.9 * min(1, u / P_ZOOM)) * (1 - k) + ZB * k
        cw, ch = bw / z, bh / z
        xA = 0.0; xB = scx - 610 / ZB                     # slime lands right of centre, Cleo's legs on the left
        cy = cyA * (1 - k) + (LANEY[CI] - 55) * k     # slime sits low in the shot so the heart clears CLEO WINS!
        x0 = max(0, min(W - cw, xA * (1 - k) + xB * k)); y0 = max(BY0, min(BY1 - ch, cy - ch / 2))""",
"""        z = (1 + (ZP - 1) * min(1, u / P_ZOOM)) * (1 - k) + ZB * k
        cw, ch = bw / z, bh / z
        xA, yA = 0.0, LY0 - 5; xB = scx - 610 / ZB; yB = scy - (1060 - BY0) / ZB     # slime lands right of centre at y~1060
        x0 = max(0, min(W - cw, xA * (1 - k) + xB * k)); y0 = max(0, min(H - ch, yA * (1 - k) + yB * k))""")
rep("""        if u < P_WIN:
            text_layer(img, [(490, HB + 105, 'PHOTO FINISH!', 60, (255, 255, 255), 9, 255)])
        else:
            q = u - P_WIN; sc = 1 + 0.3 * max(0, 1 - q / 0.12)
            text_layer(img, [(490, HB + 105, LABEL[win] + ' WINS!', int(64 * sc), (255, 214, 60), 9, 255)])""",
"""        layer(img, lambda d: d.rectangle([0, BY0 - 74, W, BY0 - 4], fill=(10, 8, 20, 215)))   # review3: dark strip behind the text
        if u < P_WIN:
            text_layer(img, [(W / 2, BY0 - 68, 'PHOTO FINISH!', 56, (255, 255, 255), 8, 255)])
        else:
            q = u - P_WIN; sc = 1 + 0.15 * max(0, 1 - q / 0.12)
            text_layer(img, [(W / 2, BY0 - 68, LABEL[win] + ' WINS!', int(56 * sc), (255, 214, 60), 8, 255)])""")
# Cleo's gummy surfacing sfx + busy window so it isn't fast-forwarded
rep("""_busy = sorted([(T_GO, T_GO + 0.6)]""", """_busy = sorted([(e_[0] - 1.0, e_[0]) for e_ in FX if e_[1] == 'pick' and e_[2] == 'cleo'] + [(T_GO, T_GO + 0.6)]""")
open(p, 'w').write(s); print('ok')
