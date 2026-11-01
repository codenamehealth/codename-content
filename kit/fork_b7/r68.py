import sys; sys.path.insert(0, '../fork1')
from common import *
BG = up(Image.open('hall/00.png').convert('RGBA'), 3)
FY = 1700
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
def dialog(img, text, t0, t):
    n = max(0, min(len(text), int((t - t0) * 26)))
    layer(img, lambda d: d.rounded_rectangle([40, 1720, W - 40, 1880], 18, fill=(16, 12, 34, 235), outline=(190, 140, 240, 255), width=5))
    img.alpha_composite(FACE, (60, 1735)); d = ImageDraw.Draw(img)
    d.text((190, 1745), 'RAYLEIGH', font=F(26), fill=(200, 150, 255)); d.text((190, 1805), text[:n], font=F(28), fill=(255, 255, 255))
w = Writer('v68/noaudio.mp4')
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
    text_layer(img, [(390, FY - 420 + bob, 'SAVE', 28, (170, 230, 255), 5, 255)])
    rf = RAY[int(t * 8) % len(RAY)]; img.alpha_composite(rf, (130 - rf.width // 2 + 40, FY - 78 * 4))
    if not phase2:
        # door glow
        if 1.3 < t < 2.6:
            a = min(1, (t - 1.3) / 0.3) * (0.75 + 0.25 * math.sin(t * 30))
            layer(img, lambda d: [d.ellipse([1005 - r, 1300 - r * 1.8, 1005 + r, 1300 + r * 1.8], fill=(170, 80, 255, int(a * al))) for r, al in ((230, 70), (170, 95), (110, 130))])
            if t < 1.35: ev(t, 'boom')
        # hollow
        if t < 1.4: hx = -80 + (t / 1.4) * 680; hspr = HRUN[int(t * 14) % 8]
        else: hx = 600; hspr = BONK[0]
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
        if 2.4 <= t < 3.0: text_layer(img, [(hx, FY - 640, 'BONK!', 70, (255, 230, 80), 9, int(255 * min(1, (3.0 - t) / 0.2)))])
        if 2.9 <= t < 4.2:
            a = int(170 * min(1, (t - 2.9) / 0.3)); img.alpha_composite(Image.new('RGBA', (W, H), (60, 0, 10, a)))
            sc = 1 + 0.15 * max(0, 1 - (t - 2.9) / 0.25)
            text_layer(img, [(W / 2, 820, 'GAME OVER', int(100 * sc), (240, 50, 50), 10, 255), (W / 2, 980, 'NO SAVE FOUND', 34, (255, 255, 255), 6, int(255 * min(1, max(0, (t - 3.3) / 0.3))))])
            ev(2.9, 'buzz_8bit')
        if 3.95 <= t < 4.2: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (t - 3.95) / 0.25))))
        if 0.4 <= t < 2.9: dialog(img, "Aren't you going to save?", 0.45, t)
    else:
        u = t - 4.2
        if u < 0.25: img.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (1 - u / 0.25)))))
        sspr = SIT[min(len(SIT) - 1, int(u * 12))]; hx = 640
        img.alpha_composite(sspr, (int(hx - sspr.width / 2), FY - 78 * 4))
        L = Image.new('RGBA', (W, H)); dl = ImageDraw.Draw(L)
        for k in range(3):
            a = t * 4 + k * 2.1; x, y = hx + 70 * math.cos(a), FY - 300 + 22 * math.sin(a)
            dl.polygon([(x, y - 14), (x + 5, y - 4), (x + 15, y - 4), (x + 7, y + 3), (x + 10, y + 13), (x, y + 7), (x - 10, y + 13), (x - 7, y + 3), (x - 15, y - 4), (x - 5, y - 4)], fill=(255, 230, 90, 255))
        img.alpha_composite(L)
        text_layer(img, [(W / 2, 520, 'CONTINUE?', 54, (255, 255, 255), 7, int(255 * min(1, u / 0.3)))])
        if u > 1.3:
            v = min(1, (u - 1.3) / 0.9); gx = 230 + (hx - 230) * v; gy = FY - 330 - math.sin(v * math.pi) * 180
            if v < 1: img.alpha_composite(MEL, (int(gx - MEL.width / 2), int(gy - MEL.height / 2)))
            else: text_layer(img, [(hx, FY - 400 - (u - 2.2) * 40, '+HP', 46, (120, 255, 140), 7, int(255 * max(0, 1 - (u - 2.2) / 1.0)))]); ev(4.2 + 2.2, 'twinkle')
            ev(4.2 + 1.3, 'whoosh_8bit')
        dialog(img, '...Rest first next time.', 4.5, t)
    layer(img, lambda d: d.rounded_rectangle([40, 80, W - 40, 300], 22, fill=(14, 10, 24, 215), outline=(255, 214, 60, 255), width=4))
    d = ImageDraw.Draw(img); ctext(d, W / 2, 120, 'SKIPPING THE SAVE POINT', F(40)); ctext(d, W / 2, 200, 'BEFORE THE BOSS', F(50), (255, 214, 60))
    w.write(img)
w.close(); json.dump(events, open('v68/events.json', 'w')); print(events)
