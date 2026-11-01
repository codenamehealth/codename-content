"""#31 Hold your thumb on the crystal, Oct 29 notes (Bennett): Joy moved down, checklist gone. The viewer puts a thumb on the
crystal in the middle of the screen with no idea what happens next; dark energy is pulled out from under their thumb and swirls
around it (build-up), Joy blasts it with light and it bursts into petals and hearts, the gloomy shrine lights up
(feel-good payoff), and the hook text becomes NEGATIVE ENERGY / REMOVED! in the same fade. Base: fork_hfg3/v31/r31.py."""
import numpy as np, math, random, subprocess, json, os, glob, sys
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
os.chdir(os.path.dirname(os.path.abspath(__file__)))
R = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, R + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['HOLD YOUR THUMB', 'ON THE CRYSTAL'], accent=1)
END1, _ = hook_fade(['NEGATIVE ENERGY', 'REMOVED!'], accent=1, color=(140, 240, 110))
print('hook bottom', HB)
FONT = R + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30
TEST = len(sys.argv) > 1
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
BG = up(Image.open(R + 'fork_a3/shrine1/00.png').convert('RGBA'), 3).crop((36, 60, 36 + W, 60 + H))
BGB = ImageEnhance.Color(ImageEnhance.Brightness(BG).enhance(1.18)).enhance(1.25)     # after: the shrine lit up
c0 = Image.open(R + 'fork_a3/crystal/03.png').convert('RGBA'); CRY = up(c0.crop(c0.getbbox()), 6)
CRYD = ImageEnhance.Brightness(CRY).enhance(0.45)                                      # crystal clouded by the dark energy
CX, CY = 540, 770            # centre of the screen, floating over the shrine pedestal
JS = 6
CAST = [up(Image.open(p).convert('RGBA'), JS) for p in sorted(glob.glob(R + 'fork_a3/joy_cast/*.png'))]
_v = Image.open(R + 'pause/assets/vic_Victory_Pose.gif'); VIC = []
for i in range(_v.n_frames):
    _v.seek(i); VIC.append(up(_v.convert('RGBA').resize((92, 92), Image.NEAREST), JS))
_j = Image.open(R + 'pause/assets/idle_0.gif'); JIDLE = []
for i in range(_j.n_frames):
    _j.seek(i); JIDLE.append(up(_j.convert('RGBA').resize((92, 92), Image.NEAREST), JS))
JX, JY = 290, 1490           # Joy's feet, moved down to the path (bottom left, clear of a right thumb)
STAFF = (JX + 72, JY - 396)  # staff tip at 6x (approx)
T_HOLD = 0.8                 # arrow hides (thumb is on); the ring keeps filling until the burst
T_DARK = 1.0                 # dark energy starts coming out
T_CAST = 3.6                 # the crystal starts to shake (no beam: the thumb does it)
T_POP = 4.5                  # ring full -> burst out of the crystal
DUR = T_POP + 2.0; N = int(round(DUR * FPS))
rng = random.Random(3); FLIES = [(rng.uniform(0, W), rng.uniform(450, 1450), rng.uniform(0, 6.3)) for _ in range(30)]
pr = random.Random(9)
DARK = [(pr.uniform(0, 6.283), pr.uniform(0.0, 1.0), pr.choice([24, 30, 36, 48, 60]), pr.uniform(0.7, 1.3), pr.choice([(30, 14, 46), (52, 22, 70), (14, 8, 22), (14, 8, 22), (90, 30, 110)])) for _ in range(320)]
PET = [(pr.uniform(0, 6.283), pr.uniform(600, 1500), pr.choice([(255, 170, 200), (255, 255, 255), (255, 214, 60), (170, 255, 140), (255, 120, 160)]), pr.choice([10, 14, 18]), pr.uniform(-1, 1)) for _ in range(140)]
FLOWERS = [(pr.uniform(90, 990), pr.uniform(1180, 1700), pr.choice([(255, 150, 190), (255, 255, 255), (255, 214, 60), (190, 140, 255)]), pr.uniform(0, 0.5)) for _ in range(34)]
FLOWERS = [f for f in FLOWERS if not (JX - 90 < f[0] < JX + 90 and f[1] < JY + 30)]
events = [(round(T_DARK, 3), 'whoosh_8bit'), (round(T_POP, 3), 'poofpops'), (round(T_POP + 0.05, 3), 'victory')]
def heart(d, x, y, s, col):
    p = [(0, 1), (1, 0), (2, 0), (3, 1), (4, 0), (5, 0), (6, 1), (6, 2), (5, 3), (4, 4), (3, 5), (2, 4), (1, 3), (0, 2)]
    d.polygon([(x + (px - 3) * s, y + (py - 2) * s) for px, py in p], fill=col)
def flower(d, x, y, s, col, a=255):
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        d.rectangle([x + dx * s - s / 2, y + dy * s - s / 2, x + dx * s + s / 2, y + dy * s + s / 2], fill=col + (a,))
    d.rectangle([x - s / 2, y - s / 2, x + s / 2, y + s / 2], fill=(255, 220, 80, a))
def frame(f):
    t = f / FPS
    after = t >= T_POP
    img = (BGB if after else BG).copy()
    layer(img, lambda d: [d.rectangle([x, y + 20 * math.sin(t + p), x + 5, y + 5 + 20 * math.sin(t + p)], fill=(230, 255, 140, int(120 + 110 * math.sin(t * 2.5 + p)))) for x, y, p in FLIES])
    # build-up: the shrine gets gloomier while the dark energy comes out
    dk = 0 if t < T_DARK else min(1, (t - T_DARK) / (T_POP - T_DARK))
    if not after and dk > 0:
        layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(18, 6, 30, int(150 * dk))))
    if after:
        u = t - T_POP
        # sun rays through the canopy
        def rays(d):
            for k in range(6):
                x = 80 + k * 190 + 30 * math.sin(t + k); a = int(min(1, u / 0.4) * (46 + 20 * math.sin(t * 2 + k)))
                d.polygon([(x, 0), (x + 90, 0), (x - 260, H), (x - 420, H)], fill=(255, 245, 190, a))
        layer(img, rays)
        def fl(d):
            for x, y, col, dl in FLOWERS:
                v = u - 0.1 - dl
                if v > 0:
                    s = 8 if v > 0.12 else 5
                    flower(d, x, y, s, col)
        layer(img, fl)
    shake = (0, 0)
    if T_CAST < t < T_POP:
        r2 = random.Random(f); m = int(4 + 10 * (t - T_CAST) / (T_POP - T_CAST)); shake = (r2.randint(-m, m), r2.randint(-m, m))
    bob = 10 * math.sin(t * 2.2)
    cx, cy = CX + shake[0], CY + bob + shake[1]
    held = t >= T_HOLD
    def aura(d):
        g = (0.6 + 0.4 * math.sin(t * 4)) * (1.6 if after else 1)
        col = (140, 220, 255) if (after or dk < 0.3) else (150, 70, 200)
        for k in range(6, 0, -1):
            r = 70 + k * 22 * (1.2 if held else 1)
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col + (int(min(255, 16 * g * (7 - k))),))
    layer(img, aura)
    cr = CRYD if (dk > 0.35 and not after) else CRY
    img.alpha_composite(cr, (int(cx - cr.width / 2), int(cy - cr.height / 2)))
    # hold ring + arrow (ring already part-filled on frame 0)
    if t < T_POP:
        prog = min(1, 0.15 + 0.85 * t / T_POP); a = 255      # review: the thumb drives it, fills slowly through the build
        def ring(d):
            d.arc([CX - 150, CY - 150, CX + 150, CY + 150], 0, 360, fill=(255, 255, 255, min(a, 110)), width=12)
            d.arc([CX - 150, CY - 150, CX + 150, CY + 150], -90, -90 + 360 * prog, fill=(150, 240, 120, a), width=14)
        layer(img, ring)
        if not held:
            ay = CY - 200 + 10 * math.sin(t * 6 + 1.2); d = ImageDraw.Draw(img)
            d.polygon([(CX - 32, ay), (CX + 32, ay), (CX, ay + 40)], fill=(255, 255, 255), outline=(20, 15, 35), width=5)
            d.rectangle([CX - 12, ay - 40, CX + 12, ay], fill=(255, 255, 255), outline=(20, 15, 35), width=5)
    # dark energy: seeps out from under the thumb and swirls around it, thicker and wider over time
    if T_DARK <= t < T_POP + 0.02:
        Q = 6                                                     # drawn at 1/6 and scaled up: chunky pixel smoke
        sm = Image.new('RGBA', (W // Q, H // Q), (0, 0, 0, 0)); d = ImageDraw.Draw(sm)
        blobs = []
        for a0, ph, s_, sp, col in DARK:
            if ph > dk * 1.1: continue                           # more of it as time goes on
            life = (t * 0.35 * sp + ph) % 1.0
            rad = 100 + life * (140 + 340 * dk)
            ang = a0 + t * 1.6 * sp + life * 2.5
            x = cx + rad * math.cos(ang); y = cy + rad * math.sin(ang) * 0.9 - life * 60
            al = min(1, life / 0.15) * min(1, (1 - life) / 0.3)
            blobs.append((x, y, s_ * 1.5, al))
        for k in range(18):                                        # wisps pulled straight up out of the crystal
            life = (t * 0.9 + k / 18) % 1.0
            x = cx + (60 + 140 * dk) * math.sin(k * 2.1 + t * 3); y = cy - 40 - life * (220 + 160 * dk)
            blobs.append((x, y, 30 + 30 * dk, 1 - life))
        for x, y, r_, al in blobs:                                 # purple rim
            r_ = (r_ / 2 + 10) / Q; d.ellipse([x / Q - r_, y / Q - r_, x / Q + r_, y / Q + r_], fill=(110, 40, 150, int(150 * al)))
        for x, y, r_, al in blobs:                                 # dark core
            r_ = (r_ / 2) / Q; d.ellipse([x / Q - r_, y / Q - r_, x / Q + r_, y / Q + r_], fill=(22, 8, 34, int(235 * al)))
        img.alpha_composite(sm.resize((W, H), Image.NEAREST))
    # burst: flash, petals and hearts fly out where the dark energy was
    if after:
        u = t - T_POP
        if u < 0.35: layer(img, lambda d: d.rectangle([0, 0, W, H], fill=(255, 255, 255, int(230 * (1 - u / 0.35)))))
        if u < 0.6:   # the burst comes out of the crystal under the thumb
            layer(img, lambda d: [d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 245, 255, int(255 * (1 - u / 0.6))), width=18) for r in (150 + u * 1400, 90 + u * 900) if r > 0])
        def pet(d):
            for a0, v, col, s, wob in PET:
                x = cx + math.cos(a0) * v * u * (1 - 0.35 * u); y = cy + math.sin(a0) * v * u * (1 - 0.35 * u) + 260 * u * u
                x += 20 * math.sin(t * 6 + wob * 5)
                if -40 < y < H:
                    if s == 18: heart(d, x, y, 4, col + (255,))
                    else: d.rectangle([x - s / 2, y - s / 2, x + s / 2, y + s / 2], fill=col + (255,))
        layer(img, pet)
        def hearts(d):
            for k in range(7):
                life = (u * 0.5 + k / 7) % 1.0
                if u < 0.3: continue
                x = JX + 40 + 70 * math.sin(k * 1.7 + t * 2); y = JY - 380 - life * 300
                heart(d, x, y, 5, (255, 110, 150, int(255 * min(1, (1 - life) / 0.3))))
        layer(img, hearts)
    # Joy
    if after: fr = VIC[int((t - T_POP) * 10) % len(VIC)]
    else: fr = JIDLE[int(t * 8) % len(JIDLE)]                            # Syeda's idle; she reacts with the victory pose at the burst
    layer(img, lambda d: d.ellipse([JX - 90, JY - 18, JX + 90, JY + 16], fill=(0, 0, 0, 80)))
    img.alpha_composite(fr, (JX - fr.width // 2, JY - 78 * JS))
    # hook; at the payoff the same fade carries the result
    if after:
        u = t - T_POP
        if u < 0.12: img.alpha_composite(HOOK)
        else: img.alpha_composite(END1)
    else:
        img.alpha_composite(HOOK)
    return img
if TEST:
    for ts in sys.argv[1:]: frame(int(float(ts) * FPS)).convert('RGB').save(f't_{ts}.png')
    sys.exit()
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v31_noaudio.mp4'], stdin=subprocess.PIPE)
for f in range(N): ff.stdin.write(frame(f).convert('RGB').tobytes())
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open('v31_events.json', 'w')); print('done', N, DUR)
