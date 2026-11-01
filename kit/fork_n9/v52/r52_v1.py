"""#52 Which duo are you: review recut (fork_rc15). Source fork_c4/v52/r52.py.
Name tags ~2x (44-48px, long ones on two lines, all inside the safe zone), TAG YOUR OTHER HALF as a 44px+ band line from frame 0
(same band all reel, so the loop is seamless), planner cards 22px -> 44px (two cards), bubbles/+1 STR >= 44px, end hold 1.9 -> 1.3s with
a hop wave, SFX on events only (no whoosh metronome), ACV gloss + ACV GUMMY tag on the lineup. No Joy teeth (Syeda joy-talk.gif kept)."""
import sys, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
OUT = SP0 + 'fork_n9/v52/'
os.chdir(SP0 + 'fork_b5/v52'); sys.path.insert(0, SP0 + 'fork1'); sys.path.insert(0, SP0 + 'pixellab/safezone'); sys.path.insert(0, SP0 + 'fork_rc2')
from common import *
from rc2 import hook_layer2, acv_gloss, acv_tag
from hook import hook_fade
# hfg5: soft fade, no box; 'TAG YOUR OTHER HALF' sub cut (caption asks)
HK1, HB1 = hook_fade(['WHICH DUO', 'ARE YOU?'], accent=1); print('HB', HB1)
K = 5; FOOT = 78 * K
def native(path, n=92):
    return [f.resize((n, n), Image.NEAREST) for f in gif_frames(path)]
def anim(d, lo=1, hi=9): return seq('../' + d, K, lo, hi)
def notooth(d, box, lo=1, hi=9):
    out = []
    for p in sorted(glob.glob('../' + d + '/*.png'))[lo:hi]:
        im = Image.open(p).convert('RGBA'); px = im.load()
        for x in range(box[0], box[2]):
            for y in range(box[1], box[3]):
                r, g, b_, al = px[x, y]
                if al and r > 235 and g > 225 and b_ > 215: px[x, y] = (106, 38, 9, 255)   # Syeda-style dark open mouth, no teeth
        out.append(up(im, K))
    return out
JOY_TALK = [up(f, K) for f in native(SP + 'fork_c4/talk/joy-talk.gif')]
HOL_NOD = anim('hollow_nod'); CY_LIFT = anim('cyrus_lift'); JOY_STR = notooth('joy_stretch', (40, 28, 51, 36))
CLEO_READ = anim('cleo_read'); CY_SHRUG = notooth('cyrus_shrug', (43, 33, 49, 37))
# n9: early bird Joy = Syeda's own victory pose (staff sparkle), not the PixelLab yawn with a recoloured mouth (Joy's face only as Syeda drew it)
JOY_VIC = [up(f, K) for f in native(A + VIC['joy'])]
RAY_CAST = seq('../../fork3/ray_cast', K, 1, 9)
CLEO_VIC = [up(f, K) for f in native(A + VIC['cleo'])]
HOL_WALK = [up(f, K) for f in native(A + 'hollow-walk-side.gif')]
BED = [up(f.resize((128, 128), Image.NEAREST), 4) for f in gif_frames(SP + 'pixellab/ray/rayleigh_sleeping_v3.gif')]
IDL = {g: idle(g, 3) for g in ['joy', 'cyrus', 'cleo', 'ray', 'hollow']}
BGS = {
 'hub': bg_frames('hub.gif', (W, H), box=(560, 0, 1167, 1080), step=2, bright=0.85),
 'found': bg_frames('found_hd.gif', (W, H), box=(660, 0, 1267, 1080), step=2, bright=0.85),
 'sun': bg_frames('sun_hd.gif', (W, H), box=(660, 0, 1267, 1080), step=2, bright=0.85),
 'vit': bg_frames('vit_hd.gif', (W, H), box=(560, 0, 1167, 1080), step=2, bright=0.85),
 'moon': bg_frames('recov_hd.gif', (W, H), box=(690, 0, 1297, 1080), step=2, bright=0.8),
}
def gum(k, s):
    g0 = Image.open(PL + f'gummies/pick_{k}.png').convert('RGBA')
    return up(acv_gloss(g0) if k == 'acv' else g0, s)
G = {k: gum(k, 3) for k in ['mush', 'acv', 'mel', 'cre', 'gold']}
G2 = {k: gum(k, 2) for k in ['acv', 'mel']}
SC = [('intro', 0.6), ('yap', 2.2), ('gym', 2.2), ('main', 2.2), ('owl', 2.2), ('plan', 2.2), ('outro', 1.3)]
T0 = []; acc = 0
for n, d in SC: T0.append(acc); acc += d
DUR = acc; NF = int(round(DUR * FPS))
TITLE = {'yap': ('YAPPER', 'LISTENER'), 'gym': ('GYM RAT', 'BED ROT'), 'main': ('MAIN CHARACTER', 'SIDE QUEST'), 'owl': ('NIGHT OWL', 'EARLY BIRD'), 'plan': ('PLANNER', 'WINGER')}
# tags: 2x the old 24-28px; long names split on two lines so they stay inside x70..887 (lower section)
TAGL = {'MAIN CHARACTER': ['MAIN', 'CHARACTER'], 'SIDE QUEST': ['SIDE', 'QUEST'], 'NIGHT OWL': ['NIGHT', 'OWL'], 'EARLY BIRD': ['EARLY', 'BIRD']}
HUB_FOOT = 1195   # n9: hub street line behind the fountain rim (fountain water starts ~y1290, rim top ~y1225)
GY = 1330      # feet (was 1405) so two-line tags end above y1500
XL, XR = 285, 690
OWL_RAY = 1075   # n9: night half ground = stone steps above the pool (pool spans ~y1093-1387)
def put(img, spr, cx, foot=None):
    foot = GY if foot is None else foot; img.alpha_composite(spr, (int(cx - spr.width / 2), int(foot - FOOT)))
def tags(img, a, b, xa=XL, xb=XR, gy=None):
    gy = GY if gy is None else gy
    items = []; boxes = []
    for nm, x, col in ((a, xa, (255, 214, 60)), (b, xb, (255, 255, 255))):
        if not nm: continue
        ls = TAGL.get(nm, [nm]); fs = 48 if max(len(l) for l in ls) <= 7 else 44
        w = max(len(l) for l in ls) * fs; h = len(ls) * fs + (len(ls) - 1) * 12
        y0 = gy + 22
        boxes.append([x - w / 2 - 20, y0, x + w / 2 + 20, y0 + h + 30])
        for i, l in enumerate(ls): items.append((x, y0 + 15 + i * (fs + 12), l, fs, col, 6, 255))
    text_layer(img, [it[:5] + (8,) + it[6:] for it in items])     # hfg5: no plates, thicker stroke
def header(img, a, b, u):
    return   # hfg5: 'X & Y' header plate cut: it repeated the two name tags under the characters
ev = [(0.05, 'chime')]
LOOPK = max(1, round(DUR * 4 / (2 * math.pi)))   # gummy bob completes whole cycles over the reel -> seamless loop
wr = Writer(OUT + 'v52_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    si = max(i for i in range(len(SC)) if T0[i] <= t + 1e-6); name = SC[si][0]; u = t - T0[si]
    fi = int(t * 9)
    if name in ('intro', 'outro'):
        img = BGS['hub'][(int(t * 6) % len(BGS['hub'])) if name == 'intro' else (int(u * 6) % len(BGS['hub']))].copy()
        xs = [150, 320, 490, 650, 810]
        for i, (g, x) in enumerate(zip(['joy', 'cyrus', 'cleo', 'ray', 'hollow'], xs)):
            fr = IDL[g][(fi if name == 'intro' else int(u * 9)) % len(IDL[g])]
            if name == 'intro':
                hop = int(50 * max(0, math.sin(math.pi * min(1, max(0, (u - i * 0.06) / 0.3)))))
            else:   # small hop wave mid-hold, settled again for the last 0.35s so the cut back to frame 0 is seamless
                hop = int(30 * max(0, math.sin(math.pi * min(1, max(0, (u - 0.25 - i * 0.07) / 0.3)))))
            img.alpha_composite(fr, (int(x - fr.width / 2), int(HUB_FOOT - 78 * 3 - hop)))   # n9: on the street, not in the fountain
        for k, x in zip(['acv', 'mush', 'cre', 'mel', 'gold'], xs):
            g = G[k]; bob = 8 * math.sin(2 * math.pi * LOOPK * t / DUR + x); img.alpha_composite(g, (int(x - g.width / 2), int(HUB_FOOT - 78 * 3 - 30 - g.height + bob)))
        # hfg5: ACV GUMMY tag on the lineup cut (label)
    elif name == 'yap':
        img = BGS['found'][int(t * 6) % len(BGS['found'])].copy()
        put(img, JOY_TALK[int(t * 10) % len(JOY_TALK)], XL); put(img, HOL_NOD[(fi // 2) % 8], XR)
        syms = ['!', '?!', '...', '!!', 'OMG', 'AND', 'WAIT']
        for k in range(6):
            uu = (u * 2.6 - k * 0.38)
            if 0 < uu < 1.2:
                if k in (0, 3) and uu - 2.6 / FPS <= 0: ev.append((round(t, 3), 'boing'))
                x = 330 + 60 * math.sin(k * 2.1) + 120 * uu * (1 if k % 2 else -1) * 0.4; y = GY - FOOT + 40 - uu * 150
                al = int(255 * min(1, (1.2 - uu) / 0.4))
                layer(img, lambda d, x=x, y=y, al=al: d.rounded_rectangle([x - 115, y - 50, x + 115, y + 42], 20, fill=(255, 255, 255, al), outline=(20, 15, 35, al), width=5))
                text_layer(img, [(x, y - 26, syms[k], 46, (40, 30, 60), 0, al)])
        header(img, *TITLE['yap'], u); tags(img, *TITLE['yap'])
    elif name == 'gym':
        img = BGS['sun'][int(t * 6) % len(BGS['sun'])].copy()
        put(img, CY_LIFT[fi % 8], XL - 30)
        bd = BED[int(t * 8) % len(BED)]; img.alpha_composite(bd, (int(XR - bd.width / 2), int(GY + 60 - bd.height)))
        for k in range(3):
            uu = (u * 1.8 - k * 0.55) % 1.6
            if uu < 1: text_layer(img, [(255 + (k - 1) * 50, GY - FOOT - 20 - uu * 120, '+1 STR', 48, (255, 200, 80), 7, int(255 * (1 - uu)))])
        for k in range(3):
            uu = (u * 1.2 + k * 0.33) % 1
            text_layer(img, [(XR + 30 + 40 * k + uu * 40, GY - 330 - uu * 160 - k * 20, 'Z', 46 + k * 12, (230, 210, 255), 7, int(255 * (1 - uu)))])
        g = G['cre']; img.alpha_composite(g, (XL + 60, int(GY - 60 + 6 * math.sin(t * 5))))
        if abs(u - 0.3) < 0.5 / FPS: ev.append((round(t, 3), 'stomp_8bit'))
        header(img, *TITLE['gym'], u); tags(img, *TITLE['gym'])
    elif name == 'main':
        img = BGS['vit'][int(t * 6) % len(BGS['vit'])].copy()
        layer(img, lambda d: d.polygon([(XL - 60, 0), (XL + 60, 0), (XL + 190, GY + 20), (XL - 160, GY + 20)], fill=(255, 240, 180, 70)))
        put(img, CLEO_VIC[(fi // 2) % len(CLEO_VIC)], XL)
        for k in range(8):
            a = t * 2 + k * 0.785; sx, sy = XL + 150 * math.cos(a), GY - 200 + 120 * math.sin(a * 1.3)
            layer(img, lambda d, sx=sx, sy=sy: d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 240, 160, 230)))
        hx = 800 - (u * 110) % 300
        put(img, HOL_WALK[(fi // 2) % len(HOL_WALK)].transpose(Image.FLIP_LEFT_RIGHT), hx)
        g = G['gold']; img.alpha_composite(g, (int(hx - g.width / 2), int(GY - FOOT + 20 - g.height + 5 * math.sin(t * 8))))
        if abs(u - 0.1) < 0.5 / FPS: ev.append((round(t, 3), 'twinkle'))
        header(img, *TITLE['main'], u); tags(img, *TITLE['main'])
    elif name == 'owl':
        night = BGS['moon'][int(t * 6) % len(BGS['moon'])]; day = BGS['found'][int(t * 6) % len(BGS['found'])]
        img = day.copy(); img.alpha_composite(night.crop((0, 0, W // 2, H)), (0, 0))
        layer(img, lambda d: d.rectangle([W // 2 - 4, 0, W // 2 + 4, H], fill=(255, 214, 60, 255)))
        layer(img, lambda d: [d.ellipse([110 + k * 37 % 300, 760 + k * 53 % 300, 116 + k * 37 % 300, 766 + k * 53 % 300], fill=(255, 250, 220, int(150 + 100 * math.sin(t * 3 + k)))) for k in range(14)])
        layer(img, lambda d: (d.ellipse([810, 760, 970, 920], fill=(255, 220, 90, 255)), d.ellipse([780, 730, 1000, 950], outline=(255, 230, 120, 120), width=12)))
        put(img, RAY_CAST[fi % 8], 260, foot=OWL_RAY); put(img, JOY_VIC[(fi // 2) % len(JOY_VIC)], 720)
        g = G['mel']; img.alpha_composite(g, (int(420 - g.width / 2), int(600 + 10 * math.sin(t * 3))))
        g = G['acv']; img.alpha_composite(g, (int(610 - g.width / 2), int(600 + 10 * math.sin(t * 3 + 1))))
        if abs(u - 0.15) < 0.5 / FPS: ev.append((round(t, 3), 'chime'))
        header(img, *TITLE['owl'], u)
        tags(img, TITLE['owl'][0], '', xa=XL - 25, gy=OWL_RAY); tags(img, '', TITLE['owl'][1], xb=XR + 40)
    elif name == 'plan':
        img = BGS['hub'][int(t * 6) % len(BGS['hub'])].copy()
        put(img, CLEO_READ[(fi // 2) % 8], XL, foot=HUB_FOOT); put(img, CY_SHRUG[fi % 8], XR + 20, foot=HUB_FOOT)
        for k, (kd, txt) in enumerate([('acv', '8:00 ACV'), ('mel', '22:00 SLEEP')]):
            ts = 0.25 + k * 0.4
            if u > ts:
                if abs(u - ts) < 1.01 / FPS: ev.append((round(t, 3), 'tick_8bit'))
                pp = min(1, (u - ts) / 0.12); y0 = 560 + k * 96
                layer(img, lambda d, y0=y0: d.rounded_rectangle([86, y0, 686, y0 + 84], 14, fill=(240, 228, 196, 245), outline=(90, 60, 30, 255), width=5))
                g = G2[kd]; img.alpha_composite(g, (104, y0 + 10))
                text_layer(img, [(184 + len(txt) * 22, y0 + 20, txt, 44, (60, 40, 20), 0, int(255 * pp))])
        text_layer(img, [(XR + 20, HUB_FOOT - FOOT - 10, '?', 70, (255, 214, 60), 7, int(255 * (0.6 + 0.4 * math.sin(t * 6))))])
        header(img, *TITLE['plan'], u)
        tags(img, *TITLE['plan'], xb=XR + 20, gy=HUB_FOOT)
    if name == 'outro' and abs(u - 0.05) < 0.5 / FPS: ev.append((round(t, 3), 'ding_8bit'))
    if si > 0 and name != 'outro' and u < 0.12: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(200 * (1 - u / 0.12)))))
    if name == 'outro' and u < 0.12: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(200 * (1 - u / 0.12)))))
    img.alpha_composite(HK1)
    wr.write(img)
    if f % 15 == 0: img.convert('RGB').save(OUT + f'p_{f:04d}.png')
wr.close()
json.dump({'events': ev}, open(OUT + 'ev52.json', 'w')); print('done', DUR, NF, ev)
