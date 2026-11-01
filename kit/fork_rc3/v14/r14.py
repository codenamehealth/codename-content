import sys, os
SP0 = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP0 + 'fork_sz14')
from common import *
sys.path.insert(0, SP0 + 'fork_rc2'); from rc2 import hook_layer2, gummy_src, acv_tag
sys.path.insert(0, SP0 + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
STILL = os.environ.get('STILL')
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 11)
K = 5; GY = 1340; XS = [172, 464, 756]   # 6x Joys don't fit three side by side inside x70-887 (bbox 282px > 267px spacing): kept 5x (320px)
# rc3: comment prompt as a real 52px band line from frame 0; at the question the band itself becomes the question
HOOK, HB = hook_layer2(['WATCH', 'CAREFULLY'], accent=1, sub='Comment A, B or C')
HOOKQ, HBQ = hook_layer2(['WHERE IS', 'THE GUMMY?'], accent=1, sub='Comment A, B or C')
print('hook bottoms', HB, HBQ)
IDL = idle('joy', K); RUN = seq(PL + 'race/joy_run', K, 1); RUNL = [f.transpose(Image.FLIP_LEFT_RIGHT) for f in RUN]
GUM = up(acv_gummy_strong(), 5)          # Syeda's ACV gummy + gummy gloss (vetting: reads as a gummy, not a real apple)
g = Image.open(A + 'found_hd.gif'); BG = []
for i in range(0, g.n_frames, 2):
    g.seek(i); BG.append(g.convert('RGB').resize((3413, 1920), Image.NEAREST).crop((1166, 0, 1166 + W, H)).convert('RGBA'))
HOLDER = 1
# rc3 timing: hover 0.6-1.7s (ACV GUMMY tag), visible drop into the middle Joy's hands 1.7-2.0s, sparkle burst 2.0-2.35s, shuffle from 2.5s
T_HIDE = 1.7; T_IN = 2.0; T_SHUF = 2.5
swaps = []; t = T_SHUF
durs = [0.62, 0.58, 0.54, 0.5, 0.46, 0.42, 0.4, 0.38, 0.36, 0.36]
for d in durs:
    a, b = rnd.sample([0, 1, 2], 2); swaps.append((t, d, a, b)); t += d + 0.06
T_LINE = t + 0.1
T_Q = T_LINE + 0.3; DUR = T_Q + 1.4          # rc3: 5.3s frozen end -> 1.4s hold, then cut back to the opening drop (loop)
def joy_state(j, tt):
    slot = j
    for (ts, d, a, b) in swaps:
        if tt < ts: break
        sa = slot
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
print('gummy ends at slot', XS.index(final_slot), 'ABC'[XS.index(final_slot)], 'T_Q', round(T_Q, 2), 'DUR', round(DUR, 2))
out = Writer('v14_noaudio.mp4' if not STILL else 'still_tmp.mp4'); ev = []
def once(name, t0, tt):
    if t0 <= tt < t0 + 1 / FPS and (round(t0, 3), name) not in ev: ev.append((round(t0, 3), name))
HANDY = GY - 150     # middle Joy's hands at 5x
NF = int(round(DUR * FPS))
for f in ([int(x) for x in STILL.split(',')] if STILL else range(NF)):
    tt = f / FPS; img = BG[int(tt * 6) % len(BG)].copy()
    sts = [(j,) + joy_state(j, tt) for j in range(3)]
    layer(img, lambda d: [d.ellipse([x - 75, y - 14, x + 75, y + 14], fill=(0, 0, 0, 70)) for (_, x, y, vx, m) in sts])
    for j, x, y, vx, mv in sorted(sts, key=lambda s: s[2]):
        if mv: fr = (RUN if vx > 0 else RUNL)[int(tt * 16) % 8]; ox = 46 * K
        else: fr = IDL[(int(tt * 8) + j * 2) % 6]; ox = 46 * K
        hop = 0
        if j == HOLDER and T_IN <= tt < T_IN + 0.3:   # little catch hop as the gummy lands in her hands
            hop = int(-36 * math.sin(math.pi * (tt - T_IN) / 0.3))
        img.alpha_composite(fr, (int(x - ox), int(y - 78 * K + hop)))
    gx = XS[HOLDER]
    if tt < T_IN:
        if tt < 0.6:
            v = tt / 0.6; gy = -150 + (GY - 40 + 150) * v * v; s = 1.0
        elif tt < T_HIDE:
            gy = GY - 40 - 330 * min(1, (tt - 0.6) / 0.4) + 10 * math.sin(tt * 5); s = 1.0
        else:   # drops into the middle Joy's hands, shrinking as she tucks it away
            v = (tt - T_HIDE) / (T_IN - T_HIDE); gy0 = GY - 370 + 10 * math.sin(T_HIDE * 5)
            gy = gy0 + (HANDY + 40 - gy0) * v * v; s = 1 - 0.65 * v
        gi = up(GUM, s) if s < 1 else GUM
        img.alpha_composite(gi, (int(gx - gi.width / 2), int(gy - gi.height)))
        if 0.6 < tt < T_HIDE:
            L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
            for k in range(5):
                a = tt * 3 + k * 1.256; px, py = gx + 80 * math.cos(a), gy - 50 + 40 * math.sin(a)
                d.rectangle([px - 5, py - 5, px + 5, py + 5], fill=(255, 245, 190, 230))
            img.alpha_composite(L)
            ta = int(255 * min(1, (tt - 0.6) / 0.15, (T_HIDE - tt) / 0.12))
            acv_tag(img, gx, int(gy - GUM.height) - 6, ta)
    if T_IN <= tt < T_IN + 0.35:   # sparkle burst where the gummy disappears into her hands
        u = (tt - T_IN) / 0.35
        L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); al = int(255 * (1 - u))
        cy = HANDY
        for k in range(8):
            a = k * math.pi / 4; r0, r1 = 30 + 90 * u, 70 + 110 * u
            d.line([(gx + r0 * math.cos(a), cy + r0 * math.sin(a)), (gx + r1 * math.cos(a), cy + r1 * math.sin(a))], fill=(255, 245, 190, al), width=12)
        rr = 40 * (1 - u) + 6; d.rectangle([gx - rr, cy - rr, gx + rr, cy + rr], fill=(255, 255, 230, al))
        img.alpha_composite(L)
    once('whoosh_8bit', 0.0, tt); once('coin_8bit', 0.6, tt); once('poof', T_IN, tt)
    for (ts, d, a, b) in swaps: once('swish', ts, tt)
    once('chime', T_Q, tt)
    items = []
    if tt < T_SHUF - 0.3:
        items.append((W / 2, HB + 26, 'Remember the gummy', 48, (255, 255, 255), 7, 255))
    if tt >= T_Q:
        for k, x in enumerate(XS):
            items.append((x + 12, GY + 30, 'ABC'[k], 72, (255, 255, 255), 8, 255))
    text_layer(img, items)
    if tt >= T_Q:   # band becomes the question, hard pop
        sc = 1 + 0.08 * max(0, 1 - (tt - T_Q) / 0.2)
        if sc > 1.001:
            Hs = HOOKQ.resize((int(W * sc), int(H * sc)), Image.NEAREST); ox_, oy_ = int((Hs.width - W) / 2), int(262 * (sc - 1))
            img.alpha_composite(Hs.crop((ox_, oy_, ox_ + W, oy_ + H)))
        else: img.alpha_composite(HOOKQ)
    else: img.alpha_composite(HOOK)
    out.write(img)
    if STILL: img.convert('RGB').save(f'still_{f}.png')
out.close()
if not STILL: json.dump({'events': ev}, open('v14_events.json', 'w')); print('done', round(DUR, 2), len(ev))
