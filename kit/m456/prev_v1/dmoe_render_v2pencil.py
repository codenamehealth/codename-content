# m06 DMOEx9VvQTm recreation: render. usage: python3 dmoe_render.py SEED [stills t1,t2,..]
import sys, os, json, math, random
from dmoe_map import *
from rlib import *
FPS = 30
SEED = sys.argv[1]
R = run(SEED, dur=float(os.environ.get('DUR', '80')))
FR, EV, WIN = R['frames'], R['ev'], R['win']
T_WIN, WINNER = WIN
T_CARD = T_WIN + 0.5; T_END = T_CARD + float(os.environ.get('HOLD', '2.5')); NF = int(round(T_END * FPS))
print('win', WIN, 'end', round(T_END, 2), 'frames', NF)
def fidx(t): return min(max(0, int(round(t * FPS))), len(FR) - 1)
def frame_at(t): return FR[fidx(t)]
OUTS = {g: (R['X'][g]['out'] if R['X'][g]['out'] is not None and R['X'][g]['out'] <= T_WIN else None) for g in G}   # the card freezes the board at T_CARD
MX0, MY0, MX1, MY1 = OX, OY, OX + COLS * C, OY + ROWS * C
BG = checker_bg((70, 26, 26), (58, 20, 20), 60); BG = Image.alpha_composite(BG, Image.new('RGBA', (W, H), (0, 0, 0, 70)))
WALLC = (178, 66, 56); RIM = (110, 34, 30); HI = (222, 118, 98)
def isw(r, c): return r < 0 or c < 0 or r >= ROWS or c >= COLS or Wd.wall[r, c]
floor_mask = Image.new('L', (W, H), 0); fd = ImageDraw.Draw(floor_mask)
for r in range(ROWS):
    for c in range(COLS):
        if not Wd.wall[r, c] or Wd.haz[r, c]: fd.rectangle([OX + c * C, OY + r * C, OX + c * C + C - 1, OY + r * C + C - 1], fill=255)
for p in PENCILS: fd.rectangle([OX + p['x0'] * C, OY + p['slot0'] * C, OX + p['x1'] * C - 1, OY + p['slot1'] * C - 1], fill=255)   # the slot behind the pencil is floor
# hook on the solid upper-left wall (soft fade masked off the floor); roster 2x2 on the same wall under it
HOOK, HB = hook_wall(os.environ.get('HOOK', 'WHO OUTRUNS|THE WATER?').split('|'), 420, 272, 60, floor_mask)
RSP = {'joy': (80, 446), 'cleo': (339, 446), 'cyrus': (80, 548), 'ray': (339, 548)}
BOARD = Image.new('RGBA', (W, H), (0, 0, 0, 0)); bd = ImageDraw.Draw(BOARD)
bd.rounded_rectangle([MX0 - 6, MY0 - 6, MX1 + 5, MY1 + 5], 10, fill=(40, 12, 12, 255), outline=(26, 8, 8, 255), width=4)
bd.rectangle([MX0, MY0, MX1 - 1, MY1 - 1], fill=WALLC + (255,))
FL = floor_layer(None, MX0, MY0, MX1, MY1, tones=[(236, 222, 190), (228, 212, 178)])
BOARD.paste(FL, (0, 0), floor_mask); bd = ImageDraw.Draw(BOARD)
def solid_vis(r, c):
    if r < 0 or c < 0 or r >= ROWS or c >= COLS: return True
    if Wd.haz[r, c]: return False
    for p in PENCILS:
        if p['slot0'] <= r < p['slot1'] and p['x0'] <= c < p['x1']: return False
    return bool(Wd.wall[r, c])
for r in range(ROWS):
    for c in range(COLS):
        if not solid_vis(r, c): continue
        x0, y0 = OX + c * C, OY + r * C
        if not solid_vis(r + 1, c): bd.rectangle([x0, y0 + C - 3, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
        if not solid_vis(r - 1, c): bd.rectangle([x0, y0, x0 + C - 1, y0 + 2], fill=HI + (255,))
        if not solid_vis(r, c - 1): bd.rectangle([x0, y0, x0 + 2, y0 + C - 1], fill=RIM + (255,))
        if not solid_vis(r, c + 1): bd.rectangle([x0 + C - 3, y0, x0 + C - 1, y0 + C - 1], fill=RIM + (255,))
EX0, EY0, EX1, EY1 = Wd.px(*EXIT)                                   # exit: green block over a checkered slot (reference: 60 green + 30 checker)
GH = 5 * C
bd.rectangle([EX0, EY0, EX1 - 1, EY0 + GH - 1], fill=(96, 226, 100, 255)); bd.rectangle([EX0, EY0, EX1 - 1, EY0 + GH - 1], outline=(30, 110, 40, 255), width=3)
for i in range((EY1 - EY0 - GH) // 10):
    for j in range((EX1 - EX0) // 10):
        bd.rectangle([EX0 + j * 10, EY0 + GH + i * 10, EX0 + j * 10 + 9, EY0 + GH + i * 10 + 9], fill=(240, 240, 240, 255) if (i + j) % 2 == 0 else (24, 24, 30, 255))
def pencil_img(p, cap):
    # tip cone over the hazard cells (4 cols), yellow body over the solid body cells, ferrule + eraser cap at the board edge
    x0 = OX + p['x0'] * C; x1 = OX + p['x1'] * C; y0 = OY + p['row0'] * C; h = (p['row1'] - p['row0']) * C; tl = 4 * C; L_ = x1 - x0
    im = Image.new('RGBA', (L_, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(0, h // 2), (tl, 0), (tl, h - 1)], fill=(150, 84, 34, 255), outline=(40, 22, 12, 255)); d.polygon([(0, h // 2), (11, h // 2 - 4), (11, h // 2 + 4)], fill=(40, 36, 44, 255))
    d.rectangle([tl, 0, L_ - 30, h - 1], fill=(222, 196, 40, 255)); d.rectangle([tl, h // 2 - 2, L_ - 30, h // 2 + 1], fill=(184, 156, 22, 255))
    d.rectangle([tl, 0, L_ - 30, h - 1], outline=(40, 30, 10, 255), width=2)
    d.rectangle([L_ - 30, 0, L_ - 20, h - 1], fill=(190, 190, 200, 255)); d.rectangle([L_ - 20, 0, L_ - 1, h - 1], fill=cap + (255,)); d.rectangle([L_ - 30, 0, L_ - 1, h - 1], outline=(30, 26, 34, 255), width=2)
    return im, (x0, y0)
CAPS = [(255, 140, 170), (170, 110, 240), (90, 170, 255), (110, 210, 120), (250, 200, 70)]
WATER = (34, 92, 190)
BOXI = {g: box_img(g, 2 * HS) for g in G}; XBOX = {g: box_img(g, 2 * HS, x_mark=True) for g in G}
VIC_W = vic_frames(WINNER, 5)
def draw(f):
    t = f / FPS; st, tau, hp, gm = frame_at(min(t, T_CARD))   # board frozen under the winner card
    img = BG.copy(); img.alpha_composite(BOARD)
    cap = CAPS[int(t / 2.0) % len(CAPS)]
    for p in PENCILS:
        pim, pos = pencil_img(p, cap); img.alpha_composite(pim, pos)
    trails(img, FR, fidx(min(t, T_CARD)), G, HS, lambda g: st[g][4] is None and st[g][5] is None, spd=SPD)   # solid colour trails, ~4 box lengths
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
    roster_at(img, RSP, OUTS, t, WINNER, T_WIN)
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
        text_layer(img, [(540, 680, NAME[WINNER] + ' WINS!', fs, COL[WINNER], 10, int(255 * a_))])
    img.alpha_composite(HOOK)
    return img
STILLS = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else []
if STILLS:
    for x in STILLS: draw(int(round(x * FPS))).convert('RGB').save(f'sm_{x:.2f}.png')
    sys.exit()
OUTV = os.environ.get('OUTV', 'm06_noaudio.mp4'); wr = Writer(OUTV)
for f in range(NF): wr.write(draw(f))
wr.close()
out_ev = []; last = -9
for i, cf in enumerate(R['contacts']):
    t = i / FPS
    if any(cf.values()) and t - last > 0.3 and t < T_WIN: out_ev.append((round(t, 3), tick_name(t))); last = t
for e in EV:
    if e[1] == 'out' and e[0] <= T_WIN: out_ev += [(round(e[0], 3), 'squish_ko'), (round(e[0] + 0.03, 3), 'buzz_ko')]   # KO SFX +8/+4 dB variants
out_ev += [(round(T_WIN, 3), 'win_sting'), (round(T_CARD, 3), 'victory'), (round(T_CARD + 0.1, 3), 'cheer')]
out_ev = sorted(e for e in out_ev if e[0] < T_END - 0.1)
json.dump({'events': out_ev, 'end': T_END, 'beats': {'win': T_WIN, 'winner': WINNER, 'card': T_CARD, 'end': T_END, 'outs': OUTS}}, open('m06_events.json', 'w'), indent=1)
print('done', NF)
