import sys; sys.path.insert(0, '../../fork1')
from common import *
K = 5; FOOT = 78 * K
def native(path, n=92):
    return [f.resize((n, n), Image.NEAREST) for f in gif_frames(path)]
def anim(d, lo=1, hi=9): return seq('../' + d, K, lo, hi)
JOY_TALK = anim('joy_talk'); HOL_NOD = anim('hollow_nod'); CY_LIFT = anim('cyrus_lift'); JOY_STR = anim('joy_stretch')
CLEO_READ = anim('cleo_read'); CY_SHRUG = anim('cyrus_shrug')
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
SC = [('intro', 1.4), ('yap', 2.2), ('gym', 2.2), ('main', 2.2), ('owl', 2.2), ('plan', 2.2), ('outro', 1.9)]
T0 = []; acc = 0
for n, d in SC: T0.append(acc); acc += d
DUR = acc; NF = int(DUR * FPS)
TITLE = {'yap': ('YAPPER', 'LISTENER'), 'gym': ('GYM RAT', 'BED ROT'), 'main': ('MAIN CHARACTER', 'SIDE QUEST'), 'owl': ('NIGHT OWL', 'EARLY BIRD'), 'plan': ('PLANNER', 'WINGER')}
GY = 1600
def put(img, spr, cx, foot=None):
    foot = GY if foot is None else foot; img.alpha_composite(spr, (int(cx - spr.width / 2), int(foot - FOOT)))
def tags(img, a, b, xa=300, xb=780, al=255):
    layer(img, lambda d: [d.rounded_rectangle([x - 150, GY + 30, x + 150, GY + 90], 14, fill=(14, 10, 24, int(200 * al / 255))) for x in (xa, xb)])
    text_layer(img, [(xa, GY + 46, a, 24 if len(a) > 10 else 28, (255, 214, 60), 4, al), (xb, GY + 46, b, 24 if len(b) > 10 else 28, (255, 255, 255), 4, al)])
def header(img, a, b, u):
    al = int(255 * min(1, u / 0.15))
    layer(img, lambda d: d.rectangle([0, 230, W, 380], fill=(14, 10, 24, int(170 * al / 255))))
    text_layer(img, [(W / 2, 262, a + ' &', 52, (255, 214, 60), 7, al), (W / 2, 326, b, 52, (255, 255, 255), 7, al)])
ev = []
wr = Writer('v52_noaudio.mp4')
for f in range(NF):
    t = f / FPS
    si = max(i for i in range(len(SC)) if T0[i] <= t); name = SC[si][0]; u = t - T0[si]
    if abs(u) < 0.5 / FPS and si > 0: ev.append((round(t, 3), 'whoosh_8bit'))
    fi = int(t * 9)
    if name in ('intro', 'outro'):
        img = BGS['hub'][int(t * 6) % len(BGS['hub'])].copy()
        xs = [180, 360, 540, 720, 900]
        for g, x in zip(['joy', 'cyrus', 'cleo', 'ray', 'hollow'], xs):
            fr = IDL[g][fi % len(IDL[g])]; img.alpha_composite(fr, (int(x - fr.width / 2), int(1820 - 78 * 3)))
        for k, x in zip(['acv', 'mush', 'cre', 'mel', 'gold'], xs):
            g = G[k]; bob = 8 * math.sin(t * 4 + x); img.alpha_composite(g, (int(x - g.width / 2), int(1480 + bob)))
        if name == 'intro':
            s = min(1, u / 0.25)
            text_layer(img, [(W / 2, 640, 'WHICH DUO', int(40 + 34 * s), (255, 255, 255), 8, 255), (W / 2, 760, 'ARE YOU?', int(40 + 34 * s), (255, 214, 60), 8, 255)])
        else:
            text_layer(img, [(W / 2, 600, 'TAG YOUR', 74, (255, 255, 255), 8, 255), (W / 2, 720, 'OTHER HALF', 74, (255, 214, 60), 8, 255), (W / 2, 860, 'Which duo are you two?', 34, (255, 255, 255), 5, 255)])
    elif name == 'yap':
        img = BGS['found'][int(t * 6) % len(BGS['found'])].copy()
        put(img, JOY_TALK[fi % 8], 300); put(img, HOL_NOD[(fi // 2) % 8], 780)
        syms = ['!', '?!', '...', '!!', 'OMG', 'AND', 'WAIT']
        for k in range(6):
            uu = (u * 2.6 - k * 0.38)
            if 0 < uu < 1.2:
                x = 300 + 60 * math.sin(k * 2.1) + 120 * uu * (1 if k % 2 else -1) * 0.4; y = GY - FOOT + 40 - uu * 150
                al = int(255 * min(1, (1.2 - uu) / 0.4))
                layer(img, lambda d, x=x, y=y, al=al: d.rounded_rectangle([x - 90, y - 48, x + 90, y + 36], 20, fill=(255, 255, 255, al), outline=(20, 15, 35, al), width=5))
                text_layer(img, [(x, y - 24, syms[k], 36, (40, 30, 60), 0, al)])
        layer(img, lambda d: d.rounded_rectangle([700, GY - FOOT - 10, 860, GY - FOOT + 60], 18, fill=(255, 255, 255, 230), outline=(20, 15, 35, 255), width=5))
        text_layer(img, [(780, GY - FOOT + 4, 'mhm', 28, (40, 30, 60), 0, 255)])
        header(img, *TITLE['yap'], u); tags(img, *TITLE['yap'])
    elif name == 'gym':
        img = BGS['sun'][int(t * 6) % len(BGS['sun'])].copy()
        put(img, CY_LIFT[fi % 8], 290)
        bd = BED[int(t * 8) % len(BED)]; img.alpha_composite(bd, (int(800 - bd.width / 2), int(GY + 60 - bd.height)))
        for k in range(3):
            uu = (u * 1.8 - k * 0.55) % 1.6
            if uu < 1: text_layer(img, [(290 + (k - 1) * 70, GY - FOOT - 20 - uu * 120, '+1 STR', 40, (255, 200, 80), 7, int(255 * (1 - uu)))])
        for k in range(3):
            uu = (u * 1.2 + k * 0.33) % 1
            text_layer(img, [(830 + 40 * k + uu * 40, GY - 330 - uu * 160 - k * 20, 'Z', 46 + k * 12, (230, 210, 255), 7, int(255 * (1 - uu)))])
        g = G['cre']; img.alpha_composite(g, (400, int(GY - 60 + 6 * math.sin(t * 5))))
        header(img, *TITLE['gym'], u); tags(img, *TITLE['gym'])
    elif name == 'main':
        img = BGS['vit'][int(t * 6) % len(BGS['vit'])].copy()
        layer(img, lambda d: d.polygon([(300 - 60, 0), (300 + 60, 0), (300 + 210, GY + 20), (300 - 210, GY + 20)], fill=(255, 240, 180, 70)))
        put(img, CLEO_VIC[(fi // 2) % len(CLEO_VIC)], 300)
        for k in range(8):
            a = t * 2 + k * 0.785; sx, sy = 300 + 190 * math.cos(a), GY - 200 + 120 * math.sin(a * 1.3)
            layer(img, lambda d, sx=sx, sy=sy: d.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 240, 160, 230)))
        hx = 1000 - (u * 110) % 360
        put(img, HOL_WALK[(fi // 2) % len(HOL_WALK)].transpose(Image.FLIP_LEFT_RIGHT), hx)
        g = G['gold']; img.alpha_composite(g, (int(hx - g.width / 2), int(GY - FOOT + 20 - g.height + 5 * math.sin(t * 8))))
        header(img, *TITLE['main'], u); tags(img, *TITLE['main'])
    elif name == 'owl':
        night = BGS['moon'][int(t * 6) % len(BGS['moon'])]; day = BGS['found'][int(t * 6) % len(BGS['found'])]
        img = day.copy(); img.alpha_composite(night.crop((0, 0, W // 2, H)), (0, 0))
        layer(img, lambda d: d.rectangle([W // 2 - 4, 0, W // 2 + 4, H], fill=(255, 214, 60, 255)))
        layer(img, lambda d: [d.ellipse([180 + k * 37 % 300, 420 + k * 53 % 400, 186 + k * 37 % 300, 426 + k * 53 % 400], fill=(255, 250, 220, int(150 + 100 * math.sin(t * 3 + k)))) for k in range(14)])
        layer(img, lambda d: (d.ellipse([800, 420, 960, 580], fill=(255, 220, 90, 255)), d.ellipse([770, 390, 990, 610], outline=(255, 230, 120, 120), width=12)))
        put(img, RAY_CAST[fi % 8], 270); put(img, JOY_STR[min(7, int(u * 6)) if u < 1.4 else 4 + (fi // 3) % 4], 810)
        g = G['mel']; img.alpha_composite(g, (360, int(GY - 300 + 10 * math.sin(t * 3))))
        g = G['acv']; img.alpha_composite(g, (650, int(GY - 300 + 10 * math.sin(t * 3 + 1))))
        header(img, *TITLE['owl'], u); tags(img, *TITLE['owl'], xa=270, xb=810)
    elif name == 'plan':
        img = BGS['hub'][int(t * 6) % len(BGS['hub'])].copy()
        put(img, CLEO_READ[(fi // 2) % 8], 300, 1780); put(img, CY_SHRUG[fi % 8], 780, 1780)
        for k, kd in enumerate(['acv', 'cre', 'mush', 'mel']):
            al = 255 if u > 0.3 + k * 0.25 else 0
            if al:
                layer(img, lambda d, k=k: d.rounded_rectangle([90, 520 + k * 90, 470, 590 + k * 90], 12, fill=(240, 228, 196, 235), outline=(90, 60, 30, 255), width=4))
                g = gummy(kd, 2); img.alpha_composite(g, (110, 532 + k * 90))
                text_layer(img, [(300, 542 + k * 90, ['8:00 ACV', '9:00 LIFT', '12:00 QUEST', '22:00 SLEEP'][k], 22, (60, 40, 20), 0, 255)])
        text_layer(img, [(780, 1780 - FOOT - 40, '?', 70, (255, 214, 60), 7, int(255 * (0.6 + 0.4 * math.sin(t * 6))))])
        header(img, *TITLE['plan'], u)
        _g = GY; GY = 1780; tags(img, *TITLE['plan']); GY = _g
    # quick white flash at cuts
    if si > 0 and u < 0.12: img.alpha_composite(Image.new('RGBA', (W, H), (255, 255, 255, int(200 * (1 - u / 0.12)))))
    wr.write(img)
    if f % 30 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
wr.close()
ev += [(0.05, 'chime'), (round(T0[-1] + 0.1, 3), 'twinkle')]
json.dump(ev, open('ev52.json', 'w')); print('done', DUR)
