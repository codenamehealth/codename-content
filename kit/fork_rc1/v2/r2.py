import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1'); from hook2 import hook_layer2
HOOKB, HB = hook_layer2(['Screenshot', 'when it fits'], accent=0, sub='Comment your time')
print('hook bottom', HB)
import numpy as np
G = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a11/gen/'
K = 8
NAT = Image.open(A + 'jar_creatine.png').convert('RGBA').crop((130, 20, 410, 520)).resize((28, 50), Image.NEAREST)
POT = up(NAT, K)
PED = up(crop(Image.open(G + 'pedestal/00.png').convert('RGBA')), 8)
HOOK = up(crop(Image.open(G + 'hook/03.png').convert('RGBA')), 4)
PIV = (540, 690)                    # pulley
PED_TOP = 1280                      # top surface of pedestal (raised 190px: landing spot out of the bottom 420px)
TX, TY = 540, PED_TOP - POT.height // 2 + 6   # target centre of potion
DUR = 10.1; NF = int(round(DUR * FPS)); T_FZ = 8.8
TAU = 2 * math.pi / DUR            # every frequency is a whole number of cycles per DUR -> last frame flows into frame 0
def motion(p, t):
    x = p['ax'] * math.sin(p['wx'] * t + p['px']) + p['bx'] * math.sin(p['wx2'] * t + p['px2'])
    y = p['ay'] * math.sin(p['wy'] * t + p['py'])
    a = p['aa'] * math.sin(p['wa'] * t + p['pa'])
    return x, y, a
def search(seed, F0):
    rnd = random.Random(seed); t0 = F0 / FPS; best = None
    for _ in range(int(os.environ.get('NT', '4000'))):
        p = dict(ax=rnd.uniform(180, 205), wx=TAU * rnd.choice([4, 5]), px=rnd.uniform(0, 6.3), bx=rnd.uniform(30, 42), wx2=TAU * rnd.choice([7, 8, 9]), px2=rnd.uniform(0, 6.3),
                 ay=rnd.uniform(45, 68), wy=TAU * rnd.choice([3, 4]), py=rnd.uniform(0, 6.3), aa=rnd.uniform(18, 32), wa=TAU * rnd.choice([3, 4, 5]), pa=rnd.uniform(0, 6.3))
        # fit frame = the bottom of the vertical bob while the swing passes centre at full speed
        sg = rnd.choice([0, math.pi]); p['px'] = sg - p['wx'] * t0; p['px2'] = sg - p['wx2'] * t0; p['py'] = math.pi / 2 - p['wy'] * t0
        x0, y0, a0 = motion(p, t0)
        p['ox'], p['oy'], p['oa'] = -x0, -y0, -a0
        ok = True; worst = 1e9
        for f in range(NF):
            if f == F0: continue
            x, y, a = motion(p, f / FPS); x += p['ox']; y += p['oy']; a += p['oa']
            e = max(abs(x), abs(y), abs(a) * 9)
            worst = min(worst, e)
        # keep potion well inside the screen
        xs = [motion(p, f / FPS)[0] + p['ox'] for f in range(0, NF, 3)]; ys = [motion(p, f / FPS)[1] + p['oy'] for f in range(0, NF, 3)]
        if max(map(abs, xs)) > 240 or max(ys) > 20 or min(ys) < -140: continue
        nb = []
        for df in (-2, -1, 1, 2):
            x, y, a = motion(p, (F0 + df) / FPS); nb.append(math.hypot(x + p['ox'], y + p['oy']))
        if min(nb) < 26: continue
        if best is None or worst > best[0]: best = (worst, p)
    return best
F0 = 196   # 6.53s
if len(sys.argv) > 1 and sys.argv[1] == 'search':
    for s in range(int(sys.argv[2]), int(sys.argv[3])):
        b = search(s, F0); print('RES', s, b and round(b[0], 1), flush=True)
    sys.exit()
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
best = search(SEED, F0); P = best[1]; print('min miss', round(best[0], 1))
def state(t):
    x, y, a = motion(P, t); return TX + x + P['ox'], TY + y + P['oy'], a + P['oa']
# outline from the unrotated potion mask
m = np.array(POT.getchannel('A')) > 0
edge = m & ~(np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1))
ys_, xs_ = np.nonzero(edge)
OUT = Image.new('RGBA', POT.size, (0, 0, 0, 0)); op = OUT.load()
for y, x in zip(ys_, xs_):
    if ((x // 8) + (y // 8)) % 2 == 0: op[x, y] = (255, 255, 255, 255)
OUT = OUT.filter(ImageFilter.MaxFilter(5))
GLOW = OUT.filter(ImageFilter.GaussianBlur(6))
GHOST = Image.new('RGBA', POT.size, (235, 245, 255, 0)); GHOST.putalpha(POT.getchannel('A').point(lambda v: 95 if v else 0))   # faint ghost of the bottle = the target
BG = bg_frames('vit_hd.gif', (1080, 1920), box=(960 - 304, 0, 960 + 304, 1080), step=2, bright=0.72)
CLEO = idle('cleo', 6)   # 6x (~384px): Cleo was too small at 4x
GUMC = gummy('cre', 3)
def frame_at(f):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    # pedestal + outline
    img.alpha_composite(PED, (TX - PED.width // 2, PED_TOP - 50))
    img.alpha_composite(GHOST, (TX - POT.width // 2, TY - POT.height // 2))
    gl = GLOW.copy(); gl.putalpha(gl.getchannel('A').point(lambda v: int(v * (0.6 + 0.3 * math.sin(t * 5)))))
    img.alpha_composite(gl, (TX - POT.width // 2, TY - POT.height // 2)); img.alpha_composite(OUT, (TX - POT.width // 2, TY - POT.height // 2))
    # Cleo watching
    fr = CLEO[int(t * 6) % len(CLEO)]; img.alpha_composite(fr, (70 - 19 * 6, 1496 - 78 * 6))
    for k, (gx0, gy0) in enumerate([(110, 760), (880, 720), (900, 980)]):
        img.alpha_composite(GUMC, (int(gx0 + 14 * math.sin(t * 1.3 + k)), int(gy0 + 16 * math.sin(t * 2 + k * 1.7))))
    # beam + pulley
    def beam(d):
        d.rectangle([0, 620, W, 662], fill=(92, 62, 36, 255)); d.rectangle([0, 620, W, 628], fill=(140, 98, 58, 255)); d.rectangle([0, 656, W, 662], fill=(52, 34, 20, 255))
        for x in range(30, W, 120): d.rectangle([x, 632, x + 10, 642], fill=(60, 60, 70, 255))
        d.ellipse([PIV[0] - 34, PIV[1] - 46, PIV[0] + 34, PIV[1] + 22], fill=(70, 72, 84, 255), outline=(30, 30, 40, 255), width=5)
        d.ellipse([PIV[0] - 10, PIV[1] - 22, PIV[0] + 10, PIV[1] - 2], fill=(200, 190, 150, 255))
    layer(img, beam)
    x, y, a = state(t)
    # chain from pulley to hook top
    # hook follows the rotated bottle neck so the bottle visibly hangs from it (was fixed above the unrotated centre)
    ra = math.radians(a); hx, hy = x - (POT.height / 2) * math.sin(ra), y - (POT.height / 2) * math.cos(ra) - 40
    def chain(d):
        n = int(math.hypot(hx - PIV[0], hy - PIV[1]) / 22)
        for i in range(n):
            u = i / max(1, n); cx, cy = PIV[0] + (hx - PIV[0]) * u, PIV[1] + (hy - PIV[1]) * u
            if i % 2: d.ellipse([cx - 7, cy - 12, cx + 7, cy + 12], outline=(150, 150, 165, 255), width=4)
            else: d.ellipse([cx - 4, cy - 12, cx + 4, cy + 12], outline=(110, 110, 125, 255), width=4)
    layer(img, chain)
    img.alpha_composite(HOOK, (int(hx - HOOK.width / 2), int(hy - 10)))
    # rotate the already-upscaled sprite (was: rotate the 28x50 native sprite, then upscale -> dropped/doubled pixels = glitchy)
    pr = POT.rotate(a, resample=Image.NEAREST, expand=True) if abs(a) > 0.05 else POT
    img.alpha_composite(pr, (int(round(x - pr.width / 2)), int(round(y - pr.height / 2))))
    # stopwatch
    # big stopwatch on the beam (76px digits, ~2x)
    tt = min(t, T_FZ); fz = t >= T_FZ
    def sw(d): d.rounded_rectangle([592, 590, 1020, 714], 18, fill=(14, 10, 24, 235), outline=(255, 214, 60, 255) if fz else (110, 170, 255, 255), width=6)
    layer(img, sw)
    text_layer(img, [(806, 614, f'{tt:05.2f}', 76, (255, 214, 60) if fz else (255, 255, 255), 8, 255)])
    if fz:
        u = t - T_FZ; sc = 1.0 + 0.15 * max(0, 1 - u / 0.12)      # hard pop
        cw, ch = 900, 250
        card = Image.new('RGBA', (cw, ch), (0, 0, 0, 0)); cd = ImageDraw.Draw(card)
        cd.rounded_rectangle([0, 0, cw - 1, ch - 1], 24, fill=(14, 10, 24, 240), outline=(255, 214, 60, 255), width=8)
        for txt, sz, yy, col in (('DID YOU', 72, 34, (255, 255, 255)), ('GET IT?', 72, 140, (255, 214, 60))):
            ff = F(sz); tw = cd.textlength(txt, font=ff); cd.text(((cw - tw) / 2, yy), txt, font=ff, fill=col, stroke_width=8, stroke_fill=(10, 6, 18))
        if sc > 1.01: card = card.resize((int(cw * sc), int(ch * sc)), Image.NEAREST)
        img.alpha_composite(card, (int(547 - card.width / 2), int(860 - card.height / 2)))
    img.alpha_composite(HOOKB)
    return img
if __name__ == '__main__':
    if len(sys.argv) > 2 and sys.argv[2] == 'still':
        for f in (0, 60, F0 - 1, F0, F0 + 1, 280, NF - 1): frame_at(f).convert('RGB').save(f'h_still_{f}.png')
        sys.exit()
    wr = Writer('v2_noaudio.mp4')
    for f in range(NF): wr.write(frame_at(f))
    wr.close()
    ev = [(0.2, 'chime')] + [(k * 0.9 + 0.5, 'whoosh_8bit') for k in range(10)] + [(T_FZ, 'ding_8bit')]
    json.dump({'events': ev}, open('ev.json', 'w')); print('done')
