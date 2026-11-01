# Recut of pixellab/plat/render_plat_safe.py (review-recut pass, Oct 28)
# - 3 identical attempts (jump on frame 0, every miss: fall, same puff, same reset to the ledge), 8.0s seamless loop
# - world drawn at final resolution with integer 4x sprites (was 3x world scaled 1.333x), play area moved down to fill the frame
# - exactly ONE frame shows Cyrus's feet on the log (verified numerically below, frame index printed, never marked)
# - hook via hook2: 'ONLY 1 FRAME WORKS' is a 48px second line (was 34px)
import numpy as np, subprocess, math, random, glob, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__))
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/plat/'
sys.path.insert(0, S0 + 'fork_rc_paused'); from hook2 import hook_layer2
A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30; S = 4
CYC = 80; NJ = 3; N = CYC * NJ; DUR = N / FPS          # 3 attempts, 8.0s
JF = [k * CYC for k in range(NJ)]; MATCH_K = 1          # the one good landing is inside the 2nd jump
AIRF = 18; FALLF = 9; PUFFF = 11; POPF = 5; CROUCHF = 4
FM = JF[MATCH_K] + AIRF
def F(s): return ImageFont.truetype(FONT, s)
def big(im, k=S): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def crop(im): return im.crop(im.getbbox())
JUMP = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(P + 'cyrus_jump/*.png'))]
FALL = [Image.open(f).convert('RGBA') for f in sorted(glob.glob(P + 'cyrus_fall/*.png'))]
CROUCH = big(crop(JUMP[3])); TAKEOFF = big(crop(JUMP[5]))
AIR = [big(crop(JUMP[i])) for i in (6, 7, 8, 9)]
LANDP = big(crop(JUMP[11]))
TUMBLE = [big(crop(FALL[i])) for i in (4, 5, 6, 7, 8)]
idle = Image.open(A + 'idle_8.gif'); IDLE = []
for i in range(idle.n_frames):
    idle.seek(i); f = idle.convert('RGBA').resize((92, 92), Image.NEAREST); IDLE.append(big(crop(f)))
PLANK = big(crop(Image.open(P + 'plank_cands/00.png').convert('RGBA'))); PW = PLANK.width
PLANK_SURF = 61                       # plank top -> walkable surface (same as before: 46 canvas px x 4/3)
SPK = crop(Image.open(P + 'spike_cands/04.png').convert('RGBA')); SPK = big(SPK, 5)
LEDGE = big(crop(Image.open(P + 'ledge_cands/01.png').convert('RGBA')))
DUST = crop(Image.open(P + '../king/dust_cands/00.png').convert('RGBA'))
GUM = Image.open(S0 + 'gummy/mush_gummy_single.png').convert('RGBA'); GUM = GUM.resize((128, int(GUM.height * 128 / GUM.width)), Image.LANCZOS)
# background: Liza's Thornberry forest, same crop as the safe version
X0, Y0, CW, CH = 135, 480, 810, 1440
g = Image.open(A + 'found_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); sx0 = 960 - cw / 2 + X0 / sc; sy0 = Y0 / sc
    f = g.convert('RGB').crop((int(sx0), int(sy0), int(sx0 + CW / sc), int(sy0 + CH / sc))).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.72).convert('RGBA'))
sys.path.insert(0, S0 + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['PAUSE WHEN HE', 'LANDS IT'], accent=1, size=72)   # hfg12: soft fade, no box; 'ONLY 1 FRAME WORKS' sub cut
SURF = 1185                            # feet level on the ledge and on the log
PEAK = 300
LEDGE_R = 313; LEDGE_X = LEDGE_R - LEDGE.width
XS = 153                               # Cyrus on the ledge
XL = 690                               # where every jump comes down
SPIKE_Y = 1468
CY_TOP = SURF - IDLE[0].height
assert SURF - CROUCH.height - PEAK > HB + 10, ('jump peak under the hook', SURF - CROUCH.height - PEAK, HB)
PIT = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(PIT)
for y in range(SURF + 50, H):
    a = int(min(245, 60 + (y - SURF - 50) * 0.75)); d.line([(LEDGE_R - 14, y), (W, y)], fill=(8, 6, 16, a))
for x in range(LEDGE_R - 60, W, SPK.width - 10): PIT.alpha_composite(SPK, (x, SPIKE_Y - SPK.height + 20))
d.rectangle([0, SPIKE_Y + 18, W, H], fill=(24, 20, 32, 255))
# hfg12 full-bleed: the pit floor and the ledge column run to the bottom edge (was a flat dark block from y1486 and a column ending at y1740)
STONE = SPK.crop((0, SPK.height - 70, SPK.width, SPK.height))
for r, y in enumerate(range(SPIKE_Y + 20, H, STONE.height)):
    k = max(0.42, 0.85 - 0.11 * r); st = ImageEnhance.Brightness(STONE).enhance(k)
    for x in range(LEDGE_R - 60 - (STONE.width // 2 if r % 2 else 0), W, SPK.width - 10): PIT.alpha_composite(st, (x, y))
BRICK = LEDGE.crop((0, 380, LEDGE.width, 380 + 120))
for r, y in enumerate(range(SURF - 21 + LEDGE.height - 40, H, BRICK.height)):
    PIT.alpha_composite(ImageEnhance.Brightness(BRICK).enhance(max(0.45, 0.8 - 0.12 * r)), (LEDGE_X, y))
# ---------------- plank motion: periodic over the 8.0s loop, only lines up with XL at FM
XMIN, XMAX = 345, 887 - PW // 2 - 4
def plank_fn(a, b, A1, A2, ph1, ph2, off):
    return lambda f: off + A1 * math.sin(2 * math.pi * a * f / N + ph1) + A2 * math.sin(2 * math.pi * b * f / N + ph2)
rng = random.Random(int(os.environ.get('PS', '7'))); best = None
fr = np.arange(N)
for trial in range(40000):
    a, b = rng.choice([(4, 9), (5, 11), (5, 9), (6, 13), (4, 11), (6, 11), (7, 12), (5, 13), (7, 10)])
    A1, A2 = rng.uniform(80, 190), rng.uniform(30, 100); ph1, ph2 = rng.uniform(0, 6.283), rng.uniform(0, 6.283)
    xs = A1 * np.sin(2 * np.pi * a * fr / N + ph1) + A2 * np.sin(2 * np.pi * b * fr / N + ph2)
    off = XL - xs[FM]; xs = xs + off
    if xs.min() < XMIN or xs.max() > XMAX: continue
    v = abs(xs[FM + 1] - xs[FM - 1]) * FPS / 2
    if v < float(os.environ.get("VMIN", "550")): continue
    miss = min(abs(xs[JF[k] + AIRF + j] - XL) for k in range(NJ) if k != MATCH_K for j in (-2, -1, 0, 1, 2, 3, 4))
    if best is None or miss > best[0]: best = (miss, v, a, b, A1, A2, ph1, ph2, off)
miss, VEL, a, b, A1, A2, ph1, ph2, OFF = best
plank_x = plank_fn(a, b, A1, A2, ph1, ph2, OFF)
print('plank: miss margin', round(miss), 'px (need >', PW // 2 + 50, ') speed at FM', round(VEL), 'px/s, plank width', PW)
# ---------------- Cyrus state per frame (integer frame arithmetic, no float edge cases)
def cyrus(f):
    """-> (sprite or None, centre x, feet/bottom y, kind)"""
    k = max(i for i, j in enumerate(JF) if j <= f); uf = f - JF[k]
    if uf < AIRF:
        v = uf / AIRF; x = XS + (XL - XS) * v; y = SURF - PEAK * 4 * v * (1 - v)
        spr = TAKEOFF if v < 0.12 else AIR[min(3, int((v - 0.12) / 0.88 * 4))]
        return spr, x, y, 'air'
    if uf == AIRF and k == MATCH_K:
        return LANDP, XL, SURF, 'land'
    if uf < AIRF + FALLF:
        v = (uf - AIRF + 1) / FALLF; y = SURF + 70 + (SPIKE_Y - 20 - SURF - 70) * v * v; x = XL + 10 * v
        return TUMBLE[(uf - AIRF) % len(TUMBLE)], x, y, 'fall'
    if uf < AIRF + FALLF + PUFFF: return None, XL + 10, SPIKE_Y, 'puff'
    if uf >= CYC - CROUCHF: return CROUCH, XS, SURF, 'crouch'
    spr = IDLE[(f // 4) % len(IDLE)]; kind = 'idle'
    if uf < AIRF + FALLF + PUFFF + POPF:
        p = (uf - AIRF - FALLF - PUFFF + 1) / POPF; spr = spr.resize((max(1, int(spr.width * (0.4 + 0.6 * p))), max(1, int(spr.height * (0.4 + 0.6 * p)))), Image.NEAREST); kind = 'pop'
    return spr, XS, SURF, kind
# ---------------- verify: exactly one frame with feet on the log
on_log = []
for f in range(N):
    spr, x, y, kind = cyrus(f); px = plank_x(f)
    if spr is not None and abs(y - SURF) <= 12 and abs(x - px) <= PW / 2 - 8: on_log.append((f, kind))
near = [(f, round(cyrus(f)[2] - SURF), round(cyrus(f)[1] - plank_x(f))) for f in range(N) if cyrus(f)[0] is not None and cyrus(f)[1] > LEDGE_R and abs(cyrus(f)[2] - SURF) < 80]
print('frames with feet on the log:', on_log, '| FM =', FM, '(t=%.3fs)' % (FM / FPS))
print('frames near log height (f, dy, dx to plank centre):', near)
assert on_log == [(FM, 'land')], on_log
if os.environ.get('CHECK'): sys.exit()
def put(img, spr, cx, bottom): img.alpha_composite(spr, (int(round(cx - spr.width / 2)), int(round(bottom - spr.height))))
out = os.path.join(HERE, 'plat_rc_noaudio.mp4')
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
events = []
os.makedirs(os.path.join(HERE, 'prev'), exist_ok=True)
for f in range(N):
    img = BGS[(f // 6) % len(BGS)].copy(); img.alpha_composite(PIT)
    px = plank_x(f); spr, x, y, kind = cyrus(f)
    def draw_plank():
        img.alpha_composite(PLANK, (int(round(px - PW / 2)), SURF - PLANK_SURF))
        img.alpha_composite(GUM, (int(px + PW / 2 - GUM.width - 24), SURF - PLANK_SURF + 18 - GUM.height + 10))
    if kind == 'fall': put(img, spr, x, y); draw_plank()          # dropping below the log: log stays in front
    else: draw_plank()
    img.alpha_composite(LEDGE, (LEDGE_X, SURF - 21))
    k = max(i for i, j in enumerate(JF) if j <= f); uf = f - JF[k]
    if kind in ('air', 'land', 'crouch', 'idle', 'pop'): put(img, spr, x, y + 5)
    elif kind == 'puff':
        v = (uf - AIRF - FALLF) / PUFFF
        sc2 = 1.0 + 0.25 * v; dw, dh = int(DUST.width * 2.4 * sc2), int(DUST.height * 2.4 * sc2)
        du = DUST.resize((dw, dh), Image.NEAREST); al = du.getchannel('A').point(lambda p: int(p * max(0, 1 - v * 0.85))); du.putalpha(al)
        img.alpha_composite(du, (int(x - dw / 2), SPIKE_Y - dh + 30))
    if uf == 0: events.append((round(f / FPS, 3), 'swish'))
    if uf == AIRF + FALLF: events.append((round(f / FPS, 3), 'punch')); events.append((round(f / FPS, 3), 'poof'))
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 10 == 0: img.convert('RGB').resize((216, 384)).save(os.path.join(HERE, f'prev/p_{f:03d}.png'))
    if abs(f - FM) <= 1: img.convert('RGB').save(os.path.join(HERE, f'm_{f - FM:+d}.png'))
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open(os.path.join(HERE, 'plat_rc_events.json'), 'w'))
print('done', N, 'frames', DUR, 's; landing frame', FM)
