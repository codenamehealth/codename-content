import sys
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP_ + 'fork1')
from common import *
sys.path.insert(0, SP_ + 'pixellab/safezone'); from hook import hook_fade, hook_band
# Oct 29 hookfade pass: boxed band, COMMENT WHERE HE IS, 'FIND HIM' + arrow on the card and 'DID YOU FIND HIM?' cut
HSTYLE = os.environ.get('HSTYLE', 'fade')
HOOK, HB = (hook_fade if HSTYLE == 'fade' else hook_band)(['ONLY 1% CAN FIND', 'THIS HOLLOW'], accent=1, size=64)
os.chdir(SP_ + 'fork3')   # crowd assets (hollow_eat) live there; outputs go to fork_rc4/v25
OUTD = SP_ + 'fork_n3/v25/'
PREVIEW = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else None
PUNCH = 0.45; TIMER = 14.0; ENDH = 1.4          # review: 37s search -> 14s; punch-in on the target card first
T_UP = PUNCH + TIMER; DUR = T_UP + ENDH; NF = int(round(DUR * FPS))
rnd = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 3)
K = 2
NAMES = ['joy', 'cyrus', 'cleo', 'ray', 'hollow']
IDL = {g: idle(g, K) for g in NAMES}
CHEER = {g: seq(PL + f'maze/anim/{g}_panic', K, 1, 9) for g in NAMES}
EAT = seq('hollow_eat', K, 0, 13)
# Oct 29 review (#25): the red gummy that marks the target was ~12px on screen. Enlarge it 2x (integer, native pixels doubled)
# on the target frames and the card, from the sprite's own gummy (hollow_eat/02 rows 40-45), with the sprite's own dark rim;
# no glow, no pulse. Decoy frames (05/06/08) have no red, so the target is still the only gummy holder.
from PIL import ImageFilter as _IF
_g2 = Image.open('hollow_eat/02.png').convert('RGBA').crop((43, 39, 52, 46))
_gm = _g2.getchannel('A').point(lambda v: 0)
for _y in range(_g2.height):
    for _x in range(_g2.width):
        if _g2.getpixel((_x, _y))[0] > 200: _gm.putpixel((_x, _y), 255)
_g2.putalpha(_gm); _G = _g2.resize((_g2.width * 2, _g2.height * 2), Image.NEAREST)
_rim = _G.getchannel('A').filter(_IF.MaxFilter(3)); _R = Image.new('RGBA', _G.size, (6, 6, 8, 255)); _R.putalpha(_rim)
def big_gummy(i):
    im = Image.open('hollow_eat/%02d.png' % i).convert('RGBA')
    pts = [(x, y) for y in range(im.height) for x in range(im.width) if (lambda q: q[3] > 0 and q[0] > 150 and q[1] < 110 and q[2] < 120)(im.getpixel((x, y)))]
    cx = (min(p[0] for p in pts) + max(p[0] for p in pts) + 1) / 2; cy = (min(p[1] for p in pts) + max(p[1] for p in pts) + 1) / 2
    o = (int(round(cx - _G.width / 2)), int(round(cy - _G.height / 2)))
    im.alpha_composite(_R, o); im.alpha_composite(_G, o); return im
BIGG = {i: big_gummy(i) for i in (2, 3, 4)}
for _i in (2, 3, 4): EAT[_i] = up(BIGG[_i], K)
TGT = [EAT[2], EAT[3], EAT[4], EAT[3]]           # holding the red gummy
HEAT = [EAT[5], EAT[6], EAT[5], EAT[8]]          # decoys: hands at mouth, no gummy visible
FOOT = 78 * K
# background: Liza's castle (vit_hd) scaled to full height
BG = bg_frames('vit_hd.gif', (3413, 1920), step=2)
BG = [b.crop((1415, 0, 1415 + W, H)) for b in BG]
# crowd layout
sprites = []
rows = list(range(700, 2060, 44))
TR = 18; TX = 772
for ri, y in enumerate(rows):
    off = (ri % 2) * 32
    for x in range(-40 + off, 1130, 64):
        x2 = x + rnd.randint(-10, 10); y2 = y + rnd.randint(-6, 6)
        if ri == TR and abs(x2 - TX) < 50: continue
        if ri == TR + 1 and abs(x2 - TX) < 44: continue
        if ri == TR + 2 and abs(x2 - TX) < 20: continue
        g = rnd.choices(NAMES, weights=[1, 1, 1, 1, 1.3])[0]
        r = rnd.random()
        if g == 'hollow' and r < 0.25: kind = 'heat'
        elif r < 0.62: kind = 'idle'
        else: kind = 'cheer'
        sprites.append(dict(g=g, x=x2, y=y2, kind=kind, ph=rnd.randint(0, 7), flip=rnd.random() < 0.5, ri=ri))
def _safe(s):
    cx, ft = s['x'], s['y']
    if ft > 1540 or cx < 92 or cx > 1003: return False
    return not (ft > 1180 and cx > 862)
# Oct 29 (Bennett #25): the crowd fills the whole frame, safe-zone margins included (no cut-out corner, no
# black box showing through); only the target Hollow has to sit inside the safe zone.
# Oct 29 review: keep the target's head, eyes, hands and gummy unobstructed: the few crowd sprites that used to be drawn in
# front of his upper body (same row within 60px, next row within 70px) are drawn BEHIND him instead (no hole in the crowd,
# which would give him away); decided after generation so the crowd layout itself is unchanged
for s in sprites:
    if (s['ri'] == TR and abs(s['x'] - TX) < 60) or (s['ri'] == TR + 1 and abs(s['x'] - TX) < 70): s['z'] = rows[TR] + 7 - 1
TGT_S = dict(g='hollow', x=TX, y=rows[TR] + 7, kind='target', ph=0, flip=False); assert _safe(TGT_S)
sprites.append(TGT_S)
sprites.sort(key=lambda s: s.get('z', s['y']))
def spr(s, k):
    if s['kind'] == 'target': fr = TGT[(k // 2) % 4]
    elif s['kind'] == 'heat': fr = HEAT[(k // 2 + s['ph']) % 4]
    elif s['kind'] == 'idle': L = IDL[s['g']]; fr = L[(k + s['ph']) % len(L)]
    else: L = CHEER[s['g']]; fr = L[(k + s['ph']) % len(L)]
    return fr.transpose(Image.FLIP_LEFT_RIGHT) if s['flip'] and s['kind'] != 'target' else fr
NC = 24
CROWD = []
for k in range(NC):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for s in sprites:
        f = spr(s, k); L.alpha_composite(f, (int(s['x'] - f.width / 2), int(s['y'] - FOOT)))
    CROWD.append(L)
# soft shadow band where the crowd meets the castle
SH = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(SH)
for y in range(560, 760): sd.line([(0, y), (W, y)], fill=(20, 14, 10, int(120 * (y - 560) / 200)))
# header card (pre-rendered once, scaled for the punch-in)
CARD_IMG = up(crop(BIGG[3]), 3)
CX0, CX1 = 430, 650
def card(t):
    RY = HB + 12; C = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(C)
    d.rounded_rectangle([CX0, RY, CX1, RY + 214], 22, fill=(250, 246, 236, 240), outline=(40, 30, 50, 255), width=6)
    bob = int(4 * math.sin(t * 3))
    C.alpha_composite(CARD_IMG, (540 - CARD_IMG.width // 2, RY + 107 - CARD_IMG.height // 2 + bob))
    return C
w = None if PREVIEW else Writer(OUTD + 'v25_noaudio.mp4'); ev = []
for f in ([int(round(x * FPS)) for x in PREVIEW] if PREVIEW else range(NF)):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy(); img.alpha_composite(SH)
    img.alpha_composite(CROWD[int(t * 8) % NC])
    RY = HB + 12
    rem = max(0.0, TIMER - max(0.0, t - PUNCH)); frac = rem / TIMER
    def bar(d):
        d.rounded_rectangle([90, RY + 226, 990, RY + 298], 16, fill=(20, 14, 30, 220))
        col = (110, 220, 90) if frac > 0.35 else ((250, 200, 60) if frac > 0.15 else (240, 80, 70))
        if frac > 0: d.rounded_rectangle([98, RY + 234, 98 + (884 - 120) * frac, RY + 290], 12, fill=col + (255,))
    layer(img, bar)
    C = card(t)
    if t < PUNCH:      # Oct 29 review: card starts in its final place (the pop-in used to cover the timer bar); the crowd dim still fades
        u = t / PUNCH; layer(img, lambda d: d.rectangle([0, RY + 306, W, H], fill=(10, 6, 18, int(110 * (1 - u)))))
    img.alpha_composite(C)
    if t < T_UP:
        if t >= PUNCH: text_layer(img, [(924, RY + 238, f'{int(math.ceil(rem))}', 48, (255, 255, 255), 7, 255)])
        if 0.5 < rem < 3.5 and abs(rem - round(rem)) < 0.5 / FPS: ev.append((round(t, 3), 'tick_8bit'))
    else:
        u = t - T_UP; sc = 1 + 0.3 * max(0, 1 - u / 0.12)
        text_layer(img, [(540, 980, "TIME'S UP!", int(84 * sc), (255, 214, 60), 10, 255)])
        if f == int(round(T_UP * FPS)): ev.append((round(t, 3), 'buzz_8bit'))
    img.alpha_composite(HOOK)
    if PREVIEW: img.convert('RGB').save(OUTD + f'p_{f:04d}.png')
    else: w.write(img)
if not PREVIEW:
    w.close(); json.dump({'events': [[0.0, 'whoosh_8bit']] + ev}, open(OUTD + 'v25_events.json', 'w'))
print('done', len(sprites), 'sprites', 'dur', DUR)
