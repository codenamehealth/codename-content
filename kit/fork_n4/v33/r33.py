"""#33, Oct 29 notes (Bennett): the old hook ('If you know her, you know') didn't match, the guides aren't all girls. Reworked as
WHO WOULD WIN IN A FIGHT?: the four cards flip in as contenders with their gummy power (STRENGTH / SPEED / SHIELD / SLEEP),
then FIGHT!: Cleo swings, Cyrus punches, Joy whips her vine, and Rayleigh (the one nobody picks) eats a melatonin gummy and puts
everyone to sleep. The hook fade then reads RAYLEIGH WINS. Base: fork_hfg3/v33/r33.py (cards, courtyard)."""
import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
sys.path.insert(0, R + 'pixellab/safezone'); from hook import hook_fade
W, H, FPS = 1080, 1920, 30
TEST = len(sys.argv) > 1
_fc = {}
def F(s):
    if s not in _fc: _fc[s] = ImageFont.truetype(FONT, s)
    return _fc[s]
def up(im, k): return im.resize((int(im.width * k), int(im.height * k)), Image.NEAREST)
def flip(im): return im.transpose(Image.FLIP_LEFT_RIGHT)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255, sc=(20, 15, 35)):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=sc + (a,))
vg = Image.open(A + 'vit_hd.gif'); BG = []
for i in range(0, vg.n_frames, 2):
    vg.seek(i); f = vg.convert('RGB'); s = H / 1080; cw = int(W / s)
    f = f.crop((960 - cw // 2, 0, 960 + cw // 2, 1080)).resize((W, H), Image.NEAREST)
    BG.append(ImageEnhance.Brightness(f).enhance(0.82).convert('RGBA'))
CARD = up(Image.open(R + 'fork_a3/parch/03.png').convert('RGBA').crop(Image.open(R + 'fork_a3/parch/03.png').getbbox()), 7)
CW, CHh = CARD.size; CX, CY = W // 2, 984
def gif(p, h=None, n92=False):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    if n92: return [f.resize((92, 92), Image.NEAREST) for f in fr]
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
# contenders, in card order: the strong-looking ones first, Rayleigh last
G = [('CLEO', 'STRENGTH', (46, 93, 168), 'idle_3.gif', 'cre', 'cleo'), ('CYRUS', 'SPEED', (217, 122, 31), 'idle_1.gif', 'mush', 'cyrus'),
     ('JOY', 'SHIELD', (74, 124, 58), 'idle_0.gif', 'acv', 'joy'), ('RAYLEIGH', 'SLEEP', (107, 45, 107), 'idle_2.gif', 'mel', 'ray')]
IDL = [gif(g[3], 376) for g in G]
def gsrc(k): return Image.open(R + f'pixellab/gummies/pick_{k}.png').convert('RGBA')
GUM = {g[4]: up(gsrc(g[4]), 3) for g in G}
def card(i, t):
    c = CARD.copy(); name, power, col, _, gk, _ = G[i]
    fr = IDL[i][int(t * 8) % len(IDL[i])]; c.alpha_composite(fr, (int(CW / 2 - fr.width / 2), 252))
    d = ImageDraw.Draw(c)
    ctext(d, CW / 2, 664, name, F(50), (60, 40, 25), 0)
    ctext(d, CW / 2, 728, power, F(44), col, 0)
    g = GUM[gk]; c.alpha_composite(g, (int(CW / 2 - g.width / 2), 790))
    return c
# ---- review follow-up (Oct 29): cards ~0.5s each, then each power fires one at a time with its word, then the SLEEP twist
CARD_T = 0.5
SEQ = [(k * CARD_T, (k + 1) * CARD_T, k) for k in range(4)]
T0 = 4 * CARD_T                          # 2.0: FIGHT! (hard cut at T0 + 0.5)
T_SPD = T0 + 0.5                         # Cyrus: mushroom gummy -> SPEED! dash in
DASH0, DASH1 = T_SPD + 0.25, T_SPD + 0.55
T_STR = T_SPD + 0.65                     # Cleo: creatine gummy -> STRENGTH!, plants and swings for ~1s
ATK0 = T_STR + 0.25; ATK_LEN = 1.0; T_HIT = ATK0 + 0.35
T_SHD = ATK0 + ATK_LEN                   # Joy: ACV gummy -> SHIELD! bubble, Rayleigh's orb bounces off it
BUB0 = T_SHD + 0.25; ORB0 = T_SHD + 0.35; T_BLOCK = ORB0 + 0.3; BUB1 = T_BLOCK + 0.15
T_EAT = BUB1 + 0.3                       # Rayleigh: melatonin gummy -> SLEEP!
T_WAVE = T_EAT + 0.3
T_WIN = T_WAVE + 0.85                    # everyone asleep, RAYLEIGH WINS
DUR = T_WIN + 1.0; N = int(round(DUR * FPS))
K = 5                                    # all fight sprites ~64px native -> 320px
def seqk(d, k=K): return [up(Image.open(p).convert('RGBA'), k) for p in sorted(glob.glob(R + d + '/*.png'))]
CLEO_ATK = seqk('pixellab/race/cleo_atk'); RAY_ATK = seqk('pixellab/race/ray_atk'); CRUN = seqk('pixellab/race/cyrus_run')
CYKO = seqk('pixellab/king/cyrus_ko')
_jk = Image.open(R + 'pixellab/king/joy_ko/04.png').convert('RGBA')
KO = {'cleo': seqk('pixellab/king/cleo_ko'), 'joy': seqk('pixellab/king/joy_ko')[:4] + [up(_jk.rotate(-20, resample=Image.NEAREST, center=(64, 80)), K)]}  # Joy laid flat
CSLEEP = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(R + 'fork_a5/gen/cyrus_sleep/*.png'))]
IDLE = {g[5]: [up(f, K) for f in gif(g[3], n92=True)] for g in G}
RVIC = [up(f, K) for f in gif('vic_victoryPose_1.gif', n92=True)]
POS = {'joy': (300, 1172, 'L'), 'ray': (770, 1172, 'R'), 'cleo': (300, 1480, 'L'), 'cyrus': (770, 1480, 'R')}
CY_IN = 560                              # where Cyrus's dash stops, right in front of Cleo
SLEEP_AT = {'joy': T_WAVE + 0.15, 'cleo': T_WAVE + 0.2, 'cyrus': T_WAVE + 0.3}
def put(img, fr, x, yb, side, cxn, fyn):
    if side == 'R': fr = flip(fr); cxn = fr.width / K - cxn
    img.alpha_composite(fr, (int(x - cxn * K), int(yb - fyn * K)))
def ease(p): p = max(0, min(1, p)); return 1 - (1 - p) ** 2
def cyrus_x(t):
    if t < DASH0: return 770
    if t < DASH1: return 770 + (CY_IN - 770) * ease((t - DASH0) / (DASH1 - DASH0))
    if t < T_HIT: return CY_IN
    return CY_IN + (790 - CY_IN) * ease((t - T_HIT) / 0.35)
def draw_fighter(img, nm, t):
    x, yb, side = POS[nm]
    if nm == 'cyrus': x = cyrus_x(t)
    layer(img, lambda d: d.ellipse([x - 90, yb - 14, x + 90, yb + 14], fill=(0, 0, 0, 90)))
    if nm == 'ray':
        if t >= T_WIN: put(img, RVIC[int((t - T_WIN) * 10) % len(RVIC)], x, yb, 'L', 46, 78); return
        if ORB0 <= t < ORB0 + 0.65: put(img, RAY_ATK[min(12, int((t - ORB0) * 20))], x, yb, side, 30, 104); return
        put(img, IDLE['ray'][int(t * 8) % len(IDLE['ray'])], x, yb, 'L', 46, 78); return
    if t >= SLEEP_AT[nm]:
        u = t - SLEEP_AT[nm]
        if nm == 'cyrus': put(img, CSLEEP[min(len(CSLEEP) - 1, int(u * 18))], x, yb, 'L', 43, 78)
        else:
            fr = KO[nm][min(4, int(u * 14))]; put(img, fr, x, yb + 8, side, 63, fr.getbbox()[3] / K)   # bbox bottom on the ground line
        return
    if nm == 'cyrus':
        if DASH0 <= t < DASH1: put(img, CRUN[int(t * 24) % len(CRUN)], x, yb, side, 29, 104); return
        if T_HIT <= t < T_HIT + 0.45:   # knocked back
            fr = CYKO[1 if t < T_HIT + 0.25 else 2]; put(img, fr, x, yb, side, 63, fr.getbbox()[3] / K); return
    if nm == 'cleo' and ATK0 <= t < ATK0 + ATK_LEN:   # planted, full swing, no sliding
        put(img, CLEO_ATK[min(12, int((t - ATK0) / ATK_LEN * 13))], x, yb, side, 31, 104); return
    put(img, IDLE[nm][int(t * 8) % len(IDLE[nm])], x, yb, 'L', 46, 78)
rng = random.Random(1); SPK = [(rng.uniform(0, W), rng.uniform(450, 1700), rng.uniform(0, 6.3)) for _ in range(36)]
HOOK, HB = hook_fade(['WHO WOULD WIN', 'IN A FIGHT?'], accent=1); print('hook bottom', HB)
ENDH, _ = hook_fade(['RAYLEIGH', 'WINS'], accent=0, color=(200, 150, 255))
POWERS = [('cyrus', T_SPD, 'mush', 'SPEED!', (255, 170, 60)), ('cleo', T_STR, 'cre', 'STRENGTH!', (120, 170, 255)),
          ('joy', T_SHD, 'acv', 'SHIELD!', (130, 230, 110)), ('ray', T_EAT - 0.25, 'mel', 'SLEEP!', (200, 150, 255))]
events = [(round(s0, 3), 'swish') for s0, _, _ in SEQ]
events += [(round(T0, 3), 'go_8bit'), (round(T_SPD + 0.2, 3), 'powerup_8bit'), (round(DASH0, 3), 'whoosh_8bit'), (round(T_STR + 0.2, 3), 'powerup_8bit'),
           (round(T_HIT, 3), 'punch'), (round(T_SHD + 0.2, 3), 'powerup_8bit'), (round(T_BLOCK, 3), 'ding_8bit'), (round(T_EAT, 3), 'twinkle'),
           (round(T_WAVE, 3), 'poof'), (round(T_WIN, 3), 'victory')]
def spark(img, v, hx, hy, col=(255, 240, 160)):
    if 0 <= v < 0.3:
        layer(img, lambda d: [d.rectangle([hx + math.cos(k * 0.9) * 220 * v - 11, hy + math.sin(k * 0.9) * 220 * v - 11,
                                           hx + math.cos(k * 0.9) * 220 * v + 11, hy + math.sin(k * 0.9) * 220 * v + 11],
                                          fill=col + (int(255 * (1 - v / 0.3)),)) for k in range(7)])
def frame(f):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, y, x + 6, y + 6], fill=(255, 235, 170, int(110 + 100 * math.sin(t * 3 + p)))) for x, y, p in SPK])
    if t < T0 - 1e-6:
        s0, s1, i = next(s for s in SEQ if s[0] <= t + 1e-6 < s[1])
        c = card(i, t)
        a_in = min(1, (t - s0) / 0.12); a_out = min(1, (s1 - t) / 0.08)
        fx = 0.1 + 0.9 * (1 - (1 - min(a_in, a_out)) ** 2)
        w = max(2, int(CW * fx)); ci = c.resize((w, CHh), Image.NEAREST)
        layer(img, lambda d: d.ellipse([CX - 300, CY + CHh // 2 - 20, CX + 300, CY + CHh // 2 + 40], fill=(0, 0, 0, 90)))
        img.alpha_composite(ci, (CX - w // 2, CY - CHh // 2))
        img.alpha_composite(HOOK); return img
    # speed lines + dust behind Cyrus's dash (drawn under the fighters)
    if DASH0 <= t < DASH1 + 0.25:
        cx_ = cyrus_x(min(t, DASH1)); yb = POS['cyrus'][1]; a = 255 if t < DASH1 else int(255 * (1 - (t - DASH1) / 0.25))
        def sl(d):
            for k in range(6):
                y = yb - 300 + k * 48; L = 140 + 60 * (k % 3)
                d.rectangle([cx_ + 70, y, cx_ + 70 + L, y + 8], fill=(255, 255, 255, int(a * 0.85)))
            for k in range(7):
                dx = 60 + k * 40; r = 18 + k * 4
                d.ellipse([cx_ + dx - r, yb - 20 - r, cx_ + dx + r, yb - 20 + r], fill=(210, 180, 140, int(a * 0.6)))
        layer(img, sl)
    if T_HIT <= t < T_HIT + 0.4:     # dust where Cyrus skids back
        v = t - T_HIT; cx_ = cyrus_x(t); yb = POS['cyrus'][1]
        layer(img, lambda d: [d.ellipse([cx_ - 120 - k * 30 - 22, yb - 30 - 22, cx_ - 120 - k * 30 + 22, yb - 30 + 22], fill=(210, 180, 140, int(160 * (1 - v / 0.4)))) for k in range(4)])
    for nm in ('joy', 'ray', 'cleo', 'cyrus'): draw_fighter(img, nm, t)
    spark(img, t - T_HIT, 470, 1330)
    # Joy's shield bubble and the orb it blocks
    jx, jy, _ = POS['joy']
    if BUB0 <= t < BUB1 + 0.2:
        grow = ease((t - BUB0) / 0.15); pop = 0 if t < BUB1 else (t - BUB1) / 0.2
        r = 190 * grow * (1 + 0.3 * pop); a = int(255 * (1 - pop)); flash = T_BLOCK <= t < T_BLOCK + 0.1
        def bub(d):
            d.ellipse([jx - r, jy - 170 - r, jx + r, jy - 170 + r], fill=(120, 230, 110, int(70 * (1 - pop)) + (90 if flash else 0)), outline=(170, 255, 150, a), width=10)
            d.arc([jx - r * 0.7, jy - 170 - r * 0.7, jx + r * 0.7, jy - 170 + r * 0.7], 200, 250, fill=(240, 255, 240, a), width=8)
        layer(img, bub)
    spark(img, t - T_BLOCK, jx + 180, jy - 180, (190, 255, 170))
    # power pops: the gummy pops over the guide and drops in, with the power word
    for nm, tp, gk, word, col in POWERS:
        x, yb, _ = POS[nm]
        if nm == 'cyrus': x = cyrus_x(tp)
        v = t - tp
        if 0 <= v < 0.3:
            g = GUM[gk]; gy = yb - 420 - 50 * math.sin(math.pi * min(1, v / 0.2)) + max(0, v - 0.2) * 900
            img.alpha_composite(g, (int(x - g.width / 2), int(gy)))
        if 0.1 <= v < 0.72:
            w_ = v - 0.1; a = 255 if w_ < 0.5 else int(255 * (1 - (w_ - 0.5) / 0.12)); sc = 1 + 0.25 * max(0, 1 - w_ / 0.12)
            layer(img, lambda d, x=x, yb=yb, word=word, col=col, a=a, sc=sc: ctext(d, min(max(x, 250), 830), yb - 470, word, F(int(54 * sc)), col, 8, a))
    rx, ry, _ = POS['ray']
    if T_WAVE <= t < T_WAVE + 0.8:
        v = (t - T_WAVE) / 0.8
        def wave(d):
            for k in range(3):
                r = 60 + (v * 900) - k * 70
                if r > 0: d.ellipse([rx - r, ry - 160 - r * 0.8, rx + r, ry - 160 + r * 0.8], outline=(190, 120, 255, int(220 * (1 - v))), width=14)
        layer(img, wave)
    def zz(d):
        for nm, ts in SLEEP_AT.items():
            v = t - ts - 0.4
            if v < 0: continue
            x, yb, side = POS[nm]
            if nm == 'cyrus': x = cyrus_x(t)
            for k in range(3):
                life = (v * 0.7 + k / 3) % 1.0
                zx = x - 60 + life * 90 + 10 * math.sin(life * 6); zy = yb - 210 - life * 170
                d.text((zx, zy), 'Z', font=F(34 + k * 6), fill=(230, 220, 255, int(255 * min(1, (1 - life) / 0.3))), stroke_width=5, stroke_fill=(30, 20, 50, 255))
    layer(img, zz)
    u = t - T0
    if u < 0.5:      # FIGHT! pops in, holds at full strength, hard cut (no ghost fade)
        sc = 1 + 0.3 * max(0, 1 - u / 0.12)
        layer(img, lambda d: ctext(d, 540, 760, 'FIGHT!', F(int(92 * sc)), (255, 214, 60), 10, 255))
    img.alpha_composite(ENDH if t >= T_WIN else HOOK)
    return img
if TEST:
    for ts in sys.argv[1:]: frame(int(float(ts) * FPS)).convert('RGB').save(f't_{ts}.png')
    sys.exit()
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v33_noaudio.mp4'], stdin=subprocess.PIPE)
for f in range(N): ff.stdin.write(frame(f).convert('RGB').tobytes())
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v33_events.json', 'w')); print('done', N, DUR, T0, T_WIN)
