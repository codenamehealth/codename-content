import numpy as np, subprocess, math, random, glob, json, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
os.chdir(os.path.dirname(os.path.abspath(__file__)))
A = '../../pause/assets/'; FONT = '../../npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30; DUR = 10.0; N = int(DUR * FPS); S = 3
def F(s): return ImageFont.truetype(FONT, s)
def big(im): return im.resize((im.width * S, im.height * S), Image.NEAREST)
def crop(im): return im.crop(im.getbbox())
# --- sprites (all PixelLab, built from Syeda's Cyrus)
JUMP = [Image.open(f).convert('RGBA') for f in sorted(glob.glob('cyrus_jump/*.png'))]
FALL = [Image.open(f).convert('RGBA') for f in sorted(glob.glob('cyrus_fall/*.png'))]
def anchored(fr, mode):
    bb = fr.getbbox(); c = big(fr.crop(bb))
    return c
STAND = big(crop(JUMP[0])); CROUCH = big(crop(JUMP[3])); TAKEOFF = big(crop(JUMP[5]))
AIR = [big(crop(JUMP[i])) for i in (6, 7, 8, 9)]
LANDP = big(crop(JUMP[11]))
TUMBLE = [big(crop(FALL[i])) for i in (4, 5, 6, 7, 8)]
idle = Image.open(A + 'idle_8.gif'); IDLE = []
for i in range(idle.n_frames):
    idle.seek(i); f = idle.convert('RGBA').resize((92, 92), Image.NEAREST); IDLE.append(big(crop(f)))
PLANK = big(crop(Image.open('plank_cands/00.png').convert('RGBA'))); PW = PLANK.width
PLANK_TOP = 14 * S          # walkable surface below the rope tops
SPK = crop(Image.open('spike_cands/04.png').convert('RGBA')); SPK = SPK.resize((SPK.width * 4, SPK.height * 4), Image.NEAREST)
LEDGE = big(crop(Image.open('ledge_cands/01.png').convert('RGBA')))
DUST = crop(Image.open('../king/dust_cands/00.png').convert('RGBA'))
GUM = Image.open('../../gummy/mush_gummy_single.png').convert('RGBA'); GUM = GUM.resize((96, int(GUM.height * 96 / GUM.width)), Image.LANCZOS)
# --- background (Liza's Thornberry forest)
g = Image.open(A + 'found_hd.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, g.n_frames, 2):
    g.seek(i); f = g.convert('RGB').crop((960 - cw // 2, 0, 960 - cw // 2 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.72).convert('RGBA'))
TOPY = 1320
LEDGE_X = 210 - LEDGE.width + 40          # ledge right edge around x=250
XS = LEDGE_X + LEDGE.width - 120          # Cyrus stands near the ledge lip
XL = 700                                  # landing x (plank centre at the magic frame)
SPIKE_Y = 1760
# pit / spikes layer
PIT = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(PIT)
for y in range(TOPY + 40, H):
    a = int(min(245, 60 + (y - TOPY - 40) * 1.6)); d.line([(LEDGE_X + LEDGE.width - 10, y), (W, y)], fill=(8, 6, 16, a))
for x in range(LEDGE_X + LEDGE.width - 40, W, SPK.width - 8): PIT.alpha_composite(SPK, (x, SPIKE_Y - SPK.height + 60))
d.rectangle([0, SPIKE_Y + 30, W, H], fill=(24, 20, 32, 255))
# --- plank motion search (same idea as the original: only one frame lines up)
AIRT = 0.6; PEAK = 330
rng = random.Random(9); ts = np.arange(0, DUR, 0.02); best = None
for trial in range(1500):
    pers = [rng.uniform(0.9, 1.25) for _ in range(8)]
    J = [1.0]
    for p in pers[:-1]: J.append(J[-1] + p)
    if J[-1] + 1.1 > DUR: continue
    MK = rng.choice([4, 5]); TMf = round((J[MK] + AIRT) * FPS) / FPS
    f1, f2 = rng.choice([(0.71, 1.67), (0.61, 1.41), (0.53, 1.67)]); A1, A2 = rng.choice([(170, 80), (150, 90), (190, 70)])
    for ph in np.linspace(0, 2 * math.pi, 90):
        ph2 = rng.uniform(0, 6.28)
        bx = lambda t: 690 + A1 * np.sin(2 * math.pi * f1 * t + ph) + A2 * np.sin(2 * math.pi * f2 * t + ph2)
        off = XL - bx(TMf); xs = bx(ts) + off
        if xs.min() < 400 or xs.max() > W - PW / 2 - 6: continue
        v = abs(bx(TMf + 1 / FPS) - bx(TMf - 1 / FPS)) * FPS / 2
        if v < 900: continue
        miss = min(abs(bx(Jk + AIRT) + off - XL) for k, Jk in enumerate(J) if k != MK)
        if best is None or miss > best[0]: best = (miss, v, J, MK, f1, f2, A1, A2, ph, ph2, off)
miss, VEL, JUMPS, MATCH_K, f1, f2, A1, A2, ph, ph2, OFF = best
print('miss margin', round(miss), 'plank width', PW, 'speed', round(VEL))
TM = JUMPS[MATCH_K] + AIRT; FM = round(TM * FPS)
def plank_x(t): return 690 + A1 * math.sin(2 * math.pi * f1 * t + ph) + A2 * math.sin(2 * math.pi * f2 * t + ph2) + OFF
def ctext(img, x, y, t, f, fill=(255, 255, 255), sw=7):
    dd = ImageDraw.Draw(img); w = dd.textlength(t, font=f); dd.text((x - w / 2, y), t, font=f, fill=fill, stroke_width=sw, stroke_fill=(20, 15, 35))
def put(img, spr, cx, bottom):
    img.alpha_composite(spr, (int(cx - spr.width / 2), int(bottom - spr.height)))
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'plat_noaudio.mp4'], stdin=subprocess.PIPE)
events = []
for f in range(N):
    t = f / FPS; img = BGS[int(t * 5) % len(BGS)].copy()
    img.alpha_composite(PIT)
    img.alpha_composite(LEDGE, (LEDGE_X, TOPY - 12))
    px = plank_x(t)
    img.alpha_composite(PLANK, (int(px - PW / 2), TOPY - PLANK_TOP))
    img.alpha_composite(GUM, (int(px + PW / 2 - GUM.width - 18), TOPY - GUM.height + 8))
    k = max([i for i, Jt in enumerate(JUMPS) if Jt <= t], default=-1)
    u = t - JUMPS[k] if k >= 0 else -1
    nxt = min([Jt for Jt in JUMPS if Jt > t], default=99)
    if f == FM:
        put(img, LANDP, XL, TOPY + 4)
    elif k < 0 or u >= 0.95:
        # waiting on the ledge: idle, crouch just before the next jump, pop-in after a respawn
        if nxt - t < 0.12: put(img, CROUCH, XS, TOPY + 4)
        else:
            spr = IDLE[int(t * 8) % len(IDLE)]
            if k >= 0 and u < 1.08:
                p = (u - 0.95) / 0.13; spr = spr.resize((max(1, int(spr.width * (0.4 + 0.6 * p))), max(1, int(spr.height * (0.4 + 0.6 * p)))), Image.NEAREST)
            put(img, spr, XS, TOPY + 4)
    elif u < AIRT:
        v = u / AIRT; x = XS + (XL - XS) * v; y = TOPY - PEAK * 4 * v * (1 - v)
        spr = TAKEOFF if v < 0.12 else (AIR[min(3, int((v - 0.12) / 0.88 * 4))])
        put(img, spr, x, y + 4)
        if v < 0.04 and not any(abs(e[0] - JUMPS[k]) < 0.01 for e in events): events.append((round(JUMPS[k], 3), 'swish'))
    elif u < 0.88:
        v = (u - AIRT) / 0.28; y = TOPY + (SPIKE_Y - 40 - TOPY) * v * v; x = XL + 50 * v
        put(img, TUMBLE[int(u * 20) % len(TUMBLE)], x, y + 60)
    else:
        v = (u - 0.88) / 0.07
        sc2 = 1.0 + 0.6 * v; dw, dh = int(DUST.width * 2 * sc2), int(DUST.height * 2 * sc2)
        du = DUST.resize((dw, dh), Image.NEAREST); al = du.getchannel('A').point(lambda p: int(p * max(0, 1 - v * 0.9))); du.putalpha(al)
        img.alpha_composite(du, (int(XL + 50 - dw / 2), SPIKE_Y - dh + 30))
        if not any(abs(e[0] - (JUMPS[k] + 0.88)) < 0.01 for e in events): events.append((round(JUMPS[k] + 0.88, 3), 'punch'))
    # header
    dd = ImageDraw.Draw(img); dd.rectangle([0, 210, W, 560], fill=(14, 10, 24, 150))
    ctext(img, W / 2, 255, 'PAUSE WHEN HE', F(66)); ctext(img, W / 2, 355, 'LANDS IT', F(72), (255, 214, 60))
    ctext(img, W / 2, 470, 'Only 1 frame works', F(34))
    ff.stdin.write(img.convert('RGB').tobytes())
    if f in (FM - 1, FM, FM + 1): img.convert('RGB').crop((0, 900, W, 1920)).resize((360, 340)).save(f'm_{f - FM:+d}.png')
    if f % 20 == 0: img.convert('RGB').resize((216, 384)).save(f'prev/p_{f:03d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('plat_events.json', 'w'))
print('done, match frame', FM)
