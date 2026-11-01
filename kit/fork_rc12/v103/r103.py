# #103 Can the Hollow escape 200 rings (safe zone + hook + Bennett note: no full-size Hollow, his face in a marble)
# + gummy powers (SPEC 12): mushroom SPEED, creatine STRONG (smashes through rings), melatonin SLEEP (rings stop)
# rc12 review recut: rolling from frame 0, faster/wider-gap sim (escape ~14s, no counter stalls), each gummy visible ~0.7s on the
# marble's path before it fires, marble 1.5x (face 6x), 60px plate stamps, STRONG flames (no bubble), bigger Zzz/labels, YES OR NO prompt, 1.2s hold.
# usage: GAPDEG=110 SPD=1300 ALT=6 JIT=0.2 STRN=25 OMV=0 SPX=1.5 python3 r103.py SEED
import sys, os, math, random, json
import numpy as np
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP_ + 'fork1'); sys.path.insert(0, SP_ + 'pixellab/safezone'); sys.path.insert(0, SP_ + 'fork_rc12')
from rc12 import hook_layer2, plate
from common import *
from hook import hook_layer
OUTD = os.path.dirname(os.path.abspath(__file__)); os.chdir(OUTD)
import sim103 as S
SEED = int(sys.argv[1])
GT = [1.4, 3.4, 5.6, 7.8, 9.8, 11.6]; KD = ['mush', 'cre', 'mel', 'cre', 'mush', 'cre']   # no fixed repeating cycle
PRE, FR, EV, CB, T_ESC = S.place(SEED, GT, KD)
print('escape', round(T_ESC, 2), 'gums', [(round(e[0], 1), e[2]) for e in EV if e[1] == 'gum'])
CX, CY = 478, 1075; DS = S.DS; BALLR = int(S.BALLR)
HOOK, HB = hook_layer2(['CAN THE HOLLOW', 'ESCAPE?'], accent=1, sub='COMMENT YES OR NO')   # '200' lives in the RINGS LEFT counter
print('hook bottom', HB)
PANEL = (90, HB + 12, 866, HB + 132)
COLS = [(90, 200, 80), (255, 160, 40), (90, 150, 255), (190, 90, 240), (255, 214, 60)]
def ring_col(k):
    c = COLS[(k // 4) % 5]; lift = 30 if k % 2 else 0
    return tuple(min(255, v + lift) for v in c)
PCOL = {'mush': (255, 160, 40), 'cre': (90, 150, 255), 'mel': (190, 90, 240)}
PLAB = {'mush': 'SPEED!', 'cre': 'STRONG!', 'mel': 'SLEEP!'}
GUMS = {'mush': gummy('mush', 4), 'cre': gummy('cre', 4), 'mel': gummy('mel', 3)}
# --- Hollow face marble (Syeda's idle head, 3x, inside a glass marble)
HID = idle('hollow', 1)
def head(fr, k):
    bb = fr.getbbox(); top = bb[1]
    return up(fr.crop((33, top - 1, 62, top + 28)), k)
def marble(fr, r, hk):
    s = 2 * r + 8; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = s / 2
    d.ellipse([c - r, c - r, c + r, c + r], fill=(196, 182, 250, 255))
    d.ellipse([c - r * 0.8, c - r * 0.8, c + r * 0.8, c + r * 0.8], fill=(226, 218, 255, 255))
    h = head(fr, hk); im.alpha_composite(h, (int(c - h.width / 2), int(c - h.height / 2 + r * 0.06)))
    L = Image.new('RGBA', (s, s), (0, 0, 0, 0)); dl = ImageDraw.Draw(L)
    dl.ellipse([c - r, c - r, c + r, c + r], outline=(20, 12, 40, 255), width=max(4, r // 10))
    dl.ellipse([c - r + 4, c - r + 4, c + r - 4, c + r - 4], outline=(235, 225, 255, 230), width=max(3, r // 14))
    dl.ellipse([c - r * 0.62, c - r * 0.7, c - r * 0.3, c - r * 0.42], fill=(255, 255, 255, 210))
    dl.ellipse([c + r * 0.38, c + r * 0.38, c + r * 0.5, c + r * 0.5], fill=(255, 255, 255, 140))
    im.alpha_composite(L); return im
MARB = [marble(f, BALLR, 6) for f in HID]
BIG = [marble(f, 156, 9) for f in HID]
# --- starry cosmic background (glow centred on the field)
rng = random.Random(4)
yy, xx = np.mgrid[0:H, 0:W]; dd_ = np.hypot(xx - CX, yy - CY) / 900
bgarr = np.zeros((H, W, 3), np.float32)
bgarr[..., 0] = 30 + 40 * np.exp(-dd_ * 2); bgarr[..., 1] = 14 + 20 * np.exp(-dd_ * 2.5); bgarr[..., 2] = 50 + 70 * np.exp(-dd_ * 1.6)
BG = Image.fromarray(np.clip(bgarr, 0, 255).astype(np.uint8)).convert('RGBA')
STARS = [(rng.uniform(0, W), rng.uniform(0, H), rng.choice([2, 3, 4]), rng.uniform(0, 6.3)) for _ in range(150)]
parts = []; pops = []; waves = []; trail = []
ev_out = []; ev_i = 0
END = T_ESC + 1.2; NF = int(END * 30)
KEEP = {int(x) for x in os.environ.get('KEEP', '').split(',') if x}
wr = Writer(OUTD + '/noaudio.mp4')
def scr(x, y, scale): return CX + x * scale * DS, CY + y * scale * DS
for f in range(NF):
    t = f / 30; st = FR[min(f, len(FR) - 1)]; k = st['k']; b = st['b']; tr = st['tr']
    R = S.ring_r(min(k, S.NR - 1)); scale = S.scale_of(R)
    asleep = t < st['sl']; speedy = t < st['sp']; strong = t < st['st']
    img = BG.copy()
    layer(img, lambda d: [d.rectangle([sx, sy, sx + s, sy + s], fill=(255, 255, 255, max(0, int(120 + 120 * math.sin(t * 2 + ph))))) for (sx, sy, s, ph) in STARS])
    while ev_i < len(EV) and EV[ev_i][0] <= t:
        te, kind, val = EV[ev_i]; ev_i += 1
        if kind in ('break', 'smash'):
            rr = S.ring_r(val); col = ring_col(val) if kind == 'break' else (150, 200, 255)
            n = 14 if kind == 'break' else 5
            for q in range(n):
                a = q * 2 * math.pi / n + random.random() * 0.3
                parts.append([rr * math.cos(a), rr * math.sin(a), math.cos(a) * random.uniform(120, 340), math.sin(a) * random.uniform(120, 340), te, col, 6 if kind == 'break' else 8])
            ev_out.append((round(te, 3), 'brick_8bit' if kind == 'break' else 'crunch_8bit'))
        elif kind == 'gum':
            ev_out.append((round(te, 3), 'powerup_8bit'))
            bx, by = scr(b['x'], b['y'], scale)
            pops.append([te, val, bx, by])
            if val == 'mel': waves.append((te, bx, by)); ev_out.append((round(te + 0.05, 3), 'poof'))
            if val == 'cre': ev_out.append((round(te + 0.05, 3), 'punch'))
            if val == 'mush': ev_out.append((round(te + 0.05, 3), 'whoosh_8bit'))
        elif kind == 'escape':
            ev_out.append((round(te, 3), 'poofpops')); ev_out.append((round(te + 0.15, 3), 'victory'))
    # rings
    def rings(dd):
        lw = max(2, int(7 * scale))
        for j in range(k, S.NR):
            rr = S.ring_r(j) * scale * DS
            if rr > 1500: break
            g0 = math.degrees(S.gap_angle(j, tr)); gh = math.degrees(S.GAP) / 2
            col = ring_col(j)
            if asleep: col = tuple(int(v * 0.55 + c2 * 0.45) for v, c2 in zip(col, (150, 120, 220)))
            alpha = 255 if rr < 600 else int(255 * max(0, 1 - (rr - 600) / 500))
            dd.arc([CX - rr, CY - rr, CX + rr, CY + rr], g0 + gh, g0 - gh + 360, fill=col + (alpha,), width=lw)
            if lw >= 4:
                dd.arc([CX - rr + 1, CY - rr + 1, CX + rr - 1, CY + rr - 1], g0 + gh, g0 - gh + 360, fill=(255, 255, 255, alpha // 3), width=max(1, lw // 3))
    if k < S.NR: layer(img, rings)
    # sleep wave (purple ring expanding from the marble)
    for (tw, wx, wy) in waves:
        u = t - tw
        if 0 <= u < 0.6:
            r_ = 60 + 700 * u; a = int(200 * (1 - u / 0.6))
            layer(img, lambda d: d.ellipse([wx - r_, wy - r_, wx + r_, wy + r_], outline=(200, 140, 255, a), width=14))
    # shards
    def shards(dd):
        for p in parts:
            u = t - p[4]
            if u < 0 or u > 0.9: continue
            px = CX + (p[0] + p[2] * u / scale * 0.3) * scale * DS; py = CY + (p[1] + p[3] * u / scale * 0.3) * scale * DS + 200 * u * u
            s = p[6]; dd.rectangle([px - s, py - s, px + s, py + s], fill=p[5] + (int(255 * (1 - u / 0.9)),))
    layer(img, shards)
    parts = [p for p in parts if t - p[4] < 1.0]
    # Zzz on the sleeping rings
    if asleep and k < S.NR:
        rr = S.ring_r(k) * scale * DS
        zl = []
        for q in range(4):
            a = q * math.pi / 2 + 0.6; u = (t * 1.2 + q * 0.25) % 1
            zx = CX + (rr + 10) * math.cos(a) * 0.86; zy = CY + (rr + 10) * math.sin(a) * 0.86 - 50 * u
            zx = min(max(zx, 110), 840)
            zl += [(zx, zy, 'Z', 58, (220, 190, 255), 8, int(255 * (1 - u))), (zx + 46, zy - 46, 'z', 44, (220, 190, 255), 7, int(255 * (1 - u)))]
        text_layer(img, zl)
    # gummies
    for g in st['gums']:
        gs = GUMS[g['kind']]; gx, gy = scr(g['x'], g['y'], scale); gy += 6 * math.sin(t * 4)
        c = PCOL[g['kind']]; ua = t - g['t']; pz = min(1, ua / 0.12)
        if pz < 1: gs = gs.resize((max(1, int(gs.width * (0.5 + 0.5 * pz))), max(1, int(gs.height * (0.5 + 0.5 * pz)))), Image.NEAREST)
        rp = 62 + 14 * math.sin(t * 12)
        layer(img, lambda d: (d.ellipse([gx - rp, gy - rp, gx + rp, gy + rp], fill=c + (80,)), d.ellipse([gx - rp, gy - rp, gx + rp, gy + rp], outline=(255, 255, 255, 200), width=4)))
        img.alpha_composite(gs, (int(gx - gs.width / 2), int(gy - gs.height / 2)))
    # the Hollow marble
    if t < T_ESC:
        bx, by = scr(b['x'], b['y'], scale)
        trail.append((bx, by)); trail = trail[-6:]
        if speedy:
            vx, vy = b['vx'], b['vy']; px_, py_ = -vy, vx
            def lines(d):
                for q, off in enumerate((-36, -12, 12, 36)):
                    L0 = 70 + 40 * ((q + f) % 2)
                    x0, y0 = bx - vx * (BALLR + 6) + px_ * off, by - vy * (BALLR + 6) + py_ * off
                    d.line([x0, y0, x0 - vx * L0, y0 - vy * L0], fill=(255, 190, 90, 230), width=6)
                for i, (tx, ty) in enumerate(trail[:-1]):
                    s = 6 + i * 2; d.rectangle([tx - s, ty + BALLR - 10 - s, tx + s, ty + BALLR - 10 + s], fill=(230, 200, 150, 60 + 25 * i))
            layer(img, lines)
        if strong:                    # rc12: power flames around the marble (a blue bubble read like a shield)
            def flames(d):
                for q in range(14):
                    a_ = q * 0.4488 + t * 3; fl = 30 + 16 * math.sin(t * 18 + q * 1.7)
                    ux, uy = math.cos(a_), math.sin(a_); bx0, by0 = bx + ux * (BALLR + 4), by + uy * (BALLR + 4)
                    d.polygon([(bx0 - uy * 13, by0 + ux * 13), (bx0 + uy * 13, by0 - ux * 13), (bx0 + ux * fl, by0 + uy * fl)], fill=(255, 120 + 60 * (q % 2), 40, 220))
            layer(img, flames)
        m = MARB[int(t * 8) % len(MARB)]
        img.alpha_composite(m, (int(bx - m.width / 2), int(by - m.height / 2)))
        if asleep:
            pass
    # power pop labels (clamped inside the zone, under the counter panel)
    act = [p for p in pops if 0 <= t - p[0] < 1.0 and t < T_ESC]
    for (tp, kind, px, py) in act[-1:]:          # one stamp at a time (newest wins)
        u = t - tp; px, py = scr(b['x'], b['y'], scale)
        ly = py - BALLR - 110
        if ly < PANEL[3] + 16: ly = py + BALLR + 30
        plate(img, px, min(ly, 1400), PLAB[kind], 60, PCOL[kind], int(255 * min(1, (1 - u) / 0.2)), scale=1.25 - 0.25 * min(1, u / 0.12))
    # escape: the marble pops out big
    if t >= T_ESC:
        u = t - T_ESC
        sc = min(1, u / 0.3); bob = int(abs(math.sin(u * 4)) * 30)
        bm = BIG[int(u * 8) % len(BIG)]
        if sc < 1: bm = bm.resize((max(1, int(bm.width * sc)), max(1, int(bm.height * sc))), Image.NEAREST)
        img.alpha_composite(bm, (int(CX - bm.width / 2), int(1010 - bm.height / 2 - bob)))
        text_layer(img, [(CX, 1250, 'HE ESCAPED!', 68, (255, 214, 60), 9, int(255 * min(1, u / 0.3)))])
        rr2 = random.Random(f)
        def conf(dd):
            for _ in range(50):
                cx_, cy_ = rr2.uniform(80, 870), (rr2.uniform(-200, H) + u * 520) % H
                if PANEL[3] + 10 < cy_ < 1490: dd.rectangle([cx_, cy_, cx_ + 10, cy_ + 10], fill=rr2.choice(COLS) + (255,))
        layer(img, conf)
    # top: dark band behind hook + counter so the rings never sit behind the letters
    layer(img, lambda d: d.rectangle([0, 0, W, PANEL[3] + 8], fill=(10, 6, 22, 175)))
    left = S.NR - min(k, S.NR)
    layer(img, lambda d: d.rounded_rectangle(PANEL, 18, fill=(14, 10, 24, 225), outline=(150, 120, 255), width=5))
    items = [(210, PANEL[1] + 12, 'RINGS', 44, (220, 210, 255), 6, 255), (210, PANEL[1] + 64, 'LEFT', 44, (220, 210, 255), 6, 255),
             (480, PANEL[1] + 14, str(left), 92, (255, 255, 255), 10, 255)]
    if st['combo'] >= 3 and t < T_ESC:
        items.append((PANEL[2] - 100, PANEL[1] + 34, f"x{st['combo']}", 52, COLS[st['combo'] % 5], 7, 255))
    text_layer(img, items)
    if t < S.T0:
        text_layer(img, [(CX, 1250, 'GO HOLLOW!', 54, (255, 255, 255), 8, 255)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
wr.close()
out = []; last = -9
for e in sorted(ev_out):
    if e[1] in ('brick_8bit', 'crunch_8bit'):
        if e[0] - last < 0.09: continue
        last = e[0]
    out.append(e)
json.dump({'events': out}, open(OUTD + '/ev.json', 'w'))
print('done', round(END, 2), len(out))
