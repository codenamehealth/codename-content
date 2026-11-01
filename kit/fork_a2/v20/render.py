import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
from sim import play, dist, N
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 79
WIN, LOG, LEFT = play(SEED)
G = '../gen/'
def pk(k, i): return crop(Image.open(f'{G}{k}/{i:02d}.png').convert('RGBA'))
TL = up(pk('floor', 4), 3); TD = up(pk('floor', 12), 3)
TL = TL.resize((96, 96), Image.NEAREST); TD = TD.resize((96, 96), Image.NEAREST)
WA = pk('wall_amber', 2); WV = pk('wall_violet', 2)
def wall_spr(im, o):
    s = im.resize((206, max(1, int(im.height * 206 / im.width))), Image.NEAREST)
    return s if o == 'h' else s.transpose(Image.ROTATE_90)
WS = {('cyrus', 'h'): wall_spr(WA, 'h'), ('cyrus', 'v'): wall_spr(WA, 'v'), ('hollow', 'h'): wall_spr(WV, 'h'), ('hollow', 'v'): wall_spr(WV, 'v')}
ICONW = {'cyrus': up(Image.open(PL + 'gummies/pick_mush.png').convert('RGBA'), 1.25), 'hollow': up(Image.open(PL + 'gummies/pick_gold.png').convert('RGBA'), 1.25)}
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
CS = 104; X0 = (W - N * CS) // 2 + 4; Y0 = 470
def cell_c(r, c): return X0 + c * CS + 48, Y0 + r * CS + 48
BG = bg_frames('sun_hd.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.55, blur=3)
# board image
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
bd.rounded_rectangle([X0 - 26, Y0 - 26, X0 + N * CS + 18, Y0 + N * CS + 18], 18, fill=(46, 30, 22, 255), outline=(255, 214, 60, 255), width=5)
for r in range(N):
    for c in range(N):
        t = TL if (r + c) % 2 == 0 else TD
        BOARD.alpha_composite(t, (X0 + c * CS, Y0 + r * CS))
def tint_row(r, col):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(L).rectangle([X0, Y0 + r * CS, X0 + N * CS - 8, Y0 + r * CS + 95], fill=col)
    BOARD.alpha_composite(L)
tint_row(0, (170, 90, 255, 70)); tint_row(N - 1, (255, 150, 40, 70))
GG = gummy('gold', 2); GM = gummy('mush', 2)
for c in range(N):
    if c % 2 == 0:
        BOARD.alpha_composite(up(Image.open(PL + 'gummies/pick_gold.png').convert('RGBA'), 1), (X0 + c * CS + 34, Y0 + 6))
        BOARD.alpha_composite(up(Image.open(PL + 'gummies/pick_mush.png').convert('RGBA'), 1), (X0 + c * CS + 36, Y0 + (N - 1) * CS + 62))
SRUN_H = seq(PL + 'maze/anim/hollow_srun'); SRUN_C = seq(PL + 'race/cyrus_run')
FRUN = {g: seq(PL + f'maze/anim/{g}_frun') for g in ('hollow', 'cyrus')}
IDL = {'hollow': idle('hollow', 2), 'cyrus': idle('cyrus', 2)}
ATK = seq(PL + 'race/cyrus_atk')          # 128 canvas, offset vs run canvas
FOOTY = 78 * 2
ICON = {}
for g, src in (('hollow', 'hollow/char1.png'), ('cyrus', 'char4/char9.png')):
    im = Image.open(SP + 'syeda_src/' + src).convert('RGBA'); bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    ICON[g] = up(im.crop((cx - 16, 10, cx + 16, 42)), 3)
VICF = vic('hollow', 380)
# ---------------- timeline
TD_ = 0.47; T0 = 2.3
state = {'hollow': (N - 1, 4), 'cyrus': (0, 4)}; walls = []; left = {'hollow': 7, 'cyrus': 7}
steps = []   # per turn: dict snapshot before + event
for i, e in enumerate(LOG):
    steps.append((dict(state), list(walls), dict(left), e))
    if e[0] == 'move': state[e[1]] = e[3]
    elif e[0] == 'wall': walls.append((e[1], e[2])); left[e[1]] -= 1
FINAL = (dict(state), list(walls), dict(left))
T_END = T0 + len(LOG) * TD_; DUR = T_END + 3.6
face = {'hollow': 1, 'cyrus': 1}
wr = Writer('v20_noaudio.mp4'); events = []; F_ = 0
def distances(st, ws):
    wset = set(w for _, w in ws)
    return dist(st['hollow'], 0, wset), dist(st['cyrus'], N - 1, wset)
for f in range(int(DUR * FPS)):
    t = f / FPS
    k = int((t - T0) // TD_) if t >= T0 else -1
    u = ((t - T0) % TD_) / TD_ if k >= 0 else 0
    if k >= len(LOG): st, ws, lf = FINAL; ev = None; u = 1
    elif k >= 0: st, ws, lf, ev = steps[k]
    else: st, ws, lf = steps[0][0], [], {'hollow': 7, 'cyrus': 7}; ev = None
    shake = 0
    if ev and ev[0] == 'wall' and 0.25 < u < 0.45: shake = int(6 * math.sin(u * 90))
    img = BG[int(t * 6) % len(BG)].copy()
    img.alpha_composite(BOARD, (0, shake))
    # walls (placed) + the one being placed this turn
    for who, w in ws:
        r, c, o = w; s = WS[(who, o)]; cx, cy = X0 + (c + 1) * CS - 4, Y0 + (r + 1) * CS - 4 + shake
        img.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
    if ev and ev[0] == 'wall':
        who, w = ev[1], ev[2]; r, c, o = w; s = WS[(who, o)]; cx, cy = X0 + (c + 1) * CS - 4, Y0 + (r + 1) * CS - 4 + shake
        g = min(1, u / 0.3)
        if o == 'h': s2 = s.resize((max(1, int(s.width * (0.3 + 0.7 * g))), max(1, int(s.height * g))), Image.NEAREST)
        else: s2 = s.resize((max(1, int(s.width * g)), max(1, int(s.height * (0.3 + 0.7 * g)))), Image.NEAREST)
        img.alpha_composite(s2, (int(cx - s2.width / 2), int(cy - s2.height / 2)))
        if 0.28 < u < 0.95:
            v = (u - 0.28) / 0.67; dsz = up(DUST, 1.6 + 1.2 * v); al = dsz.getchannel('A').point(lambda p: int(p * (1 - v))); dsz.putalpha(al)
            img.alpha_composite(dsz, (int(cx - dsz.width / 2), int(cy - dsz.height / 2)))
        if abs(u - 0.3) < 0.5 / (TD_ * FPS) or (u >= 0.3 and not any(abs(x[0] - (T0 + k * TD_ + 0.3 * TD_)) < 0.01 for x in events)):
            events.append((round(T0 + k * TD_ + 0.3 * TD_, 3), 'sword_hit'))
    # pawns
    order = sorted(['hollow', 'cyrus'], key=lambda g: st[g][0])
    for g in order:
        r, c = st[g]; x, y = cell_c(r, c); spr = None
        if ev and ev[0] == 'move' and ev[1] == g:
            (r0, c0), (r1, c1) = ev[2], ev[3]; x0, y0 = cell_c(r0, c0); x1, y1 = cell_c(r1, c1)
            uu = min(1, u / 0.8); x, y = x0 + (x1 - x0) * uu, y0 + (y1 - y0) * uu
            if c1 != c0: face[g] = 1 if c1 > c0 else -1
            ph = int(uu * 8) % 8
            if r1 > r0: spr = FRUN[g][ph]
            else:
                rs = SRUN_H if g == 'hollow' else SRUN_C; spr = rs[ph] if face[g] > 0 else rs[ph].transpose(Image.FLIP_LEFT_RIGHT)
            if uu >= 1: spr = None
        if ev and ev[0] == 'wall' and ev[1] == g and g == 'cyrus' and u < 0.9:
            a = ATK[min(len(ATK) - 1, int(u / 0.9 * len(ATK)))]
            img.alpha_composite(a, (int(x - 92 - 28 + 0), int(y + 30 - FOOTY - 52 + shake)))
            continue
        if spr is None: spr = IDL[g][int(t * 8) % len(IDL[g])]
        layer(img, lambda d, x=x, y=y: d.ellipse([x - 30, y + 22, x + 30, y + 38], fill=(0, 0, 0, 90)))
        if g == 'hollow' and ev and ev[0] == 'wall' and ev[1] == 'hollow' and u < 0.6:
            layer(img, lambda d, x=x, y=y, u=u: d.ellipse([x - 50 - 30 * u, y - 60 - 30 * u, x + 50 + 30 * u, y + 40 + 30 * u], outline=(190, 120, 255, int(200 * (1 - u))), width=6))
        img.alpha_composite(spr, (int(x - spr.width / 2), int(y + 30 - FOOTY + shake)))
    # BLOCKED popup on the opponent
    pops = []
    if ev and ev[0] == 'wall' and u > 0.3:
        op = 'hollow' if ev[1] == 'cyrus' else 'cyrus'; ox, oy = cell_c(*st[op]); a = int(255 * min(1, (1 - u) / 0.3))
        pops.append((ox, oy - 150 - 30 * u, 'BLOCKED!', 30, (255, 90, 90), 5, a))
        if ev[3] >= 2: pops.append((ox, oy - 110 - 30 * u, f'+{ev[3]} STEPS', 24, (255, 255, 255), 4, a))
    # HUD
    layer(img, lambda d: (d.rectangle([0, 0, W, 430], fill=(10, 8, 20, 150)), d.rounded_rectangle([24, 214, W // 2 - 12, 410], 18, fill=(20, 14, 34, 220), outline=(180, 120, 255, 255), width=4),
                          d.rounded_rectangle([W // 2 + 12, 214, W - 24, 410], 18, fill=(20, 14, 34, 220), outline=(255, 160, 40, 255), width=4)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 56, 'NEVER GIVE UP', F(78), (255, 214, 60), 8)
    ctext(d, W / 2, 158, 'First across the board wins', F(26), (235, 235, 235), 4)
    dh, dc = distances(st, ws)
    for g, x0_, nm, col in (('hollow', 40, 'THE HOLLOW', (200, 150, 255)), ('cyrus', W // 2 + 28, 'CYRUS', (255, 180, 80))):
        img.alpha_composite(ICON[g], (x0_ + 6, 232)); d = ImageDraw.Draw(img)
        d.text((x0_ + 116, 240), nm, font=F(26), fill=col, stroke_width=4, stroke_fill=(20, 15, 35))
        d.text((x0_ + 116, 284), f'{dh if g == "hollow" else dc} STEPS LEFT', font=F(20), fill=(240, 240, 240), stroke_width=3, stroke_fill=(20, 15, 35))
        for i in range(7):
            ic = ICONW[g]; ix = x0_ + 18 + i * 66; iy = 352
            if i < lf[g]: img.alpha_composite(ic, (ix + (40 - ic.width) // 2, iy + (40 - ic.height) // 2 - 4))
            else: layer(img, lambda dd, ix=ix, iy=iy: dd.ellipse([ix + 6, iy + 2, ix + 34, iy + 30], outline=(110, 100, 130, 200), width=3))
    d = ImageDraw.Draw(img)
    if t < T0 + 0.5: pops.append((W / 2, Y0 + N * CS + 90, 'PICK A SIDE!', 52, (255, 255, 255), 8, 255))
    else: pops.append((W / 2, Y0 + N * CS + 100, 'Every wall costs a gummy', 26, (255, 230, 170), 4, 255))
    text_layer(img, pops)
    if t >= T_END:
        uu = t - T_END; a = min(1, uu / 0.35)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(160 * a))))
        vf = VICF[int(uu * 8) % len(VICF)]; img.alpha_composite(vf, (W // 2 - vf.width // 2, 1180 - vf.height))
        g2 = up(Image.open(PL + 'gummies/pick_gold.png').convert('RGBA'), 3); bob = int(8 * math.sin(uu * 5))
        img.alpha_composite(g2, (W // 2 + 150, 820 + bob))
        text_layer(img, [(W / 2, 1230, 'THE HOLLOW WINS!', 58, (255, 214, 60), 8, 255), (W / 2, 1320, 'He never gave up', 30, (255, 255, 255), 5, int(255 * a))])
        if not any(e[1] == 'victory' for e in events): events.append((round(T_END, 3), 'victory'))
    if ev and ev[0] == 'move' and u < 0.05 and not any(abs(e[0] - (T0 + k * TD_)) < 0.01 for e in events):
        events.append((round(T0 + k * TD_, 3), 'tick_8bit'))
    wr.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p_{f:04d}.png')
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': events}, open('v20_events.json', 'w'))
print('winner', WIN, 'turns', len(LOG), 'dur', round(DUR, 1))
