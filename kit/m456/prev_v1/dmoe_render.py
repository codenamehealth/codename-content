# m05 DMOEx9VvQTm recreation: render. usage: SPD=200 python3 dmoe_render.py SEED [stills]
import sys, os, json, math, random
from dmoe_map import *
from rlib import *
FPS = 30
SEED = int(sys.argv[1])
R = run(SEED, dur=float(os.environ.get('DUR', '80')))
FR, EV, WIN = R['frames'], R['ev'], R['win']
T_WIN, WINNER = WIN
T_CARD = T_WIN + 0.5; T_END = T_CARD + float(os.environ.get('HOLD', '2.5')); NF = int(round(T_END * FPS))
print('win', WIN, 'end', round(T_END, 2), 'frames', NF)
def fidx(t): return min(max(0, int(round(t * FPS))), len(FR) - 1)
def frame_at(t): return FR[fidx(t)]
OUTS = {g: R['X'][g]['out'] for g in G}
HOOK, HB = hook_fade(os.environ.get('HOOK', 'WHO OUTRUNS|THE WATER?').split('|'), accent=1)
MX0, MY0, MX1, MY1 = OX, OY, OX + COLS * C, OY + ROWS * C
RY0 = MY1 + 12
BG = checker_bg((70, 26, 26), (58, 20, 20), 60); BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (0, 0, 0, 70)))
WALLC = (178, 66, 56); RIM = (110, 34, 30); HI = (222, 118, 98)
def isw(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or Wd.wall[r, c]
floor_mask = Image.new('L', (W, H), 0); fd = ImageDraw.Draw(floor_mask)
for r in range(ROWS):
    for c in range(COLS):
        if not Wd.wall[r, c] or Wd.haz[r, c]: fd.rectangle([OX + c * C, OY + r * C, OX + c * C + C - 1, OY + r * C + C - 1], fill=255)
for p in PENCILS: fd.rectangle([OX + (p['x0'] + 2) * C, OY + p['row'] * C, OX + p['x1'] * C - 1, OY + (p['row'] + 1) * C - 1], fill=255)   # the slot behind the pencil is floor
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
bd.rounded_rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], 10, fill=(40, 12, 12, 255), outline=(26, 8, 8, 255), width=4)
bd.rectangle([MX0, MY0, MX1 - 1, MY1 - 1], fill=WALLC + (255,))
FL = floor_layer(None, MX0, MY0, MX1, MY1, tones=[(236, 222, 190), (228, 212, 178)])
BOARD.paste(FL, (0, 0), floor_mask); bd = ImageDraw.Draw(BOARD)
def solid_vis(r, c):
    if r < 0 or c < 0 or r >= ROWS or c >= COLS: return True
    if Wd.haz[r, c]: return False
    for p in PENCILS:
        if r == p['row'] and p['x0'] <= c < p['x1']: return False
    return bool(Wd.wall[r, c])
for r in range(ROWS):
    for c in range(COLS):
        if not solid_vis(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        if not solid_vis(r + 1, c): bd.rectangle([x0, y0 + C - 3, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
        if not solid_vis(r - 1, c): bd.rectangle([x0, y0, x0 + C - 1, y0 + 2], fill=HI + (255,))
        if not solid_vis(r, c - 1): bd.rectangle([x0, y0, x0 + 2, y0 + C - 1], fill=RIM + (255,))
        if not solid_vis(r, c + 1): bd.rectangle([x0 + C - 3, y0, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
EX0, EY0, EX1, EY1 = Wd.px(85, 1, 89, 6)                            # exit: green block over a checkered slot
bd.rectangle([EX0, EY0, EX1 - 1, EY0 + 2 * C - 1], fill=(96, 226, 100, 255)); bd.rectangle([EX0, EY0, EX1 - 1, EY0 + 2 * C - 1], outline=(30, 110, 40, 255), width=3)
for i in range(3):
    for j in range(EX1 - EX0 >> 3):
        bd.rectangle([EX0 + j * 8, EY0 + 2 * C + i * 7, EX0 + j * 8 + 7, EY0 + 2 * C + i * 7 + 6], fill=(240, 240, 240, 255) if (i + j) % 2 == 0 else (24, 24, 30, 255))
def pencil_img(p, cap):
    x0 = OX + p['x0'] * C; x1 = OX + p['x1'] * C; y0 = OY + p['row'] * C; h = C
    im = Image.new('RGBA', (x1 - x0 + 14, h + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im); oy = 3
    d.polygon([(0, oy + h // 2), (2 * C, oy - 1), (2 * C, oy + h)], fill=(214, 168, 112, 255)); d.polygon([(0, oy + h // 2), (7, oy + h // 2 - 3), (7, oy + h // 2 + 3)], fill=(40, 36, 44, 255))
    d.rectangle([2 * C, oy - 1, x1 - x0 - 12, oy + h], fill=(250, 206, 50, 255)); d.rectangle([2 * C, oy + h // 2 - 1, x1 - x0 - 12, oy + h // 2], fill=(214, 160, 30, 255))
    d.rectangle([x1 - x0 - 12, oy - 1, x1 - x0 - 6, oy + h], fill=(190, 190, 200, 255)); d.rectangle([x1 - x0 - 6, oy - 1, x1 - x0 + 4, oy + h], fill=cap + (255,))
    d.rectangle([0, oy - 1, x1 - x0 + 4, oy + h], outline=None)
    return im, (x0, y0 - oy)
CAPS = [(255, 140, 170), (170, 110, 240), (90, 170, 255), (110, 210, 120), (250, 200, 70)]
WATER = (34, 92, 190)
BOXI = {g: box_img(g, 2 * HS) for g in G}; XBOX = {g: box_img(g, 2 * HS, x_mark=True) for g in G}
VIC_W = vic_frames(WINNER, 5)
def draw(f):
    t = f / FPS; st, tau, hp, gm = frame_at(t)
    img = BG.copy(); img.alpha_composite(BOARD)
    cap = CAPS[int(t / 2.0) % len(CAPS)]
    for p in PENCILS:
        pim, pos = pencil_img(p, cap); img.alpha_composite(pim, pos)
    for g in G:                                                        # trails
        x, y, vx, vy, out, won = st[g]
        if out is not None or (won is not None and t >= T_CARD): continue
        for q in range(1, 6):
            s0 = frame_at(max(0, t - q * 0.033))[0][g]
            if s0[4] is not None: continue
            a_ = 90 - q * 15; s_ = int(HS * (1 - q * 0.11))
            layer(img, lambda dd, px_=s0[0], py_=s0[1], a_=a_, s_=s_, g=g: dd.rectangle([px_ - s_, py_ - s_, px_ + s_, py_ + s_], fill=COL[g] + (a_,)))
    for g in G:
        x, y, vx, vy, out, won = st[g]
        if out is not None and out <= t: continue
        if won is not None and t >= T_CARD: continue
        img.alpha_composite(BOXI[g], (int(round(x - HS)), int(round(y - HS))))
    # water (only over the open floor), surface line with a gentle ripple
    wy = None
    for (x0, y0, x1, y1, d) in Wd.flood_rects(tau): wy = y0
    if wy is not None:
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle([MX0, int(wy), MX1, MY1], fill=215); m = ImageChops.multiply(m, floor_mask)
        L = Image.new('RGBA', (W, H), WATER + (255,)); img.paste(Image.alpha_composite(img, L), (0, 0), m)
        sl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sl)
        for xx in range(MX0, MX1, 6):
            yy = wy + 2 * math.sin(xx * 0.05 + t * 3); sd.rectangle([xx, yy - 2, xx + 5, yy + 2], fill=(150, 205, 255, 230))
        sm = Image.new('L', (W, H), 0); ImageDraw.Draw(sm).rectangle([MX0, int(wy) - 5, MX1, int(wy) + 5], fill=255); sm = ImageChops.multiply(sm, floor_mask)
        img.paste(Image.alpha_composite(img, sl), (0, 0), sm)
    for g in G:                                                        # pencil victims: frozen X marker (drawn over the water, like the reference)
        x, y, vx, vy, out, won = st[g]
        if out is None or out > t: continue
        img.alpha_composite(XBOX[g], (int(round(x - HS)), int(round(y - HS))))
        if t - out < 0.45: burst(img, x, y, (t - out) / 0.45, COL[g], hash(g) % 1000, n=12, R=80)
    roster(img, RY0, OUTS, t, WINNER, T_WIN)
    if T_WIN <= t < T_CARD:
        u = (t - T_WIN) / 0.5; wx, wy_ = frame_at(T_WIN)[0][WINNER][:2]
        layer(img, lambda dd: dd.rectangle([wx - HS - 6 - 40 * u, wy_ - HS - 6 - 40 * u, wx + HS + 6 + 40 * u, wy_ + HS + 6 + 40 * u], outline=(255, 214, 60, int(255 * (1 - u))), width=6))
    if t >= T_CARD:
        u = t - T_CARD; a_ = min(1, u / 0.3); wx, wy_ = frame_at(T_WIN)[0][WINNER][:2]
        layer(img, lambda dd: dd.rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], fill=(8, 6, 16, int(170 * a_))))
        vf = VIC_W[int(u * 8) % len(VIC_W)]; q = min(1.0, u / 0.3); sc = 0.25 + 0.75 * (1 - (1 - q) ** 3)
        vf2 = vf if sc >= 0.999 else vf.resize((max(2, int(vf.width * sc)), max(2, int(vf.height * sc))), Image.NEAREST)
        FEET = 1250; cxp = wx + (540 - wx) * q; cyp = wy_ + (FEET - wy_) * q
        img.alpha_composite(vf2, (int(cxp - vf2.width / 2), int(cyp - vf2.height * (78 / 92))))
        rs = random.Random(int(t * 6))
        layer(img, lambda dd: [sparkle(dd, 540 + rs.uniform(-220, 220), FEET - rs.uniform(60, 400), rs.choice([4, 6, 8]), int(255 * (0.5 + 0.5 * math.sin(t * 9 + i)))) for i in range(7)])
        fs = min(80, int(880 / (len(NAME[WINNER]) + 6)))
        text_layer(img, [(540, MY0 + 70, NAME[WINNER] + ' WINS!', fs, COL[WINNER], 10, int(255 * a_))])
    img.alpha_composite(HOOK)
    return img
STILLS = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else []
if STILLS:
    for x in STILLS: draw(int(round(x * FPS))).convert('RGB').save(f'sm_{x:.2f}.png')
    sys.exit()
OUTV = os.environ.get('OUTV', 'm05_noaudio.mp4'); wr = Writer(OUTV)
for f in range(NF): wr.write(draw(f))
wr.close()
out_ev = []; last = -9
for i, cf in enumerate(R['contacts']):
    t = i / FPS
    if any(cf.values()) and t - last > 0.3 and t < T_WIN: out_ev.append((round(t, 3), 'reeltick_8bit')); last = t
for e in EV:
    if e[1] == 'out' and e[0] < T_END: out_ev += [(round(e[0], 3), 'squish'), (round(e[0] + 0.03, 3), 'buzz_loud')]
out_ev += [(round(T_WIN, 3), 'win_sting'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(e for e in out_ev if e[0] < T_END - 0.1)
json.dump({'events': out_ev, 'end': T_END, 'beats': {'win': T_WIN, 'winner': WINNER, 'card': T_CARD, 'end': T_END, 'outs': OUTS}}, open('m05_events.json', 'w'), indent=1)
print('done', NF)
