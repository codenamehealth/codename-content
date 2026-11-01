import sys, math, random, json, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from sim import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/pixellab/safezone'); from hook import hook_layer
HOOKB, HB = hook_layer(['Who fills', 'the machine?'], accent=1)
DY = 60
S = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
A = S + 'pause/assets/'; FONT = S + 'npmfont/ps/package/files/PressStart2P.ttf'
W, H = 1080, 1920
def F(s): return ImageFont.truetype(FONT, s)
def crop(im): return im.crop(im.getbbox())
def up(im, k): return im.resize((im.width * k, im.height * k), Image.NEAREST)
def layer(img, fn):
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); fn(ImageDraw.Draw(L)); img.alpha_composite(L)
LABEL = {'joy': 'JOY', 'cyrus': 'CYRUS', 'cleo': 'CLEO', 'ray': 'RAYLEIGH', 'hollow': 'THE HOLLOW'}
RING = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'hollow': (170, 160, 200)}
GUMOF = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel', 'hollow': 'gold'}
SRC = {'joy': 'char1/char11.png', 'ray': 'char2/char4.png', 'cleo': 'char3/char6.png', 'cyrus': 'char4/char9.png', 'hollow': 'hollow/char1.png'}
def face(name, rad):
    im = Image.open(S + 'syeda_src/' + SRC[name]).convert('RGBA')
    bb = im.getbbox(); cx = (bb[0] + bb[2]) // 2
    head = im.crop((cx - 15, 12, cx + 15, 42)).resize((2 * rad - 8, 2 * rad - 8), Image.NEAREST)
    b = Image.new('RGBA', (2 * rad + 4, 2 * rad + 4), (0, 0, 0, 0)); d = ImageDraw.Draw(b)
    d.ellipse([2, 2, 2 * rad + 1, 2 * rad + 1], fill=(20, 16, 30, 255)); d.ellipse([4, 4, 2 * rad - 1, 2 * rad - 1], fill=RING[name] + (255,))
    d.ellipse([9, 9, 2 * rad - 6, 2 * rad - 6], fill=(235, 232, 220, 255))
    m = Image.new('L', head.size, 0); ImageDraw.Draw(m).ellipse([0, 0, head.width - 1, head.height - 1], fill=255)
    b.paste(head, (6, 6), Image.composite(head, Image.new('RGBA', head.size, (0, 0, 0, 0)), m).getchannel('A'))
    return b
ICON = {n: face(n, 42) for n in NAMES}
def ball(n):
    g = up(Image.open(S + f'pixellab/gummies/pick_{GUMOF[n]}.png').convert('RGBA'), 3)
    pad = Image.new('RGBA', (g.width + 10, g.height + 10), (0, 0, 0, 0)); pad.alpha_composite(g, (5, 5))
    al = pad.getchannel('A').point(lambda p: 255 if p > 60 else 0).filter(ImageFilter.MaxFilter(7))
    o = Image.new('RGBA', pad.size, RING[n] + (255,)); o.putalpha(al)
    al2 = pad.getchannel('A').point(lambda p: 255 if p > 60 else 0).filter(ImageFilter.MaxFilter(11))
    o2 = Image.new('RGBA', pad.size, (20, 15, 30, 255)); o2.putalpha(al2)
    big = Image.new('RGBA', pad.size, (0, 0, 0, 0)); big.alpha_composite(o2); big.alpha_composite(o); big.alpha_composite(pad)
    return big
BALL = {n: ball(n) for n in NAMES}
BASE = up(crop(Image.open(S + 'forkA/assets/gb_base/02.png').convert('RGBA')), 5)
CAP = up(crop(Image.open(S + 'forkA/assets/gb_cap/08.png').convert('RGBA')), 5)
CUP = up(crop(Image.open(S + 'forkA/assets/cup/01.png').convert('RGBA')), 3)
# background: Liza's village, darkened
hub = Image.open(A + 'hub.gif'); BGS = []; sc = H / 1080; cw = int(W / sc)
for i in range(0, hub.n_frames, 2):
    hub.seek(i); f = hub.convert('RGB').crop((960 - cw // 2, 0, 960 - cw // 2 + cw, 1080)).resize((W, H), Image.NEAREST)
    BGS.append(ImageEnhance.Brightness(f).enhance(0.42).convert('RGBA'))
GY = GY + DY; CUPY = CUPY + DY; HUBY = HUBY + DY
Q = 4
def globe_back():
    L = Image.new('RGBA', (W // Q, H // Q), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    cx, cy, r = GX / Q, GY / Q, GR / Q + 2
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(40, 60, 100, 110))
    return up(L, Q)
def globe_front():
    L = Image.new('RGBA', (W // Q, H // Q), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    cx, cy, r = GX / Q, GY / Q, GR / Q + 3
    d.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], outline=(30, 30, 50, 255), width=2)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(200, 215, 240, 255), width=2)
    d.arc([cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8], 200, 255, fill=(255, 255, 255, 220), width=3)
    d.arc([cx - r + 16, cy - r + 16, cx + r - 16, cy + r - 16], 215, 235, fill=(255, 255, 255, 160), width=2)
    return up(L, Q)
GB, GF = globe_back(), globe_front()
def internals(angle):
    L = Image.new('RGBA', (W // Q, H // Q), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    # pole
    d.rectangle([CUPX / Q - 2, (CUPY + 10) / Q, CUPX / Q + 2, HUBY / Q], fill=(170, 130, 50, 255))
    d.rectangle([CUPX / Q - 1, (CUPY + 10) / Q, CUPX / Q, HUBY / Q], fill=(240, 200, 90, 255))
    # paddle
    for k in range(2):
        a = angle + k * math.pi; ex, ey = GX / Q + ARM / Q * math.cos(a), HUBY / Q + ARM / Q * math.sin(a)   # matches the physics arm (stays inside the glass)
        d.line([GX / Q, HUBY / Q, ex, ey], fill=(110, 80, 40, 255), width=5); d.line([GX / Q, HUBY / Q, ex, ey], fill=(200, 160, 80, 255), width=2)
    d.ellipse([GX / Q - 5, HUBY / Q - 5, GX / Q + 5, HUBY / Q + 5], fill=(220, 180, 70, 255), outline=(90, 60, 30, 255))
    return up(L, Q)
def ctext(d, x, y, t, f, fill=(255, 255, 255), sw=6, a=255):
    w = d.textlength(t, font=f); d.text((x - w / 2, y), t, font=f, fill=fill + (a,), stroke_width=sw, stroke_fill=(20, 15, 35, a))
VIC = {'joy': 'vic_Victory_Pose.gif', 'cyrus': 'vic_VictoryPose_1_2f3491a2-9eb4-4ed3-a96d-f50d84bb993a.gif', 'cleo': 'vic_victoryPose.gif', 'ray': 'vic_victoryPose_1.gif', 'hollow': 'hollow-victory.gif'}
def gif(p, h):
    im = Image.open(A + p); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA'))
    bb = None
    for f in fr:
        b = f.getbbox(); bb = b if bb is None else (min(bb[0], b[0]), min(bb[1], b[1]), max(bb[2], b[2]), max(bb[3], b[3]))
    fr = [f.crop(bb) for f in fr]; k = h / fr[0].height
    return [f.resize((int(f.width * k), h), Image.NEAREST) for f in fr]
SEED = int(sys.argv[1]); STILL = len(sys.argv) > 2
FR, EV, CNT, LEAD, TEND = run(SEED)
win = max(CNT, key=CNT.get); print('winner', win, CNT, LEAD, round(TEND, 1))
VICF = gif(VIC[win], 380)
PRE = 45; HOLD = 95
seqf = [0] * PRE + list(range(len(FR))) + [len(FR) - 1] * HOLD
ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v5_noaudio.mp4'], stdin=subprocess.PIPE)
out_ev = []; lastsfx = -9; F34 = F(34); F44 = F(44); F40 = F(40)
for f, k in enumerate(seqf):
    t = f / 30; ts = max(0, (f - PRE) / 30); balls, counts, ang = FR[k]
    img = BGS[int(t * 6) % len(BGS)].copy()
    img.alpha_composite(BASE, (GX - BASE.width // 2, GY + GR - 40))
    img.alpha_composite(GB)
    img.alpha_composite(internals(ang))
    for n, x, y in balls:
        b = BALL[n]; img.alpha_composite(b, (int(x - b.width / 2), int(y + DY - b.height / 2)))
    # cup + hit effects
    img.alpha_composite(CUP, (CUPX - CUP.width // 2, CUPY - CUP.height + 22))
    PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(PL)
    for (te, kind, n, kk) in EV:
        u = ts - te
        if f >= PRE and 0 <= u < 0.9:
            a = int(255 * min(1, (0.9 - u) / 0.3))
            for q in range(10):
                an = q * 0.628 + te; rr = 30 + 160 * u
                sx, sy = CUPX + rr * math.cos(an), CUPY - 40 + rr * math.sin(an) * 0.8
                d.rectangle([sx - 6, sy - 6, sx + 6, sy + 6], fill=RING[n] + (a,))
            ctext(d, CUPX, CUPY - 170 - u * 70, f'+{kk}', F44, RING[n], 6, a)
            if u < 1 / 30 and te - lastsfx > 0.18:   # was abs(u) < 1/60 inside u>=0: missed ~half the hit sounds
                out_ev.append((round(te + PRE / 30, 3), 'coin_8bit' if kk < 7 else 'powerup_8bit')); lastsfx = te
    img.alpha_composite(PL)
    img.alpha_composite(GF)
    img.alpha_composite(CAP, (GX - CAP.width // 2, GY - GR - CAP.height + 30))
    # header
    layer(img, lambda dd: dd.rounded_rectangle([70, 500, 1010, 600], 18, fill=(12, 8, 22, 225)))
    d = ImageDraw.Draw(img)
    lead = max(counts, key=counts.get) if max(counts.values()) > min(counts.values()) else None
    d.rounded_rectangle([70, 500, 1010, 600], 18, outline=(255, 214, 60, 255), width=4)
    for i, n in enumerate(NAMES):
        sx = 70 + 940 * (i + 0.5) / len(NAMES); ic = ICON[n]
        img.alpha_composite(ic, (int(sx - 88), 506))
        d = ImageDraw.Draw(img); d.text((sx + 8, 530), str(counts[n]), font=F40, fill=RING[n] + (255,), stroke_width=6, stroke_fill=(20, 15, 35, 255))
        if n == lead and f >= PRE: d.ellipse([sx - 92, 502, sx + 4, 598], outline=(255, 214, 60, 255), width=5)
    if f < PRE + 15: ctext(d, GX, 860, 'PICK ONE!', F(64), (255, 255, 255), 9)
    if f >= PRE + len(FR):
        u = (f - PRE - len(FR)) / 30; a = min(1, u / 0.3)
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, int(160 * a))))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (GX - vf.width // 2, 1180 - vf.height))
        d = ImageDraw.Draw(img); ctext(d, GX, 1230, LABEL[win] + ' WINS!', F(56), (255, 214, 60), 8)
        ctext(d, GX, 1320, f'{counts[win]} GUMMIES', F(40), RING[win], 6)
        if not any(e[1] == 'victory' for e in out_ev): out_ev.append((round(t, 3), 'victory'))
    img.alpha_composite(HOOKB)
    if STILL:
        if f in (10, PRE + len(FR) // 2, len(seqf) - 5): img.convert('RGB').save(f'h_still_{f}.png')
        continue
    ff.stdin.write(img.convert('RGB').tobytes())
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/h_{f:04d}.png')
ff.stdin.close(); ff.wait()
json.dump({'events': out_ev}, open('machine_events.json', 'w'))
print('done', len(seqf) / 30)
