import math, random, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/'; A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
K = 7
CAB = up(Image.open(S0 + 'forkA/assets/slot_pick.png').convert('RGBA'), K)
CX0, CY0 = 118, 532
WINS = [(16, 32), (37, 53), (58, 74)]; WY0, WY1 = 47, 74
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (170, 160, 200)}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
def face(name, rad):
    im = Image.open(S0 + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
SYM = [face(n, 48) for n in ['joy', 'cyrus', 'cleo', 'ray', 'hollow']] + [up(Image.open(P + f'gummies/pick_{k}.png').convert('RGBA'), 3) for k in ['mush', 'acv', 'mel', 'cre', 'gold']]
GOLD = 9
g = Image.open(A + 'recov_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2, 0, 960 - cw // 2 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.5).convert('RGBA'))
DUR = 10.0; MATCH = 184; STOP = [int(7.9 * FPS), int(8.25 * FPS), int(8.6 * FPS)]; FINAL = [GOLD, GOLD, 1]
rnd = random.Random(11)
seq = []
prev = None
for f in range(int(DUR * FPS)):
    if f == MATCH: s = [GOLD, GOLD, GOLD]
    else:
        while True:
            s = [rnd.randrange(10) for _ in range(3)]
            # tease: gold pairs show up often, never three of a kind
            if rnd.random() < 0.18: s[rnd.randrange(3)] = GOLD; s[rnd.randrange(3)] = GOLD
            if not (s[0] == s[1] == s[2]) and s != prev: break
    for r in range(3):
        if f >= STOP[r]: s[r] = FINAL[r]
    if f != MATCH and s[0] == s[1] == s[2]: s[2] = (s[2] + 3) % 10
    seq.append(s); prev = s
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'slot_safe_noaudio.mp4'], stdin=subprocess.PIPE)
for f in range(int(DUR * FPS)):
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    # glow behind cabinet
    def glow(dd):
        cx, cy = W / 2, CY0 + CAB.height / 2
        for rr, al in ((560, 30), (460, 40), (380, 50)): dd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(190, 120, 255, al))
    layer(img, glow)
    img.alpha_composite(CAB, (CX0, CY0))
    s = seq[f]
    for r, (x0, x1) in enumerate(WINS):
        wx0, wy0, wx1, wy1 = CX0 + x0 * K, CY0 + WY0 * K, CX0 + x1 * K, CY0 + WY1 * K
        win = Image.new('RGBA', (wx1 - wx0, wy1 - wy0), (246, 238, 220, 255))
        wd = ImageDraw.Draw(win)
        spinning = f < STOP[r]
        sym = SYM[s[r]]
        cx, cy = win.width // 2, win.height // 2
        if spinning:
            jit = (f * 37 + r * 13) % 3 * 6 - 6
            nxt = SYM[seq[min(f + 1, len(seq) - 1)][r]]; prv = SYM[seq[max(0, f - 1)][r]]
            for gs, oy in ((prv, -120), (nxt, 120)):
                gh = gs.copy(); gh.putalpha(gh.getchannel('A').point(lambda v: v // 4)); win.alpha_composite(gh, (cx - gh.width // 2, cy - gh.height // 2 + oy + jit))
            win.alpha_composite(sym, (cx - sym.width // 2, cy - sym.height // 2 + jit))
        else:
            bounce = int(10 * math.exp(-(f - STOP[r]) / 3) * math.cos((f - STOP[r]) * 1.6))
            win.alpha_composite(sym, (cx - sym.width // 2, cy - sym.height // 2 + bounce))
        # glass shading
        wd.rectangle([0, 0, win.width, 8], fill=(0, 0, 0, 60)); wd.rectangle([0, win.height - 8, win.width, win.height], fill=(0, 0, 0, 60))
        img.paste(win, (wx0, wy0))
    # marquee lights around the windows
    def lights(dd):
        x0, y0, x1, y1 = CX0 + 13 * K, CY0 + 42 * K, CX0 + 77 * K, CY0 + 79 * K
        pts = [(x0 + (x1 - x0) * i / 12, y0 - 18) for i in range(13)] + [(x0 + (x1 - x0) * i / 12, y1 + 18) for i in range(13)]
        for i, (px, py) in enumerate(pts):
            on = (i + int(t * 8)) % 3 == 0
            dd.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(255, 230, 120, 255) if on else (110, 80, 40, 255))
    layer(img, lights)
    layer(img, lambda dd: dd.rectangle([0, 0, W, 515], fill=(12, 8, 22, 175)))
    d = ImageDraw.Draw(img)
    ctext(d, 548, 266, 'PAUSE WHEN', F(62)); ctext(d, 548, 346, 'ALL 3 MATCH', F(62), (255, 214, 60), 8)
    ctext(d, 548, 438, 'Only 1 frame works!', F(32), (255, 255, 255), 5)
    if f >= STOP[2] + 8:
        a = min(255, int((f - STOP[2] - 8) / 8 * 255))
        PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
        pd.rounded_rectangle([150, 1150, 870, 1390], 24, fill=(12, 8, 22, int(a * 0.85)), outline=(255, 214, 60, a), width=5)
        ctext(pd, 510, 1185, 'SO CLOSE!', F(60), (255, 255, 255), 7, a); ctext(pd, 510, 1290, 'Did you catch it?', F(36), (255, 214, 60), 6, a)
        img.alpha_composite(PL)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (MATCH - 1, MATCH, MATCH + 1): img.convert('RGB').resize((360, 640)).save(f'ms_{f - MATCH:+d}.png')
ff.stdin.close(); ff.wait()
ev = [(round(i * 1.7, 3), 'slot') for i in range(5)] + [(round(STOP[r] / FPS, 3), 'punch') for r in range(3)] + [(round(STOP[2] / FPS + 0.35, 3), 'boing')]
json.dump({'events': ev}, open('slot_safe_events.json', 'w')); print('done')
