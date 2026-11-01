import math, random, json, subprocess, glob
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
S0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
P = S0 + 'pixellab/'; A = S0 + 'pause/assets/'; FONT = S0 + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H, FPS = 1080, 1920, 30; K = 7   # guides 4x -> 5x (safe pass) -> 7x (Bennett: too small)
import os; STILL = os.environ.get('STILL')
import sys; sys.path.insert(0, S0 + 'fork_rc2'); from rc2 import hook_layer2, gummy_src, acv_tag
# review r009: 'Comment 1 to 5' from frame 0 as a real 52px second line of the hook band
sys.path.insert(0, S0 + 'pixellab/safezone'); from hook import hook_fade
# Oct 29 pass: soft fade, no box; 'Comment 1 to 5' sub cut (the numbers + caption carry it)
HOOK, HB = hook_fade(['CHOOSE YOUR', 'REALM'], accent=1, color=(255, 214, 60), size=68)
import sys as _hw; _hw.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h1'); from hookw import hook_fade_w
HOOK, HG = hook_fade_w(['WHERE WOULD', 'YOU LIVE?'], ['LIVE?'], size=68, fade_to=HB + 110); print('new hook', HG)   # fork_h1 Oct 29: hook text only
END_HOOK, EHB = hook_fade(['WHICH ONE', 'IS YOURS?'], accent=1, color=(255, 214, 60), size=68)
BY = HB + 22   # realm number + short name: one line, no box
print('hook bottom', HB)
def F(s): return ImageFont.truetype(FONT, s)
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
def gif92(p):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), K))
    return fr
def pngs(d, lo=1): return [up(Image.open(f).convert('RGBA'), K) for f in sorted(glob.glob(d + '/*.png'))[lo:]]
REALMS = [
 dict(short='VILLAGE', name=['THE VILLAGE'], sub=['Every journey', 'starts here'], bg='hub.gif', walk=gif92('hollow-walk-side.gif'), idle=[up(Image.open(S0 + 'syeda_src/hollow/char2.png').convert('RGBA'), K)], gum='gold', dx=620, feet=1470, part=(255, 230, 160), wfps=8, player=True),
 dict(short='FOREST', name=['THORNBERRY', 'FOREST'], sub=["Joy's realm"], bg='found_hd.gif', walk=gif92('joy-walk-side.gif'), idle=gif92('idle_0.gif'), gum='acv', feet=1470, part=(200, 255, 140), wfps=8),
 dict(short='SUN TEMPLE', name=['THE SUN', 'TEMPLE'], sub=["Cyrus's realm"], bg='sun_hd.gif', walk=gif92('cyrus-walk-side.gif'), idle=gif92('idle_8.gif'), gum='mush', feet=1470, part=(255, 220, 120), wfps=8),
 dict(short='MOON TEMPLE', name=['THE MOON', 'TEMPLE'], sub=["Rayleigh's realm"], bg='recov_hd.gif', walk=pngs(P + 'race/ray_run'), idle=gif92('idle_6.gif'), gum='mel', feet=1470, part=(170, 200, 255), wfps=10),
 dict(short='CASTLE', name=['THE CASTLE'], sub=["Cleo's realm"], bg='vit_hd.gif', walk=pngs(P + 'cleo/walk_mm'), idle=gif92('idle_7.gif'), gum='cre', feet=1470, part=(255, 255, 255), wfps=10)]
for r in REALMS:
    g = Image.open(A + r['bg']); r['src'] = []
    for i in range(0, g.n_frames, 2): g.seek(i); r['src'].append(g.convert('RGB'))
    r['gimg'] = up(gummy_src(r['gum']), 4)   # ACV gets the gummy gloss
SEG = 2.2; TR = 0.3; INTRO = 0.0; END_HOLD = 1.5; END_CARD = END_HOLD + TR   # review: realms 3.3s -> 2.2s (idle trimmed), grid held 1.5s then dissolves back to frame 0
TOTAL = len(REALMS) * SEG + END_CARD
sc = H / 1080; cw = W / sc
def bgframe(r, t, u):
    src = r['src'][int(t * 6) % len(r['src'])]
    x0 = 960 - cw / 2 - 30 + 60 * u + r.get('dx', 0)
    return src.crop((int(x0), 0, int(x0 + cw), 1080)).resize((W, H), Image.NEAREST).convert('RGBA')
def scene(i, t, u):
    r = REALMS[i]; img = bgframe(r, t, u)
    # particles
    def parts(dd):
        rr = random.Random(i * 7)
        for q in range(26):
            px = rr.uniform(0, W); sp = rr.uniform(30, 90); ph = rr.uniform(0, 6.28)
            py = (rr.uniform(0, H) - t * sp) % H if i != 0 else (rr.uniform(0, H) + t * sp * 0.5) % H
            px += 30 * math.sin(t * 1.3 + ph); s = rr.choice([4, 6, 8]); a = int(150 + 100 * math.sin(t * 3 + ph))
            dd.rectangle([px, py, px + s, py + s], fill=r['part'] + (max(0, a),))
    layer(img, parts)
    # gummy treasure floating with glow
    gx, gy = 800, r['feet'] - 450 + 16 * math.sin(t * 2.4)   # moved right/up to clear the bigger guide
    def glow(dd):
        for rad, al in ((120, 35), (85, 55), (55, 80)):
            dd.ellipse([gx - rad, gy - rad, gx + rad, gy + rad], fill=(255, 235, 170, al))
        for k in range(5):
            a = t * 2 + k * 1.256; sx, sy = gx + 95 * math.cos(a), gy + 60 * math.sin(a)
            dd.rectangle([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 250, 210, 230))
    layer(img, glow)
    gi = r['gimg']; img.alpha_composite(gi, (int(gx - gi.width / 2), int(gy - gi.height / 2)))
    if r['gum'] == 'acv' and 0.15 < u * SEG < 1.75:   # 'ACV GUMMY' on its first appearance so Syeda's apple-shaped gummy reads as a gummy
        pass  # Oct 29: no ACV tags
    # guide walks in, then idles facing us. Village: the Hollow is the PLAYER arriving (keeps facing the
    # gummy he's walking to, 'YOU' player marker over his head, '!' when he spots it), never the realm's host.
    walk_end = 1.2 if not r.get('player') else 1.0
    X0, XS = (-130, 110) if r.get('player') else (-250, 148)   # Village: the Hollow is already mid-stride in frame at frame 0; guides enter from the edge
    if u * SEG < walk_end:
        p = (u * SEG) / walk_end; x = X0 + p * (XS - X0)
        fr = r['walk'][int(t * r['wfps']) % len(r['walk'])]
    else:
        x = XS; fr = r['idle'][int(t * 8) % len(r['idle'])]
    layer(img, lambda dd: dd.ellipse([x + 46 * K - 90, r['feet'] - 14, x + 46 * K + 90, r['feet'] + 14], fill=(0, 0, 0, 70)))
    img.alpha_composite(fr, (int(x), int(r['feet'] - 78 * K)))
    if r.get('player'):
        hx = x + 45 * K; hy = r['feet'] - 78 * K + 13 * K          # head top centre
        bob = 8 * math.sin(t * 6)
        PLm = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PLm)
        ty = hy - 40 + bob
        pd.polygon([(hx - 26, ty - 22), (hx + 26, ty - 22), (hx, ty + 6)], fill=(255, 214, 60, 255), outline=(20, 15, 35, 255), width=5)
        # 'YOU' text cut (Oct 29); the gold player marker stays
        ts = u * SEG - walk_end
        if 0.05 < ts < 1.0:
            sc_ = min(1, ts / 0.12); ex, ey = hx + 120, hy + 10
            ctext(pd, ex, ey - 50 * sc_, '!', F(int(20 + 52 * sc_)), (255, 90, 70), 8)   # plain emote, no bubble (Hollow never talks)
        img.alpha_composite(PLm)
    # header + realm banner
    # review: realm name 60px, subline 40px (were 44/26px); fixed-height banner, text fully on from the first frame of each realm
    # Oct 29: no banner box, no sublines ('Joy's realm', 'Every journey starts here'); number badge + short name, one line
    a = 255
    PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(PL)
    fN = F(56); tw = pd.textlength(r['short'], font=fN); bd = 96; gap = 24
    x0 = W / 2 - (bd + gap + tw) / 2; cy = BY + bd / 2
    pd.ellipse([x0, cy - bd / 2, x0 + bd, cy + bd / 2], fill=(255, 214, 60, a), outline=(20, 15, 35, a), width=6)
    ctext(pd, x0 + bd / 2, cy - 22, str(i + 1), F(46), (20, 15, 35), 0, a)
    pd.text((x0 + bd + gap, cy - 28), r['short'], font=fN, fill=(255, 255, 255, a), stroke_width=8, stroke_fill=(20, 15, 35, a))
    img.alpha_composite(PL)
    img.alpha_composite(HOOK)
    return img
BANDS = None
# Oct 29: end card = the 5 realms as full-width bands stacked edge to edge (was 5 small cards on flat dark).
# Top band runs to the frame top (the hook sits on it), bottom band runs to the frame bottom; badges + gummies stay inside the safe zone.
BND = [(0, 676), (676, 882), (882, 1088), (1088, 1294), (1294, 1920)]
CROWY = [566, 779, 985, 1191, 1397]   # content centre line of each band (badge + gummy)
FOC = [0.62, 0.55, 0.62, 0.6, 0.55]    # which height of each realm image sits on the content line
def bandimg(i):
    r = REALMS[i]; src = r['src'][0]
    b0, b1 = BND[i]; hh = b1 - b0
    k = max(1.0, (hh + 40) / 608)
    ww, ih = int(1080 * k), int(608 * k)
    im = src.resize((ww, ih), Image.NEAREST).convert('RGBA')
    top = int(ih * FOC[i]) - (CROWY[i] - b0); top = max(0, min(ih - hh, top))
    x0 = (ww - 1080) // 2
    return im.crop((x0, top, x0 + 1080, top + hh))
def endcard(t, u):
    global BANDS
    if BANDS is None: BANDS = [bandimg(i) for i in range(len(REALMS))]
    img = Image.new('RGBA', (W, H), (14, 10, 24, 255))
    for i, r in enumerate(REALMS):
        pop = min(1, max(0, (u - i * 0.08) / 0.2))
        if pop <= 0: continue
        b0, b1 = BND[i]; band = BANDS[i].copy()
        off = int((1 - pop) ** 2 * (1100 if i % 2 else -1100))   # bands slide in from alternating sides
        img.alpha_composite(band, (off, b0))
        if i > 0: layer(img, lambda dd: dd.rectangle([0, b0, W, b0 + 3], fill=(14, 10, 24, 255)))
        cy = CROWY[i]
        gi = r['gimg']; img.alpha_composite(gi, (int(off + 640 - gi.width / 2), int(cy - gi.height / 2)))
        d = ImageDraw.Draw(img); bx = off + 380
        d.ellipse([bx - 50, cy - 50, bx + 50, cy + 50], fill=(255, 214, 60), outline=(20, 15, 35), width=6)
        ctext(d, bx, cy - 23, str(i + 1), F(48), (20, 15, 35), 0)
    img.alpha_composite(END_HOOK)
    return img
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v9_noaudio.mp4' if not STILL else 'still_tmp.mp4'], stdin=subprocess.PIPE)
ev = []
rng = random.Random(3); BLK = 60
order = [(bx, by) for by in range(0, H, BLK) for bx in range(0, W, BLK)]; rng.shuffle(order)
F0 = None
for f in ([int(x) for x in STILL.split(',')] if STILL else range(int(round(TOTAL * FPS)))):
    t = f / FPS; i = int(t // SEG)
    if i < len(REALMS):
        u = (t - i * SEG) / SEG; img = scene(i, t, u)
        # pixel-block transition into the next realm / end card
        tl = (i + 1) * SEG - t
        if tl < TR:
            nxt = scene(i + 1, t, 0.0) if i + 1 < len(REALMS) else endcard(t, 0.0)
            n = int(len(order) * (1 - tl / TR))
            m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
            for bx, by in order[:n]: md.rectangle([bx, by, bx + BLK - 1, by + BLK - 1], fill=255)
            img.paste(nxt, (0, 0), m)
            if i + 1 == len(REALMS): img.alpha_composite(END_HOOK); img.alpha_composite(END_HOOK)   # band switches cleanly (no garbled mixed text)
    else:
        ue = t - len(REALMS) * SEG; img = endcard(t, ue)
        if ue >= END_HOLD:   # dissolve back into the exact frame-0 village so the reel loops
            if F0 is None: F0 = scene(0, 0.0, 0.0)
            n = int(len(order) * min(1, (ue - END_HOLD) / TR))
            m = Image.new('L', (W, H), 0); md = ImageDraw.Draw(m)
            for bx, by in order[:n]: md.rectangle([bx, by, bx + BLK - 1, by + BLK - 1], fill=255)
            img.paste(F0, (0, 0), m)
            img.alpha_composite(HOOK); img.alpha_composite(HOOK)
    ff.stdin.write(img.convert('RGB').tobytes())
    if STILL: img.convert('RGB').save(f'still_{f}.png')
ff.stdin.close(); ff.wait()
# SFX on real events only (no repeating twinkle): chime at the start, swish on each realm dissolve, coins as the grid cards pop, swish back to the start
ev.append((0.0, 'chime'))
for i in range(1, len(REALMS) + 1): ev.append((round(i * SEG - TR + 0.05, 3), 'swish'))
for i in range(5): ev.append((round(len(REALMS) * SEG + i * 0.08 + 0.1, 3), 'coin_8bit'))
ev.append((round(len(REALMS) * SEG + END_HOLD, 3), 'swish'))
json.dump({'events': ev}, open('v9_ev.json', 'w')); print('done', TOTAL)
