import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
SRC = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b10'
os.chdir(SRC)
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
OUTD = os.path.dirname(os.path.abspath(__file__))
HOOK1, HB1 = hook_layer(['PUT YOUR FINGER', 'ON THE SCREEN'], accent=1)
HOOK2, HB2 = hook_layer(["HE'S YOURS", 'NOW.'], accent=1)
DUR = 10.2; NF = int(DUR * 30)
BG = bg_frames('hub.gif', (1920 * 1920 // 1080, 1920), step=2)
BG = [ImageEnhance.Brightness(f.crop((560, 0, 560 + W, H))).enhance(0.8).convert('RGBA') for f in BG]
HIDLE = idle('hollow', 6)                       # feet at y=78*6
HVIC = vic('hollow', 560)
PAPER = crop(Image.open(sorted(glob.glob('paper/*.png'))[int(os.environ.get('PAPER', '1'))]).convert('RGBA'))
PAPER = up(PAPER, 10)   # 760x1040 so the whole paper fits under the hook and inside the zone
GOLD = gummy('cre', 4)   # product (creatine) gummy, was the gold gummy
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
            g = GOLD; gy = int(pc.height * 0.615 - g.height / 2 + (0 if full else 6 * math.sin(t * 4)))
            pc.alpha_composite(g, (int(pc.width / 2 - g.width / 2), gy))
        if full or t >= 4.9:
            v = 1 if full else min(1, (t - 4.9) / 0.15); sc = 1.6 - 0.6 * v
            fp = up(FP, sc); pc.alpha_composite(fp, (int(sx0 + 330 - fp.width / 2), int(sy + 10 - fp.height / 2)))
    return pc
PFULL = None
ev = []
KEEP = {int(x) for x in os.environ.get('KEEP', '45,150,250').split(',')}
wr = Writer(OUTD + '/noaudio.mp4')
RING_C = (680, 1040)
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
            items = []
            if t < 3.0:
                n = 3 - int(t)
                items.append((478, 560, str(n), 170, (255, 90, 90), 12, 255))
            text_layer(img, items)
            if f in (0, 30, 60): ev.append((round(t, 3), 'tick_8bit'))
            if f == 90: ev.append((3.0, 'stomp_8bit'))
            if t >= 3.0:
                u = (t - 3.0) / 0.4; a = int(255 * max(0, 1 - u))
                layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 255, 255, a // 2)))
        else:
            # adoption papers
            u = min(1, (t - 3.4) / 0.35); py = int(1920 - (1920 - 460) * (1 - (1 - u) ** 3))
            pp = PAPER; px = 478 - pp.width // 2
            pc = compose_paper(t)
            img.alpha_composite(pc, (px, py))
            if t >= 4.9 and f == int(4.9 * 30): ev.append((4.9, 'stomp_8bit'))
            if f == int(3.4 * 30): ev.append((3.4, 'whoosh_8bit'))
    else:
        # he's yours now
        u = t - 6.0
        hv = HVIC[int(u * 8) % len(HVIC)]
        hop = int(abs(math.sin(u * 5)) * 40)
        pp = compose_paper(t, full=True).resize((PAPER.width // 2, PAPER.height // 2), Image.LANCZOS); ang = -8
        pr = pp.rotate(ang, expand=True, resample=Image.BICUBIC)
        img.alpha_composite(pr, (884 - pr.width, 1490 - pr.height))
        img.alpha_composite(hv, (300 - hv.width // 2, 1495 - hv.height - hop))   # Hollow in front of the papers
        def hearts(d):
            for q in range(7):
                hx = 300 + 160 * math.sin(q * 1.7 + u * 1.3); hy = 1180 - ((u * 160 + q * 90) % 520)
                s = 10
                col = (255, 110, 150, 220)
                d.rectangle([hx - s * 2, hy - s, hx - s, hy], fill=col); d.rectangle([hx + s, hy - s, hx + s * 2, hy], fill=col)
                d.rectangle([hx - s * 2, hy, hx + s * 2, hy + s], fill=col); d.rectangle([hx - s, hy + s, hx + s, hy + s * 2], fill=col)
        layer(img, hearts)
        if u > 0.8:
            b = min(1, (u - 0.8) / 0.3); y0 = HB2 + 24
            layer(img, lambda d: d.rounded_rectangle([90, y0, 990, y0 + 150], 18, fill=(14, 10, 24, int(220 * b)), outline=(255, 214, 60, int(255 * b)), width=5))
            text_layer(img, [(540, y0 + 26, 'THE HOLLOW JOINED', 44, (255, 255, 255), 6, int(255 * b)), (540, y0 + 86, 'YOUR PARTY!', 44, (255, 214, 60), 6, int(255 * b))])
        if f == 180: ev.append((6.0, 'victory'))
    img.alpha_composite(HOOK1 if t < 6.0 else HOOK2)
    wr.write(img)
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:03d}.png')
wr.close()
json.dump({'events': ev}, open(OUTD + '/ev.json', 'w'))
print('done')
