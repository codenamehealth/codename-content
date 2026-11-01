import sys, os; os.chdir('../../fork_b5/v52'); OUT='../../fork_c4/v52/'; sys.path.insert(0, '../../fork1'); sys.path.insert(0, '../../pixellab/safezone')
from common import *
from hook import hook_layer
HK1, HB1 = hook_layer(['WHICH DUO', 'ARE YOU?'], accent=1)
HK2, HB2 = hook_layer(['TAG YOUR', 'OTHER HALF'], accent=1, sub='WHICH DUO ARE YOU TWO?'); print('HB', HB1, HB2)
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
# Joy talking = Syeda's own joy-talk.gif (6 frames @100ms), no PixelLab teeth
JOY_TALK = [up(f, K) for f in native(SP + 'fork_c4/talk/joy-talk.gif')]
HOL_NOD = anim('hollow_nod'); CY_LIFT = anim('cyrus_lift'); JOY_STR = notooth('joy_stretch', (40, 28, 51, 36))
CLEO_READ = anim('cleo_read'); CY_SHRUG = notooth('cyrus_shrug', (43, 33, 49, 37))
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
G = {k: gummy(k, 3) for k in ['mush', 'acv', 'mel', 'cre', 'gold']}
SC = [('intro', 0.6), ('yap', 2.2), ('gym', 2.2), ('main', 2.2), ('owl', 2.2), ('plan', 2.2), ('outro', 1.9)]
T0 = []; acc = 0
for n, d in SC: T0.append(acc); acc += d
DUR = acc; NF = int(DUR * FPS)
TITLE = {'yap': ('YAPPER', 'LISTENER'), 'gym': ('GYM RAT', 'BED ROT'), 'main': ('MAIN CHARACTER', 'SIDE QUEST'), 'owl': ('NIGHT OWL', 'EARLY BIRD'), 'plan': ('PLANNER', 'WINGER')}
GY = 1405
def put(img, spr, cx, foot=None):
    foot = GY if foot is None else foot; img.alpha_composite(spr, (int(cx - spr.width / 2), int(foot - FOOT)))
def tags(img, a, b, xa=230, xb=720, al=255):
    layer(img, lambda d: [d.rounded_rectangle([x - 150, GY + 30, x + 150, GY + 90], 14, fill=(14, 10, 24, int(200 * al / 255))) for x in (xa, xb)])
    text_layer(img, [(xa, GY + 46, a, 24 if len(a) > 10 else 28, (255, 214, 60), 4, al), (xb, GY + 46, b, 24 if len(b) > 10 else 28, (255, 255, 255), 4, al)])
def header(img, a, b, u):
    al = int(255 * min(1, u / 0.15))
    layer(img, lambda d: d.rounded_rectangle([70, HB1 + 8, 1025, HB1 + 140], 18, fill=(14, 10, 24, int(210 * al / 255))))
    text_layer(img, [(W / 2, HB1 + 22, a + ' &', 46, (255, 214, 60), 7, al), (W / 2, HB1 + 80, b, 46, (255, 255, 255), 7, al)])
ev = []
wr = Writer(OUT + 'v52_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    si = max(i for i in range(len(SC)) if T0[i] <= t); name = SC[si][0]; u = t - T0[si]
    if abs(u) < 0.5 / FPS and si > 0: ev.append((round(t, 3), 'whoosh_8bit'))
    fi = int(t * 9)
    if name in ('intro', 'outro'):
        img = BGS['hub'][int(t * 6) % len(BGS['hub'])].copy()
        xs = [150, 320, 490, 650, 810]
        for g, x in zip(['joy', 'cyrus', 'cleo', 'ray', 'hollow'], xs):
            fr = IDL[g][fi % len(IDL[g])]
            hop = int(50 * max(0, math.sin(math.pi * min(1, max(0, (u - xs.index(x) * 0.06) / 0.3))))) if name == 'intro' else 0
            img.alpha_composite(fr, (int(x - fr.width / 2), int(1495 - 78 * 3 - hop)))
        for k, x in zip(['acv', 'mush', 'cre', 'mel', 'gold'], xs):
            g = G[k]; bob = 8 * math.sin(t * 4 + x); img.alpha_composite(g, (int(x - g.width / 2), int(1170 + bob)))
    elif name == 'yap':
        img = BGS['found'][int(t * 6) % len(BGS['found'])].copy()
        put(img, JOY_TALK[int(t * 10) % len(JOY_TALK)], 230); put(img, HOL_NOD[(fi // 2) % 8], 720)
        syms = ['!', '?!', '...', '!!', 'OMG', 'AND', 'WAIT']
        for k in range(6):
            uu = (u * 2.6 - k * 0.38)
            if 0 < uu < 1.2:
                x = 300 + 60 * math.sin(k * 2.1) + 120 * uu * (1 if k % 2 else -1) * 0.4; y = GY - FOOT + 40 - uu * 150
                al = int(255 * min(1, (1.2 - uu) / 0.4))
                layer(img, lambda d, x=x, y=y, al=al: d.rounded_rectangle([x - 90, y - 48, x + 90, y + 36], 20, fill=(255, 255, 255, al), outline=(20, 15, 35, al), width=5))
                text_layer(img, [(x, y - 24, syms[k], 36, (40, 30, 60), 0, al)])
        header(img, *TITLE['yap'], u); tags(img, *TITLE['yap'])
    elif name == 'gym':
        img = BGS['sun'][int(t * 6) % len(BGS['sun'])].copy()
        put(img, CY_LIFT[fi % 8], 230)
        bd = BED[int(t * 8) % len(BED)]; img.alpha_composite(bd, (int(650 - bd.width / 2), int(GY + 60 - bd.height)))
        for k in range(3):
            uu = (u * 1.8 - k * 0.55) % 1.6
            if uu < 1: text_layer(img, [(250 + (k - 1) * 50, GY - FOOT - 20 - uu * 120, '+1 STR', 40, (255, 200, 80), 7, int(255 * (1 - uu)))])
        for k in range(3):
            uu = (u * 1.2 + k * 0.33) % 1
            text_layer(img, [(680 + 40 * k + uu * 40, GY - 330 - uu * 160 - k * 20, 'Z', 46 + k * 12, (230, 210, 255), 7, int(255 * (1 - uu)))])
        g = G['cre']; img.alpha_composite(g, (320, int(GY - 60 + 6 * math.sin(t * 5))))
        header(img, *TITLE['gym'], u); tags(img, *TITLE['gym'], xa=230, xb=650)
    elif name == 'main':
        img = BGS['vit'][int(t * 6) % len(BGS['vit'])].copy()
        layer(img, lambda d: d.polygon([(230 - 60, 0), (230 + 60, 0), (230 + 190, GY + 20), (230 - 160, GY + 20)], fill=(255, 240, 180, 70)))
        put(img, CLEO_VIC[(fi // 2) % len(CLEO_VIC)], 230)
        for k in range(8):
            a = t * 2 + k * 0.785; sx, sy = 230 + 150 * math.cos(a), GY - 200 + 120 * math.sin(a * 1.3)
            layer(img, lambda d, sx=sx, sy=sy: d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 240, 160, 230)))
        hx = 800 - (u * 110) % 300
        put(img, HOL_WALK[(fi // 2) % len(HOL_WALK)].transpose(Image.FLIP_LEFT_RIGHT), hx)
        g = G['gold']; img.alpha_composite(g, (int(hx - g.width / 2), int(GY - FOOT + 20 - g.height + 5 * math.sin(t * 8))))
        header(img, *TITLE['main'], u); tags(img, *TITLE['main'])
    elif name == 'owl':
        night = BGS['moon'][int(t * 6) % len(BGS['moon'])]; day = BGS['found'][int(t * 6) % len(BGS['found'])]
        img = day.copy(); img.alpha_composite(night.crop((0, 0, W // 2, H)), (0, 0))
        layer(img, lambda d: d.rectangle([W // 2 - 4, 0, W // 2 + 4, H], fill=(255, 214, 60, 255)))
        layer(img, lambda d: [d.ellipse([110 + k * 37 % 300, 680 + k * 53 % 360, 116 + k * 37 % 300, 686 + k * 53 % 360], fill=(255, 250, 220, int(150 + 100 * math.sin(t * 3 + k)))) for k in range(14)])
        layer(img, lambda d: (d.ellipse([810, 680, 970, 840], fill=(255, 220, 90, 255)), d.ellipse([780, 650, 1000, 870], outline=(255, 230, 120, 120), width=12)))
        put(img, RAY_CAST[fi % 8], 230); put(img, JOY_STR[min(7, int(u * 6)) if u < 1.4 else 4 + (fi // 3) % 4], 710)
        g = G['mel']; img.alpha_composite(g, (int(400 - g.width / 2), int(905 + 10 * math.sin(t * 3))))
        g = G['acv']; img.alpha_composite(g, (int(905 - g.width / 2), int(905 + 10 * math.sin(t * 3 + 1))))
        header(img, *TITLE['owl'], u); tags(img, *TITLE['owl'], xa=230, xb=710)
    elif name == 'plan':
        img = BGS['hub'][int(t * 6) % len(BGS['hub'])].copy()
        put(img, CLEO_READ[(fi // 2) % 8], 230); put(img, CY_SHRUG[fi % 8], 720)
        for k, kd in enumerate(['acv', 'cre', 'mush', 'mel']):
            al = 255 if u > 0.3 + k * 0.25 else 0
            if al:
                layer(img, lambda d, k=k: d.rounded_rectangle([90, 680 + k * 86, 470, 748 + k * 86], 12, fill=(240, 228, 196, 235), outline=(90, 60, 30, 255), width=4))
                g = gummy(kd, 2); img.alpha_composite(g, (110, 690 + k * 86))
                text_layer(img, [(300, 700 + k * 86, ['8:00 ACV', '9:00 LIFT', '12:00 QUEST', '22:00 SLEEP'][k], 22, (60, 40, 20), 0, 255)])
        text_layer(img, [(720, GY - FOOT - 40, '?', 70, (255, 214, 60), 7, int(255 * (0.6 + 0.4 * math.sin(t * 6))))])
        header(img, *TITLE['plan'], u)
        tags(img, *TITLE['plan'])
    # quick white flash at cuts
    if si > 0 and u < 0.12: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(200 * (1 - u / 0.12)))))
    img.alpha_composite(HK2 if name == 'outro' else HK1)
    wr.write(img)
    if f % 15 == 0: img.convert('RGB').save(OUT + f'p_{f:04d}.png')
wr.close()
ev += [(0.05, 'chime'), (round(T0[-1] + 0.1, 3), 'twinkle')]
json.dump(ev, open(OUT + 'ev52.json', 'w')); print('done', DUR)
