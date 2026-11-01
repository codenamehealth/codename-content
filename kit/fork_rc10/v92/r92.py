import sys; SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_a7'); from common7 import *
sys.path.insert(0, SP0 + 'pixellab/safezone'); from hook import hook_layer
# #92 Nightmare mode, lock on to Cleo: safe zone + hook only (source fork_b9/v94/render.py, seed 4). All formations are
# mapped into the zone (x' = 490 + 0.85 (x - 540), y' = 1000 + 0.85 (y - 1080)); orbs unchanged 4x; same shuffles and answer.
os.chdir(os.path.dirname(os.path.abspath(__file__))); B9 = SP0 + 'fork_b9/v94/'
import numpy as np
import hook as HK
# rc10 review recut (source fork_sz86/v92/r92.py). Bennett loves it: bug/legibility/universal fixes only; same shuffles, same answer.
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 4
rnd = random.Random(SEED)
N = 16; CX, CY = 540, 1080
def circle(r=380, a0=-math.pi / 2): return [(CX + r * math.cos(a0 + 2 * math.pi * i / N), CY + r * math.sin(a0 + 2 * math.pi * i / N)) for i in range(N)]
def cluster(): return [(CX + 70 * math.cos(i * 2.4) * math.sqrt(i + 1) / 2.2, CY + 70 * math.sin(i * 2.4) * math.sqrt(i + 1) / 2.2) for i in range(N)]
def line(): return [(CX + (-55 if i % 2 else 55), CY - 480 + i * 64) for i in range(N)]   # was 80px steps (ran y480-1680)
def star():
    pts = []
    for i in range(10):
        r = 400 if i % 2 == 0 else 170; a = -math.pi / 2 + i * math.pi / 5; pts.append((CX + r * math.cos(a), CY + r * math.sin(a)))
    for i in range(6): a = i * math.pi / 3; pts.append((CX + 70 * math.cos(a), CY + 70 * math.sin(a)))
    return pts
def grid(): return [(CX - 300 + (i % 4) * 200, CY - 300 + (i // 4) * 200) for i in range(N)]
def arrow():
    pts = [(CX - 330 + i * 85, CY) for i in range(8)]
    pts += [(CX + 300 - k * 80, CY - k * 80) for k in range(1, 5)] + [(CX + 300 - k * 80, CY + k * 80) for k in range(1, 5)]
    return pts
def chevron(): return [(CX - 405 + i * 54, CY + 260 - (i if i < 8 else 15 - i) * 90 - (0 if i < 8 else 0)) for i in range(N)]
def spiral(): return [(CX + (90 + i * 22) * math.cos(i * 0.85), CY + (90 + i * 22) * math.sin(i * 0.85)) for i in range(N)]
FORMS = [circle(341), cluster(), line(), star(), grid(), spiral(), arrow(), chevron(), circle(341)]
FX, FY, FS = 496, 1030, 0.85   # rc10: play area 30px lower (taller hook band), x +6 so the bigger numbers clear the left edge
FORMS = [[(FX + (x - CX) * FS, FY + (y - CY) * FS) for x, y in fm] for fm in FORMS]
def band(lines, accent, sub, subsize=46, color=(255, 214, 60), subcol=(255, 214, 60)):
    f, s_ = HK._fit([l.upper() for l in lines], HK.X1 - HK.X0 - 40)
    gap = int(s_ * 0.38); pad = 22; fs = ImageFont.truetype(HK.FONT, subsize)
    h = len(lines) * s_ + (len(lines) - 1) * gap + 2 * pad + subsize + gap
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle([HK.X0, HK.Y0, HK.X1, HK.Y0 + h], 22, fill=(14, 10, 24, 225), outline=color, width=6)
    y = HK.Y0 + pad
    for i, l in enumerate(lines):
        l = l.upper(); w_ = d.textlength(l, font=f)
        d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), l, font=f, fill=color if accent == i else (255, 255, 255), stroke_width=9, stroke_fill=(10, 6, 18)); y += s_ + gap
    w_ = d.textlength(sub, font=fs)
    d.text(((HK.X0 + HK.X1) / 2 - w_ / 2, y), sub, font=fs, fill=subcol, stroke_width=7, stroke_fill=(10, 6, 18))
    return L, HK.Y0 + h
# rc10: COMMENT HER NUMBER (46px) in the band from frame 0; replaces the 26px end card 'Which number is Cleo? / COMMENT IF YOU KEPT HER'
HOOKS = {k: band(['NIGHTMARE MODE', k], 0, 'COMMENT HER NUMBER', color=(255, 70, 80)) for k in ('LOCK ON TO CLEO', "DON'T LOSE HER.", 'WHICH NUMBER?')}
HBMAX = max(v[1] for v in HOOKS.values()); print('hook bottoms', [v[1] for v in HOOKS.values()])
# timeline
T_INTRO = 1.9; MOVE, HOLD = 1.05, 0.45   # rc10: intro 2.6 -> 1.9s (shrink starts 0.5s)
sched = []; t = T_INTRO
for k in range(1, len(FORMS)): sched.append((t, t + MOVE, k)); t += MOVE + HOLD
T_END = t; DUR = T_END + 2.0   # rc10: question hold 3.2 -> 2.0s, then loop
# assignment: orb i sits at slot perm[k][i] in form k
perm = [list(range(N))]
for k in range(1, len(FORMS)):
    p = list(range(N)); rnd.shuffle(p); perm.append(p)
CLEO = 0  # orb index; starts at slot 0 of circle? pick a slot
perm[0] = list(range(N)); start_slot = 13; perm[0][CLEO], perm[0][start_slot] = start_slot, 0
def pos(i, t):
    if t < sched[0][0]: return FORMS[0][perm[0][i]]
    for (t0, t1, k) in sched:
        if t0 <= t < t1:
            u = (t - t0) / (t1 - t0); e = u * u * (3 - 2 * u)
            a = FORMS[k - 1][perm[k - 1][i]]; b = FORMS[k][perm[k][i]]
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2; dx, dy = b[0] - a[0], b[1] - a[1]
            off = (0.35 if i % 2 else -0.35) * math.sin(math.pi * e)
            return (a[0] + dx * e - dy * off * 0.6, a[1] + dy * e + dx * off * 0.6)
        if t < t0: return FORMS[k - 1][perm[k - 1][i]]
    return FORMS[-1][perm[-1][i]]
_pos0 = pos
def pos(i, t):
    x, y = _pos0(i, t); y = max(HBMAX + 76 + 50, min(1500 - 52, y))
    return max(70 + 46, min((887 if y + 50 > 1110 else 1025) - 46, x)), y
final_slot = perm[-1][CLEO]  # slot index in final circle; numbers clockwise from top = slot+1
print('CLEO final number', final_slot + 1)
ORB = up(crop(Image.open(B9 + '../gen/orb/00.png').convert('RGBA')), 4)
_m = Image.open(A + 'bg_moon.gif'); _m.seek(0); MOON = _m.convert('RGBA').crop((700, 40, 930, 270))
_mm = Image.new('L', MOON.size, 0); ImageDraw.Draw(_mm).ellipse([17, 14, 216, 209], fill=255); MOON.putalpha(_mm)
MOON = up(ImageEnhance.Brightness(MOON).enhance(0.5), 2)
_sky = Image.new('RGBA', (W, H)); _sd = ImageDraw.Draw(_sky)
for y in range(H): c = int(18 + 14 * y / H); _sd.line([(0, y), (W, y)], fill=(c, 8, c + 22, 255))
_gl = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _gd = ImageDraw.Draw(_gl)
for r, a in ((330, 18), (280, 26), (240, 34)): _gd.ellipse([W // 2 - r, 140 - r, W // 2 + r, 140 + r], fill=(200, 170, 120, a))
_sky.alpha_composite(_gl); _sky.alpha_composite(MOON, (W // 2 - MOON.width // 2, 140 - MOON.height // 2))   # moon peeks above the hook
BGF = [_sky]
VIG = Image.new('RGBA', (W, H), (0, 0, 0, 0)); vd = ImageDraw.Draw(VIG)
for k in range(40):
    a = int(k * 4.2); vd.rectangle([k * 9, k * 12, W - k * 9, H - k * 12], outline=(90, 0, 20, max(0, 170 - a)), width=10)
CLEO_ID = idle('cleo', 3); FACE = None
rs = random.Random(9); STARS = [(rs.uniform(0, W), rs.uniform(0, H), rs.uniform(0, 6)) for _ in range(120)]
out = Writer('v92_noaudio.mp4'); events = []   # rc10: no fixed-interval whoosh_8bit on every formation change
trail = {i: [] for i in range(N)}
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BGF[int(t * 6) % len(BGF)].copy()
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for x, y, p in STARS:
        a = int(110 + 110 * math.sin(t * 2.5 + p)); d.rectangle([x, y, x + 3, y + 3], fill=(220, 220, 255, max(0, a)))
    img.alpha_composite(L); img.alpha_composite(VIG)
    P = [pos(i, t) for i in range(N)]
    # trails
    TL = Image.new('RGBA', (W, H), (0, 0, 0, 0)); td = ImageDraw.Draw(TL)
    for i in range(N):
        trail[i] = (trail[i] + [P[i]])[-7:]
        for j, (x, y) in enumerate(trail[i][:-1]):
            r = 6 + j * 3; td.ellipse([x - r, y - r, x + r, y + r], fill=(140, 170, 255, 25 + j * 12))
    img.alpha_composite(TL)
    for i in range(N):
        x, y = P[i]; bob = 5 * math.sin(t * 3 + i)
        img.alpha_composite(ORB, (int(x - ORB.width / 2), int(y - ORB.height / 2 + bob)))
    # intro: Cleo shrinks into her orb
    if t < T_INTRO:
        x, y = P[CLEO]
        def ring(dd, x=x, y=y):   # rc10: the gold lock-on ring spins from frame 0
            for j in range(8):
                a0 = j * 45 + t * 160; dd.arc([x - 70, y - 70, x + 70, y + 70], a0, a0 + 30, fill=(255, 214, 60, 255), width=8)
        layer(img, ring)
        if t < 1.0:
            k = 1.0 if t < 0.5 else max(0.05, 1 - (t - 0.5) / 0.5)
            cf = CLEO_ID[int(t * 6) % len(CLEO_ID)]; cf = cf.resize((max(1, int(cf.width * k)), max(1, int(cf.height * k))), Image.NEAREST)
            img.alpha_composite(cf, (int(x - cf.width / 2), int(y - 40 * k - 78 * 3 * k + cf.height * 0.18)))
            text_layer(img, [(x, y - 312, 'CLEO', 56, (120, 170, 255), 8, 255)])   # rc10: 40 -> 56px
        if 0.5 <= t < 1.0 and not any(e[1] == 'poof' for e in events): events.append((0.5, 'poof'))
        if t >= 1.0:
            if not any(e[1] == 'twinkle' for e in events): events.append((1.0, 'twinkle'))
            text_layer(img, [(x + 268, y - 22, '<THAT ONE', 44, (255, 214, 60), 8, int(255 * min(1, (T_INTRO - t) / 0.4)))])   # rc10: 34 -> 48px
    sub = 'LOCK ON TO CLEO' if t < T_INTRO else ("DON'T LOSE HER." if t < T_END else 'WHICH NUMBER?')
    if T_INTRO <= t < T_END:
        k_done = sum(1 for s in sched if t >= s[1])
        lvl = min(k_done + 1, len(sched))   # rc10 BUG FIX: capped (it read LEVEL 9/8 during the last settle)
        layer(img, lambda dd: dd.rounded_rectangle([547 - 220, HBMAX + 10, 547 + 220, HBMAX + 74], 14, fill=(10, 6, 20, 225), outline=(190, 180, 230, 255), width=4))
        text_layer(img, [(547, HBMAX + 20, f'LEVEL {lvl}/{len(sched)}', 44, (210, 200, 245), 7, 255)])   # 28 -> 44px
    if t >= T_END:
        if not any(e[1] == 'ding_8bit' for e in events): events.append((round(T_END, 3), 'ding_8bit'))
        a = min(255, int((t - T_END) / 0.3 * 255))
        items = []
        for s in range(N):
            ang = -math.pi / 2 + 2 * math.pi * s / N; nx, ny = FX + 374 * math.cos(ang), FY + 374 * math.sin(ang)
            items.append((nx, ny - 24, str(s + 1), 48, (255, 214, 60), 7, a))   # rc10: numbers 34 -> 48px
        text_layer(img, items)
    img.alpha_composite(HOOKS[sub][0])
    out.write(img)
    if f in (0, 12, 40, int(sched[-1][1] * FPS) + 5, int(DUR * FPS) - 1): img.convert('RGB').save(f'f92_{f}.png')
out.close(); json.dump({'events': events}, open('v92_ev.json', 'w')); print('dur', DUR, 'hb', HBMAX)
