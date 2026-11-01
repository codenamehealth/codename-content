import sys, os, math, random, json, glob
import numpy as np
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
SRC = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b10'
os.chdir(SRC)
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
# rc12 review recut (concept is flagged for Bennett, so legibility/rule/universal fixes only, wording unchanged):
# rune ring moved onto the SIGN line so the print lands exactly where the finger is; contract body text 26 -> 34px,
# revealed line by line; 3-2-1 in 2.4s with the Hollow hopping on each beat and sparkles spiralling into the ring;
# 'TAG WHO SHOULD SIGN' as a band line on the end card; end hold 4.2s -> ~2.4s (1.3s after the last box lands), then loop.
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc12'); from rc12 import hook_layer2
OUTD = os.path.dirname(os.path.abspath(__file__))
HOOK1, HB1 = hook_layer(['PUT YOUR FINGER', 'ON THE SCREEN'], accent=1)
HOOK2, HB2 = hook_layer2(["HE'S YOURS", 'NOW.'], accent=1, sub='TAG WHO SHOULD SIGN')
SH = 0.6                                         # rc12: every beat after the countdown moves 0.6s earlier (3-2-1 in 2.4s)
DUR = 7.8; NF = int(DUR * 30)
BG = bg_frames('hub.gif', (1920 * 1920 // 1080, 1920), step=2)
BG = [ImageEnhance.Brightness(f.crop((560, 0, 560 + W, H))).enhance(0.8).convert('RGBA') for f in BG]
HIDLE = idle('hollow', 6)                       # feet at y=78*6
HVIC = vic('hollow', 560)
PAPER = crop(Image.open(sorted(glob.glob('paper/*.png'))[int(os.environ.get('PAPER', '1'))]).convert('RGBA'))
PAPER = up(PAPER, 10)   # 760x1040 so the whole paper fits under the hook and inside the zone
GOLD = gummy('cre', 3)   # rc12: 4x -> 3x to make room for the bigger contract text   # product (creatine) gummy, was the gold gummy
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
    lines = [('HOLLOW', 54, (150, 30, 40)), ('ADOPTION PAPERS', 30, (150, 30, 40)), ('', 4, None),
             ('I agree to take', 34, (60, 40, 30)), ('home one (1)', 34, (60, 40, 30)), ('Hollow.', 34, (60, 40, 30)), ('', 2, None),
             ('Feed him one', 34, (60, 40, 30)), ('gummy every day.', 34, (60, 40, 30)), ('', 2, None), ('No returns.', 34, (60, 40, 30))]
    y = 112; T0 = 3.75 - SH; shown = 99 if full else (t - T0) / 0.11   # rc12: 34px body, one line at a time
    if full or t >= T0:
        for i, (s_, sz, col) in enumerate(lines):
            if col and i <= shown:
                w_ = d.textlength(s_, font=F(sz)); d.text((pc.width / 2 - w_ / 2, y), s_, font=F(sz), fill=col + (255,), stroke_width=1, stroke_fill=col + (255,))
            y += sz + 12
        sy = int(pc.height * 0.74); sx0 = int(pc.width * 0.36)
        d.text((sx0, sy), 'SIGN:', font=F(30), fill=(60, 40, 30, 255)); d.line([sx0 + 160, sy + 34, pc.width - 90, sy + 34], fill=(60, 40, 30, 255), width=4)
        if full or t > 4.3 - SH:
            g = GOLD; gy = int(pc.height * 0.62 - g.height / 2 + (0 if full else 6 * math.sin(t * 4)))
            pc.alpha_composite(g, (int(pc.width / 2 - g.width / 2), gy))
        if full or t >= 4.9 - SH:
            v = 1 if full else min(1, (t - 4.9 + SH) / 0.15); sc = 1.6 - 0.6 * v
            fp = up(FP, sc); pc.alpha_composite(fp, (int(sx0 + 330 - fp.width / 2), int(sy + 10 - fp.height / 2)))
    return pc
PFULL = None
ev = []
KEEP = {int(x) for x in os.environ.get('KEEP', '0,40,75,140,200,233').split(',')}
wr = Writer(OUTD + '/noaudio.mp4')
RING_C = (98 + 273 + 330, 460 + 769 + 10)   # rc12: exactly where the print lands on the SIGN line (was (680, 1040), 200px off)
for f in range(NF):
    t = f / 30
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(20, 12, 30, 60)))
    if t < 6.0 - SH:
        # the Hollow waiting, a glowing gold rune ring where your finger goes
        k = 0 if t < 3.0 - SH else min(1, (t - 3.0 + SH) / 0.25)
        hf = HIDLE[int(t * 8) % len(HIDLE)]
        hx, hy = 330, 1500
        if t < 3.4 - SH:
            ub = (t % 0.8); hop = int(34 * math.sin(math.pi * ub / 0.32)) if ub < 0.32 and t < 2.4 else 0   # rc12: hops on each beat
            img.alpha_composite(hf, (hx - hf.width // 2, hy - 78 * 6 - hop))
            def spark(d):                                  # rc12: sparkles spiralling into the ring from frame 0
                cx, cy = RING_C
                for q in range(14):
                    u = (t * 0.7 + q / 14) % 1; a = q * 2.4 + u * 5; r = 330 * (1 - u) + 40
                    x1, y1 = cx + r * math.cos(a), cy + r * math.sin(a) * 0.9
                    sz = 5 + 4 * (1 - u); d.rectangle([x1 - sz, y1 - sz, x1 + sz, y1 + sz], fill=(255, 230, 140, int(230 * min(1, u * 3))))
            if t < 2.4: layer(img, spark)
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
            if t >= 3.0 - SH:
                fp = FP.copy(); a = fp.getchannel('A').point(lambda p: int(p * k)); fp.putalpha(a)
                img.alpha_composite(fp, (RING_C[0] - fp.width // 2, RING_C[1] - fp.height // 2))
            items = []
            if t < 2.4:
                n = 3 - int(t / 0.8); ub = t % 0.8; szn = int(170 * (1.3 - 0.3 * min(1, ub / 0.12)))   # rc12: 0.8s beats, scale punch
                items.append((478, 600 - (szn - 170) // 2, str(n), szn, (255, 90, 90), 12, 255))
            text_layer(img, items)
            if f in (0, 24, 48): ev.append((round(t, 3), 'tick_8bit'))
            if f == 72: ev.append((2.4, 'stomp_8bit'))
            if t >= 3.0 - SH:
                u = (t - 3.0 + SH) / 0.4; a = int(255 * max(0, 1 - u))
                layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 255, 255, a // 2)))
        else:
            # adoption papers
            u = min(1, (t - 3.4 + SH) / 0.35); py = int(1920 - (1920 - 460) * (1 - (1 - u) ** 3))
            pp = PAPER; px = 478 - pp.width // 2
            pc = compose_paper(t)
            img.alpha_composite(pc, (px, py))
            if f == int(round((4.9 - SH) * 30)): ev.append((4.3, 'stomp_8bit'))
            if f == int(round((3.4 - SH) * 30)): ev.append((2.8, 'whoosh_8bit'))
    else:
        # he's yours now
        u = t - (6.0 - SH)
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
        if f == int(round((6.0 - SH) * 30)): ev.append((5.4, 'victory'))
    img.alpha_composite(HOOK1 if t < 6.0 - SH else HOOK2)
    wr.write(img)
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:03d}.png')
wr.close()
json.dump({'events': ev}, open(OUTD + '/ev.json', 'w'))
print('done')
