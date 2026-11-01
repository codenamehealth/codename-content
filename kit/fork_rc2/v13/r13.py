import math, random, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/'; A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30
import sys, os; sys.path.insert(0, S0 + 'fork_rc2'); from rc2 import hook_layer2, gummy_src
HOOK, HB = hook_layer2(['PAUSE WHEN', 'ALL 3 MATCH'], accent=1, color=(255, 214, 60), sub='Only 1 frame works!')   # sub 36 -> 46px
STILL = os.environ.get('STILL')
print('hook bottom', HB)
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
K = 10   # review r013: cabinet 8x -> 10x around the reels (windows 128 -> 160px); the cabinet's left trim runs off the left edge, the plinth below y1500
_SRC = Image.open(S0 + 'forkA/assets/slot_pick.png').convert('RGBA')
# split the lever (arm + ball head) off the cabinet so it can be pulled
_body = _SRC.copy(); _lev = Image.new('RGBA', _SRC.size, (0, 0, 0, 0))
for y in range(34, 74):   # rows above 34 at x88+ are the cabinet's turret trim, not the lever
    for x in range(88, 112):
        px = _SRC.getpixel((x, y))
        if px[3]: _lev.putpixel((x, y), px); _body.putpixel((x, y), (0, 0, 0, 0))
HEAD = _lev.crop((0, 0, 112, 57)); STICK = _lev.crop((0, 57, 112, 74))
CAB = up(_body, K)
def lever_img(sy):
    # sy 1 = up, smaller = pulled toward the viewer (stick foreshortened, head rides down with it)
    L = Image.new('RGBA', _SRC.size, (0, 0, 0, 0))
    sh = max(1, round(STICK.height * sy)); st = STICK.resize((112, sh), Image.NEAREST)
    top = 74 - sh; extra = round(10 * (1 - sy) / 0.94)   # head comes forward/down past the stick on the full pull
    L.alpha_composite(st, (0, top)); L.alpha_composite(HEAD, (0, top - 57 + extra))
    return up(L, K)
LEVS = {}
def lever_at(t):
    T0, T1, T2, T3 = 0.10, 0.33, 0.45, 0.85
    if t < T0 or t >= T3: sy = 1.0
    elif t < T1: u = (t - T0) / (T1 - T0); sy = 1 - 0.94 * u * u
    elif t < T2: sy = 0.06
    else: u = (t - T2) / (T3 - T2); sy = 0.06 + 0.94 * (1 - (1 - u) ** 2)
    sy = round(sy * 17) / 17
    if sy not in LEVS: LEVS[sy] = lever_img(sy)
    return LEVS[sy], sy
CX0, CY0 = -85, HB - 322   # 10x: reel windows x75-655 y732-1002, lever ball right edge x1025, body clears the lower-right notch
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
# review/vetting: the Hollow's face is off the reels (it read as a jackpot prize); ACV gummy gets the gummy gloss
SYM = [face(n, 70) for n in ['joy', 'cyrus', 'cleo', 'ray']] + [up(gummy_src(k), 5) for k in ['mush', 'acv', 'mel', 'cre', 'gold']]
GOLD = 8; NS = len(SYM)
g = Image.open(A + 'recov_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2, 0, 960 - cw // 2 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.5).convert('RGBA'))
# review: staggered stops (reel 1 6.0s, reel 2 7.0s, reel 3 slows into the near-miss at 7.8s); SO CLOSE held ~1s, fades, and frame 0
# opens on the same gold, gold, Cyrus so the lever pull reads as 'spin again'. Still exactly ONE all-gold frame (never revealed).
DUR = 9.3; MATCH = 184; STOP = [int(6.0 * FPS), int(7.0 * FPS), int(7.8 * FPS)]; FINAL = [GOLD, GOLD, 1]
SPIN0 = int(0.33 * FPS)
rnd = random.Random(11)
# reel 3 deceleration: symbol changes at growing gaps between reel 2's stop and its own stop
SLOWCH = []; c = STOP[1]; gap = 1.0
while c < STOP[2]: SLOWCH.append(int(c)); c += gap; gap *= 1.32
SLOWCH = sorted(set([x for x in SLOWCH if x < STOP[2]]))
slow_sym = {}; last = None
for ch in SLOWCH:
    while True:
        v = rnd.randrange(NS)
        if v != GOLD and v != last and v != FINAL[2]: break
    slow_sym[ch] = v; last = v
seq = []
prev = None
NF = int(round(DUR * FPS))
for f in range(NF):
    if f < SPIN0: s = list(FINAL)
    elif f == MATCH: s = [GOLD, GOLD, GOLD]
    else:
        while True:
            s = [rnd.randrange(NS) for _ in range(3)]
            # tease: gold pairs show up often, never three of a kind
            if rnd.random() < 0.18: s[rnd.randrange(3)] = GOLD; s[rnd.randrange(3)] = GOLD
            if not (s[0] == s[1] == s[2]) and s != prev: break
    for r in range(3):
        if f >= STOP[r]: s[r] = FINAL[r]
    if STOP[1] <= f < STOP[2]: s[2] = slow_sym[max(c_ for c_ in SLOWCH if c_ <= f)]
    if f != MATCH and s[0] == s[1] == s[2]: s[2] = (s[2] + 3) % NS
    if f != MATCH and s[0] == s[1] == s[2]: s[2] = (s[2] + 1) % NS
    seq.append(s); prev = s
allg = [f for f in range(NF) if seq[f] == [GOLD, GOLD, GOLD]]
assert allg == [MATCH], allg
print('one-frame check: all-gold only at frame', allg, 'slow changes', SLOWCH)
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v13_noaudio.mp4' if not STILL else 'still_tmp.mp4'], stdin=subprocess.PIPE)
F44 = F(44)
for f in ([int(x) for x in STILL.split(',')] if STILL else range(NF)):
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    # glow behind cabinet
    def glow(dd):
        cx, cy = CX0 + CAB.width / 2, CY0 + CAB.height / 2
        for rr, al in ((560, 30), (460, 40), (380, 50)): dd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=(190, 120, 255, al))
    layer(img, glow)
    img.alpha_composite(CAB, (CX0, CY0))
    LV, lsy = lever_at(t); img.alpha_composite(LV, (CX0, CY0))
    if 0.10 <= t < 0.36:   # motion streaks above the ball on the down stroke
        def streak(dd):
            by = CY0 + (74 - round(17 * lsy) - 57 + round(10 * (1 - lsy) / 0.94) + 36) * K
            for k, dx in enumerate((-30, 0, 30)):
                dd.rectangle([CX0 + 103 * K + dx - 4, by - 120 + k * 14, CX0 + 103 * K + dx + 4, by - 30], fill=(255, 245, 210, 200))
        layer(img, streak)
    s = seq[f]
    for r, (x0, x1) in enumerate(WINS):
        wx0, wy0, wx1, wy1 = CX0 + x0 * K, CY0 + WY0 * K, CX0 + x1 * K, CY0 + WY1 * K
        win = Image.new('RGBA', (wx1 - wx0, wy1 - wy0), (246, 238, 220, 255))
        wd = ImageDraw.Draw(win)
        spinning = SPIN0 <= f < STOP[r]
        sym = SYM[s[r]]
        cx, cy = win.width // 2, win.height // 2
        if r == 2 and STOP[1] <= f < STOP[2]:   # slowing: each symbol rolls down through the window, slower and slower
            c0 = max(c_ for c_ in SLOWCH if c_ <= f); nxts = [c_ for c_ in SLOWCH if c_ > f]; c1 = nxts[0] if nxts else STOP[2]
            pr = (f - c0) / max(1, c1 - c0); oy = int((pr - 0.5) * 150)
            nsym = SYM[slow_sym[c1]] if c1 in slow_sym else SYM[FINAL[2]]
            for gs, o2 in ((sym, oy), (nsym, oy - 190)):
                win.alpha_composite(gs, (cx - gs.width // 2, cy - gs.height // 2 + o2))
        elif spinning:
            jit = (f * 37 + r * 13) % 3 * 8 - 8
            nxt = SYM[seq[min(f + 1, len(seq) - 1)][r]]; prv = SYM[seq[max(0, f - 1)][r]]
            for gs, oy in ((prv, -175), (nxt, 175)):
                gh = gs.copy(); gh.putalpha(gh.getchannel('A').point(lambda v: v // 4)); win.alpha_composite(gh, (cx - gh.width // 2, cy - gh.height // 2 + oy + jit))
            win.alpha_composite(sym, (cx - sym.width // 2, cy - sym.height // 2 + jit))
        else:
            bounce = 0 if f < STOP[r] else int(14 * math.exp(-(f - STOP[r]) / 3) * math.cos((f - STOP[r]) * 1.6))
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
    # comment prompt from 0.5s on its own dark plate under the reels (review: was only at 9.0s); gives way to SO CLOSE
    if 15 <= f < STOP[2] + 8:
        a = int(255 * min(1, (f - 15) / 6, (STOP[2] + 8 - f) / 6))
        PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
        pd.rounded_rectangle([110, 1090, 780, 1236], 22, fill=(12, 8, 22, int(a * 0.9)), outline=(255, 214, 60, a), width=5)
        ctext(pd, 445, 1110, 'Comment if', F44, (255, 255, 255), 6, a); ctext(pd, 445, 1172, 'you got it!', F44, (255, 214, 60), 6, a)
        img.alpha_composite(PL)
    if f >= STOP[2] + 8:
        a = min(255, int((f - STOP[2] - 8) / 6 * 255)); tf = NF - 1 - f
        if tf < 8: a = int(a * tf / 8)   # fades before the loop back to the same reels at frame 0
        sc_ = 1 + 0.2 * max(0, 1 - (f - STOP[2] - 8) / 6)
        PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
        pd.rounded_rectangle([80, 1076, 880, 1290], 24, fill=(12, 8, 22, int(a * 0.9)), outline=(255, 214, 60, a), width=6)
        ctext(pd, 480, 1102, 'SO CLOSE!', F(int(64 * sc_)), (255, 255, 255), 8, a); ctext(pd, 480, 1206, 'Did you catch it?', F44, (255, 214, 60), 6, a)
        img.alpha_composite(PL)
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if STILL: img.convert('RGB').save(f'still_{f}.png')
ff.stdin.close(); ff.wait()
ev = [(round(i * 1.7, 3), 'slot') for i in range(4)] + [(round(STOP[r] / FPS, 3), 'punch') for r in range(3)] + [(round(STOP[2] / FPS + 0.3, 3), 'boing')]
ev += [(round(c_ / FPS, 3), 'reeltick_8bit') for c_ in SLOWCH[1:]]   # decelerating clicks on reel 3 (real events, slowing)
json.dump({'events': ev}, open('v13_events.json', 'w')); print('done')
