# rc6 recut of #47 (Bennett: safe zone only, keep as is). Source: fork_sz44/v47/render.py
# VETTING r047 (high priority): Cyrus (Energy guide) crashing under a Zzz read as "energy gummy = crash" -> Motivation recast to Joy
# (PixelLab joy_run + joy_ko from the race/king reels), she collapses with burnout smoke, no Zzz (Zzz only for melatonin sleep).
import sys, math, json, random, os, glob
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork1'); from common import *
sys.path.insert(0, SP0 + 'fork_rc1'); from hook2 import hook_layer2
os.chdir(os.path.dirname(os.path.abspath(__file__)))
K = 5; FOOTY = 78 * K                       # 3x -> 5x
RUN = seq(SP0 + 'pixellab/race/joy_run', K, 1, 9)
SLIDE = [up(Image.open(p).convert('RGBA'), K) for p in sorted(glob.glob(SP0 + 'pixellab/maze/anim/joy_slide/*.png'))]
KO = SLIDE[:4]                              # collapse into a slump (PixelLab joy_slide 0-3), lies on 3-6, gets up 7-8 on the rewind
WALK = seq(SP0 + 'fork_a5/gen/cleo_walk', K, 1, 9)
WIN = seq(SP0 + 'fork_a5/gen/cleo_win', K, 0, 9)
FLAG = up(crop(Image.open(SP0 + 'fork_a5/gen/flag/00.png').convert('RGBA')), 4).transpose(Image.FLIP_LEFT_RIGHT)
GUM = gummy('cre', 4)
HOOK, HB = hook_layer2(['MOTIVATION', 'VS DISCIPLINE'], accent=0, color=(120, 225, 90), border=(255, 214, 60), sub='Which one are you?')
print('hook bottom', HB)
PX0, PW = 70, 817
P1 = HB + 10; PH = (1498 - P1 - 10) // 2; P2 = P1 + PH + 10
TOP = bg_frames('sun_hd.gif', (PW, PH), box=(470, 170, 470 + 980, 170 + int(980 * PH / PW)), step=2, bright=0.8)
BOT = bg_frames('vit_hd.gif', (PW, PH), box=(470, 170, 470 + 980, 170 + int(980 * PH / PW)), step=2, bright=0.8)
GROUND = PH - 34; X0, XF = 190, 800
print('panels', P1, P2, P2 + PH, 'PH', PH)
MCOL = (120, 225, 90); DCOL = (100, 165, 255)
T_RUN_END, T_KO = 2.0, 2.0; KO_D = 0.5; T_BURN = T_KO + KO_D       # sprint 0-2.0s, collapse 2.0-2.5s, BURNED OUT 2.5s
XJ = 470
T_ARR = 6.6; T_FIN = T_ARR; HOLD = 1.3; RW = 0.3                    # Cleo at the flag 6.6s, FINISHED, hold, rewind (loop)
DUR = T_ARR + HOLD + RW + 0.2; NF = int(round(DUR * FPS)); T_RW = DUR - RW
GX = [330, 460, 590, 720]
wr = Writer('v47_noaudio.mp4'); ev = []; popped = {}
def put(img, spr, x, gy, foot):
    img.alpha_composite(spr, (int(x - spr.width / 2), int(gy - foot)))
def stamp(img, cx, cy, txt, col, u, size=72):
    sc = 1.0 if u > 0.12 else 0.7 + 2.5 * u
    s = int(size * sc)
    def pl(d):
        w = d.textlength(txt, font=F(s)); d.rounded_rectangle([cx - w / 2 - 26, cy - 22, cx + w / 2 + 26, cy + s + 24], 18, fill=(14, 10, 24, 235), outline=col + (255,), width=7)
    layer(img, pl); text_layer(img, [(cx, cy, txt, s, col, 10, 255)])
for f in range(NF):
    t = f / FPS
    rw = t >= T_RW; ur = min(1.0, (t - T_RW) / (RW - 1 / FPS)) if rw else 0
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    for py, bgs, lab, col in ((P1, TOP, 'MOTIVATION', MCOL), (P2, BOT, 'DISCIPLINE', DCOL)):
        img.alpha_composite(bgs[int(t * 5) % len(bgs)], (PX0, py))
        layer(img, lambda d: (d.rectangle([PX0, py + GROUND + 4, PX0 + PW - 1, py + PH - 1], fill=(14, 10, 24, 90)), d.rectangle([PX0, py, PX0 + PW - 1, py + PH - 1], outline=col + (255,), width=8)))
        layer(img, lambda dd: dd.rounded_rectangle([PX0 + 20, py + 20, PX0 + 20 + dd.textlength(lab, font=F(44)) + 36, py + 94], 16, fill=(14, 10, 24, 210)))
        d = ImageDraw.Draw(img); d.text((PX0 + 38, py + 36), lab, font=F(44), fill=col, stroke_width=6, stroke_fill=(20, 15, 35))
        img.alpha_composite(FLAG, (PX0 + PW - 16 - FLAG.width, py + GROUND - FLAG.height + 8))
    # --- Joy = Motivation (top): sprints from frame 0, burns out
    gy = P1 + GROUND
    if rw:
        x = XJ + (X0 - XJ) * ur; spr = SLIDE[7] if ur < 0.35 else (SLIDE[8] if ur < 0.7 else RUN[0]); foot = FOOTY
    elif t < T_RUN_END:
        u = t / T_RUN_END; x = X0 + (XJ - X0) * (u ** 0.8); spr = RUN[int(t * 22) % 8]; foot = FOOTY
        layer(img, lambda dd: [dd.ellipse([x - 80 - q * 34 - (t * 300 % 30), gy - 14 - q * 5, x - 44 - q * 34 - (t * 300 % 30), gy + 4], fill=(230, 210, 170, 150 - q * 40)) for q in range(3)])
    else:
        x = XJ; k = min(len(KO) - 1, int((t - T_KO) / KO_D * len(KO))); spr = KO[k] if t < T_BURN else SLIDE[3 + int((t - T_BURN) * 3) % 4]
        foot = spr.getbbox()[3]                       # lying frames sit on the ground (no float)
        if t >= T_BURN:                               # burnout smoke (no Zzz: those are melatonin-only)
            u = t - T_BURN
            layer(img, lambda dd: [dd.ellipse([x - 20 + 30 * math.sin(u * 3 + q) - (8 + ((u * 0.9 + q / 4) % 1) * 30), gy - 110 - ((u * 0.9 + q / 4) % 1) * 170 - (8 + ((u * 0.9 + q / 4) % 1) * 30),
                                                   x - 20 + 30 * math.sin(u * 3 + q) + (8 + ((u * 0.9 + q / 4) % 1) * 30), gy - 110 - ((u * 0.9 + q / 4) % 1) * 170 + (8 + ((u * 0.9 + q / 4) % 1) * 30)],
                                                  fill=(150, 150, 160, int(170 * (1 - (u * 0.9 + q / 4) % 1)))) for q in range(4)])
    layer(img, lambda dd: dd.ellipse([x - 60, gy - 12, x + 60, gy + 12], fill=(0, 0, 0, 80)))
    put(img, spr, x, gy, foot)
    if f == 0: ev.append((0.0, 'swish'))
    if abs(t - T_KO - 0.35) < 0.5 / FPS: ev.append((round(t, 3), 'punch'))
    if abs(t - T_BURN) < 0.5 / FPS: ev.append((round(t, 3), 'poof'))
    # --- Cleo = Discipline (bottom): steady walk, stacks creatine gummies
    gy = P2 + GROUND
    for i, gxp in enumerate(GX):
        if not rw and i in popped and t >= popped[i]:
            u = t - popped[i]
            if u < 0.9: text_layer(img, [(gxp, gy - 330 - u * 40, '+1', 60, (140, 200, 255), 8, int(255 * min(1, (0.9 - u) / 0.3)))])
            if u < 0.4:
                layer(img, lambda dd: [dd.rectangle([gxp + (20 + 110 * u) * math.cos(q * 0.785) - 6, gy - 80 + (20 + 110 * u) * math.sin(q * 0.785) - 6,
                                                     gxp + (20 + 110 * u) * math.cos(q * 0.785) + 6, gy - 80 + (20 + 110 * u) * math.sin(q * 0.785) + 6], fill=(190, 225, 255, int(255 * (1 - u / 0.4)))) for q in range(8)])
            continue
        bob = int(8 * math.sin(t * 4 + i))
        layer(img, lambda dd: dd.ellipse([gxp - 52, gy - 132 + bob, gxp + 52, gy - 28 + bob], fill=(120, 180, 255, 60)))
        img.alpha_composite(GUM, (int(gxp - GUM.width / 2), int(gy - 80 - GUM.height / 2 + bob)))
    XC_END = XF - 70
    if rw:
        x = XC_END + (X0 - XC_END) * ur; spr = WALK[0]
    elif t < T_ARR:
        x = X0 + (XC_END - X0) * t / T_ARR; spr = WALK[int(t * 9) % 8]
        for i, gxp in enumerate(GX):
            if i not in popped and x >= gxp - 10: popped[i] = t; ev.append((round(t, 3), 'coin_8bit'))
    else:
        x = XC_END; spr = WIN[min(8, int((t - T_ARR) * 10))]
        if abs(t - T_ARR) < 0.5 / FPS: ev.append((round(t, 3), 'victory'))
        layer(img, lambda dd: [dd.rectangle([x + 60 + 90 * math.cos(t * 3 + q * 1.26), gy - 330 + 70 * math.sin(t * 3 + q * 1.26), x + 70 + 90 * math.cos(t * 3 + q * 1.26), gy - 320 + 70 * math.sin(t * 3 + q * 1.26)], fill=(255, 230, 120, 230)) for q in range(5)])
    layer(img, lambda dd: dd.ellipse([x - 60, gy - 12, x + 60, gy + 12], fill=(0, 0, 0, 80)))
    put(img, spr, x, gy, FOOTY)
    # big event stamps (one per lane, never overlapping)
    if T_BURN <= t < T_RW: stamp(img, PX0 + PW / 2, P1 + 120, 'BURNED OUT', (255, 110, 80), t - T_BURN)
    if T_FIN <= t < T_RW: stamp(img, 350, P2 + 130, 'FINISHED', (255, 214, 60), t - T_FIN, 60)   # left of Cleo's victory pose
    if rw:   # rewind streaks while both lanes snap back to the start pose
        layer(img, lambda dd: [dd.rectangle([PX0, py + 40 + q * 70, PX0 + PW - 1, py + 46 + q * 70], fill=(255, 255, 255, int(70 * (1 - ur)))) for py in (P1, P2) for q in range(6)])
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (0, 30, 62, 75, 140, 200, 240, NF - 1): img.convert('RGB').save(f'p47_{f:04d}.png')
wr.close()
ev.append((round(T_RW, 3), 'rewind'))
json.dump({'events': ev}, open('v47_ev.json', 'w')); print('done', DUR, NF, ev)
