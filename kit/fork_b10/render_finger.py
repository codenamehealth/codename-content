import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DUR = 10.2; NF = int(DUR * 30)
BG = bg_frames('hub.gif', (1920 * 1920 // 1080, 1920), step=2)
BG = [ImageEnhance.Brightness(f.crop((560, 0, 560 + W, H))).enhance(0.8).convert('RGBA') for f in BG]
HIDLE = idle('hollow', 6)                       # feet at y=78*6
HVIC = vic('hollow', 560)
PAPER = crop(Image.open(sorted(glob.glob('paper/*.png'))[int(os.environ.get('PAPER', '1'))]).convert('RGBA'))
PAPER = up(PAPER, max(1, round(860 / PAPER.width)))
GOLD = gummy('gold', 4)
# fingerprint whorl (procedural, red ink)
def fingerprint(r=78, col=(200, 40, 50)):
    s = 2 * r + 8; im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy = s / 2, s / 2
    for k in range(9):
        rr = 10 + k * 8; ry = rr * 1.25
        for a0 in range(0, 360, 40):
            gap = (a0 + k * 17) % 360
            d.arc([cx - rr, cy - ry, cx + rr, cy + ry], gap + 6, gap + 34, fill=col + (230,), width=4)
    m = Image.new('L', (s, s), 0); ImageDraw.Draw(m).ellipse([cx - r, cy - r * 1.25, cx + r, cy + r * 1.25], fill=255)
    a = im.getchannel('A'); a = Image.fromarray(np.minimum(np.array(a), np.array(m))); im.putalpha(a)
    return im
FP = fingerprint()

def compose_paper(t, full=False):
    pp = PAPER; pc = pp.copy(); d = ImageDraw.Draw(pc)
    lines = [('HOLLOW', 54, (150, 30, 40)), ('ADOPTION PAPERS', 30, (150, 30, 40)), ('', 20, None),
             ('I agree to take home', 26, (60, 40, 30)), ('one (1) Hollow.', 26, (60, 40, 30)), ('', 20, None),
             ('Feed him one gummy', 26, (60, 40, 30)), ('every day.', 26, (60, 40, 30)), ('', 20, None), ('No returns.', 26, (60, 40, 30))]
    y = 110; shown = 99 if full else (t - 3.75) / 0.12
    if full or t >= 3.75:
        for i, (s_, sz, col) in enumerate(lines):
            if col and i <= shown:
                w_ = d.textlength(s_, font=F(sz)); d.text((pc.width / 2 - w_ / 2, y), s_, font=F(sz), fill=col + (255,))
            y += sz + 18
        sy = int(pc.height * 0.74); sx0 = int(pc.width * 0.36)
        d.text((sx0, sy), 'SIGN:', font=F(30), fill=(60, 40, 30, 255)); d.line([sx0 + 160, sy + 34, pc.width - 90, sy + 34], fill=(60, 40, 30, 255), width=4)
        if full or t > 4.3:
            g = GOLD; gy = int(pc.height * 0.56 - g.height / 2 + (0 if full else 6 * math.sin(t * 4)))
            pc.alpha_composite(g, (int(pc.width / 2 - g.width / 2), gy))
        if full or t >= 4.9:
            v = 1 if full else min(1, (t - 4.9) / 0.15); sc = 1.6 - 0.6 * v
            fp = up(FP, sc); pc.alpha_composite(fp, (int(sx0 + 330 - fp.width / 2), int(sy + 10 - fp.height / 2)))
    return pc
PFULL = None
ev = []
wr = Writer('finger_noaudio.mp4')
RING_C = (780, 1180)
for f in range(NF):
    t = f / 30
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(20, 12, 30, 60)))
    if t < 6.0:
        # the Hollow waiting, a glowing gold rune ring where your finger goes
        k = 0 if t < 3.0 else min(1, (t - 3.0) / 0.25)
        hf = HIDLE[int(t * 8) % len(HIDLE)]
        hx, hy = 330, 1500
        if t < 3.4:
            img.alpha_composite(hf, (hx - hf.width // 2, hy - 78 * 6))
            pul = 1 + 0.06 * math.sin(t * 6)
            rr = int(120 * pul)
            def ring(d, rr=rr):
                cx, cy = RING_C
                d.ellipse([cx - rr - 30, cy - rr - 30, cx + rr + 30, cy + rr + 30], fill=(255, 220, 120, 40))
                for q in range(24):
                    a = q * math.pi / 12 + t * 1.2
                    x1, y1 = cx + rr * math.cos(a), cy + rr * math.sin(a)
                    d.rectangle([x1 - 7, y1 - 7, x1 + 7, y1 + 7], fill=(255, 214, 60, 230))
            layer(img, ring)
            if t >= 3.0:
                fp = FP.copy(); a = fp.getchannel('A').point(lambda p: int(p * k)); fp.putalpha(a)
                img.alpha_composite(fp, (RING_C[0] - fp.width // 2, RING_C[1] - fp.height // 2))
            items = [(W / 2, 330, 'PUT YOUR FINGER', 58, (255, 255, 255), 8, 255), (W / 2, 420, 'ON THE SCREEN', 58, (255, 214, 60), 8, 255)]
            if t < 3.0:
                n = 3 - int(t)
                items.append((W / 2, 600, str(n), 170, (255, 90, 90), 12, 255))
            text_layer(img, items)
            if f in (0, 30, 60): ev.append((round(t, 3), 'tick_8bit'))
            if f == 90: ev.append((3.0, 'stomp_8bit'))
            if t >= 3.0:
                u = (t - 3.0) / 0.4; a = int(255 * max(0, 1 - u))
                layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 255, 255, a // 2)))
        else:
            # adoption papers
            u = min(1, (t - 3.4) / 0.35); py = int(1920 - (1920 - 360) * (1 - (1 - u) ** 3))
            pp = PAPER; px = W // 2 - pp.width // 2
            pc = compose_paper(t)
            img.alpha_composite(pc, (px, py))
            if t >= 4.9 and f == int(4.9 * 30): ev.append((4.9, 'stomp_8bit'))
            if f == int(3.4 * 30): ev.append((3.4, 'whoosh_8bit'))
    else:
        # he's yours now
        u = t - 6.0
        hv = HVIC[int(u * 8) % len(HVIC)]
        hop = int(abs(math.sin(u * 5)) * 40)
        img.alpha_composite(hv, (360 - hv.width // 2, 1560 - hv.height - hop))
        pp = compose_paper(t, full=True).resize((PAPER.width // 2, PAPER.height // 2), Image.LANCZOS); ang = -8
        pr = pp.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(pr, (600, 980))
        # hearts
        def hearts(d):
            for q in range(7):
                hx = 360 + 160 * math.sin(q * 1.7 + u * 1.3); hy = 1100 - ((u * 160 + q * 90) % 520)
                s = 10
                col = (255, 110, 150, 220)
                d.rectangle([hx - s * 2, hy - s, hx - s, hy], fill=col); d.rectangle([hx + s, hy - s, hx + s * 2, hy], fill=col)
                d.rectangle([hx - s * 2, hy, hx + s * 2, hy + s], fill=col); d.rectangle([hx - s, hy + s, hx + s, hy + s * 2], fill=col)
        layer(img, hearts)
        a = int(255 * min(1, u / 0.3))
        text_layer(img, [(W / 2, 420, "HE'S YOURS NOW.", 60, (255, 255, 255), 8, a)])
        if u > 0.8:
            b = min(1, (u - 0.8) / 0.3)
            layer(img, lambda d: d.rounded_rectangle([60, 1640, W - 60, 1840], 18, fill=(14, 10, 24, int(220 * b)), outline=(255, 214, 60, int(255 * b)), width=5))
            text_layer(img, [(W / 2, 1680, 'THE HOLLOW JOINED', 38, (255, 255, 255), 5, int(255 * b)), (W / 2, 1750, 'YOUR PARTY!', 38, (255, 214, 60), 5, int(255 * b))])
        if f == 180: ev.append((6.0, 'victory'))
    wr.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/f_{f:04d}.png')
wr.close()
json.dump({'events': ev}, open('finger_events.json', 'w'))
print('done')
