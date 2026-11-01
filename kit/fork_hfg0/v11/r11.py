import math, random, json, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/'; A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30
import sys, os; sys.path.insert(0, S0 + 'fork_rc2'); from rc2 import hook_layer2
# review r011: 'Comment your score' from frame 0 as a real band line (replaces 'HOW MANY CAN YOU GET?', which doubled the end card)
sys.path.insert(0, S0 + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['GUESS THE', 'GUIDE'], accent=1, color=(255, 214, 60), size=72)   # Oct 29: soft fade, no box; 'Comment your score' sub cut
STILL = os.environ.get('STILL')
print('hook bottom', HB)
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
POSES = [P + 'race/cyrus_atk/06.png', P + 'maze/anim/cleo_slide/04.png', P + 'maze/anim/ray_panic/03.png', P + 'race/joy_atk/04.png', P + 'race/cleo_atk/06.png']   # Hollow silhouette swapped for Cleo's sword-and-shield attack (Hollow rule)
def sil(p):
    im = Image.open(p).convert('RGBA'); im = im.crop(im.getbbox())
    k = max(1, min(9, 448 // im.width, 466 // im.height)); im = up(im, k)
    a = im.getchannel('A').point(lambda v: 255 if v > 90 else 0)
    s = Image.new('RGBA', im.size, (16, 10, 26, 255)); s.putalpha(a)
    pad = Image.new('RGBA', (im.width + 24, im.height + 24), (0, 0, 0, 0)); pad.alpha_composite(s, (12, 12))
    glow = pad.getchannel('A').filter(ImageFilter.MaxFilter(13))
    g = Image.new('RGBA', pad.size, (255, 250, 220, 255)); g.putalpha(glow.point(lambda v: int(v * 0.9)))
    out = Image.new('RGBA', pad.size, (0, 0, 0, 0)); out.alpha_composite(g); out.alpha_composite(pad)
    return out
SIL = [sil(p) for p in POSES]
GOLD = up(Image.open(P + 'gummies/pick_gold.png').convert('RGBA'), 5)
g = Image.open(A + 'found_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2, 0, 960 - cw // 2 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.8).convert('RGBA'))   # Oct 29: the forest is the scene now (was blurred + 45% backdrop)
# card 560 wide x 464 tall (was 560 square): the tallest silhouette (451px with glow) still fits at its old size, freeing room for a 4x lineup
CS = 560; CSH = 464; Q = 4
CX = 478; CY = HB + 12 + (CSH + 32) // 2   # card centred on the safe column (70-887) so the lower block clears the notch
def card_frame():
    n = CS // Q; m = CSH // Q
    L = Image.new('RGBA', (n + 8, m + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rectangle([0, 0, n + 7, m + 7], fill=(60, 34, 12, 255))
    d.rectangle([2, 2, n + 5, m + 5], fill=(220, 160, 40, 255)); d.rectangle([3, 3, n + 4, m + 4], fill=(255, 214, 80, 255))
    d.rectangle([5, 5, n + 2, m + 2], fill=(150, 95, 25, 255)); d.rectangle([6, 6, n + 1, m + 1], fill=(0, 0, 0, 0))
    for (x, y) in ((1, 1), (n + 2, 1), (1, m + 2), (n + 2, m + 2)): d.rectangle([x, y, x + 4, y + 4], fill=(255, 240, 160, 255))
    return up(L, Q)
FRAME = card_frame()
NAMES = ['JOY', 'CLEO', 'RAYLEIGH', 'CYRUS']; COLS = [(90, 200, 80), (90, 150, 255), (190, 90, 240), (255, 160, 40)]   # Rayleigh moved inside so her 44px name fits
IDF = {'JOY': 'idle_0.gif', 'CYRUS': 'idle_1.gif', 'RAYLEIGH': 'idle_2.gif', 'CLEO': 'idle_3.gif'}
def idle3(fn):
    im = Image.open(A + fn); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), 4))   # review: lineup 3x -> 4x (~256px), feet at 78*4
    return fr
IDLES = {n: idle3(IDF[n]) for n in NAMES}
PX0, PX1, PY0, PY1 = 74, 885, 1104, 1497; FEET = 1482; XS = [172, 372, 572, 768]
F44 = F(44)
def lineup(img, t):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    # Oct 29: no panel; the guides stand on the forest floor
    for i, nm in enumerate(NAMES):
        x = XS[i]; d.ellipse([x - 70, FEET - 10, x + 70, FEET + 8], fill=(10, 20, 10, 120))
    img.alpha_composite(L)
    for i, nm in enumerate(NAMES):
        x = XS[i]; fr = IDLES[nm]; spr = fr[int(t * 8 + i * 2) % len(fr)]
        img.alpha_composite(spr, (int(x - spr.width / 2), FEET - 78 * 4))
    # Oct 29: name labels cut (you match the silhouette to the lineup, names aren't needed)
def round_col(img, r, p, a=255):
    """right of the card: round number + vertical timer bar (the 22px PAUSE label is gone)"""
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    top = CY - (CSH + 32) // 2; bot = CY + (CSH + 32) // 2
    ctext(d, 906, top + 10, f'{r + 1}/5', F44, (255, 255, 255), 8, a)   # round counter, no box
    by0, by1 = top + 84, bot; bx0, bx1 = 884, 928
    col = (90, 220, 90) if p > 0.5 else ((255, 200, 60) if p > 0.25 else (230, 70, 60))
    d.rectangle([bx0 - 6, by0 - 6, bx1 + 6, by1 + 6], fill=(20, 15, 35, a))
    h = int((by1 - by0) * p)
    if h > 0: d.rectangle([bx0, by1 - h, bx1, by1], fill=col + (a,))
    img.alpha_composite(L)
EGY = HB + 250   # end-card gummy top
GOLD = up(Image.open(P + 'gummies/pick_gold.png').convert('RGBA'), 5)
RND = 2.5; TD = 0.15; TIMER = 2.1; HOLD = 1.5; COL = 0.25; ENDC = HOLD + COL; NR = 5; TOTAL = NR * RND + ENDC   # review: rounds 3.6 -> 2.5s, end card 1.5s then collapses into round 1's flip
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v11_noaudio.mp4' if not STILL else 'still_tmp.mp4'], stdin=subprocess.PIPE)
ev = []
for f in ([int(x) for x in STILL.split(',')] if STILL else range(int(round(TOTAL * FPS)))):
    t = f / FPS; img = BGS[int(t * 6) % len(BGS)].copy()
    r = int(t // RND)
    # header
    d = ImageDraw.Draw(img)
    if r < NR:
        u = t - r * RND
        pass
        # flip-in scale
        fx = min(1, u / 0.22)
        card = Image.new('RGBA', (CS, CSH), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        # rotating sunburst inside the card
        def burst(dd):
            dd.rectangle([0, 0, CS, CS], fill=(255, 200, 60, 255))
            for k in range(14):
                a1 = t * 0.6 + k * math.pi / 7; a2 = a1 + math.pi / 14
                dd.polygon([(CS / 2, CS / 2), (CS / 2 + 900 * math.cos(a1), CS / 2 + 900 * math.sin(a1)), (CS / 2 + 900 * math.cos(a2), CS / 2 + 900 * math.sin(a2))], fill=(255, 236, 140, 255))
        burst(cd)
        rr = random.Random(r)
        for q in range(4):
            qx = rr.uniform(60, CS - 120); qy = (rr.uniform(0, CSH) - u * 60) % CSH
            cd.text((qx, qy), '?', font=F(48), fill=(200, 130, 40, 255))
        s = SIL[r]; bob = int(5 * math.sin(t * 3))
        card.alpha_composite(s, (CS // 2 - s.width // 2, CSH // 2 - s.height // 2 + bob))
        card.alpha_composite(Image.new('RGBA', (1, 1), (0, 0, 0, 0)))
        fr = Image.new('RGBA', FRAME.size, (0, 0, 0, 0)); fr.alpha_composite(card, (6 * Q, 6 * Q)); fr.alpha_composite(FRAME)
        if fx < 1: fr = fr.resize((max(1, int(fr.width * fx)), fr.height), Image.NEAREST)
        img.alpha_composite(fr, (CX - fr.width // 2, CY - fr.height // 2))
        p = max(0, 1 - max(0, u - TD) / TIMER)
        round_col(img, r, p)
        lineup(img, t)
    else:
        u = t - NR * RND
        EC = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(EC)
        sc_ = 1 + 0.2 * max(0, 1 - u * 6)   # hard pop
        ctext(d, CX, HB + 40, 'HOW MANY', F(int(72 * sc_)), (255, 255, 255), 9); ctext(d, CX, HB + 134, 'DID YOU GET?', F(int(64 * sc_)), (255, 214, 60), 9)
        bob = int(8 * math.sin(t * 3)); EC.alpha_composite(GOLD, (CX - GOLD.width // 2, EGY + bob))
        for k in range(8):
            an = t * 1.5 + k * 0.785; sx, sy = CX + 140 * math.cos(an), EGY + GOLD.height / 2 + 90 * math.sin(an)
            d.rectangle([sx - 6, sy - 6, sx + 6, sy + 6], fill=(255, 245, 190, 230))
        # Oct 29: '5/5 = GOLDEN GUMMY' explainer and the 1-5 boxes cut; the question + gold gummy stay
        if u >= HOLD:   # collapse into the thin vertical line round 1 flips open from -> seamless loop
            v = min(1, (u - HOLD + 1 / FPS) / COL); w_ = max(1, int(W * (1 - v) ** 2))
            EC = EC.resize((w_, H), Image.NEAREST); E2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); E2.alpha_composite(EC, (CX - w_ // 2, 0)); EC = E2
            round_col(img, 0, 1.0, int(255 * v))
        img.alpha_composite(EC)
        lineup(img, t)
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if STILL: img.convert('RGB').save(f'still_{f}.png')
ff.stdin.close(); ff.wait()
# SFX on real events only: the card flip each round, ding + twinkle on the end card, swish on the collapse (no metronome ticks)
for r in range(NR): ev.append((round(r * RND, 3), 'swish'))
ev.append((round(NR * RND, 3), 'ding_8bit')); ev.append((round(NR * RND + 0.3, 3), 'twinkle'))
json.dump({'events': ev}, open('v11_events.json', 'w')); print('done', TOTAL)
