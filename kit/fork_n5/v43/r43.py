# n5 rework of #43 (Bennett Oct 29: "same as before. doesnt break expectations").
# New story: 1 HP Hollow fights through a gauntlet to the save point (job: will he make it?), an angry King Slime slams down
# in front of the crystal, then turns out to be friendly and the camera reveals the four guides partying at a campfire by the
# save crystal. Hearts refill, Rayleigh tosses a melatonin gummy, he dozes off by the fire. Base: fork_hfg4/v43/r43.py.
# usage: python3 r43.py [preview t1 t2 ...]
import sys, os, glob
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
from PIL import ImageChops
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_fade
HOOK, HB = hook_fade(['1 HP LEFT.', 'WILL HE MAKE IT?'], accent=0, color=(255, 92, 92), size=64)
K = 5; KS = 4
def frames(d, k=K): return [up(Image.open(p).convert('RGBA'), k) for p in sorted(glob.glob(SP0 + d + '/*.png'))]
SRUN = frames('pixellab/maze/anim/hollow_srun'); PANIC = frames('pixellab/maze/anim/hollow_panic')
SLIDE = frames('pixellab/maze/anim/hollow_slide'); PUNCH = frames('fork_b5/hollow_punch2')
SIT = frames('fork_a4/hollow_sit'); EAT = frames('fork3/hollow_eat'); HIDLE = idle('hollow', K)
JOY = frames('fork2/joy_clap'); CYR = frames('fork2/cyrus_dance'); CLEO = frames('fork2/cleo_stomp')
RDANCE = frames('fork2/ray_dance'); RCAST = frames('fork3/ray_cast')
GI = {'joy': idle('joy', K), 'cyrus': idle('cyrus', K), 'cleo': idle('cleo', K), 'ray': idle('ray', K)}
KL = frames('pixellab/king/king_land', KS); KI = frames('pixellab/king/king_idle', KS)
K2L = frames('pixellab/king/king2_land', KS); K2I = frames('pixellab/king/king2_idle', KS)
SL1 = frames('pixellab/race/slime_idle_c', 4); SL2 = frames('fork_b10/mslime', 6)
FIRE = frames('fork_b8/fire_anim', 4)
CRY = up(crop(Image.open(SP0 + 'fork_a3/crystal/05.png').convert('RGBA')), 4)
MEL = gummy('mel', 4)
P0X = (PUNCH[0].getbbox()[0] + PUNCH[0].getbbox()[2]) / 2 / K     # punch canvas: character centre in frame 0

# background: Liza/Syeda moon temple (recov_hd), whole width, camera pans in world coords (world = bg * SC)
BGI = Image.open(A + 'recov_hd.gif'); BGF = []
for i in range(BGI.n_frames): BGI.seek(i); BGF.append(BGI.convert('RGB'))
SC = 1920 / 1080; Y0 = 180                                   # rows 180..1080 -> screen 0..1600, rows 900..1080 repeat below
def bg(t, cam):
    fr = BGF[int(t * 8) % len(BGF)]; bx = cam / SC; bw = W / SC
    top = fr.resize((W, 1600), Image.NEAREST, box=(bx, Y0, bx + bw, 1080))
    bot = fr.resize((W, 320), Image.NEAREST, box=(bx, 900, bx + bw, 1080))
    o = Image.new('RGBA', (W, H)); o.paste(top.convert('RGBA'), (0, 0)); o.paste(bot.convert('RGBA'), (0, 1600)); return o

G = 1380; GB = 1150                     # front row / run ground, back row ground
def put(img, spr, sx, foot, base=78, cx=46, k=K):
    img.alpha_composite(spr, (int(sx - cx * k), int(foot - base * k)))
def sm(a, b, t):
    u = min(1.0, max(0.0, (t - a) / (b - a))); return u * u * (3 - 2 * u)

# ---- timeline (s)
V = 400; X0 = 723
PFPS = 20; T_P0, T_P1 = 0.85, 0.85 + 0.9   # fiery punch (slime 1): he STOPS ~0.9s to throw it (Bennett: shoves/hits stop for the animation)
PD = T_P1 - (0.85 + 13 / 30)              # everything after the punch shifts by this
T_S0 = 1.85 + PD; T_S1 = T_S0 + 9 / 22        # slide under slime 2
T_STOP = 2.9 + PD; T_KF = 2.75 + PD; T_KL = 2.95 + PD  # King Slime falls / lands
T_TW = 4.0 + PD                              # twist: King Slime is friendly
T_PAN0, T_PAN1 = 4.4 + PD, 5.3 + PD
T_KX = 4.0 + PD + 0.6 + 1.2
T_HEART = [5.35 + PD, 5.5 + PD, 5.65 + PD]
T_CAST = 5.8 + PD; T_G0, T_G1 = 5.95 + PD, 6.45 + PD; T_EAT1 = T_G1 + 13 / 30; T_SIT = T_EAT1 + 0.02; T_Z = T_SIT + 0.35
T_XF = 0.3
def hx_run(t):
    """Hollow world x during the run (0..T_STOP)"""
    x = X0; tt = min(t, T_STOP)
    x += V * min(tt, T_P0)
    if tt > T_P1: x += V * (min(tt, T_S0) - T_P1)
    if tt > T_S0: x += 1.3 * V * (min(tt, T_S1) - T_S0)
    if tt > T_S1: x += V * (tt - T_S1)
    return x
HX_STOP = hx_run(T_STOP)                # ~1760
CAM_K = HX_STOP - 400
CAM_E = CAM_K + 800
XC = CAM_E + 150                        # save crystal (world)
HX_E = CAM_E + 270                      # where he sits (world)
XK = CAM_K + 790                        # King Slime landing (world)
PARTY = {'joy': (CAM_E + 455, GB), 'cyrus': (CAM_E + 665, GB), 'cleo': (CAM_E + 875, GB), 'ray': (CAM_E + 770, G)}
XF = CAM_E + 530                        # campfire (front row)
CXPIN = 975                             # waypoint x for the crystal before it scrolls into view
def cam_at(t):
    if t < T_PAN0: return hx_run(t) - (300 + 100 * sm(2.3 + PD, T_STOP, t))
    return CAM_K + (CAM_E - CAM_K) * sm(T_PAN0, T_PAN1, t)
def hollow_x(t):
    if t < T_PAN0: return hx_run(t)
    return HX_STOP + (HX_E - HX_STOP) * sm(T_PAN0, T_PAN1 - 0.05, t)
HPX = HX_STOP * 0 + 0
H_P = hx_run(T_P0); SL1_HIT = H_P + 300; T_HIT = T_P0 + 4 / PFPS
H_S = hx_run(T_S0 + 0.2)

def heart(d, x, y, full, s=8, a=255):
    pat = ['.XX.XX.', 'XXXXXXX', 'XXXXXXX', '.XXXXX.', '..XXX..', '...X...']
    for r, row in enumerate(pat):
        for c, ch in enumerate(row):
            if ch == 'X':
                d.rectangle([x + c * s - 3, y + r * s - 3, x + c * s + s + 2, y + r * s + s + 2], fill=(12, 8, 20, a))
    for r, row in enumerate(pat):
        for c, ch in enumerate(row):
            if ch == 'X':
                col = (235, 60, 70, a) if full else (60, 50, 70, a)
                if full and r == 1 and c in (1, 2): col = (255, 170, 170, a)
                d.rectangle([x + c * s, y + r * s, x + c * s + s - 1, y + r * s + s - 1], fill=col)

def render(f):
    t = f / FPS; cam = cam_at(t)
    img = bg(t, cam)
    S_ = lambda wx: wx - cam
    # save crystal (world XC), bobbing over a glow on the back-row ground
    flash = 0.0
    if t >= T_HEART[0]: flash = max(0.0, 1 - abs(t - T_HEART[0] - 0.15) / 0.5)
    if t >= T_SIT: flash = max(flash, 0.6 * max(0.0, 1 - abs(t - T_SIT - 0.3) / 0.5))
    cx = S_(XC); cy = GB - 250 + 10 * math.sin(t * 2.6)
    pinned = cx > CXPIN
    if pinned: cx = CXPIN                       # review fix: the save crystal waits at the far end from 0.0s
    if -250 < cx < W + 250:
        def glow(d):
            for r, a in ((150, 35), (110, 60), (80, 90)):
                aa = int(min(255, a * (1 + 2.2 * flash))); d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 210, 255, aa))
            d.ellipse([cx - 95, GB - 20, cx + 95, GB + 12], fill=(120, 190, 255, int(70 + 120 * flash)))
            for k in range(8):
                ph = (t * 0.6 + k * 0.125) % 1.0; sx = cx + 70 * math.sin(k * 2.4 + t); sy = cy + 80 - ph * 260
                d.rectangle([sx - 4, sy - 4, sx + 4, sy + 4], fill=(220, 240, 255, int(220 * (1 - ph))))
        layer(img, glow)
        img.alpha_composite(CRY, (int(cx - CRY.width / 2), int(cy - CRY.height / 2)))
        if pinned:                              # waypoint chevrons pointing at it
            def chev(d):
                for j in range(2):
                    ph = (t * 2 + j * 0.5) % 1.0; x0 = cx - 150 + 40 * j + 20 * ph; a = int(230 * (1 - abs(ph - 0.5) * 1.4))
                    d.line([(x0, cy - 26), (x0 + 22, cy), (x0, cy + 26)], fill=(200, 235, 255, a), width=9)
            layer(img, chev)
    # King Slime hopping off on the ground: drawn behind the party
    if T_TW + 0.6 <= t < T_KX:
        u = t - (T_TW + 0.6); wx = XK + 1700 * u; y = G - 156 * KS - 150 * abs(math.sin(math.pi * u / 0.42))
        spr = K2I[int(t * 8) % len(K2I)]
        img.alpha_composite(spr, (int(S_(wx) - 80 * KS), int(y)))
    # party (back row first), dancing until he falls asleep, then idle
    asleep = t >= T_SIT + 0.2
    for g, spr in (('joy', JOY), ('cyrus', CYR), ('cleo', CLEO)):
        wx, ft = PARTY[g]; sx = S_(wx)
        if sx < -200 or sx > W + 200: continue
        seqs = GI[g] if asleep else spr
        put(img, seqs[int(t * (8 if asleep else 12)) % len(seqs)], sx, ft)
    # campfire (front row)
    fx = S_(XF)
    if -200 < fx < W + 200:
        def fglow(d):
            a = int(60 + 20 * math.sin(t * 9))
            d.ellipse([fx - 210, G - 260, fx + 210, G + 40], fill=(255, 150, 60, a // 2))
        layer(img, fglow)
        fr = FIRE[int(t * 12) % len(FIRE)]; img.alpha_composite(fr, (int(fx - fr.width / 2), int(G - 60 * 4 + 6)))
    # Rayleigh (front row): dances, casts the gummy toss, then idles
    rx = S_(PARTY['ray'][0])
    if -200 < rx < W + 200:
        if T_CAST <= t < T_CAST + 9 / 30: spr = RCAST[min(len(RCAST) - 1, int((t - T_CAST) * 30))]
        elif t >= T_CAST: spr = GI['ray'][int(t * 8) % len(GI['ray'])]
        else: spr = RDANCE[int(t * 12) % len(RDANCE)]
        put(img, spr, rx, G)
    # slime 1: hops in, takes the fiery punch, flies off spinning
    if 0.15 <= t < T_HIT + 0.6:
        if t < T_HIT:
            u = (t - 0.15) / (T_HIT - 0.15); wx = SL1_HIT + 560 * (1 - u)
            hop = abs(math.sin(u * math.pi * 2)) * 120
            spr = SL1[int(t * 12) % len(SL1)]; img.alpha_composite(spr, (int(S_(wx) - spr.width / 2), int(G - 62 * 4 - hop)))
        else:
            v = t - T_HIT; wx = SL1_HIT + 1500 * v; y = G - 62 * 4 - 900 * v + 600 * v * v
            spr = SL1[0].rotate(-720 * v, resample=Image.NEAREST, expand=True)
            img.alpha_composite(spr, (int(S_(wx) - spr.width / 2), int(y)))
            if v < 0.12:
                def burst(d):
                    for k in range(10):
                        ang = k * 0.628; r = 60 + 500 * v
                        bx_, by_ = S_(SL1_HIT) + r * math.cos(ang), G - 120 + r * math.sin(ang)
                        d.rectangle([bx_ - 8, by_ - 8, bx_ + 8, by_ + 8], fill=(255, 220, 90, 230))
                layer(img, burst)
    # slime 2 (orange): flies at head height, he slides under it
    T_OVER = T_S0 + 0.2
    if 1.35 + PD <= t < 2.7 + PD:
        wx = H_S - 1100 * (t - T_OVER); y = G - 380 + 10 * math.sin(t * 25)
        spr = SL2[int(t * 15) % len(SL2)].transpose(Image.FLIP_LEFT_RIGHT)
        img.alpha_composite(spr, (int(S_(wx) - spr.width / 2), int(y)))
    # King Slime: shadow, fall, angry landing, then friendly, squash-stretch, hops off to the right
    if T_KF - 0.25 <= t < T_TW + 0.6:
        kx = S_(XK)
        if t < T_KL:
            def shadow(d):
                r = 60 + 160 * sm(T_KF - 0.25, T_KL, t); d.ellipse([kx - r, G - 18, kx + r, G + 14], fill=(0, 0, 0, 120))
            layer(img, shadow)
            if t >= T_KF:
                y = G - 156 * KS - 1500 * (1 - (t - T_KF) / (T_KL - T_KF)) ** 2
                img.alpha_composite(KI[0], (int(kx - 80 * KS), int(y)))
        else:
            if t < T_KL + 0.6: spr = KL[min(12, 1 + int((t - T_KL) / 0.6 * 12))]
            elif t < T_TW: spr = KI[int(t * 8) % len(KI)]
            elif t < T_TW + 0.3: spr = K2I[int(t * 8) % len(K2I)]
            elif t < T_TW + 0.6: spr = K2L[min(12, int((t - T_TW - 0.3) / 0.3 * 13))]
            else: spr = K2I[int(t * 8) % len(K2I)]
            y = G - 156 * KS; wx = XK
            img.alpha_composite(spr, (int(S_(wx) - 80 * KS), int(y)))
            if T_TW <= t < T_TW + 0.7:   # pink heart pop over the king (friendly reveal)
                v = t - T_TW
                def hp(d):
                    heart(d, kx - 28 + 40, G - 156 * KS - 40 - 120 * v, True, s=8, a=int(255 * min(1, (0.7 - v) / 0.2)))
                layer(img, hp)
    # the Hollow
    hx = S_(hollow_x(t))
    if t < T_STOP:
        if T_P0 <= t < T_P1: put(img, PUNCH[min(12, int((t - T_P0) * PFPS))], hx, G, base=104, cx=P0X)
        elif T_S0 <= t < T_S1:
            put(img, SLIDE[min(8, int((t - T_S0) * 22))], hx, G)
            def dust(d):
                for k in range(5):
                    dx = -40 - k * 30 - 200 * ((t * 3 + k * 0.2) % 1.0); a = int(160 * (1 - k / 5))
                    d.ellipse([hx + dx - 18, G - 30, hx + dx + 18, G], fill=(210, 200, 180, a))
            layer(img, dust)
        else: put(img, SRUN[int(t * 14) % len(SRUN)], hx, G)
    elif t < T_TW: put(img, PANIC[int(t * 12) % len(PANIC)], hx, G)
    elif t < T_PAN0: put(img, HIDLE[int(t * 8) % len(HIDLE)], hx, G)
    elif t < T_PAN1 - 0.05: put(img, SRUN[int(t * 14) % len(SRUN)], hx, G)
    elif t < T_G1: put(img, HIDLE[int(t * 8) % len(HIDLE)], hx, G)
    elif t < T_EAT1: put(img, EAT[min(12, int((t - T_G1) * 30))], hx, G)
    else: put(img, SIT[min(8, int((t - T_SIT) / 0.3 * 9))], hx, G)
    # melatonin gummy toss (Rayleigh -> Hollow)
    if T_G0 <= t < T_G1:
        u = (t - T_G0) / (T_G1 - T_G0); sx0 = rx + 145; sy0 = G - 230; sx1 = hx + 10; sy1 = G - 240
        gx = sx0 + (sx1 - sx0) * u; gy = sy0 + (sy1 - sy0) * u - 110 * math.sin(math.pi * u)
        img.alpha_composite(MEL, (int(gx - MEL.width / 2), int(gy - MEL.height / 2)))
        if u < 0.3:                             # magic burst at the staff tip as it launches
            def burst(d):
                for k in range(8):
                    a = k * 0.785; r = 20 + 220 * u
                    d.rectangle([sx0 + r * math.cos(a) - 6, sy0 + r * math.sin(a) - 6, sx0 + r * math.cos(a) + 6, sy0 + r * math.sin(a) + 6], fill=(220, 170, 255, int(255 * (1 - u / 0.3))))
            layer(img, burst)
    if T_G0 <= t < T_EAT1 + 0.3:
        a = int(255 * min(1, (t - T_G0) / 0.12, (T_EAT1 + 0.3 - t) / 0.2))
        text_layer(img, [(330, G - 640, 'SLEEP!', 64, (215, 185, 255), 9, a)])
    # Zzz while he sleeps
    if t >= T_Z:
        v = t - T_Z; items = []
        for (sz, dx, dy, t0) in [(52, 0, 0, 0.0), (66, 20, -85, 0.3), (84, 34, -185, 0.6)]:
            if v >= t0:
                a = int(255 * min(1, (v - t0) / 0.15)); wob = 8 * math.sin((t - t0) * 5)
                items.append((hx + dx + wob, G - 380 + dy, 'Z', sz, (240, 230, 255), 9, a))
        text_layer(img, items)
    # screen shake on the King's landing
    if T_KL <= t < T_KL + 0.3:
        a = 16 * (1 - (t - T_KL) / 0.3); img = ImageChops.offset(img, int(a * math.sin(t * 90)), int(a * math.cos(t * 70)))
    # HP hearts (HUD): 1 of 3, blinking while in danger, refill at the save point
    nfull = 1 + sum(1 for th in T_HEART if t >= th)
    danger = T_KF <= t < T_TW
    def hud(d):
        for i in range(3):
            full = i < nfull
            pop = 1 if (i == 0 and danger and int(t * 8) % 2) else 0
            if i >= 1 and T_HEART[i - 1] <= t < T_HEART[i - 1] + 0.2: pop = 1
            heart(d, 92 + i * 92 - pop * 4, HB + 36 - pop * 4, full, s=10 + pop)
            if i >= 1 and T_HEART[i - 1] <= t < T_HEART[i - 1] + 0.35:
                v = t - T_HEART[i - 1]
                for k in range(6):
                    ang = k * 1.047 + 0.3; r = 30 + 160 * v
                    px, py = 92 + i * 92 + 34 + r * math.cos(ang), HB + 60 + r * math.sin(ang)
                    d.rectangle([px - 5, py - 5, px + 5, py + 5], fill=(255, 200, 210, int(255 * (1 - v / 0.35))))
    layer(img, hud)
    ha = 1 - sm(T_PAN1 - 0.3, T_PAN1, t)
    if ha > 0.99: img.alpha_composite(HOOK)
    elif ha > 0.01:
        Hk = HOOK.copy(); Hk.putalpha(HOOK.getchannel('A').point(lambda v: int(v * ha))); img.alpha_composite(Hk)
    return img

T_END = T_Z + 0.75 + T_XF
NF = int(round(T_END * FPS)); NXF = int(round(T_XF * FPS))
_F0 = None
def frame(f):
    global _F0
    img = render(f)
    k = f - (NF - NXF)
    if k >= 0:
        if _F0 is None: _F0 = render(0)
        img = Image.blend(img, _F0, (k + 1) / (NXF + 1))
    return img
if len(sys.argv) > 1 and sys.argv[1] == 'preview':
    for ts in sys.argv[2:]:
        f = int(round(float(ts) * FPS)); frame(f).convert('RGB').save(f'pv_{f:04d}.png')
    sys.exit()
wr = Writer('v43_noaudio.mp4')
for f in range(NF):
    wr.write(frame(f))
wr.close()
ev = [(0.35, 'boing'), (T_HIT - 0.05, 'punch'), (T_HIT + 0.05, 'poof'), (T_S0, 'swish'), (T_KL, 'boom'), (T_KL + 0.05, 'stomp_8bit'),
      (T_TW, 'chime'), (T_TW + 0.6, 'jump'), (T_PAN0 + 0.5, 'cheer'), (T_HEART[0], 'powerup1'), (T_G0, 'swish'), (T_G1 + 0.05, 'squish'),
      (T_SIT + 0.1, 'twinkle')]
json.dump({'events': ev}, open('v43_ev.json', 'w')); print('done', NF)
