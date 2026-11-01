import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '../../'; FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'; A = R + 'pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def crop(im): return im.crop(im.getbbox())
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=7, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
sg = Image.open(A + 'sun_hd.gif'); BG = []
for i in range(0, sg.n_frames, 2):
    sg.seek(i); f = sg.convert('RGB'); s = H / 1080; cw = int(W / s)
    BG.append(f.crop((960 - cw // 2, 0, 960 + cw // 2, 1080)).resize((W, H), Image.NEAREST).convert('RGBA'))
CUP0 = up(crop(Image.open('../../fork_a3/cups/08.png').convert('RGBA')), 8)
# dark 5px outline so the gold vases read against the gold floor
_a = CUP0.getchannel('A').filter(ImageFilter.MaxFilter(11)); CUP = Image.new('RGBA', (CUP0.width + 12, CUP0.height + 12), (0, 0, 0, 0))
_o = Image.new('RGBA', CUP.size, (30, 14, 4, 0)); _m = Image.new('L', CUP.size, 0); _m.paste(_a, (6, 6)); _o.putalpha(_m.point(lambda v: 235 if v else 0)); CUP.alpha_composite(_o); CUP.alpha_composite(CUP0, (6, 6))
GUM = up(Image.open(R + 'pixellab/gummies/pick_mush.png').convert('RGBA'), 7)   # 5x -> 7x
HIDE = [up(Image.open(p).convert('RGBA'), 4) for p in sorted(glob.glob('../../fork_a3/cyrus_hide/*.png'))]
JUMP = [up(Image.open(p).convert('RGBA'), 4) for p in sorted(glob.glob(R + 'pixellab/plat/cyrus_jump/*.png'))]
ig = Image.open(A + 'idle_1.gif'); IDLE = []
for i in range(ig.n_frames): ig.seek(i); IDLE.append(ig.convert('RGBA'))
k = HIDE[0].height / IDLE[0].height * (crop(HIDE[0]).height / crop(IDLE[0]).height); IDLE = [f.resize((HIDE[0].width, HIDE[0].height), Image.NEAREST) for f in IDLE]
FLOOR = 1240; SLOT = [200, 478, 756]; CXY = 1020  # Cyrus feet y (behind cups)
# shuffle plan
rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
T_SH0 = 1.5; swaps = []; t = T_SH0; dur = 0.62
while t < 6.2:
    a, b = rng.sample([0, 1, 2], 2); swaps.append((t, t + dur, a, b)); t += dur + 0.05; dur = max(0.3, dur * 0.93)
T_SH1 = t
pos = [0, 1, 2]  # cup index at each slot -> slot of each cup
cupslot = [0, 1, 2]; GUMCUP = 1
plan = []
for (s0, s1, a, b) in swaps:
    ca = cupslot.index(a); cb = cupslot.index(b)
    plan.append((s0, s1, ca, cb, a, b)); cupslot[ca], cupslot[cb] = b, a
final_slot = cupslot.index(1) if False else None
# cupslot[c] = slot index of cup c? track properly
slots_of = [0, 1, 2]
for (s0, s1, a, b) in swaps:
    ca = slots_of.index(a) if False else None
print('swaps', len(swaps), 'end', round(T_SH1, 2))
# simpler tracking: cup c has slot S[c]; a swap exchanges the cups standing in slots a and b
S = [0, 1, 2]; HIST = []
for (s0, s1, a, b) in swaps:
    ia = S.index(a); ib = S.index(b); HIST.append((s0, s1, ia, ib, a, b)); S[ia], S[ib] = b, a
print('gummy cup ends in slot', S[1] + 1)
def cup_pos(c, t):
    s = [0, 1, 2]
    for (s0, s1, ia, ib, a, b) in HIST:
        if t < s0: break
        if t < s1 and c in (ia, ib):
            u = (t - s0) / (s1 - s0); u = u * u * (3 - 2 * u)
            fa, fb = (a, b) if c == ia else (b, a)
            x = SLOT[fa] + (SLOT[fb] - SLOT[fa]) * u; lift = (1 if c == ia else -1) * 90 * math.sin(u * math.pi)
            return x, FLOOR + lift, -lift
        s[c] = b if c == ia else a
    # resolve current slot
    cur = c
    S2 = [0, 1, 2]
    for (s0, s1, ia, ib, a, b) in HIST:
        if t >= s1: S2[ia], S2[ib] = b, a
    return SLOT[S2[c]], FLOOR, 0
sys.path.insert(0, R + 'pixellab/safezone'); from hook import hook_fade, hook_band
# Oct 29: no box, 'Comment 1, 2 or 3' cut (caption asks; the 1/2/3 under the cups set up the answer); at the question the hook
# itself turns into WHERE'S / THE GUMMY? (no separate plate)
HS = os.environ.get('HS', 'band'); HF = hook_fade if HS == 'fade' else hook_band   # strip: the sun temple frieze is busy (same call as #17); HF = hook_fade if HS == 'fade' else hook_band
HOOK, HB = HF(['Find the', 'gummy'], accent=1); HOOKQ, _ = HF(["Where's", 'the gummy?'], accent=1); print('hook bottom', HB)
T_Q = T_SH1 + 0.2; DUR = T_Q + 1.5; N = int(round(DUR * FPS)); print('dur', round(DUR, 2))
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v34_noaudio.mp4'], stdin=subprocess.PIPE)
ONLY = [int(x) for x in os.environ.get('ONLY', '').split(',') if x]
events = []   # no per-swap whooshes (fixed-interval 8-bit SFX rule)
T_HIDE0, T_HIDE1, T_DROP = 0.0, 0.85, 1.25; T_JUMP = 999.0  # jump removed per Bennett (never add back)
for f in range(N):
    t = f / FPS; img = BG[int(t * 6) % len(BG)].copy()
    # ticker
    # Cyrus
    if t < T_HIDE0: cy = IDLE[int(t * 8) % len(IDLE)]
    elif t < T_HIDE1: cy = HIDE[min(8, 1 + int((t - T_HIDE0) / (T_HIDE1 - T_HIDE0) * 8))]
    else: cy = IDLE[int(t * 8) % len(IDLE)]
    cxp, cyp = SLOT[1], CXY
    if T_JUMP <= t < T_JUMP + 1.0:
        u = (t - T_JUMP) / 1.0; cxp = SLOT[1]; cyp = CXY - 200 * 4 * u * (1 - u)
        cy = crop(JUMP[min(len(JUMP) - 1, 5 + int(u * 6))]); cy = cy
        if abs(t - T_JUMP) < 0.5 / FPS: events.append((round(T_JUMP, 3), 'jump'))
    layer(img, lambda d: d.ellipse([SLOT[1] - 90, CXY - 16, SLOT[1] + 90, CXY + 14], fill=(0, 0, 0, 70)))
    if cy.height < 330: img.alpha_composite(cy, (int(cxp - cy.width / 2), int(cyp - cy.height)))
    else: img.alpha_composite(cy, (int(cxp - cy.width / 2), int(cyp - 78 * 4)))
    # gummy: held, then placed in front of slot 1
    if t < T_HIDE1:
        gx, gy = SLOT[1], (CXY - 320 if t < T_HIDE0 else CXY - 320 + (FLOOR + 37 - (CXY - 320)) * min(1, (t - T_HIDE0) / (T_HIDE1 - T_HIDE0)))
        img.alpha_composite(GUM, (int(gx - GUM.width / 2), int(gy - GUM.height / 2) + int(6 * math.sin(t * 6))))
    elif t < T_DROP + 0.25:
        img.alpha_composite(GUM, (SLOT[1] - GUM.width // 2, FLOOR + 37 - GUM.height // 2))
    # cups (back to front by lift)
    cups = []
    for c in range(3):
        if t < T_DROP: x, y, z = SLOT[c], FLOOR - 260 * (1 - min(1, max(0, (t - 1.0) / 1.0))) - (200 if t < 1.0 else 0) * 0, 0
        else: x, y, z = cup_pos(c, t)
        if t < T_DROP:
            if t < T_HIDE1 + 0.1: continue
            u = min(1, (t - T_HIDE1 - 0.1) / (T_DROP - T_HIDE1 - 0.1)); y = FLOOR - 1300 * (1 - u) ** 2
        cups.append((z, c, x, y))
    for z, c, x, y in sorted(cups):
        layer(img, lambda d, x=x: d.ellipse([x - 140, FLOOR + 112, x + 140, FLOOR + 156], fill=(0, 0, 0, 110)))
        img.alpha_composite(CUP, (int(x - CUP.width / 2), int(y - CUP.height / 2)))
    if abs(t - T_DROP) < 0.5 / FPS: events.append((round(T_DROP, 3), 'stomp_8bit'))
    # labels + question
    d = ImageDraw.Draw(img)
    if t >= T_SH1 + 0.2:
        u = t - T_SH1 - 0.2
        for i, x in enumerate(SLOT):
            s_ = min(1, max(0, (u - i * 0.12) / 0.2))
            if s_ > 0: ctext(d, x, FLOOR + 148, str(i + 1), F(int(72 * s_) + 1), (255, 225, 120), 9)
        if not any(e[1] == 'ding_8bit' for e in events): events.append((round(T_SH1 + 0.2, 3), 'ding_8bit'))
    img.alpha_composite(HOOKQ if t >= T_SH1 + 0.2 else HOOK)
    if ONLY:
        if f in ONLY: img.convert('RGB').save(f't_{HS}_{f}.png')
        continue
    ff.stdin.write(img.convert('RGB').tobytes())
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v34_events.json', 'w')); print('done')
