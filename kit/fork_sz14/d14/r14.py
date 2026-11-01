import sys; sys.path.insert(0, '..')
from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
K = 5; GY = 1340; XS = [172, 464, 756]
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['WATCH', 'CAREFULLY'], accent=1)
IDL = idle('joy', K); RUN = seq(PL + 'race/joy_run', K, 1); RUNL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in RUN]
GUM = gummy('acv', 5)
g = Image.open(A + 'found_hd.gif'); BG = []
for i in range(0, g.n_frames, 2):
    g.seek(i); BG.append(g.convert('RGB').resize((3413, 1920), Image.NEAREST).crop((1166, 0, 1166 + W, H)).convert('RGBA'))
# shell swaps
HOLDER = 1                                   # gummy hidden with the Joy who starts in the middle
pos = [0, 1, 2]                              # pos[j] = slot of Joy j
T_HIDE = 2.2; T_SHUF = 3.2
swaps = []; t = T_SHUF
durs = [0.62, 0.58, 0.54, 0.5, 0.46, 0.42, 0.4, 0.38, 0.36, 0.36]
for d in durs:
    a, b = rnd.sample([0, 1, 2], 2); swaps.append((t, d, a, b)); t += d + 0.06
T_LINE = t + 0.1
T_Q = T_LINE + 0.3; T_C = T_Q + 2.6; DUR = T_C + 2.4
# precompute slot timeline per joy
def joy_state(j, tt):
    """returns x, y, vx, moving"""
    slot = j  # initial slot
    for (ts, d, a, b) in swaps:
        if tt < ts: break
        sa = slot
        # which slots swap: slots a and b
        if sa in (a, b):
            other = b if sa == a else a
            if tt < ts + d:
                u = (tt - ts) / d; e = u * u * (3 - 2 * u)
                x0, x1 = XS[sa], XS[other]; x = x0 + (x1 - x0) * e
                arc = (1 if sa < other else -1) * 150 * math.sin(math.pi * u) * (abs(other - sa) / 2 + 0.5)
                arc = arc * 0.5 if arc > 0 else arc
                return x, GY + arc, (x1 - x0), True
            slot = other
    return XS[slot], GY, 0, False
final_slot = joy_state(HOLDER, 99)[0]
print('gummy ends at slot', XS.index(final_slot), 'ABC'[XS.index(final_slot)])
out = Writer('d14_noaudio.mp4'); ev = []
def once(name, t0, tt):
    if t0 <= tt < t0 + 1 / FPS and (round(t0, 3), name) not in ev: ev.append((round(t0, 3), name))
for f in range(int(DUR * FPS)):
    tt = f / FPS; img = BG[int(tt * 6) % len(BG)].copy()
    sts = [(j,) + joy_state(j, tt) for j in range(3)]
    layer(img, lambda d: [d.ellipse([x - 75, y - 14, x + 75, y + 14], fill=(0, 0, 0, 70)) for (_, x, y, vx, m) in sts])
    for j, x, y, vx, mv in sorted(sts, key=lambda s: s[2]):
        if mv: fr = (RUN if vx > 0 else RUNL)[int(tt * 16) % 8]; ox = 46 * K
        else: fr = IDL[(int(tt * 8) + j * 2) % 6]; ox = 46 * K
        img.alpha_composite(fr, (int(x - ox), int(y - 78 * K)))
    # gummy intro: drops in front of the middle Joy, floats, then she tucks it away
    if tt < T_HIDE + 0.4:
        gx = XS[HOLDER]
        if tt < 0.6:
            v = tt / 0.6; gy = -150 + (GY - 40 + 150) * v * v; s = 1.0
        elif tt < T_HIDE:
            gy = GY - 40 - 330 * min(1, (tt - 0.6) / 0.4) + 10 * math.sin(tt * 5); s = 1.0
        else:
            v = (tt - T_HIDE) / 0.4; gy = GY - 370 + 200 * v; s = 1 - v
        gi = up(GUM, max(0.05, s)) if s < 1 else GUM
        img.alpha_composite(gi, (int(gx - gi.width / 2), int(gy - gi.height)))
        if 0.6 < tt < T_HIDE:
            L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            for k in range(5):
                a = tt * 3 + k * 1.256; px, py = gx + 80 * math.cos(a), gy - 50 + 40 * math.sin(a)
                d.rectangle([px - 5, py - 5, px + 5, py + 5], fill=(255, 245, 190, 230))
            img.alpha_composite(L)
    once('whoosh_8bit', 0.0, tt); once('coin_8bit', 0.6, tt); once('poof', T_HIDE, tt)
    for (ts, d, a, b) in swaps: once('swish', ts, tt)
    once('chime', T_Q, tt); once('tick_8bit', T_C, tt)
    # text
    items = []
    head = 'Remember the gummy' if tt < T_SHUF - 0.3 else ('Watch carefully!!' if tt < T_Q else ('Where is the gummy?' if tt < T_C else 'Comment your answer'))
    items.append((W / 2, HB + 22, head, 44, (255, 255, 255) if tt < T_Q else (255, 214, 60), 7, 255))
    if tt >= T_Q:
        for k, x in enumerate(XS):
            items.append((x + 12, GY + 30, 'ABC'[k], 72, (255, 255, 255), 8, 255))
    text_layer(img, items); img.alpha_composite(HOOK)
    out.write(img)
    pass
out.close(); json.dump(ev, open('ev.json', 'w')); print('done', round(DUR, 2), len(ev))
