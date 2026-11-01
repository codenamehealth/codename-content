"""#28 Swipe to the beat (approved): review recut, fixes only.
first hit on beat 1 (0.49s, a note is already mid-lane on frame 0), lane 160 -> 260px wide, notes 2x -> 4x, ring r66 -> r104,
PERFECT! 30px green -> 56px white on a dark outline, Hollow 3/4/5x -> 4/5/6x, 'SWIPE UP' text removed (arrows only),
'DID YOU HIT ALL 8?' as a 44px band line from frame 0, ACV gummy gloss + ACV GUMMY tag, victory held 1.5s then cut to frame 0."""
import sys; SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP + 'fork1'); sys.path.insert(0, SP + 'fork_rc2')
from common import *
from rc2 import hook_layer2, acv_gloss, FF
os.chdir(os.path.dirname(os.path.abspath(__file__)))
TEST = len(sys.argv) > 1
HOOK, HB = hook_layer2(['SWIPE TO', 'THE BEAT!'], accent=1, sub='DID YOU HIT ALL 8?')
print('hook bottom', HB)
BG = up(Image.open(SP + 'fork3/tavern2/00.png').convert('RGBA'), 3)
B0, BP = 0.03, 0.4643
HITS = [B0 + BP * k for k in range(1, 17, 2)]           # 8 swipes on every other beat, first on beat 1
KINDS = ['mush', 'acv', 'mel', 'cre', 'mush', 'acv', 'mel', 'cre']
TFIN = HITS[-1] + 1.0
HOLD = 1.5
DUR = TFIN + HOLD; NF = int(round(DUR * FPS))
EAT1 = [Image.open(SP + f'fork3/hollow_eat/{i:02d}.png').convert('RGBA') for i in range(13)]
VICT = vic('hollow', 576)
def gs(k): g = Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA'); return acv_gloss(g) if k == 'acv' else g
G2 = {k: up(gs(k), 2) for k in ['mush', 'acv', 'mel', 'cre']}
G4 = {k: up(gs(k), 4) for k in G2}
HX, HY = 360, 1480            # Hollow feet
RX, RY = 742, 884             # hit ring; lane x612-872 (inside the x887 notch below y1110)
RR = 104; LW = 130
LB = 1496                     # lane bottom
def hscale(n): return 4 if n < 2 else (5 if n < 5 else 6)
ev = []
for h in HITS: ev.append((round(h, 3), 'swish'))
ev.append((round(TFIN, 3), 'victory'))
def frame(f):
    t = f / FPS; img = BG.copy()
    eaten = sum(1 for h in HITS if t >= h + 0.25)
    sx_ = HX if t < TFIN else 540; layer(img, lambda d: (d.ellipse([sx_ - 300, HY - 60, sx_ + 300, HY + 60], fill=(255, 220, 140, 60))))
    # gummy counter row
    for i in range(8):
        x = W / 2 + (i - 3.5) * 104; y = HB + 52
        if i < eaten:
            g = G2[KINDS[i]]; pop = max(0, 1 - (t - HITS[i] - 0.25) / 0.2); g2 = up(g, 1 + 0.4 * pop) if pop > 0 else g
            img.alpha_composite(g2, (int(x - g2.width / 2), int(y - g2.height / 2)))
        else:
            layer(img, lambda d, x=x, y=y: d.ellipse([x - 28, y - 28, x + 28, y + 28], fill=(20, 12, 6, 120), outline=(255, 230, 180, 200), width=5))
    # Hollow
    if t < TFIN:
        last = max([h for h in HITS if h <= t], default=None)
        k = 0
        if last is not None:
            u = t - last
            if u < 0.5: k = [4, 5, 6, 7, 8][min(4, int(u / 0.1))]
            elif u < 0.8: k = [9, 10, 11][min(2, int((u - 0.5) / 0.1))]
        sc = hscale(eaten); spr = up(EAT1[k], sc)
        bob = int(6 * abs(math.sin(math.pi * (t - B0) / BP)))
        layer(img, lambda d: d.ellipse([HX - 26 * sc, HY - 5 * sc, HX + 26 * sc, HY + 5 * sc], fill=(0, 0, 0, 90)))
        img.alpha_composite(spr, (HX - spr.width // 2, HY - 78 * sc - bob))
        mouth = (HX, HY - 78 * sc + 30 * sc); head = HY - 65 * sc
    else:
        u = t - TFIN
        v = VICT[int(u * 8) % len(VICT)]
        layer(img, lambda d: d.ellipse([540 - 300, HY - 50, 540 + 300, HY + 50], fill=(0, 0, 0, 90)))
        img.alpha_composite(v, (540 - v.width // 2, HY - v.height))
        mouth = (HX, HY - 400); head = HY - 500
    # swipe lane (arrows only, no 'SWIPE UP' text)
    if t < TFIN:
        def lane(d):
            d.rounded_rectangle([RX - LW, RY - RR - 22, RX + LW, LB], 60, fill=(20, 12, 6, 185), outline=(255, 214, 60, 230), width=6)
            for j in range(5):
                yy = LB - 30 - ((t * 300 + j * 110) % 520)
                if yy > RY + RR + 30: d.line([(RX - 46, yy + 24), (RX, yy - 20), (RX + 46, yy + 24)], fill=(255, 230, 160, 150), width=10)
            beat = (t - B0) / BP; pulse = max(0, 1 - (beat - round(beat)) ** 2 * 12)
            d.ellipse([RX - RR, RY - RR, RX + RR, RY + RR], outline=(20, 12, 6, 230), width=16 + int(6 * pulse))
            d.ellipse([RX - RR, RY - RR, RX + RR, RY + RR], outline=(255, 240, 200, 240), width=8 + int(6 * pulse))
        layer(img, lane)
    for i, h in enumerate(HITS):
        g = G4[KINDS[i]]
        if h - 1.0 <= t < h:
            p = (t - (h - 1.0)) / 1.0; y = LB + 70 - (LB + 70 - RY) * p
            gc = g.crop((0, 0, g.width, max(1, min(g.height, int(LB - 8 - (y - g.height / 2))))))
            img.alpha_composite(gc, (int(RX - g.width / 2), int(y - g.height / 2)))
        elif h <= t < h + 0.25 and t < TFIN:
            p = (t - h) / 0.25; x = RX + (mouth[0] - RX) * p; y = RY + (mouth[1] - RY) * p - 180 * math.sin(math.pi * p)
            gg = up(G2[KINDS[i]], 2 - p * 0.9)
            img.alpha_composite(gg, (int(x - gg.width / 2), int(y - gg.height / 2)))
        if 0 <= t - h < 0.35:
            a = int(255 * (1 - (t - h) / 0.35)); r = RR + (t - h) * 300
            layer(img, lambda d, r=r, a=a: d.ellipse([RX - r, RY - r, RX + r, RY + r], outline=(255, 214, 60, a), width=10))
        if 0.0 <= t - h < 0.75 and t < TFIN:
            u = t - h; a = int(255 * min(1, (0.75 - u) / 0.3)); sc_ = 1 + 0.25 * max(0, 1 - u / 0.12)
            text_layer(img, [(RX - 14, RY - RR - 96, 'PERFECT!', int(56 * sc_), (255, 255, 255), 9, a)])
        if 0.25 <= t - h < 1.0 and t < TFIN:
            u = t - h - 0.25; a = int(255 * min(1, (0.75 - u) / 0.3))
            text_layer(img, [(HX, int(head - 120 - u * 60), '+1', 64, (255, 214, 60), 9, a)])
    # ACV GUMMY tag next to the ring as the first ACV gummy arrives
    ha = HITS[KINDS.index('acv')]
    if ha - 0.55 <= t < ha + 0.5:
        a = int(255 * min(1, (t - ha + 0.55) / 0.12, (ha + 0.5 - t) / 0.15))
        def tag(d):
            f_ = FF(44); s = 'ACV GUMMY'; tw = d.textlength(s, font=f_); x1 = RX - LW - 30; x0 = x1 - tw - 36; y0 = RY - 36
            d.rounded_rectangle([x0, y0, x1, y0 + 72], 14, fill=(14, 10, 24, int(235 * a / 255)), outline=(90, 200, 80, a), width=5)
            d.polygon([(x1 - 2, y0 + 22), (x1 - 2, y0 + 50), (x1 + 24, y0 + 36)], fill=(90, 200, 80, a))
            d.text((x0 + 18, y0 + 14), s, font=f_, fill=(255, 255, 255, a), stroke_width=5, stroke_fill=(10, 6, 18, a))
        layer(img, tag)
    if t >= TFIN:
        u = t - TFIN; a = int(255 * min(1, u / 0.2)); sc_ = 1 + 0.3 * max(0, 1 - u / 0.15)
        text_layer(img, [(W / 2, HB + 116, '8/8 GUMMIES', int(64 * sc_), (255, 255, 255), 9, a), (W / 2, HB + 204, 'FULL COMBO!', int(76 * sc_), (255, 214, 60), 10, a)])
        cr = random.Random(f)
        def conf(d):
            for _ in range(60):
                x = cr.uniform(0, W); y = (cr.uniform(-300, H) + u * 600) % H
                d.rectangle([x, y, x + 12, y + 12], fill=cr.choice([(255, 214, 60, 255), (255, 120, 120, 255), (120, 220, 120, 255), (150, 180, 255, 255)]))
        layer(img, conf)
    img.alpha_composite(HOOK)
    return img
if TEST:
    for ts in sys.argv[1:]: frame(int(float(ts) * FPS)).convert('RGB').save(f't_{ts}.png')
    sys.exit()
w = Writer('v28_noaudio.mp4')
for f in range(NF): w.write(frame(f))
w.close(); json.dump({'events': ev}, open('v28_events.json', 'w')); print('done', [round(h, 2) for h in HITS], TFIN, DUR)
