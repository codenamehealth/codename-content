import sys, math, random, json, subprocess, os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from sim5 import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1'); from hook2 import hook_layer2
HOOKB, HB = hook_layer2(['Who fills', 'the machine?'], accent=1, sub='Comment your pick')   # comment prompt from frame 0, 44px+
DY = 0   # sim5 already has the final globe position
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
ICON = {n: face(n, 48) for n in NAMES}   # scoreboard faces 88 -> 100px
def ball(n):
    g0 = Image.open(S + f'pixellab/gummies/pick_{GUMOF[n]}.png').convert('RGBA')
    if GUMOF[n] == 'acv':    # gummy gloss on Syeda's apple-shaped ACV gummy so it reads as a gummy, not a real apple
        gl = Image.new('RGBA', g0.size, (0, 0, 0, 0)); ImageDraw.Draw(gl).arc([5, 7, 26, 29], 290, 350, fill=(255, 240, 230, 170), width=2)
        gl.putalpha(Image.fromarray(__import__('numpy').minimum(__import__('numpy').array(gl.getchannel('A')), __import__('numpy').array(g0.getchannel('A')))))
        g0.alpha_composite(gl)
    g = up(g0, 3)
    pad = Image.new('RGBA', (g.width + 18, g.height + 18), (0, 0, 0, 0)); pad.alpha_composite(g, (9, 9))
    al = pad.getchannel('A').point(lambda p: 255 if p > 60 else 0).filter(ImageFilter.MaxFilter(11))   # thicker guide-colour ring: ownership reads at a glance
    o = Image.new('RGBA', pad.size, RING[n] + (255,)); o.putalpha(al)
    al2 = pad.getchannel('A').point(lambda p: 255 if p > 60 else 0).filter(ImageFilter.MaxFilter(15))
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
SEED = int(sys.argv[1]); STILLS = [float(x) for x in sys.argv[2:]]
FR, EV, CNT, LEAD, TEND = run(SEED)
win = max(CNT, key=CNT.get); print('winner', win, CNT, LEAD, round(TEND, 1), 'frames', len(FR))
VICF = gif(VIC[win], 380)
HOLD = 38; RESET = 9                    # recut: motion from frame 0 (no static pre-roll), winner held ~1.27s, 0.3s reset, loop
NR = len(FR); seqf = list(range(NR)) + [NR - 1] * (HOLD + RESET)
# lead-change stamps (no overlaps: a new stamp replaces the old one; a lead that lasts <0.5s is not stamped unless it is the winner)
lead_at = []
for k in range(NR):
    c = FR[k][1]; mx = max(c.values()); ld = [n for n in NAMES if c[n] == mx]
    lead_at.append(ld[0] if len(ld) == 1 else None)
changes = []; cur = None
for k, L in enumerate(lead_at):
    if L is not None and L != cur:
        hold = 0
        while k + hold < NR and lead_at[k + hold] in (L, None): hold += 1
        if hold >= 15 or k + hold >= NR: changes.append((k, L))
        cur = L
STAMPS = []
for i, (k, L) in enumerate(changes):
    end = min(k + 21, changes[i + 1][0] if i + 1 < len(changes) else NR)
    STAMPS.append((k, end, L))
print('stamps', [(round(a / 30, 2), round(b / 30, 2), L) for a, b, L in STAMPS])
ACV_T0 = (STAMPS[0][1] / 30 + 0.05) if STAMPS else 0.3
def stamp_img(L, u):
    f1, f2 = F(60), F(46); t1 = LABEL[L]; t2 = 'TAKES THE LEAD!'
    im = Image.new('RGBA', (900, 160), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 895, 155], 22, fill=(14, 10, 24, 245), outline=RING[L] + (255,), width=8)
    ctext(d, 450, 22, t1, f1, RING[L], 8); ctext(d, 450, 96, t2, f2, (255, 255, 255), 7)
    sc = 1.0 + 0.25 * max(0, 1 - u / 0.12)
    if sc > 1.01: im = im.resize((int(im.width * sc), int(im.height * sc)), Image.NEAREST)
    return im
ff = None if STILLS else subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', '30', '-i', '-',
                       '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', 'v5_noaudio.mp4'], stdin=subprocess.PIPE)
out_ev = []; lastsfx = -9; F64 = F(56); F80 = F(80)   # score digits 40 -> 56px
SB0 = HB + 10; SB1 = SB0 + 116          # scoreboard band (2x: 104px faces, 64px numbers)
for f, k in enumerate(seqf):
    t = f / 30; ts = k / 30; balls, counts, ang = FR[k]
    if STILLS and not any(abs(t - x) < 0.5 / 30 for x in STILLS): continue
    reset = f >= NR + HOLD; ru = (f - NR - HOLD) / RESET if reset else 0
    if reset: counts = {n: 3 for n in NAMES}
    img = BGS[int(t * 6) % len(BGS)].copy()
    img.alpha_composite(BASE, (GX - BASE.width // 2, GY + GR - 40))
    img.alpha_composite(GB)
    img.alpha_composite(internals(ang))
    for n, x, y in balls:
        b = BALL[n]
        if reset:     # machine empties back to the start: every gummy pops away
            sc = max(0.0, 1 - ru)
            if sc <= 0.05: continue
            b = b.resize((max(1, int(b.width * sc)), max(1, int(b.height * sc))), Image.NEAREST)
        img.alpha_composite(b, (int(x - b.width / 2), int(y - b.height / 2)))
    img.alpha_composite(CUP, (CUPX - CUP.width // 2, CUPY - CUP.height + 22))
    PL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(PL)
    for ei, (te, kind, n, kk) in enumerate(EV):
        u = ts - te
        if f < NR and 0 <= u < 0.9:
            a = int(255 * min(1, (0.9 - u) / 0.3))
            for q in range(10):
                an = q * 0.628 + te; rr = 30 + 160 * u
                sx, sy = CUPX + rr * math.cos(an), CUPY - 40 + rr * math.sin(an) * 0.8
                d.rectangle([sx - 7, sy - 7, sx + 7, sy + 7], fill=RING[n] + (a,))
            px_ = CUPX + (-150 if ei % 2 else 150)     # alternate sides so back-to-back pops never stack
            ctext(d, px_, CUPY - 200 - u * 60, f'+{kk}', F80, RING[n], 9, a)
            if u < 1 / 30 and te - lastsfx > 0.18:
                out_ev.append((round(te, 3), 'coin_8bit' if kk < 7 else 'powerup_8bit')); lastsfx = te
    img.alpha_composite(PL)
    img.alpha_composite(GF)
    img.alpha_composite(CAP, (GX - CAP.width // 2, GY - GR - CAP.height + 30))
    # scoreboard (2x)
    layer(img, lambda dd: dd.rounded_rectangle([70, SB0, 1025, SB1], 18, fill=(12, 8, 22, 230), outline=(255, 214, 60, 255), width=4))
    lead = lead_at[min(k, NR - 1)] if not reset else None
    for i, n in enumerate(NAMES):
        sx = 70 + 955 * (i + 0.5) / len(NAMES); ic = ICON[n]
        img.alpha_composite(ic, (int(sx - 114), SB0 + 6))
        d = ImageDraw.Draw(img); d.text((sx - 8, SB0 + 32), str(counts[n]), font=F64, fill=RING[n] + (255,), stroke_width=7, stroke_fill=(20, 15, 35, 255))
        if n == lead and f < NR: d.ellipse([sx - 118, SB0 + 2, sx - 6, SB0 + 114], outline=(255, 214, 60, 255), width=6)
    if f < min(45, STAMPS[0][0] if STAMPS else 45): ctext(ImageDraw.Draw(img), GX, GY - 250, 'PICK ONE!', F(72), (255, 255, 255), 10)
    # 'ACV GUMMY' tag on a Joy gummy the first time the board is calm (after the first stamp, before Joy's first burst)
    if ACV_T0 <= t < ACV_T0 + 1.2 and not reset:
        jb = [(x, y) for n, x, y in balls if n == 'joy']
        if jb:
            jx, jy = min(jb, key=lambda p: p[1]); tag = 'ACV GUMMY'; f44 = F(44)
            L2 = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d2 = ImageDraw.Draw(L2); tw = d2.textlength(tag, font=f44)
            x0 = max(80, min(1015 - tw - 36, jx - tw / 2 - 18)); y0 = jy - 150
            d2.rounded_rectangle([x0, y0, x0 + tw + 36, y0 + 72], 14, fill=(14, 10, 24, 235), outline=RING['joy'] + (255,), width=5)
            d2.polygon([(jx - 14, y0 + 70), (jx + 14, y0 + 70), (jx, y0 + 100)], fill=RING['joy'] + (255,))
            d2.text((x0 + 18, y0 + 14), tag, font=f44, fill=(255, 255, 255), stroke_width=5, stroke_fill=(10, 6, 18))
            img.alpha_composite(L2)
    for (a0, a1, L) in STAMPS:
        if a0 <= f < a1 and f < NR:
            sti = stamp_img(L, (f - a0) / 30); img.alpha_composite(sti, (int(GX - sti.width / 2), int(SB1 + 8 + 80 - sti.height / 2)))
            if f == a0: out_ev.append((round(t, 3), 'whoosh_8bit'))
    if NR <= f < NR + HOLD:
        u = (f - NR) / 30
        img.alpha_composite(Image.new('RGBA', (W, H), (8, 6, 14, 165)))
        vf = VICF[int(u * 8) % len(VICF)]; img.alpha_composite(vf, (GX - vf.width // 2, 1170 - vf.height))
        sc = 1.0 + 0.2 * max(0, 1 - u / 0.12)
        d = ImageDraw.Draw(img); ctext(d, GX, 1200, LABEL[win] + ' WINS!', F(int(64 * sc)), (255, 214, 60), 9)
        ctext(d, GX, 1300, f'{counts[win]} GUMMIES', F(52), RING[win], 8)
        if f == NR: out_ev.append((round(t, 3), 'victory'))
    if f == NR + HOLD: out_ev.append((round(t, 3), 'poof'))
    img.alpha_composite(HOOKB)
    if STILLS: img.convert('RGB').save(f'st_{t:.2f}.png'); continue
    ff.stdin.write(img.convert('RGB').tobytes())
if not STILLS:
    ff.stdin.close(); ff.wait()
    json.dump({'events': out_ev}, open('machine_events.json', 'w'))
print('done', len(seqf) / 30, 'win at', NR / 30)
