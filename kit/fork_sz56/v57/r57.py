import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter
OUT = SP + 'fork_sz56/v57/'
HOOK, HB = hook_layer(['HOW MANY HOLLOWS', 'DO YOU SEE?'], accent=1)
K = 1.15; X0 = 80; TOP = 290   # screen = X0 + (sx-300)*K, TOP + sy*K
SX0 = 300 - X0 / K; SW = W / K
SH = int(1080 * K)
im = Image.open(A + 'found_hd.gif'); BG = []
for i in range(im.n_frames):
    im.seek(i); f = im.convert('RGB').crop((int(SX0), 0, int(SX0) + int(SW), 1080)).resize((W, SH), Image.NEAREST)
    f = f.convert('RGBA'); full = Image.new('RGBA', (W, H), (10, 20, 12, 255))
    bot = f.crop((0, SH - (H - TOP - SH), W, SH)).transpose(Image.FLIP_TOP_BOTTOM)
    bot = ImageEnhance.Brightness(bot.filter(ImageFilter.GaussianBlur(6))).enhance(0.45)
    topp = f.crop((0, 0, W, TOP)).transpose(Image.FLIP_TOP_BOTTOM)
    topp = ImageEnhance.Brightness(topp.filter(ImageFilter.GaussianBlur(6))).enhance(0.45)
    full.alpha_composite(topp, (0, 0)); full.alpha_composite(f, (0, TOP)); full.alpha_composite(bot, (0, TOP + SH))
    BG.append(full)
def S(sx, sy): return (X0 + (sx - 300) * K, TOP + sy * K)
def darken(spr, k=0.7, a=0.92):
    s = ImageEnhance.Brightness(spr).enhance(k); al = s.getchannel('A').point(lambda p: int(p * a)); s.putalpha(al); return s
H_FRONT = Image.open(SP + 'syeda_src/hollow/char1.png').convert('RGBA')
H_SIDE = Image.open(SP + 'syeda_src/hollow/char2.png').convert('RGBA')
SIT = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(SP + 'fork_a4/hollow_sit/*.png'))]
DANCE = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(SP + 'fork2/hollow_dance/*.png'))][1:]
EAT = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(SP + 'fork3/hollow_eat/*.png'))][1:]
GOLD = gummy('gold', 2)
def feet_paste(img, spr, x, y): img.alpha_composite(spr, (int(x - spr.width / 2), int(y - spr.height)))
# hidden hollows: (kind, source x, source y feet, scale)
HID = [('eyes', 556, 452, 1), ('stand', 420, 655, 1.55), ('sit', 945, 606, 1.25), ('eyes', 418, 205, 1),
       ('peek', 330, 1010, 2.5), ('dance', 1088, 592, 0.95), ('eat', 352, 770, 0.85), ('eyes', 612, 296, 0.8)]
T_END = 11.6; NF = int(T_END * FPS)
LEAVES = [(random.Random(i).uniform(0, W), random.Random(i * 7).uniform(0, 1), random.Random(i * 3).uniform(0.5, 1.2)) for i in range(14)]
FLIES = [(random.Random(i + 50).uniform(90, 990), random.Random(i + 90).uniform(560, 1460)) for i in range(18)]
EV = []
for k, tt in enumerate([7.6, 8.6, 9.6]): EV.append((tt, 'tick_8bit'))
EV.append((10.6, 'ding_8bit'))
wr = Writer(OUT + 'v57_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    img = Image.new('RGBA', (W, H), (10, 20, 12, 255))
    img.alpha_composite(BG[int(t * 8) % len(BG)], (0, 0))
    blink = lambda ph: (t * 1.0 + ph) % 3.1 < 0.14
    for i, (kind, sx, sy, sc) in enumerate(HID):
        x, y = S(sx, sy)
        if kind == 'eyes':
            if not blink(i * 0.7):
                L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
                d.ellipse([x - 26 * sc, y - 22 * sc, x + 26 * sc, y + 16 * sc], fill=(20, 12, 30, 170))
                for ex in (-11, 11): d.rectangle([x + ex * sc - 5 * sc, y - 8 * sc, x + ex * sc + 5 * sc, y + 2 * sc], fill=(235, 235, 250, 255))
                img.alpha_composite(L)
        elif kind == 'stand':
            feet_paste(img, darken(up(H_FRONT, sc), 0.62, 0.9), x, y + 14 * sc)
        elif kind == 'sit':
            fr = SIT[min(len(SIT) - 1, 6)] if len(SIT) > 6 else SIT[-1]
            feet_paste(img, darken(up(fr, sc), 0.7), x, y + 14 * sc)
        elif kind == 'peek':
            spr = darken(up(H_SIDE, sc), 0.55); spr = spr.crop((0, 0, spr.width, int(spr.height * 0.45)))
            bob = int(4 * math.sin(t * 2))
            feet_paste(img, spr, x, y - bob)
        elif kind == 'dance':
            fr = DANCE[int(t * 6) % len(DANCE)]; feet_paste(img, darken(up(fr, sc), 0.65), x, y + 14 * sc)
        elif kind == 'eat':
            fr = EAT[int(t * 5) % len(EAT)]; feet_paste(img, darken(up(fr, sc), 0.5, 0.85), x, y + 14 * sc)
    # ambience: falling leaves and fireflies
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i, (lx, ph, sp) in enumerate(LEAVES):
        yy = 520 + ((ph + t * 0.06 * sp) % 1.0) * 960; xx = lx + 40 * math.sin(t * 1.5 + i)
        d.rectangle([xx - 5, yy - 3, xx + 5, yy + 3], fill=(150, 190, 60, 220) if i % 2 else (210, 160, 60, 220))
    for i, (fx, fy) in enumerate(FLIES):
        a = int(140 + 110 * math.sin(t * 3 + i * 1.7))
        xx, yy = fx + 25 * math.sin(t * 0.8 + i), fy + 18 * math.cos(t * 0.9 + i * 2)
        d.rectangle([xx - 3, yy - 3, xx + 3, yy + 3], fill=(250, 240, 150, max(0, a)))
    img.alpha_composite(L)
    # timer under the hook
    d = ImageDraw.Draw(img)
    frac = max(0, 1 - t / 10.6)
    layer(img, lambda dd: dd.rounded_rectangle([70, HB + 6, 1025, HB + 44], 14, fill=(12, 10, 22, 220)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([82, HB + 12, 1013, HB + 38], 12, outline=(255, 214, 60, 255), width=4)
    if frac > 0: d.rounded_rectangle([88, HB + 18, 88 + (1007 - 88) * frac, HB + 32], 8, fill=(120, 220, 90, 255) if frac > 0.3 else (240, 120, 60, 255))
    if 7.6 <= t < 10.6:
        n = 3 - int((t - 7.6) / 1.0)
        text_layer(img, [(W / 2, 900, str(n), 200, (255, 214, 60), 12, int(255 * (1 - ((t - 7.6) % 1.0) * 0.5)))])
    elif t >= 10.6:
        a = int(255 * min(1, (t - 10.6) / 0.3))
        layer(img, lambda dd: dd.rounded_rectangle([90, 860, W - 90, 1090], 24, fill=(12, 10, 22, int(215 * a / 255))))
        text_layer(img, [(W / 2, 900, 'TIME\'S UP!', 64, (255, 214, 60), 8, a), (W / 2, 1000, 'COMMENT YOUR ANSWER', 34, (255, 255, 255), 6, a)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(OUT + f'p57_{f:04d}.png')
wr.close()
json.dump({'events': EV}, open(OUT + 'v57_ev.json', 'w'))
for i, (kind, sx, sy, sc) in enumerate(HID): print(kind, [round(v) for v in S(sx, sy)])
print('done', T_END, 'hidden', len(HID))
