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
CARD_T = 1.05
SEQ = [(k * CARD_T, (k + 1) * CARD_T, k) for k in range(4)]
T0 = 4 * CARD_T                          # 4.2: FIGHT!
T_ATK = T0 + 0.55                        # attacks start
T_EAT = T0 + 1.55                        # Rayleigh eats a melatonin gummy
T_WAVE = T_EAT + 0.35                    # sleep wave
T_WIN = T_WAVE + 0.95                    # everyone asleep, RAYLEIGH WINS
DUR = T_WIN + 1.75; N = int(round(DUR * FPS))
K = 5                                    # all fight sprites ~64px native -> 320px
def seqk(d, k=K): return [up(Image.open(p).convert('RGBA'), k) for p in sorted(glob.glob(R + d + '/*.png'))]
ATK = {'cleo': seqk('pixellab/race/cleo_atk'), 'cyrus': seqk('pixellab/race/cyrus_atk'), 'joy': seqk('pixellab/race/joy_atk'), 'ray': seqk('pixellab/race/ray_atk')}
KO = {'cleo': seqk('pixellab/king/cleo_ko'), 'joy': seqk('pixellab/king/joy_ko')}
CSLEEP = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(R + 'fork_a5/gen/cyrus_sleep/*.png'))]
IDLE = {g[5]: [up(f, K) for f in gif(g[3], n92=True)] for g in G}
RVIC = [up(f, K) for f in gif('vic_victoryPose_1.gif', n92=True)]
# arena: left side faces right, right side faces left; both rows stand on the courtyard ground
POS = {'joy': (300, 1172, 'L'), 'ray': (770, 1172, 'R'), 'cleo': (300, 1480, 'L'), 'cyrus': (770, 1480, 'R')}
ATK_AT = {'cleo': T_ATK, 'cyrus': T_ATK + 0.12, 'joy': T_ATK + 0.25}
SLEEP_AT = {'joy': T_WAVE + 0.15, 'cleo': T_WAVE + 0.2, 'cyrus': T_WAVE + 0.3}
def put(img, fr, x, yb, side, cxn, fyn):
    """fr: frame at K, cxn/fyn: native character centre x / feet y in its canvas"""
    if side == 'R': fr = flip(fr); cxn = fr.width / K - cxn
    img.alpha_composite(fr, (int(x - cxn * K), int(yb - fyn * K)))
def draw_fighter(img, nm, t):
    x, yb, side = POS[nm]
    layer(img, lambda d: d.ellipse([x - 90, yb - 14, x + 90, yb + 14], fill=(0, 0, 0, 90)))
    if nm == 'ray':
        if t >= T_WIN:
            fr = RVIC[int((t - T_WIN) * 10) % len(RVIC)]; put(img, fr, x, yb, 'L', 46, 78); return       # victory pose faces front
        if T_WAVE - 0.15 <= t < T_WAVE + 0.9:
            k = min(12, int((t - (T_WAVE - 0.15)) * 14)); put(img, ATK['ray'][k], x, yb, side, 30, 104); return
        fr = IDLE['ray'][int(t * 8) % len(IDLE['ray'])]; put(img, fr, x, yb, 'L', 46, 78); return
    if t >= SLEEP_AT[nm]:
        u = t - SLEEP_AT[nm]
        if nm == 'cyrus':
            k = min(len(CSLEEP) - 1, int(u * 18)); put(img, CSLEEP[k], x, yb, 'L', 43, 78)
        else:
            k = [0, 1, 2, 3, 4][min(4, int(u * 14))]          # stagger and lie down flat (frame 4), not the full tumble
            fr = KO[nm][k]; bb = fr.getbbox(); put(img, fr, x, yb, side, 63, bb[3] / K)
        return
    if nm in ATK_AT and t >= ATK_AT[nm]:
        k = min(12, int((t - ATK_AT[nm]) * 13)); cxn = {'cleo': 31, 'cyrus': 29, 'joy': 34}[nm]
        put(img, ATK[nm][k], x, yb, side, cxn, 104); return
    fr = IDLE[nm][int(t * 8) % len(IDLE[nm])]; put(img, fr, x, yb, 'L', 46, 78)
rng = random.Random(1); SPK = [(rng.uniform(0, W), rng.uniform(450, 1700), rng.uniform(0, 6.3)) for _ in range(36)]
HOOK, HB = hook_fade(['WHO WOULD WIN', 'IN A FIGHT?'], accent=1); print('hook bottom', HB)
ENDH, _ = hook_fade(['RAYLEIGH', 'WINS'], accent=0, color=(200, 150, 255))
events = [(round(s0, 3), 'swish') for s0, _, _ in SEQ]
events += [(round(T0, 3), 'go_8bit'), (round(ATK_AT['cleo'] + 0.15, 3), 'sword_swish'), (round(ATK_AT['cyrus'] + 0.15, 3), 'punch'),
           (round(ATK_AT['joy'] + 0.2, 3), 'whoosh_8bit'), (round(T_EAT, 3), 'twinkle'), (round(T_WAVE, 3), 'poof'), (round(T_WIN, 3), 'victory')]
def frame(f):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x, y, x + 6, y + 6], fill=(255, 235, 170, int(110 + 100 * math.sin(t * 3 + p)))) for x, y, p in SPK])
    if t < T0 - 1e-6:
        s0, s1, i = next(s for s in SEQ if s[0] <= t + 1e-6 < s[1])
        c = card(i, t)
        a_in = min(1, (t - s0) / 0.2); a_out = min(1, (s1 - t) / 0.15)
        fx = 0.1 + 0.9 * (1 - (1 - min(a_in, a_out)) ** 2)
        w = max(2, int(CW * fx)); ci = c.resize((w, CHh), Image.NEAREST)
        layer(img, lambda d: d.ellipse([CX - 300, CY + CHh // 2 - 20, CX + 300, CY + CHh // 2 + 40], fill=(0, 0, 0, 90)))
        bob = int(round(3 * math.sin((t - s0) * 3.2)))
        img.alpha_composite(ci, (CX - w // 2, CY - CHh // 2 + bob))
        if t - s0 < 0.45:
            uu = (t - s0) / 0.45
            layer(img, lambda d: [d.rectangle([CX + math.cos(k * 0.785) * (200 + 260 * uu) - 8, CY - 120 + math.sin(k * 0.785) * (200 + 260 * uu) - 8,
                                               CX + math.cos(k * 0.785) * (200 + 260 * uu) + 8, CY - 120 + math.sin(k * 0.785) * (200 + 260 * uu) + 8],
                                              fill=G[i][2] + (int(255 * (1 - uu)),)) for k in range(8)])
        img.alpha_composite(HOOK); return img
    u = t - T0
    for nm in ('joy', 'ray', 'cleo', 'cyrus'): draw_fighter(img, nm, t)
    # clash sparks where the front row's attacks meet, and where Joy's vine snaps
    for t_hit, (hx, hy) in ((ATK_AT['cleo'] + 0.3, (540, 1330)), (ATK_AT['joy'] + 0.35, (560, 1010))):
        v = t - t_hit
        if 0 <= v < 0.3:
            layer(img, lambda d, v=v, hx=hx, hy=hy: [d.rectangle([hx + math.cos(k * 0.9) * 200 * v - 10, hy + math.sin(k * 0.9) * 200 * v - 10,
                                                                  hx + math.cos(k * 0.9) * 200 * v + 10, hy + math.sin(k * 0.9) * 200 * v + 10],
                                                                 fill=(255, 240, 160, int(255 * (1 - v / 0.3)))) for k in range(7)])
    # Rayleigh eats a melatonin gummy (pops up, drops to her mouth)
    rx, ry, _ = POS['ray']
    if T_EAT - 0.25 <= t < T_EAT + 0.15:
        v = (t - (T_EAT - 0.25)) / 0.4; g = GUM['mel']
        gy = ry - 430 - 60 * math.sin(math.pi * min(1, v * 1.4)) + max(0, v - 0.7) * 300
        img.alpha_composite(g, (int(rx - g.width / 2), int(gy)))
    if T_EAT <= t < T_EAT + 0.8:
        v = t - T_EAT; a = int(255 * min(1, (0.8 - v) / 0.2)); sc = 1 + 0.25 * max(0, 1 - v / 0.12)
        layer(img, lambda d: ctext(d, rx, ry - 470, 'SLEEP!', F(int(56 * sc)), (200, 150, 255), 8, a))
    # sleep wave: purple rings out of Rayleigh across the arena
    if T_WAVE <= t < T_WAVE + 0.8:
        v = (t - T_WAVE) / 0.8
        def wave(d):
            for k in range(3):
                r = 60 + (v * 900) - k * 70
                if r > 0: d.ellipse([rx - r, ry - 160 - r * 0.8, rx + r, ry - 160 + r * 0.8], outline=(190, 120, 255, int(220 * (1 - v))), width=14)
        layer(img, wave)
    # Zzz over the sleepers
    def zz(d):
        for nm, ts in SLEEP_AT.items():
            v = t - ts - 0.4
            if v < 0: continue
            x, yb, side = POS[nm]
            for k in range(3):
                life = (v * 0.7 + k / 3) % 1.0
                zx = x - 70 + life * 80 + 10 * math.sin(life * 6); zy = yb - 130 - life * 170
                d.text((zx, zy), 'Z', font=F(34 + k * 6), fill=(230, 220, 255, int(255 * min(1, (1 - life) / 0.3))), stroke_width=5, stroke_fill=(30, 20, 50, 255))
    layer(img, zz)
    if u < 0.6:
        a = int(255 * min(1, (0.6 - u) / 0.2)); sc = 1 + 0.3 * max(0, 1 - u / 0.12)
        layer(img, lambda d: ctext(d, 540, 760, 'FIGHT!', F(int(92 * sc)), (255, 214, 60), 10, a))
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
