import sys, os; os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '../../fork1')
from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
random.seed(68)
SH = 205   # whole scene raised 205px: floor y1700 -> 1495 (hall background raised, bottom rows repeated)
BG0 = up(Image.open('../../fork_b7/hall/00.png').convert('RGBA'), 3)
BG = Image.new('RGBA', (W, H)); BG.paste(BG0, (0, -SH)); BG.paste(BG0.crop((0, H - SH, W, H)), (0, H - SH))
FY = 1700 - SH
# #68 note: the punchline PLAN AHEAD was stuck in the small sub line. Now the lead-in is the small top line and
# PLAN AHEAD is the big gold main line (same band style as hook.py: x70-1025 from y262, dark band, gold border, 9px stroke)
def hook68():
    X0, X1, Y0, pad = 70, 1025, 262, 26
    fs, fm = F(36), F(80); gap = 26
    lead, punch = 'SAVING IS FOR PEOPLE WHO', 'PLAN AHEAD'
    h = pad + 36 + gap + 80 + pad
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([X0, Y0, X1, Y0 + h], 22, fill=(14, 10, 24, 225), outline=(255, 214, 60), width=6)
    cx = (X0 + X1) / 2; y = Y0 + pad
    d.text((cx - d.textlength(lead, font=fs) / 2, y), lead, font=fs, fill=(255, 255, 255), stroke_width=6, stroke_fill=(10, 6, 18)); y += 36 + gap
    d.text((cx - d.textlength(punch, font=fm) / 2, y), punch, font=fm, fill=(255, 214, 60), stroke_width=9, stroke_fill=(10, 6, 18))
    return L, Y0 + h
HOOK, HB = hook68()
HX0 = 478   # where the Hollow stops (was 600) so the King Slime's splat stays clear of the lower-right buttons
HRUN = seq(PL + 'maze/anim/hollow_srun', 4, 1, 9)
BONK = seq(SP + 'fork_a4/hollow_bonk', 4, 0)
SIT = seq(SP + 'fork_a4/hollow_sit', 4, 0)
KLAND = seq(PL + 'king/king2_land', 5, 0); KIDLE = seq(PL + 'king/king2_idle', 5, 0)
RAY = idle('ray', 4)
CRY = up(crop(Image.open(SP + 'fork_a3/crystal/01.png').convert('RGBA')), 5)
MEL = gummy('mel', 3)
FACE = up(Image.open(SP + 'syeda_src/char2/char4.png').convert('RGBA').crop((28, 10, 64, 46)), 3)
DUR = 7.4; events = []
def ev(t, n):
    if not any(e[1] == n and abs(e[0] - t) < 0.05 for e in events): events.append((round(t, 3), n))
DBOX = 150   # rc16: dialogue 28px -> 48px on two lines (review: ~30px too small); 26px name tag cut, her portrait identifies her
def dialog(img, lines, t0, t):
    n = max(0, int((t - t0) * 26))
    y0 = HB + 12
    layer(img, lambda d: d.rounded_rectangle([70, y0, 1025, y0 + DBOX], 18, fill=(16, 12, 34, 235), outline=(190, 140, 240, 255), width=5))
    img.alpha_composite(FACE, (88, y0 + (DBOX - FACE.height) // 2)); d = ImageDraw.Draw(img)
    for i, ln in enumerate(lines):
        k = max(0, min(len(ln), n)); n -= len(ln)
        if k: d.text((214, y0 + 18 + i * 66), ln[:k], font=F(48), fill=(255, 255, 255), stroke_width=3, stroke_fill=(10, 6, 18))
w = Writer('v68_noaudio.mp4')
for f in range(int(DUR * FPS)):
    t = f / FPS
    sx = sy = 0
    if 1.4 < t < 2.0 or 2.4 < t < 2.7: sx, sy = random.randint(-10, 10), random.randint(-8, 8)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255)); img.alpha_composite(BG, (sx, sy))
    phase2 = t >= 4.2
    # save crystal + Rayleigh
    bob = int(10 * math.sin(t * 3))
    layer(img, lambda d: (d.ellipse([310, FY - 30, 470, FY + 20], fill=(120, 200, 255, 90)), d.ellipse([340, FY - 340 + bob, 440, FY - 240 + bob], fill=(160, 220, 255, 60))))
    img.alpha_composite(CRY, (390 - CRY.width // 2, FY - 300 + bob - CRY.height // 2))
    text_layer(img, [(390, FY - 436 + bob, 'SAVE', 44, (170, 230, 255), 7, 255)])
    rf = RAY[int(t * 8) % len(RAY)]; img.alpha_composite(rf, (130 - rf.width // 2 + 40, FY - 78 * 4))
    if not phase2:
        # door glow
        if 1.3 < t < 2.6:
            a = min(1, (t - 1.3) / 0.3) * (0.75 + 0.25 * math.sin(t * 30))
            layer(img, lambda d: [d.ellipse([1005 - r, 1300 - SH - r * 1.8, 1005 + r, 1300 - SH + r * 1.8], fill=(170, 80, 255, int(a * al))) for r, al in ((230, 70), (170, 95), (110, 130))])
            if t < 1.35: ev(t, 'boom')
        # hollow
        if t < 0.9: hx = 340 + (t / 0.9) * (HX0 - 340); hspr = HRUN[int(t * 12) % 8]
        else: hx = HX0; hspr = BONK[0]
        king_y = None
        if 1.9 <= t < 2.4: king_y = -600 + (t - 1.9) / 0.5 * (FY + 600); kspr = KIDLE[0]
        elif t >= 2.4:
            k = min(len(KLAND) - 1, int((t - 2.4) * 14)); kspr = KLAND[k] if t < 3.3 else KIDLE[int(t * 8) % len(KIDLE)]; king_y = FY
            hspr = BONK[12]
            if t < 2.45: ev(t, 'boom'); ev(t + 0.02, 'boing')
        if 1.9 <= t < 2.4:
            r = 40 + 200 * (t - 1.9) / 0.5; layer(img, lambda d: d.ellipse([hx - r, FY - r * 0.25, hx + r, FY + r * 0.25], fill=(0, 0, 0, 120)))
        img.alpha_composite(hspr, (int(hx - hspr.width / 2), FY - 78 * 4))
        if king_y is not None:
            img.alpha_composite(kspr, (int(hx - kspr.width / 2 + 10), int(king_y - 156 * 5 // 1.0 + (160 - 156) * 5)))
            img.alpha_composite(rf, (130 - rf.width // 2 + 40, FY - 78 * 4))   # Rayleigh stays in front of the King Slime (never hidden)
        if 2.4 <= t < 3.0: text_layer(img, [(hx, FY - 640, 'BONK!', 70, (255, 230, 80), 9, int(255 * min(1, (3.0 - t) / 0.2)))])
        if 2.9 <= t < 4.2:
            a = int(170 * min(1, (t - 2.9) / 0.3)); img.alpha_composite(Image.new('RGBA', (W, H), (60, 0, 10, a)))
            sc = 1 + 0.15 * max(0, 1 - (t - 2.9) / 0.25)
            text_layer(img, [(W / 2, 820, 'GAME OVER', int(90 * sc), (240, 50, 50), 10, 255), (W / 2, 975, 'NO SAVE FOUND', 44, (255, 255, 255), 6, int(255 * min(1, max(0, (t - 3.3) / 0.3))))])
            ev(2.9, 'buzz_8bit')
        if 3.95 <= t < 4.2: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (t - 3.95) / 0.25))))
        if 0.3 <= t < 2.9: dialog(img, ["Aren't you going", "to save?"], 0.3, t)
    else:
        u = t - 4.2
        if u < 0.25: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (1 - u / 0.25)))))
        sspr = SIT[min(len(SIT) - 1, int(u * 12))]; hx = 640
        TL, TG = 0.85, 1.55   # gummy thrown at 5.05s, lands on the Hollow's head at 5.75s
        asleep = u >= TG
        nod = 4 if asleep and (u - TG) % 1.0 > 0.5 else 0   # slow 1-pixel (4px) nod while asleep
        img.alpha_composite(sspr, (int(hx - sspr.width / 2), FY - 78 * 4 + nod))
        HEADY = FY - 78 * 4 + 116   # top of the sitting Hollow's head
        L = Image.new('RGBA', (W, H)); dl = ImageDraw.Draw(L)
        for k in (range(3) if not asleep else []):
            a = t * 4 + k * 2.1; x, y = hx + 70 * math.cos(a), FY - 300 + 22 * math.sin(a)
            dl.polygon([(x, y - 14), (x + 5, y - 4), (x + 15, y - 4), (x + 7, y + 3), (x + 10, y + 13), (x, y + 7), (x - 10, y + 13), (x - 7, y + 3), (x - 15, y - 4), (x - 5, y - 4)], fill=(255, 230, 90, 255))
        img.alpha_composite(L)
        ca = int(255 * min(1, u / 0.3)); cy = HB + 12 + DBOX + 36
        text_layer(img, [(W / 2, cy, 'CONTINUE?', 64, (255, 255, 255), 8, ca)])
        L2 = Image.new('RGBA', (W, H)); d2 = ImageDraw.Draw(L2); f2 = F(56)
        parts = [('YES', (110, 240, 120)), (' / ', (255, 255, 255)), ('NO', (255, 90, 90))]
        x = W / 2 - sum(d2.textlength(p, font=f2) for p, _ in parts) / 2
        for p, c in parts:
            d2.text((x, cy + 92), p, font=f2, fill=c + (ca,), stroke_width=8, stroke_fill=(10, 6, 18, ca)); x += d2.textlength(p, font=f2)
        img.alpha_composite(L2)
        if u > TL:
            v = min(1, (u - TL) / (TG - TL)); hy = HEADY - MEL.height // 2 + 10
            gx = 230 + (hx - 230) * v; gy = (FY - 330) + (hy - (FY - 330)) * v - math.sin(v * math.pi) * 200
            if v < 1: img.alpha_composite(MEL, (int(gx - MEL.width / 2), int(gy - MEL.height / 2)))
            else:
                w_ = u - TG
                if w_ < 0.25:   # gummy lands on his head and is absorbed in a purple pop
                    r = 30 + 160 * w_
                    layer(img, lambda d: d.ellipse([hx - r, hy - r, hx + r, hy + r], outline=(200, 140, 255, int(255 * (1 - w_ / 0.25))), width=8))
                    if w_ < 0.12: img.alpha_composite(MEL, (int(hx - MEL.width / 2), int(hy - MEL.height / 2)))
                zs = []
                for k in range(3):   # melatonin Zzz rising from the Hollow
                    p = (w_ * 0.9 + k / 3) % 1.0
                    if w_ * 0.9 < k / 3: continue
                    zs.append((hx + 40 + 70 * p + 10 * k, HEADY - 40 - 220 * p, 'Z', 54 + 14 * k, (200, 150, 255), 8, int(255 * min(1, (1 - p) * 3))))
                text_layer(img, zs)
                ev(4.2 + TG, 'twinkle')
            ev(4.2 + TL, 'whoosh_8bit')
        dialog(img, ['...Rest first', 'next time.'], 4.45, t)
        if t >= DUR - 0.3: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * min(1, (t - (DUR - 0.3)) / 0.25)))))   # fade to black: the loop restarts as a retry
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (0, 45, 100, 150, 170, 190, 215): img.convert('RGB').save(f'k68_{f}.png')
w.close(); json.dump(events, open('v68_ev.json', 'w')); print(events, 'HB', HB)
