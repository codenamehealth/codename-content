import numpy as np, math, random, subprocess, json, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from scipy import ndimage
OUTD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'v105' if sys.argv[1] == 'cyrus' else 'v106')
os.chdir('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_b11/pick')
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc2'); from rc2 import hook_layer2, acv_gloss
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
FONT = S + 'npmfont/ps/package/files/PressStart2P.ttf'; A = S + 'pause/assets/'
W, H, FPS = 1080, 1920, 30
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def crop(im): return im.crop(im.getbbox())
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
def clean(im, minpx=40):
    a = np.array(im); al = a[:, :, 3] > 0
    lab, n = ndimage.label(al)
    if n > 1:
        sizes = ndimage.sum(al, lab, range(1, n + 1))
        for i, sz in enumerate(sizes):
            if sz < minpx: a[lab == i + 1] = 0
    return Image.fromarray(a)
CFG = {
 'cyrus': dict(bg='../gen/bg_grove_1/00.png', run='race/cyrus_run', pick='../gen/cyrus_pick', idle='idle_1.gif',
               vic='vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', bottle=A + 'mush_main.png', gummy='mush',
               hook=('Cyrus is picking mushrooms', 'for his gummy'), col=(217, 122, 31), floor=1730, hk=(['CYRUS PICKS', 'MUSHROOMS'], (255, 160, 40), 'FOR HIS GUMMY'),
               items=[('gen', '../gen/mush_0/07.png'), ('gen', '../gen/mush_1/21.png'), ('gen', '../gen/mush_2/00.png'), ('gen', '../gen/mush_3/00.png'),
                      ('gen', '../gen/mush_4/01.png'), ('gen', '../gen/mush_5/00.png'), ('gen', '../gen/mush_6/02.png'), ('gen', '../gen/mush_7/00.png')],
               how=['grow', 'drop', 'grow', 'grow', 'drop', 'grow', 'grow', 'drop'], banner='ENERGY GUMMY', music='fantasy_adventure'),
 'joy': dict(bg='../gen/bg_garden_1/00.png', run='race/joy_run', pick='../gen/joy_pick', idle='idle_0.gif',
             vic='vic_Victory_Pose.gif', bottle=S + 'screenshot/acv_main.png', gummy='acv',
             hook=('Joy is picking everything', 'for the ACV gummy'), col=(118, 200, 80), floor=1760, hk=(['JOY PICKS', 'EVERYTHING'], (130, 225, 90), 'FOR THE ACV GUMMY'),
             items=[('gen', '../gen/acv_0/01.png'), ('orb', 'B6', (242, 163, 58)), ('gen', '../gen/acv_2/00.png'), ('orb', 'B12', (199, 116, 217)),
                    ('orb', 'I', (111, 211, 181)), ('gen', '../gen/acv_5/00.png'), ('gen', '../gen/acv_6/02.png'), ('gen', '../gen/acv_7/05.png')],
             how=['grow', 'float', 'drop', 'float', 'float', 'drop', 'pull', 'pull'], banner='FOUNDATION GUMMY', music='glockenspiel_pop'),
}
G = sys.argv[1]; C = CFG[G]
BG0 = up(Image.open(C['bg']).convert('RGBA'), 3)
FLOOR = 1495; DY = C['floor'] - FLOOR          # raise the scene so the guide's feet stay on the same ground, now inside the safe zone
BG = Image.new('RGBA', (W, H)); BG.paste(BG0.crop((0, DY, W, H)), (0, 0))
BG.paste(BG0.crop((0, H - DY, W, H)).transpose(Image.FLIP_TOP_BOTTOM), (0, H - DY))
HOOK, HB = hook_layer2(C['hk'][0], accent=1, color=C['hk'][1], sub=C['hk'][2], sub_color=(255, 255, 255))   # sub line 'FOR THE ACV GUMMY' now 52px (was ~30px); print('hook bottom', HB)
K = 4; FOOT = 78 * K
def seq(d, lo=1, hi=9, cl=False):
    out = []
    for p in sorted(glob.glob(d + '/*.png'))[lo:hi]:
        im = Image.open(p).convert('RGBA')
        if cl: im = clean(im)
        out.append(up(im, K))
    return out
RUN = seq(S + 'pixellab/' + C['run']); RUNL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in RUN]
PICK = seq(C['pick'], 1, 9, True); PICKL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in PICK]
def gif(p, scale=None, h=None):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    if scale: return [up(f.resize((92, 92), Image.NEAREST), scale) for f in fr]
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
IDLE = gif(C['idle'], scale=K); IDLEL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in IDLE]
VIC = gif(C['vic'], h=330)
def orb(txt, col, k=1):
    # LEGIBILITY: vitamin coin labels were 8px art upscaled (16px in the bar); now drawn after upscaling, 24-48px
    c = Image.new('RGBA', (40, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.ellipse([2, 2, 37, 37], fill=(30, 22, 40, 255)); d.ellipse([4, 4, 35, 35], fill=col + (255,))
    dk = tuple(int(v * 0.75) for v in col); d.arc([4, 4, 35, 35], 20, 160, fill=dk + (255,), width=3)
    d.ellipse([9, 8, 15, 13], fill=(255, 255, 255, 200))
    c = up(c, k); d = ImageDraw.Draw(c)
    fs = {1: 8, 2: 24, 3: 32}[k] if len(txt) == 3 else ({1: 8, 2: 32, 3: 40}[k] if len(txt) == 2 else {1: 8, 2: 40, 3: 48}[k])
    f = ImageFont.truetype(FONT, fs); w = d.textlength(txt, font=f)
    d.text((20 * k - w / 2, 20 * k - fs / 2 + k), txt, font=f, fill=(40, 25, 30, 255), stroke_width=max(1, k), stroke_fill=(255, 250, 235, 255))
    return c
ICON3 = []; ICON2 = []
for it in C['items']:
    if it[0] == 'gen': i = crop(Image.open(it[1]).convert('RGBA')); ICON3.append(up(i, 3)); ICON2.append(up(i, 2))
    else: ICON3.append(orb(it[1], it[2], 3)); ICON2.append(orb(it[1], it[2], 2))
GUM = up(acv_gloss(crop(Image.open(S + f'pixellab/gummies/pick_{C["gummy"]}.png').convert('RGBA'))), 8)   # gummy gloss on Syeda's ACV gummy (VETTING)
bot = crop(Image.open(C['bottle']).convert('RGBA')); BOT = bot.resize((int(bot.width * 430 / bot.height), 430), Image.LANCZOS)
CX = 478
# ---- choreography
rnd = random.Random(7 if G == 'cyrus' else 11)
SPOTS = [230, 700, 300, 840, 600, 880, 380, 660]           # first spot on the left so Joy (starting at centre) never covers item 1 on frame 0
NEWX = lambda x: int(180 + (x - 230) * (580 / 650))          # drawn spots x180-760 so the guide and the item stay inside the zone
SIDE = lambda x: 1 if NEWX(x) < 478 else -1                 # item on the open side, never under the guide
IOFF = 118
T0 = -0.2; STEPS = [1.05, 1.15, 1.0, 1.2, 1.05, 1.15, 1.1]   # OPEN IN MOTION: item 1 already growing and Joy running on frame 0; uneven beats (no metronome)
events = []
x0 = 230 + (CX - 180) * 650 / 580   # Joy starts at centre = where her victory pose ends, so the loop is seamless
PICKD = 0.5
timeline = []      # per item: (t_appear, t_run0, t_arrive, t_pick_end, t_fly_end, x)
px = x0
for k in range(8):
    ta = T0 + sum(STEPS[:k])
    x = SPOTS[k]; dist = abs(x - px); trun = min(0.42, dist / 1500)
    t_run0 = ta + 0.18; t_arr = t_run0 + trun; t_pe = t_arr + PICKD; t_fe = t_pe + 0.45
    timeline.append((ta, t_run0, t_arr, t_pe, t_fe, x, px)); px = x
T_CRAFT = timeline[-1][4] + 0.2; T_BOTTLE = T_CRAFT + 1.9; T_RESET = T_BOTTLE + 1.75; END = T_RESET + 0.3   # bottle 0.6s + hold ~1.2s, 0.25s reset to the opening state
BAR_Y = HB + 26; SLOT_X = [W / 2 + (k - 3.5) * 104 for k in range(8)]
def char_state(t):
    # returns sprite, x
    if t < timeline[0][1]: return IDLE[int(t * 8) % len(IDLE)], NEWX(x0)
    for k, (ta, tr, tarr, tpe, tfe, x, pxx) in enumerate(timeline):
        nxt = timeline[k + 1][1] if k < 7 else T_CRAFT
        face_left = x < pxx; side_left = SIDE(x) < 0
        if tr <= t < tarr:
            u = (t - tr) / max(1e-3, tarr - tr); cx = NEWX(pxx) + (NEWX(x) - NEWX(pxx)) * u
            fr = (RUNL if face_left else RUN)[int(t * 16) % 8]; return fr, cx
        if tarr <= t < tpe:
            u = (t - tarr) / PICKD; fr = (PICKL if side_left else PICK)[min(7, int(u * 8))]; return fr, NEWX(x)
        if tpe <= t < nxt:
            return (IDLEL if side_left else IDLE)[int(t * 8) % len(IDLE)], NEWX(x)
    return IDLE[int(t * 8) % len(IDLE)], NEWX(timeline[-1][5])
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', OUTD + '/noaudio.mp4'], stdin=subprocess.PIPE)
KEEP = {int(v) for v in os.environ.get('KEEP', '').split(',') if v}
NF = int(END * FPS)
motes = [(rnd.uniform(0, W), rnd.uniform(500, 1700), rnd.uniform(0, 6.3), rnd.uniform(0.3, 1.0)) for _ in range(28)]
motes = [(m[0], m[1] - DY, m[2], m[3]) for m in motes]
def ev(t, name):
    t = max(0.0, t)
    if not any(e[1] == name and abs(e[0] - t) < 0.02 for e in events): events.append((round(t, 3), name))
for f in range(NF):
    t = f / FPS
    img = BG.copy(); d = ImageDraw.Draw(img)
    # floating light motes
    def motes_fn(dd):
        for (mx, my, ph, sp) in motes:
            yy = my - (t * 40 * sp) % 400; xx = mx + 20 * math.sin(t * sp * 2 + ph); a = int(120 + 100 * math.sin(t * 3 + ph))
            dd.rectangle([xx, yy, xx + 6, yy + 6], fill=(255, 236, 160, max(0, a)))
    layer(img, motes_fn)
    # ingredients on the ground / in the air
    filled = 0; FLY = []
    for k, (ta, tr, tarr, tpe, tfe, x, pxx) in enumerate(timeline):
        how = C['how'][k]; ic = ICON3[k]; xo = x; x = NEWX(xo); ix = x + SIDE(xo) * IOFF
        if t >= tfe: filled = k + 1; continue
        if t < ta: continue
        if t < tarr + 0.35:
            u = min(1, (t - ta) / 0.35)
            if how in ('grow', 'pull'):
                sc = 0.2 + 0.8 * (1 - (1 - u) ** 3) + 0.08 * math.sin(min(1, u) * 9) * (1 - u)
                im = ic.resize((max(1, int(ic.width * sc)), max(1, int(ic.height * sc))), Image.NEAREST)
                gx, gy = ix, FLOOR - im.height
                if how == 'pull' and u < 1: gy += int((1 - u) * 40)
            elif how == 'drop':
                yy = (FLOOR - 760) + 760 * min(1, u * u)
                im = ic; gx, gy = ix, int(yy - ic.height)
            else:  # float down glowing
                yy = FLOOR - 520 + 520 * (1 - (1 - u) ** 2); im = ic; gx, gy = ix, int(yy - ic.height)
                layer(img, lambda dd: dd.ellipse([gx - ic.width * 0.7, gy - 10, gx + ic.width * 0.7, gy + ic.height + 10], fill=(255, 255, 220, 60)))
            if u < 1 and how in ('grow', 'pull'):
                for q in range(6):
                    a = q * 1.05 + t * 4; rr = 40 + 60 * u
                    layer(img, lambda dd, a=a, rr=rr: dd.rectangle([ix + rr * math.cos(a) - 4, FLOOR - 40 + rr * math.sin(a) * 0.5 - 4, ix + rr * math.cos(a) + 4, FLOOR - 40 + rr * math.sin(a) * 0.5 + 4], fill=(255, 245, 190, int(220 * (1 - u)))))
            if t - 1 / FPS < ta <= t: ev(ta, 'poof' if how in ('grow', 'pull') else ('jump' if how == 'drop' else 'twinkle'))
            if how == 'drop' and t - 1 / FPS < (ta + 0.35) <= t: ev(t, 'boing')
            img.alpha_composite(im, (int(gx - im.width / 2), int(gy)))
        # picked: overhead then fly
        elif t < tpe:
            sp, cx = char_state(t)
            img.alpha_composite(ic, (int(cx - ic.width / 2 + 20 * SIDE(xo)), int(FLOOR - FOOT + 30 - ic.height)))
        else:
            FLY.append(k); continue
            sx, sy = x, FLOOR - FOOT + 30 - ic.height / 2; tx, ty = SLOT_X[k], BAR_Y + 50
            cx = sx + (tx - sx) * e; cy = sy + (ty - sy) * e - math.sin(math.pi * u) * 260
            sc = 1 - 0.33 * e; im = ic.resize((max(1, int(ic.width * sc)), max(1, int(ic.height * sc))), Image.NEAREST)
            img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    # character
    if t < T_BOTTLE:
        sp, cx = char_state(t)
        layer(img, lambda dd: dd.ellipse([cx - 60, FLOOR - 14, cx + 60, FLOOR + 10], fill=(0, 0, 0, 70)))
        img.alpha_composite(sp, (int(cx - sp.width / 2), int(FLOOR - FOOT)))     # guide drawn after every prop: never covered
    # header: hook + bar
    SHOWBAR = t < T_BOTTLE or t >= T_RESET + 0.12
    RA = 1.0 if t < T_RESET else min(1.0, (t - T_RESET - 0.12) / 0.15)   # bar + prompt fade back in after the bottle is gone
    HL = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(HL)
    if SHOWBAR: d.rounded_rectangle([W / 2 - 430, BAR_Y - 14, W / 2 + 430, BAR_Y + 114], 40, fill=(26, 20, 34), outline=(26, 20, 34))
    if SHOWBAR: d.rounded_rectangle([W / 2 - 420, BAR_Y - 4, W / 2 + 420, BAR_Y + 104], 34, fill=(247, 240, 222))
    for k in (range(8) if SHOWBAR else []):
        sx = SLOT_X[k]; glow = 0
        tfe = timeline[k][4]
        if 0 <= t - tfe < 0.4: glow = 1 - (t - tfe) / 0.4
        d.ellipse([sx - 46, BAR_Y + 4, sx + 46, BAR_Y + 96], fill=(228, 220, 200) if not glow else (255, 236, 150))
        if k == 7 and t < tfe and t < T_BOTTLE:   # GUESS: the last slot is a pulsing '?' until Joy picks it
            pq = 1 + 0.08 * math.sin(t * 6); fq = F(int(56 * pq)); ctext(d, sx, BAR_Y + 50 - fq.size / 2, '?', fq, (255, 214, 60), 7)
        if t >= tfe and t < T_CRAFT + 0.3:
            ic = ICON2[k]; pop = 1 + 0.25 * glow
            im = ic.resize((int(ic.width * pop), int(ic.height * pop)), Image.NEAREST) if glow else ic
            HL.alpha_composite(im, (int(sx - im.width / 2), int(BAR_Y + 50 - im.height / 2)))
            if t - 1 / FPS < tfe <= t: ev(tfe, 'ding_8bit')
    if t >= T_RESET: HL.putalpha(HL.getchannel('A').point(lambda p: int(p * RA)))
    img.alpha_composite(HL); d = ImageDraw.Draw(img)
    # COMMENT PROMPT from frame 0 (one line, 46px, own dark plate) until the last ingredient lands
    PY = BAR_Y + 128
    if t < timeline[-1][4] + 0.15 or t >= T_RESET + 0.12:
        pa = int(255 * RA)
        layer(img, lambda dd: dd.rounded_rectangle([W / 2 - 440, PY, W / 2 + 440, PY + 78], 18, fill=(14, 10, 24, int(pa * 0.92)), outline=(130, 225, 90, pa), width=4))
        layer(img, lambda dd: ctext(dd, W / 2, PY + 16, 'GUESS THE LAST ONE!', F(46), (255, 255, 255), 6, pa))   # on a layer so the fade really blends
    # icons flying from Joy into the bar (drawn above the bar now, so they visibly land in their slot)
    for k in FLY:
        ta, tr, tarr, tpe, tfe, xo, pxx = timeline[k]; ic = ICON3[k]; x = NEWX(xo)
        u = (t - tpe) / (tfe - tpe); e = u * u * (3 - 2 * u)
        sx, sy = x, FLOOR - FOOT + 30 - ic.height / 2; tx, ty = SLOT_X[k], BAR_Y + 50
        cx = sx + (tx - sx) * e; cy = sy + (ty - sy) * e - math.sin(math.pi * u) * 260
        sc = 1 - 0.33 * e; im = ic.resize((max(1, int(ic.width * sc)), max(1, int(ic.height * sc))), Image.NEAREST)
        img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    # craft: icons spiral from the bar into a gummy above the guide
    cxg, cyg = CX, 1000
    if T_CRAFT <= t < T_BOTTLE:
        u = (t - T_CRAFT) / 0.9
        if u < 1:
            for k in range(8):
                e = u * u; ang = k * 0.785 + u * 6
                sx, sy = SLOT_X[k], BAR_Y + 50
                rx = cxg + (sx - cxg) * (1 - e) + math.cos(ang) * 120 * (1 - e) * e * 4
                ry = cyg + (sy - cyg) * (1 - e) + math.sin(ang) * 120 * (1 - e) * e * 4
                ic = ICON2[k]; img.alpha_composite(ic, (int(rx - ic.width / 2), int(ry - ic.height / 2)))
            if t - 1 / FPS < T_CRAFT <= t: ev(T_CRAFT, 'whoosh_8bit')
        else:
            v = (t - T_CRAFT - 0.9) / 0.7
            if v < 0.25: layer(img, lambda dd: dd.ellipse([cxg - 300 * v * 4, cyg - 300 * v * 4, cxg + 300 * v * 4, cyg + 300 * v * 4], fill=(255, 250, 220, int(230 * (1 - v * 4)))))
            sc = min(1, v * 2.2); wb = 0.07 * math.sin(t * 11) * math.exp(-max(0, v - 0.45) * 1.2)   # jelly squash-stretch: it wobbles like a gummy, not a fruit
            g = GUM.resize((max(1, int(GUM.width * sc * (1 + wb))), max(1, int(GUM.height * sc * (1 - wb)))), Image.NEAREST)
            bob = math.sin(t * 4) * 12
            layer(img, lambda dd: [dd.ellipse([cxg - r, cyg - r, cxg + r, cyg + r], fill=C['col'] + (a,)) for r, a in ((260, 40), (190, 60), (130, 80))])
            img.alpha_composite(g, (int(cxg - g.width / 2), int(cyg - g.height / 2 + bob)))
            if t - 1 / FPS < (T_CRAFT + 0.9) <= t: ev(T_CRAFT + 0.9, 'powerup_8bit')
            pa = int(255 * min(1, v * 4))
            layer(img, lambda dd: dd.rounded_rectangle([CX - 330, PY - 4, CX + 330, PY + 96], 20, fill=(14, 10, 24, int(pa * 0.92)), outline=C['col'] + (pa,), width=6))
            layer(img, lambda dd: ctext(dd, CX, PY + 14, 'ACV GUMMY!', F(int(68 * (0.85 + 0.15 * min(1, v * 3)))), C['col'], 9, pa))
    # bottle reveal + victory
    if t >= T_BOTTLE:
        u = t - T_BOTTLE; e = min(1, u / 0.6); e = 1 - (1 - e) ** 3
        fo = 1.0 if t < T_RESET else max(0.0, 1 - (t - T_RESET) / 0.14)   # LOOP: bottle/glow/CRAFTED fade out, empty bar fades in
        img0 = img; img = Image.new('RGBA', img.size, (0, 0, 0, 0))
        layer(img, lambda dd: [dd.ellipse([CX - r, 870 - r, CX + r, 870 + r], fill=(255, 240, 190, a)) for r, a in ((380, 35), (300, 45), (220, 55))])
        for q in range(10):
            a = q * 0.628 + t * 1.2; rr = 290 + 20 * math.sin(t * 3 + q)
            layer(img, lambda dd, a=a, rr=rr: dd.rectangle([CX + rr * math.cos(a) - 6, 870 + rr * math.sin(a) - 6, CX + rr * math.cos(a) + 6, 870 + rr * math.sin(a) + 6], fill=(255, 220, 90, 230)))
        b = BOT; yy = int(852 - b.height / 2 + (1 - e) * 500 + math.sin(t * 2.5) * 8)
        bb = b.copy(); bb.putalpha(bb.getchannel('A').point(lambda p: int(p * min(1, u / 0.3))))
        img.alpha_composite(bb, (int(CX - b.width / 2), yy))
        d = ImageDraw.Draw(img); ctext(d, CX, 1098, 'CRAFTED!', F(60), (255, 214, 60), 8)
        if fo < 1: img.putalpha(img.getchannel('A').point(lambda p: int(p * fo)))
        img0.alpha_composite(img); img = img0
        vf = VIC[int(u * 8) % len(VIC)] if t < T_RESET else RUNL[int(t * 16) % 8]   # into her opening run on the reset
        layer(img, lambda dd: dd.ellipse([CX - 80, FLOOR - 14, CX + 80, FLOOR + 10], fill=(0, 0, 0, 70)))
        img.alpha_composite(vf, (int(CX - vf.width / 2), int(FLOOR - vf.height)))
        if 0 <= u < 1 / FPS: ev(T_BOTTLE, 'victory')
    img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if f == 0: ev(0.0, 'poof')
    if f in KEEP: img.convert('RGB').save(OUTD + f'/k_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': events}, open(OUTD + '/ev.json', 'w'))
print('done', round(END, 2), C['music'])
