import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
from collections import deque
OUT = SP + 'fork_hfg10/v95/'
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
import hook as HK
# rc11 (review recut; Bennett loves #95, concept/beats kept): first ingredient on frame 0; B12 pill -> pink gummy; melatonin
# moon arcs up and fades before the right margin; ingredient icons 4x -> 5x; CHARM POWER label cut; comment prompt
# WOULD YOU TRY IT? as a 52px 3rd band line from frame 0 (the 38px end line cut); end hold 3.6 -> 1.5s then loop;
# ACV gummy gloss + 'ACV GUMMY' tag on the burst.
def band(lines, accent, sub, subsize=52, color=(255, 214, 60), subcol=(255, 255, 255)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 24; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
from hook import hook_fade; G = SP + 'fork_a10/gen/'
# hfg10: soft fade, no box; WOULD YOU TRY IT? moves out of the hook and replaces the hook text at the payoff (no CHARM COMPLETE! line)
HOOK, HB = hook_fade(["BUILD JOY'S", 'PERFECT CHARM'], accent=1, color=(140, 230, 90), size=64)
HOOK_END, _ = hook_fade(['WOULD YOU', 'TRY IT?'], accent=1, color=(140, 230, 90), size=64)
sys.path.insert(0, SP + 'fork_rc2'); from rc2 import gummy_src, acv_tag
K = 12  # potion native 54px -> 648
P0 = np.array(Image.open(SP + 'fork_a10/jar54.png').convert('RGBA'))
Hh, Ww = P0.shape[:2]
def isout(p): return p[3] > 200 and int(p[0]) < 40 and int(p[1]) < 40 and int(p[2]) < 40
def isg(p): return p[3] == 255 and int(p[1]) > int(p[0]) + 30 and int(p[1]) > int(p[2])
mask = np.zeros((Hh, Ww), bool); q = deque([(42, 27)]); mask[42, 27] = True
while q:
    y, x = q.popleft()
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = y + dy, x + dx
        if 24 <= ny < Hh and 0 <= nx < Ww and not mask[ny, nx] and P0[ny, nx, 3] > 0 and not isout(P0[ny, nx]):
            mask[ny, nx] = True; q.append((ny, nx))
over = P0.copy()
for y in range(24, Hh):
    for x in range(Ww):
        if mask[y, x] and isg(P0[y, x]): over[y, x] = (0, 0, 0, 0)
OVER = Image.fromarray(over)
rows = [y for y in range(Hh) if mask[y].any()]; BOT, TOPR = max(rows), 26
FULL = up(Image.fromarray(P0), K)
# ingredients
def item(name, i, k=5):
    if name == 'b12': return up(Image.open(OUT + 'b12_gummy.png').convert('RGBA'), 5)   # rc11: pink gummy, no pill
    return up(crop(Image.open(G + f'{name}/{i:02d}.png').convert('RGBA')), k)
ING = [('vinegar', 0, '+ACV COMPLEX', (214, 140, 40)), ('apple', 1, '+CRISP APPLE', (205, 45, 45)), ('beet', 2, '+BEET', (140, 25, 80)),
       ('moon', 1, 'MELATONIN?!', None), ('b12', 0, '+VITAMIN B12', (236, 110, 172)), ('folate', 1, '+FOLATE', (96, 176, 56)), ('cherry', 0, '+A LITTLE TART', (168, 28, 58))]
ITEMS = [item(n, i) for n, i, _, _ in ING]
BENCH = up(crop(Image.open(G + 'bench/03.png').convert('RGBA')), 4)
BGS = bg_frames('found_hd.gif', (W, H), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.9)
JOY_IDLE = idle('joy', 5)
CAST = seq(SP + 'fork_a3/joy_cast', 5, 1, None)
ATK = seq(PL + 'race/joy_atk', 5, 1, None)
VICJ = vic('joy', 400)
GUM = up(gummy_src('acv'), 4)
# layout
BX, BY = 650, 1745            # bench centre x, bench bottom y
BTOP = BY - int(BENCH.height * 0.52)     # table surface
PX = 660; PBOT = 1495            # potion stands on the forest floor
POT_Y = PBOT - (BOT + 1) * K; POT_X = PX - Ww * K // 2
NECK = (PX, POT_Y + 4 * K)
JX, JY = 300, 1490
T_ING0, SLOT = 0.0, 1.35
T_BREW = T_ING0 + 7 * SLOT; T_FLASH = T_BREW + 0.8; END = T_FLASH + 1.5
def liquid_img(levels, t):
    """levels: list of (color, rows_filled_float)"""
    L = np.zeros((Hh, Ww, 4), np.uint8); y0 = BOT + 1.0
    for li, (col, h) in enumerate(levels):
        y1 = y0 - h
        for y in range(Hh):
            if not mask[y].any(): continue
            for x in range(Ww):
                if not mask[y, x]: continue
                wav = 0.45 * math.sin(t * 7 + x * 0.6 + li) if li == len(levels) - 1 else 0
                if y + 0.5 >= y1 + wav and y + 0.5 < y0:
                    c = col
                    if y + 0.5 < y1 + wav + 1.0 and li == len(levels) - 1: c = tuple(min(255, int(v * 1.25 + 30)) for v in col)
                    elif int(y + 0.5) == int(y0 - 0.5): c = tuple(int(v * 0.8) for v in col)
                    L[y, x] = c + (255,)
        y0 = y1
    return Image.fromarray(L)
def potion(t, levels, glow=0.0):
    base = Image.new('RGBA', (Ww, Hh), (0, 0, 0, 0))
    gl = np.zeros((Hh, Ww, 4), np.uint8); gl[mask] = (210, 255, 210, 60); base.alpha_composite(Image.fromarray(gl))
    base.alpha_composite(liquid_img(levels, t))
    # bubbles
    if levels:
        top = BOT + 1 - sum(h for _, h in levels); bb = ImageDraw.Draw(base)
        for k in range(5):
            ph = (t * 0.9 + k * 0.37) % 1.0; yy = BOT - ph * (BOT - top); xx = 20 + (k * 7) % 14
            if top < yy < BOT and mask[int(yy), int(xx)]: bb.point((xx, int(yy)), fill=(255, 255, 255, 170))
    base.alpha_composite(OVER)
    im = up(base, K)
    if glow > 0:
        g = Image.new('RGBA', im.size, (255, 255, 200, 0)); a = im.getchannel('A').point(lambda p: int(p * glow * 0.6)); g.putalpha(a); im.alpha_composite(g)
    return im
def joy_feet(spr, x, y, k=5): return (int(x - spr.width / 2), int(y - 78 * k))
TAGK = int(os.environ.get('TAGK', '1')); ACVX, ACVY = 0, 0
w = Writer(OUT + 'noaudio.mp4'); ev = []
NF = int(END * FPS); filled = []
for f in range(NF):
    t = f / FPS
    img = BGS[int(t * 6) % len(BGS)].copy()
    # header band
    # power bar
    done = [i for i in range(7) if ING[i][3] and t >= T_ING0 + i * SLOT + 1.0]
    frac = len(done) / 6.0
    if t >= T_FLASH: frac = 1.0
    bx0, bx1, byy = 160, 940, HB + 26
    layer(img, lambda d2: d2.rectangle([bx0 - 6, byy - 6, bx1 + 6, byy + 42], fill=(20, 16, 30, 200)))   # hfg10: plain dark track, no gold box
    d = ImageDraw.Draw(img)
    if frac > 0: d.rectangle([bx0, byy, bx0 + int((bx1 - bx0) * frac), byy + 36], fill=(110, 200, 70))
    d.rectangle([bx0, byy, bx0 + int((bx1 - bx0) * frac), byy + 8], fill=(170, 240, 120)) if frac > 0 else None
    img.alpha_composite(up(Image.fromarray(P0), 1), (bx0 - 70, byy - 14))
    # bench + potion
    layer(img, lambda d2: d2.ellipse([PX - 250, PBOT - 30, PX + 250, PBOT + 26], fill=(0, 0, 0, 90)))
    levels = []
    for i in range(7):
        n, idx, lab, col = ING[i]
        if col is None: continue
        ts = T_ING0 + i * SLOT + 0.95
        if t >= ts: levels.append((col, 4.0 * min(1, (t - ts) / 0.4)))
    if t < T_FLASH:
        glow = max(0, (t - T_BREW) / 0.8) if t >= T_BREW else 0
        pim = potion(t, levels, glow)
        shake = int(4 * math.sin(t * 60)) if t >= T_BREW else 0
        img.alpha_composite(pim, (POT_X + shake, POT_Y))
    else:
        img.alpha_composite(FULL, (POT_X, POT_Y))
        u = t - T_FLASH
        if u < 0.5: layer(img, lambda d2: d2.rectangle([0, 0, W, H], fill=(255, 255, 230, int(255 * (1 - u / 0.5)))))
    # joy
    slot = int((t - T_ING0) // SLOT) if T_ING0 <= t < T_BREW else -1; st = (t - T_ING0) - slot * SLOT if slot >= 0 else 0
    if t >= T_FLASH:
        vf = VICJ[int((t - T_FLASH) * 8) % len(VICJ)]; img.alpha_composite(vf, (int(JX - vf.width / 2), JY - vf.height))
    elif slot == 3 and 0.3 <= st < 1.1:
        k = min(len(ATK) - 1, int((st - 0.3) / 0.8 * len(ATK))); fr = ATK[k]
        img.alpha_composite(fr, (int(JX - 64 * 5 + 14 * 5 + 20), int(JY - fr.height + 26 * 5 - 14 * 5 + 10)))
    elif slot >= 0 and ING[slot][3] and 0.3 <= st < 1.0 or (T_BREW <= t < T_FLASH):
        u = (st - 0.3) / 0.7 if slot >= 0 and t < T_BREW else ((t - T_BREW) / 0.8)
        fr = CAST[min(len(CAST) - 1, int(u * len(CAST)))]; img.alpha_composite(fr, joy_feet(fr, JX, JY))
    else:
        fr = JOY_IDLE[int(t * 8) % len(JOY_IDLE)]; img.alpha_composite(fr, joy_feet(fr, JX, JY))
    # ingredient in flight
    if slot >= 0:
        n, idx, lab, col = ING[slot]; it = ITEMS[slot]
        sx, sy = 760, HB + 260
        if st < 0.35:
            s = 0.3 + 0.7 * min(1, st / 0.2) + 0.12 * math.sin(st * 30) * (st < 0.3); x, y = sx, sy + 8 * math.sin(t * 6)
        elif col is not None and st < 0.95:
            u = (st - 0.35) / 0.6; u = u * u * (3 - 2 * u)
            x = sx + (NECK[0] - sx) * u; y = sy + (NECK[1] - sy) * u - 220 * math.sin(math.pi * u); s = 1 - 0.55 * u
        elif col is None and st < 0.6:
            x, y, s = sx, sy + 8 * math.sin(t * 6), 1.0
        elif col is None and st < 1.35:
            u = (st - 0.6) / 0.75; x, y, s = sx + 200 * u, sy - 120 * u + 260 * u * u, 1.0   # rc11: shorter fling, fades out before x~1000
        else: s = 0
        if s > 0:
            ii = it.resize((max(1, int(it.width * s)), max(1, int(it.height * s))), Image.NEAREST)
            if col is None and st >= 0.6:
                ii = ii.rotate(-(st - 0.6) * 900, expand=True); fa = max(0.0, min(1.0, (1.25 - st) / 0.5))
                ii.putalpha(ii.getchannel('A').point(lambda p_: int(p_ * fa)))
            # sparkle halo
            layer(img, lambda d2: d2.ellipse([x - 70 * s, y - 70 * s, x + 70 * s, y + 70 * s], fill=(255, 250, 200, 60)))
            img.alpha_composite(ii, (int(x - ii.width / 2), int(y - ii.height / 2)))
        # label
        if st < 1.25:
            a = int(255 * min(1, st / 0.15) * min(1, (1.25 - st) / 0.25))
            colr = (255, 230, 120) if col is not None else (200, 140, 255)
            text_layer(img, [(W / 2, HB + 92, lab, 46, colr, 7, a)])
        # hfg10: "THAT'S RAYLEIGH'S!" cut (MELATONIN?! + Joy flinging it away already lands the gag)
        # splash
        if col is not None and 0.95 <= st < 1.3:
            u = (st - 0.95) / 0.35
            def sp(d2):
                for k2 in range(8):
                    an = -math.pi / 2 + (k2 - 3.5) * 0.35; r = 30 + 90 * u
                    xx, yy = NECK[0] + r * math.cos(an), NECK[1] + r * math.sin(an) + 120 * u * u
                    d2.rectangle([xx - 8, yy - 8, xx + 8, yy + 8], fill=col + (int(255 * (1 - u)),))
            layer(img, sp)
        # events
        if abs(st - 0.0) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit'))
        if abs(st - 0.35) < 0.5 / FPS: ev.append((round(t, 3), 'chime' if col is not None else 'sword_swish'))
        if col is not None and abs(st - 0.95) < 0.5 / FPS: ev.append((round(t, 3), 'squish'))
        if col is None and abs(st - 0.6) < 0.5 / FPS: ev.append((round(t, 3), 'boing'))
    if abs(t - T_BREW) < 0.5 / FPS: ev.append((round(t, 3), 'powerup_8bit'))
    if abs(t - T_FLASH) < 0.5 / FPS: ev.append((round(t, 3), 'victory'))
    if t >= T_FLASH:
        u = t - T_FLASH
        # gummies burst out and settle on the bench / ground
        for k2 in range(8):
            an = -math.pi * (0.15 + 0.7 * k2 / 7); v = 520 + 60 * (k2 % 3)
            tt = min(u, 1.1); cx_ = math.cos(an); gx = PX + cx_ * v * tt * (0.42 if cx_ > 0 else 0.95); gx = max(70 + GUM.width / 2 + 4, min(882 - GUM.width / 2, gx)); gy = POT_Y + 260 - math.sin(-an) * v * tt + 900 * tt * tt
            gy = min(gy, 1470 - (k2 % 2) * 30); img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2)))
            if k2 == TAGK: ACVX, ACVY = gx, gy
        vf = VICJ[int((t - T_FLASH) * 8) % len(VICJ)]; img.alpha_composite(vf, (int(JX - vf.width / 2), JY - vf.height))  # Joy stays in front of the gummies
        a = int(255 * min(1, u / 0.3))
        # hfg10: CHARM COMPLETE! cut (the burst shows it; the end question replaces the hook) and the 'ACV GUMMY' tag cut (consistency rule)
        def conf(d2):
            rr = random.Random(f)
            for _ in range(36):
                cx_, cy_ = rr.uniform(0, W), (rr.uniform(-200, H) + u * 420) % H
                d2.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr.choice([(255, 214, 60), (110, 200, 70), (230, 90, 90), (255, 255, 255)]) + (220,))
        layer(img, conf)
    img.alpha_composite(HOOK_END if t >= T_FLASH else HOOK)
    w.write(img)
    if f in (0, 3, NF - 1, int((T_ING0 + 3 * SLOT + 0.9) * FPS), int((T_ING0 + 4 * SLOT + 0.2) * FPS), int(1.0 * FPS), int(2.6 * FPS), int(5.6 * FPS), int(9.6 * FPS), int((T_BREW + 0.5) * FPS), int((T_FLASH + 1.5) * FPS)): img.convert('RGB').save(OUT + f'k_{f:03d}.png')
w.close()
json.dump(ev, open(OUT + 'ev.json', 'w')); print('done', END, len(ev))
