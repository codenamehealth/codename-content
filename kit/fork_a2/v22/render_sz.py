import sys, math, json, random
sys.path.insert(0, '../../fork1'); from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['CHOOSE YOUR PATH'], accent=0, sub='A, B OR C?')
HOOK2, HB2 = hook_layer(['WHAT DID YOU GET?'], accent=0, sub='COMMENT YOUR LETTER')
import numpy as np
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
BG = bg_frames('bg_thorn.gif', (W, H), box=(800 - 253, 0, 800 + 253, 900), step=1, bright=0.45, blur=1)
FRM = up(crop(Image.open('../gen/frame/00.png').convert('RGBA')), 4)
CHEST = up(crop(Image.open('../gen/chest/01.png').convert('RGBA')), 3)
GOLDG = gummy('gold', 5)
_J = Image.open(A + 'jar_mushroom.png').convert('RGBA'); _J = _J.crop(_J.getbbox()); JAR = _J.resize((_J.width * 2 // 5, _J.height * 2 // 5), Image.NEAREST)
CYR = idle('cyrus', 3)
GK = ['mush', 'acv', 'mel', 'cre']; GSM = {k: gummy(k, 2) for k in GK}
SX = [250, 540, 830]; PCY = HB + 18 + 124; TOPY = PCY + 124 + 24; BOTY = 1124
PRX = [204, 540, 876]
PERM = [1, 2, 0]           # A->prize1, B->prize2, C->prize0 (never revealed)
COL = [((255, 205, 60), (150, 100, 10)), ((180, 110, 255), (80, 40, 140)), ((70, 225, 200), (20, 110, 100))]
# random sway terms per path
TERMS = [[(rng.uniform(60, 150), rng.uniform(1.2, 3.4), rng.uniform(0, 6.28), rng.uniform(0.4, 1.1)) for _ in range(4)] for _ in range(3)]
def path_pts(i, t, grow):
    amp = min(1.0, max(0.0, (t - 4.0) / 3.0)) * 0.6 + 0.4 + 0.25 * min(1, max(0, (t - 10) / 4))
    pts = []
    n = 120
    for k in range(n + 1):
        s = k / n                          # 0 bottom -> 1 top
        y = BOTY - (BOTY - TOPY) * s
        base = SX[i] + (PRX[PERM[i]] - SX[i]) * (3 * s * s - 2 * s * s * s)
        env = math.sin(math.pi * s) ** 0.8
        off = sum(a * math.sin(2 * math.pi * fq * s + ph + sp * t) for a, fq, ph, sp in TERMS[i]) * env * amp * 0.55
        x = max(84, min(W - 84, base + off))
        pts.append((x, y))
    m = max(2, int((n + 1) * grow))
    return pts[:m]
def draw_vines(t, grow):
    L = Image.new('RGBA', (W // 2, H // 2), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(3):
        pts = [(x / 2, y / 2) for x, y in path_pts(i, t, grow)]
        c, dk = COL[i]
        d.line(pts, fill=(20, 12, 30, 255), width=22, joint='curve')
        d.line(pts, fill=dk + (255,), width=17, joint='curve')
        d.line(pts, fill=c + (255,), width=11, joint='curve')
        d.line([(x - 2.5, y - 1.5) for x, y in pts], fill=tuple(min(255, v + 70) for v in c) + (255,), width=3, joint='curve')
        # little leaves along the vine
        for k in range(6, len(pts) - 4, 14):
            x, y = pts[k]; s = 1 if (k // 14) % 2 else -1
            d.ellipse([x + 3 * s - 3, y - 3, x + 3 * s + 3, y + 1], fill=dk + (255,))
    return L.resize((W, H), Image.NEAREST)
# background particles: drifting product gummies + sparkles
PART = [(rng.uniform(40, W - 40), rng.uniform(450, 1650), rng.choice(GK), rng.uniform(0, 6.28)) for _ in range(16)]
PART = [(90 + (x - 40) / (W - 80) * 760, 520 + (y - 450) / 1200 * 900, k, ph) for x, y, k, ph in PART]
SPK = [(rng.uniform(0, W), rng.uniform(400, 1700), rng.uniform(0, 6.28)) for _ in range(40)]
DUR = 19.5; wr = Writer('sz22_noaudio.mp4'); events = [(2.5, 'whoosh_8bit'), (5.6, 'chime'), (16.0, 'ding_8bit')]
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    def parts(d):
        for x, y, k, ph in PART: pass
        for x, y, ph in SPK:
            a = int(140 + 110 * math.sin(t * 3 + ph))
            if a > 120: d.rectangle([x - 3, y - 3 + 20 * math.sin(t + ph), x + 3, y + 3 + 20 * math.sin(t + ph)], fill=(255, 240, 180, a))
    layer(img, parts)
    for x, y, k, ph in PART:
        g = GSM[k]; yy = y + 30 * math.sin(t * 0.8 + ph); img.alpha_composite(g, (int(x), int(yy)))
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(8, 6, 18, 70)))
    # prizes at the top
    pr = min(1, max(0, (t - 5.4) / 0.5))
    for j, px in enumerate(PRX):
        sc = 0.6 + 0.4 * pr if pr < 1 else 1.0
        fr = FRM if pr >= 1 else up(FRM, sc)
        cy_ = PCY
        layer(img, lambda d, px=px: d.rounded_rectangle([px - 122, cy_ - 122, px + 122, cy_ + 122], 18, fill=(16, 10, 30, 235)))
        img.alpha_composite(fr, (int(px - fr.width / 2), int(cy_ - fr.height / 2)))
        if pr > 0:
            if j == 0: bob = int(5 * math.sin(t * 3 + 1)); img.alpha_composite(JAR, (int(px - JAR.width / 2), int(cy_ - JAR.height / 2 + bob)))
            elif j == 1: img.alpha_composite(CHEST, (int(px - CHEST.width / 2), int(cy_ - CHEST.height / 2)))
            else:
                bob = int(6 * math.sin(t * 4)); img.alpha_composite(GOLDG, (int(px - GOLDG.width / 2), int(cy_ - GOLDG.height / 2 + bob)))
        else:
            text_layer(img, [(px, cy_ - 36, '?', 80, (255, 214, 60), 7, 255)])
    # vines
    grow = min(1, max(0.0, (t - 2.5) / 2.6))
    if grow > 0: img.alpha_composite(draw_vines(t, grow))
    # A B C nodes
    for i, x in enumerate(SX):
        c = COL[i][0]
        layer(img, lambda d, x=x, c=c: (d.ellipse([x - 44, BOTY - 44, x + 44, BOTY + 44], fill=(20, 12, 30, 255)), d.ellipse([x - 36, BOTY - 36, x + 36, BOTY + 36], fill=c + (255,))))
        text_layer(img, [(x, BOTY - 20, 'ABC'[i], 40, (30, 20, 40), 0, 255)])
        if pr > 0:
            layer(img, lambda d, x=PRX[i]: d.ellipse([x - 16, TOPY - 16, x + 16, TOPY + 16], fill=(255, 240, 200, 255)))
    # Cyrus
    cs = CYR[int(t * 8) % len(CYR)]; img.alpha_composite(cs, (W // 2 - cs.width // 2, 1496 - 78 * 3))
    if t < 2.5: text_layer(img, [(W / 2, BOTY + 56, 'START!', 40, (255, 255, 255), 6, 255)])
    img.alpha_composite(HOOK if t < 16.0 else HOOK2)
    wr.write(img)
wr.p.stdin.close(); wr.p.wait()
json.dump({'events': events}, open('sz22_events.json', 'w')); print('done')
