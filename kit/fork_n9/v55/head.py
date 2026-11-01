import sys, os, math, random, json, glob
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
from PIL import Image, ImageDraw, ImageEnhance
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a6'); OUT = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_n9/v55/'
sys.path.insert(0, '../pixellab/safezone'); sys.path.insert(0, '../fork_rc2'); from rc2 import hook_layer2, acv_gloss, acv_tag
from hook import hook_band
HK, HB = hook_band(['WHO WOULD WIN', 'THE RACE?'], accent=1); print('HB', HB)   # Oct 29: full-width strip, no box, no sub line
KS = 4   # runners 3x -> 4x (review: ~1.4x bigger)
def MX(x): return 200 + (x - 120) * (620 / 852)
rnd = random.Random(55)
# ---------------- ground: PixelLab Wang tiles, clay track inside grass
meta = json.load(open('track_meta.json')); sheet = Image.open('track_sheet.png').convert('RGBA')
TILE = {}
for t in meta['tileset_data']['tiles']:
    c = t['corners']; key = tuple(c[k] == 'lower' for k in ('NW', 'NE', 'SW', 'SE')); bb = t['bounding_box']
    TILE[key] = up(sheet.crop((bb['x'], bb['y'], bb['x'] + bb['width'], bb['y'] + bb['height'])), 2)
Y0 = 420; TS = 64; GC, GR = 17, 24   # 24 rows: grass now runs to the bottom edge (was a flat green strip below y1764)
def low(i, j): return 3 <= j <= 17
GROUND = Image.new('RGBA', (W, H), (40, 90, 40, 255))
for j in range(GR):
    for i in range(GC):
        key = (low(i, j), low(i + 1, j), low(i, j + 1), low(i + 1, j + 1)); tl = TILE[key]
        if all(key) or not any(key):
            if (i * 7 + j * 3) % 2: tl = tl.transpose(Image.FLIP_LEFT_RIGHT)
        GROUND.alpha_composite(tl, (i * TS - 10, Y0 + j * TS))
TY0, TY1 = Y0 + 3 * TS + 6, Y0 + 17 * TS - 6
LH = (TY1 - TY0) / 4
NAMES = ['joy', 'cyrus', 'cleo', 'ray']
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (150, 140, 180)}
def lane_y(k): return TY0 + LH * (k + 0.5) + 102    # feet (lower in the lane so 4x heads clear the band)
gd = ImageDraw.Draw(GROUND)
for k in range(1, 4):
    y = int(TY0 + LH * k)
    for x in range(0, W, 36): gd.rectangle([x, y - 3, x + 22, y + 2], fill=(245, 236, 220, 255))
X0, XF = 120, 972
for y in range(int(TY0), int(TY1), 6): gd.rectangle([MX(X0) - 4, y, MX(X0) + 2, y + 3], fill=(245, 236, 220, 255))
for r in range(int((TY1 - TY0) / 14) + 1):
    for c in range(2):
        col = (245, 245, 245, 255) if (r + c) % 2 == 0 else (25, 22, 30, 255)
        gd.rectangle([MX(XF) + c * 14 - 14, TY0 + r * 14, MX(XF) + c * 14 - 1, min(TY1, TY0 + r * 14 + 13)], fill=col)
# lane name tags
def face(name, rad):
    SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
    im = Image.open(SP + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 28) for n in NAMES}
for k, n in enumerate(NAMES):
    ic = ICON[n]; GROUND.alpha_composite(ic, (100 - ic.width // 2, int(TY0 + LH * k + 14)))
# ---------------- sprites
SR = {g: seq(PL + f'race/{g}_run', KS) for g in ['joy', 'cyrus', 'cleo', 'ray']}
hw = Image.open(A + 'hollow-walk-side.gif'); HW = []
for i in range(hw.n_frames):
    hw.seek(i); f = hw.convert('RGBA').crop((290, 120, 610, 790)); k = 192 / 650
    HW.append(f.resize((int(f.width * k), int(f.height * k)), Image.NEAREST))
HEAT = seq(SP + 'fork3/hollow_eat', 3)
CBLK = seq(SP + 'fork_a4/cleo_block', KS)
RCAST = seq(SP + 'fork3/ray_cast', KS)
# n9: Joy plays music with Syeda's own victory pose (staff sparkling), not the PixelLab joy_cast (Joy's face only as Syeda drew it)
JVIC = [up(f.resize((92, 92), Image.NEAREST), KS) for f in gif_frames(A + VIC['joy'])]
CVIC = vic('cyrus', 300)
HVIC = vic('cleo', 360)
CWALK = [up(Image.open(f'../fork_a5/gen/cleo_walk/{i:02d}.png').convert('RGBA'), KS) for i in range(1, 9)]
GUM = {k: up(acv_gloss(Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA')) if k == 'acv' else Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA'), 3) for k in ('mush', 'cre', 'acv', 'mel')}
PANIC = {g: seq(PL + f'maze/anim/{g}_panic', KS) for g in ['cyrus', 'ray', 'joy']}
ROCK = up(Image.open('rock/08.png').convert('RGBA'), 4)
SLIME = seq(PL + 'race/slime_idle_c', 3)
SLIME_S = [up(f, 0.62) for f in SLIME]
STAND = {g: up(Image.open(SP + 'syeda_src/' + p).convert('RGBA'), KS) for g, p in {'joy': 'char1/char8.png', 'cyrus': 'char4/char10.png', 'cleo': 'char3/char7.png', 'ray': 'char2/char5.png'}.items()}
# ---------------- header bg (Liza castle)
HDR = bg_frames('vit_hd.gif', (W, 430), box=(0, 40, 1920, 40 + 764), step=2, bright=0.62)
