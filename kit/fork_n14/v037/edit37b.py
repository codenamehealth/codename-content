p = 'r37.py'; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]; s = s.replace(a, b)
# constants
rep("SPEED_T, SPEED_K = 2.0, 1.8; STRONG_T = 2.5; SLEEP_T = 1.0; STUN_T = 0.6",
"""SPEED_T, SPEED_K = 2.0, 1.8; STRONG_T = 2.5; SLEEP_T = 1.0; STUN_T = 0.6
# n14 (Bennett Oct 29: 'a clear shove animation... they have to stop for a second to perform the shove'):
# Cleo's STRENGTH shove = she stops, stands up waist-deep and swings (existing race cleo_atk animation, 13 frames), the swing lands at
# HIT_T and sends the wave that BONKs the lanes next to her; she dives back in at SHOVE_T, then the STRENGTH x1.2 strokes run for STRONG_T
SHOVE_T = float(os.environ.get('SHT', '1.0')); HIT_T = 0.4""")
rep("""                if r['boost'] is not None and t - r['boost'] < STRONG_T and GK[n] == 'cre': sp *= 1.2""",
"""                if r['boost'] is not None and GK[n] == 'cre':
                    if t - r['boost'] < SHOVE_T: continue                      # stopped: performing the shove
                    if t - r['boost'] < SHOVE_T + STRONG_T: sp *= 1.2""")
rep("""                    elif k == 'cre':
                        i = NAMES.index(n); FX.append((t, 'wave', n))
                        for j in (i - 1, i + 1):
                            if 0 <= j < len(NAMES): PEND.append((t + 0.25, NAMES[j]))""",
"""                    elif k == 'cre':
                        i = NAMES.index(n); FX.append((t + HIT_T, 'wave', n))
                        for j in (i - 1, i + 1):
                            if 0 <= j < len(NAMES): PEND.append((t + HIT_T + 0.15, NAMES[j]))
                        continue                                                  # stops on the spot to shove""")
# stricter search: every power fires and a bonk actually lands, Cleo wins
rep("""    if not any(e[1] in ('sleep', 'block') for e in fx) or not any(e[1] in ('bonk',) for e in fx): return None""",
"""    if not any(e[1] in ('sleep', 'block') for e in fx) or not any(e[1] in ('bonk',) for e in fx): return None
    if not any(e[1] == 'block' for e in fx) or len([e for e in fx if e[1] == 'pick']) < 4: return None
    if fins[0][1] != 'cleo': return None""")
# load Cleo's attack frames
rep("# n14: the cheater = a green slime", """_CA = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(SP + 'pixellab/race/cleo_atk/*.png'))]
_cb = None
for f in _CA:
    b = f.getbbox(); _cb = b if _cb is None else (min(_cb[0], b[0]), min(_cb[1], b[1]), max(_cb[2], b[2]), max(_cb[3], b[3]))
CATK = [up(f.crop(_cb), SS) for f in _CA]; CATK_WAIST = (75 - _cb[1]) * SS      # waterline at her waist (sprite y ~75 of 40-104)
CATK_CX = (28 - _cb[0]) * SS                                                     # body centre column (sprite x ~28)
# n14: the cheater = a green slime""")
# swimmer(): standing shove pose
rep("""def swimmer(img, n, s, t, moving, fx={}):
    x, d = xpos(s); i = NAMES.index(n); y = LANEY[i]
    fr = SWIM[n][int(t * 10) % len(SWIM[n])] if moving else SWIM[n][0]
    if d < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    bob = 4 * math.sin(t * 6 + i)
    top = int(y - fr.height * 0.62 + bob); left = int(x - fr.width / 2)""",
"""def swimmer(img, n, s, t, moving, fx={}):
    x, d = xpos(s); i = NAMES.index(n); y = LANEY[i]
    fr = SWIM[n][int(t * 10) % len(SWIM[n])] if moving else SWIM[n][0]
    if d < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    bob = 4 * math.sin(t * 6 + i)
    top = int(y - fr.height * 0.62 + bob); left = int(x - fr.width / 2)
    if fx.get('shove') is not None:          # stands up waist-deep and swings (existing cleo_atk frames), facing her swim direction
        u = fx['shove']; k = int(u / HIT_T * 4) if u < HIT_T else min(12, 4 + int((u - HIT_T) / (SHOVE_T - HIT_T) * 9))
        fr = CATK[k]; cxo = CATK_CX
        if d < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT); cxo = fr.width - CATK_CX
        bob = 2 * math.sin(t * 4 + i); top = int(y + 6 + bob - CATK_WAIST); left = int(x - cxo)""")
rep("""        fx = dict(speed=b is not None and k == 'mush' and 0 <= t_sim - b < SPEED_T, strong=b is not None and k == 'cre' and 0 <= t_sim - b < STRONG_T,""",
"""        shv = (t_sim - b) if (b is not None and k == 'cre' and 0 <= t_sim - b < SHOVE_T and r['fin'] is None) else None
        if shv is not None: moving = False
        fx = dict(shove=shv, speed=b is not None and k == 'mush' and 0 <= t_sim - b < SPEED_T, strong=b is not None and k == 'cre' and 0 <= t_sim - b < SHOVE_T + STRONG_T,""")
# splash as she stands up / dives back in
rep("""        swimmer(img, n, r['s'], t_anim, moving, fx)""",
"""        swimmer(img, n, r['s'], t_anim, moving, fx)
        if b is not None and k == 'cre':
            for t0_ in (b, b + SHOVE_T):
                if 0 <= t_sim - t0_ < 0.3:
                    x_, _ = xpos(r['s']); burst(img, x_, LANEY[NAMES.index(n)] + 6, (t_sim - t0_) / 0.3, (225, 245, 255), n=12, r0=30, r1=110)""")
# Cleo's STRENGTH stamp sits at the bottom of her lane so it doesn't cover her standing swing
rep("""    STAMPS.append([t0, i, text, col, cx, LY0 + LH * i + 40, t0 + 1.15])""",
"""    cy = LY0 + LH * i + 40 if text != POWER['cre'][0] else LY0 + LH * (i + 1) - 44
    STAMPS.append([t0, i, text, col, cx, cy, t0 + 1.15])""")
# hide lane face icons in the frozen photo-finish zoom
rep("""    for i, n in enumerate(NAMES):
        img.alpha_composite(ICON[n], (74, int(LANEY[i] - LH / 2 + 2)))""",
"""    for i, n in enumerate(NAMES):
        if t_sim < T_F: img.alpha_composite(ICON[n], (74, int(LANEY[i] - LH / 2 + 2)))""")
# quiet windows derived from this seed's events (no stamp on screen, nothing firing)
rep("""R_Q = float(os.environ.get('RQ', '1.7')); QUIET = [(1.15, 2.15), (4.45, 5.15), (6.5, 7.25)]""",
"""R_Q = float(os.environ.get('RQ', '1.7'))
_busy = sorted([(T_GO, T_GO + 0.6)] + [(e[0], e[0] + (1.15 if e[1] in ('pick', 'bonk', 'block') else (SLEEP_T if e[1] == 'sleep' else 0.5))) for e in FX]
               + [(e[0], e[0] + SHOVE_T + 0.2) for e in FX if e[1] == 'pick' and e[3] == 'cre'] + [(e[0], e[0] + SPEED_T) for e in FX if e[1] == 'pick' and e[3] == 'mush'])
QUIET = []; _c = 0.0
for a_, b_ in _busy:
    if a_ - 0.15 - (_c + 0.1) >= 0.6: QUIET.append((_c + 0.1, a_ - 0.15))
    _c = max(_c, b_)
print('quiet windows', [(round(a_, 2), round(b_, 2)) for a_, b_ in QUIET])""")
rep("heart(d, int(hx), int(hy), s_ + 4, (12, 8, 20)); heart(d, int(hx), int(hy), s_)", "heart(d, int(hx), int(hy), s_ + 5, (12, 8, 20)); heart(d, int(hx), int(hy), s_)")
rep("def hfn(d, hx=hx, hy=hy, s_=int(14 * pop)):", "def hfn(d, hx=hx, hy=hy, s_=int(18 * pop)):")
open(p, 'w').write(s); print('ok')
