p = 'r37.py'; s = open(p).read()
def rep(a, b):
    global s
    assert s.count(a) == 1, a[:60]; s = s.replace(a, b)
rep("HOOK, HB = hook_fade(['Choose your', 'champion'], accent=1, color=(110, 200, 255))   # Oct 29: soft fade, sub line cut",
"HOOK, HB = hook_fade(['Can you spot', 'the cheater?'], accent=1, color=(255, 214, 60))   # n14 Oct 29: job hook (Bennett-approved idea), same soft fade + size")
rep("# scene\n",
"""# n14: the cheater = a green slime (existing race slime idle frames, pixellab/race/slime_idle_c) under the water pushing Cleo's feet the whole race
import glob as _g, numpy as _np
def _nored(im):
    a = _np.array(im); r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    a[(r > 140) & (g < 110) & (b < 140)] = 0
    return Image.fromarray(a)
_SL = [_nored(Image.open(f).convert('RGBA')) for f in sorted(_g.glob(SP + 'pixellab/race/slime_idle_c/*.png'))]
_bb = None
for f in _SL:
    b = f.getbbox(); _bb = b if _bb is None else (min(_bb[0], b[0]), min(_bb[1], b[1]), max(_bb[2], b[2]), max(_bb[3], b[3]))
SLK = 3; SLIME = [up(f.crop(_bb), SLK) for f in _SL]     # faces right (eyes on the right)
SL_ALPHA = float(os.environ.get('SLA', '0.42'))       # under-water visibility during the race (subtle, findable on a rewatch)
REV = dict(rise=0.0, ta=None)                          # set during the reveal: rise 0..1 (eyes break the surface), ta = slime anim time
SLBOX = [None]
# scene
""")
rep("""TMAP = []; ts = 0.0; tv = 0.0
while ts < T_F - 1e-9:
    TMAP.append(ts); rate = 1 if tv < A_SPR else 1 + (R_SPR - 1) * min(1, (tv - A_SPR) / 0.5); ts = min(T_F, ts + rate / FPS); tv += 1 / FPS""",
"""# n14: tighten dead time: the quiet stretches between powers (no stamp on screen, no power firing) run at R_Q x (sim unchanged, smooth 0.2s ramps)
R_Q = float(os.environ.get('RQ', '1.7')); QUIET = [(1.15, 2.15), (4.45, 5.15), (6.5, 7.25)]
def qrate(ts):
    w = 0.0
    for a, b in QUIET:
        if a <= ts <= b: w = max(w, min(1, (ts - a) / 0.2, (b - ts) / 0.2))
    return 1 + (R_Q - 1) * w
TMAP = []; ts = 0.0; tv = 0.0
while ts < T_F - 1e-9:
    TMAP.append(ts); rate = qrate(ts) if ts < A_SPR else 1 + (R_SPR - 1) * min(1, (ts - A_SPR) / 0.5); ts = min(T_F, ts + rate / FPS); tv += 1 / FPS
def s2v(t0):   # sim time -> video time (for the sfx events)
    import bisect
    return bisect.bisect_left(TMAP, t0) / FPS""")
rep("HOLD = 1.4                                    # photo finish freeze",
"""# n14 photo-finish beats (s after the finish frame): zoom in on the wall, CLEO WINS!, slide back along her lane, the slime surfaces + heart
P_ZOOM, P_WIN, P_SLIDE0, P_SLIDE1, P_RISE0, P_RISE1, P_HEART, P_END = 0.35, 0.75, 1.2, 1.8, 1.85, 2.2, 2.15, float(os.environ.get('PEND', '3.5'))""")
rep("CARD = float(os.environ.get('CARD', '1.5'))\nEND = T_FV + HOLD + CARD", "END = T_FV + P_END")
rep("add_stamp(e[0], e[2], POWER[e[3]][0], POWER[e[3]][1]); ev.append((round(e[0], 3), SFX[e[3]]))",
    "add_stamp(e[0], e[2], POWER[e[3]][0], POWER[e[3]][1]); ev.append((round(s2v(e[0]), 3), SFX[e[3]]))")
rep("add_stamp(e[0], e[2], 'BONK!', (255, 255, 255)); ev.append((round(e[0], 3), 'punch'))",
    "add_stamp(e[0], e[2], 'BONK!', (255, 255, 255)); ev.append((round(s2v(e[0]), 3), 'punch'))")
rep("add_stamp(e[0], e[2], 'BLOCKED!', (150, 255, 120)); ev.append((round(e[0], 3), 'boing'))",
    "add_stamp(e[0], e[2], 'BLOCKED!', (150, 255, 120)); ev.append((round(s2v(e[0]), 3), 'boing'))")
rep("""    for n in NAMES:
        r = st[n]; moving = r['fin'] is None and t_sim >= r['sleep']""",
"""    draw_slime(img, st, t_sim, t_anim)
    for n in NAMES:
        r = st[n]; moving = r['fin'] is None and t_sim >= r['sleep']""")
rep("OPEN = []\ndef scene(", '''CI = NAMES.index('cleo')
T_TURN = next((k / FPS for k, st_ in enumerate(FR) if st_['cleo']['s'] >= LEN), 99)
def draw_slime(img, st, t_sim, t_anim):
    """the slime rides right behind Cleo's feet, under the water (same waterline split + tint as the swimmers' submerged half).
    At her turn it slides under her to the new trailing side over 0.4s (no teleport)."""
    s_ = st['cleo']['s']; x, d = xpos(s_); y = LANEY[CI]; bob = 4 * math.sin(t_anim * 6 + CI)
    sw = SWIM['cleo'][0].width
    u = (t_sim - T_TURN) / 0.4; side = 1.0 if u <= 0 else (-1.0 if u >= 1 else 1 - 2 * (0.5 - 0.5 * math.cos(math.pi * u)))
    ta = REV['ta'] if REV['ta'] is not None else t_anim
    fr = SLIME[int(ta * 9) % len(SLIME)]
    if side < 0: fr = fr.transpose(Image.FLIP_LEFT_RIGHT)
    cx = x - side * (sw * 0.5 + fr.width * 0.18)
    wl = int(y + 6 + bob)
    top = int(wl + 6 - REV['rise'] * fr.height * 0.62); left = int(cx - fr.width / 2)
    cut = wl - top
    a = fr.getchannel('A'); fr2 = fr.copy(); a2 = a.point(lambda p: int(p * SL_ALPHA))
    if cut > 0: a2.paste(a.crop((0, 0, fr.width, min(cut, fr.height))), (0, 0))
    fr2.putalpha(a2)
    tint = Image.new('RGBA', fr.size, (40, 130, 210, 0)); ta_ = a.copy()
    if cut > 0: ta_.paste(0, (0, 0, fr.width, min(cut, fr.height)))
    tint.putalpha(ta_.point(lambda p: int(p * 0.5 * SL_ALPHA))); fr2.alpha_composite(tint)
    img.alpha_composite(fr2, (left, top))
    if REV['rise'] > 0:
        layer(img, lambda dd: dd.arc([left - 14, wl - 10, left + fr.width + 14, wl + 22], 200, 340, fill=(220, 245, 255, int(200 * REV['rise'])), width=4))
    SLBOX[0] = (left, top, left + fr.width, top + fr.height)
OPEN = []
def scene(''')
old_start = s.index("for f in range(int(END * FPS)):")
old_end = s.index("    img.alpha_composite(HOOK)\n    if STILLS:")
new_loop = '''def heart(d, cx, cy, s, col=(255, 90, 140)):   # pixel heart emote (same as fork_n7/render_race4.py)
    for (x, y) in [(-2, -1), (-1, -2), (1, -2), (2, -1), (-2, 0), (-1, -1), (0, -1), (1, -1), (2, 0), (-1, 0), (0, 0), (1, 0), (-1, 1), (0, 1), (1, 1), (0, 2), (-2, -1)]:
        d.rectangle([cx + x * s - s // 2, cy + y * s - s // 2, cx + x * s + s // 2 - 1, cy + y * s + s // 2 - 1], fill=col)
def ease(q): q = max(0.0, min(1.0, q)); return 0.5 - 0.5 * math.cos(math.pi * q)
for f in range(int(round(END * FPS))):
    t = f / FPS
    frozen = f >= NRACE
    t_sim = TMAP[f] if not frozen else T_F
    u = t - T_FV
    if frozen:
        REV['rise'] = ease((u - P_RISE0) / (P_RISE1 - P_RISE0)); REV['ta'] = T_F + max(0.0, u - P_SLIDE1)   # the slime comes alive once the camera lands on it
    img, st = scene(t_sim, t_sim)
    for n in NAMES:
        r = st[n]
        if r['s'] >= LEN and n not in seen_turn: seen_turn.add(n); ev.append((round(t, 3), 'swish'))
    if frozen:
        # photo finish: zoom on the finish wall around the two leaders, then the camera slides back along Cleo's lane to her feet
        ys = [LANEY[NAMES.index(win)], LANEY[NAMES.index(second)]]; cyA = (ys[0] + ys[1]) / 2
        BX0, BY0, BX1, BY1 = 0, int(LY0 - 40), W, 1500; bw, bh = BX1 - BX0, BY1 - BY0
        sl = SLBOX[0]; scx, scy = (sl[0] + sl[2]) / 2, (sl[1] + sl[3]) / 2
        ZB = float(os.environ.get('ZB', '3.0'))
        k = ease((u - P_SLIDE0) / (P_SLIDE1 - P_SLIDE0))
        z = (1 + 0.9 * min(1, u / P_ZOOM)) * (1 - k) + ZB * k
        cw, ch = bw / z, bh / z
        xA = 0.0; xB = scx - 610 / ZB                     # slime lands right of centre, Cleo's legs on the left
        cy = cyA * (1 - k) + (LANEY[CI] + 10) * k
        x0 = max(0, min(W - cw, xA * (1 - k) + xB * k)); y0 = max(BY0, min(BY1 - ch, cy - ch / 2))
        zoom = img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((bw, bh), Image.NEAREST)
        img.paste(zoom, (BX0, BY0))
        if u < 0.12: layer(img, lambda d: d.rectangle([BX0, BY0, BX1, BY1], fill=(255, 255, 255, int(200 * (1 - u / 0.12)))))
        layer(img, lambda d: d.rectangle([BX0, BY0, BX1, BY1], outline=(255, 255, 255, 255), width=8))
        if u < P_WIN:
            text_layer(img, [(490, HB + 70, 'PHOTO FINISH!', 60, (255, 255, 255), 9, 255)])
        else:
            q = u - P_WIN; sc = 1 + 0.3 * max(0, 1 - q / 0.12)
            text_layer(img, [(490, HB + 70, LABEL[win] + ' WINS!', int(64 * sc), (255, 214, 60), 9, 255)])
        if u >= P_HEART:   # heart emote over the slime
            q = u - P_HEART; hx = BX0 + (scx - x0) * z; htop = BY0 + (sl[1] - y0) * z
            hy = htop - 60 - 40 * ease(q / 0.3); pop = 1 + 0.4 * max(0, 1 - q / 0.15)
            def hfn(d, hx=hx, hy=hy, s_=int(14 * pop)):
                heart(d, int(hx), int(hy), s_ + 4, (12, 8, 20)); heart(d, int(hx), int(hy), s_)
            layer(img, hfn)
        if not any(e[1] == 'ding_8bit' for e in ev): ev.append((round(T_FV, 3), 'ding_8bit'))
        if u >= P_WIN and not any(e[1] == 'victory' for e in ev): ev.append((round(t, 3), 'victory'))
        if u >= P_SLIDE0 and not any(e[1] == 'whoosh_8bit' for e in ev): ev.append((round(t, 3), 'whoosh_8bit'))
        if u >= P_RISE0 and not any(e[1] == 'jump' for e in ev): ev.append((round(t, 3), 'jump'))
        if u >= P_HEART and not any(e[1] == 'chime' for e in ev): ev.append((round(t, 3), 'chime'))
    if T_GO <= t < T_GO + 0.6:
        text_layer(img, [(490, 960, 'GO!', 130, (255, 214, 60), 10, 255)])
        if not any(e[1] == 'go_8bit' for e in ev): ev.append((round(T_GO, 3), 'go_8bit'))
'''
s = s[:old_start] + new_loop + s[old_end:]
s = s.replace("VF = vic(win, 360)\n", "")
open(p, 'w').write(s)
print('ok')
