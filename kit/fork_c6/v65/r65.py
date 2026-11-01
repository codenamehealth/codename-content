import sys, os; os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '../../fork1')
from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
B7 = '../../fork_b7/'
HOOK, HB = hook_layer(['HOW MANY GUMMIES', 'ARE IN THE JAR?'], accent=1)
HOOK2, HB2 = hook_layer(['COMMENT', 'YOUR GUESS'], accent=1)
import numpy as np, pymunk
random.seed(65)
BG0 = Image.open(SP + 'fork3/tavern3/00.png').convert('RGBA').crop((0, 0, 360, 494)).resize((1140, 1564), Image.NEAREST).crop((30, 0, 1110, 1564))
BG = Image.new('RGBA', (W, H), (40, 22, 14, 255)); BG.alpha_composite(ImageEnhance.Brightness(BG0).enhance(0.9), (0, 0))
# pixel wooden shop counter (drawn at 1/3 res then scaled). #65 note: shorter face (156px) so the Hollow can stand
# on the shop floor IN FRONT of it (customer side) with his feet inside the safe zone
cr = random.Random(3); CT = Image.new('RGBA', (360, 52), (0, 0, 0, 0)); cd = ImageDraw.Draw(CT)
cd.rectangle([0, 0, 359, 9], fill=(150, 92, 52, 255)); cd.rectangle([0, 0, 359, 1], fill=(214, 150, 92, 255)); cd.rectangle([0, 9, 359, 11], fill=(70, 38, 22, 255))
for x0 in range(0, 360, 30):
    c = cr.choice([(122, 70, 40), (112, 64, 36), (132, 78, 44)])
    cd.rectangle([x0, 12, x0 + 29, 51], fill=c + (255,)); cd.line([x0, 12, x0, 51], fill=(64, 34, 20, 255))
    for _ in range(2):
        yy = cr.randint(16, 46); cd.line([x0 + 3, yy, x0 + cr.randint(8, 26), yy], fill=(c[0] - 14, c[1] - 10, c[2] - 6, 255))
for x0 in range(15, 345, 66):
    cd.rectangle([x0, 20, x0 + 50, 44], outline=(84, 46, 26, 255)); cd.rectangle([x0 + 1, 21, x0 + 49, 21], fill=(160, 102, 60, 255))
    cd.rectangle([x0 + 22, 30, x0 + 28, 34], fill=(212, 170, 70, 255))
cd.rectangle([0, 12, 359, 14], fill=(212, 170, 70, 255)); cd.rectangle([0, 48, 359, 51], fill=(58, 30, 18, 255))
CT = up(CT, 3); CTY = 1330   # counter top; counter face y1330-1486, shop floor below
# shop floor in front of the counter (planks, 1/3 res)
FL = Image.new('RGBA', (360, 146), (0, 0, 0, 0)); fd = ImageDraw.Draw(FL); fr_ = random.Random(5)
for yy in range(0, 146, 9):
    off = fr_.randint(0, 40)
    for x0 in range(-off, 360, 48):
        c = fr_.choice([(118, 72, 42), (108, 64, 38), (126, 80, 46)])
        fd.rectangle([x0, yy, x0 + 47, yy + 8], fill=c + (255,)); fd.line([x0, yy, x0, yy + 8], fill=(66, 38, 22, 255))
    fd.line([0, yy + 8, 359, yy + 8], fill=(72, 42, 24, 255))
FL = up(FL, 3); FLY = 1486
# jar: strip the cork, build back (tinted glass) and front (outline + highlights) layers
J = Image.open(B7 + 'jar/01.png').convert('RGBA'); a = np.array(J)
CORK_END = 57
cork = J.crop((0, 0, 128, CORK_END)); cork = crop(cork)
a[:CORK_END] = 0
K = 7
jar = Image.fromarray(a); jar = crop(jar); jbb = Image.fromarray(a).getbbox()
ja = np.array(jar).astype(np.int32)
lum = ja[..., :3].mean(-1)
front = ja.copy(); back = ja.copy()
glass = (ja[..., 3] > 0) & (lum > 150) & (lum < 236)
front[glass, 3] = 60
back[..., 3] = np.where(ja[..., 3] > 0, 70, 0)
JF = up(Image.fromarray(front.astype(np.uint8)), K); JB = up(Image.fromarray(back.astype(np.uint8)), K)
JX = 478 - JF.width // 2; JBOT = CTY + 18; JY = JBOT - JF.height
CORK = up(cork, 4)
# interior walls from the mask (per row inner edges)
m = ja[..., 3] > 0
rows = []
for y in range(jar.height):
    xs = np.where(m[y])[0]
    if len(xs): rows.append((y, xs.min(), xs.max()))
space = pymunk.Space(); space.gravity = (0, 2600)
sb = space.static_body
def seg(p, q):
    s = pymunk.Segment(sb, p, q, 6); s.friction = 0.8; s.elasticity = 0.1; space.add(s)
pts_l = [(JX + (x0 + 2) * K, JY + y * K) for (y, x0, x1) in rows[::3]]
pts_r = [(JX + (x1 - 1) * K, JY + y * K) for (y, x0, x1) in rows[::3]]
for i in range(len(pts_l) - 1): seg(pts_l[i], pts_l[i + 1]); seg(pts_r[i], pts_r[i + 1])
floor_y = JY + (rows[-1][0] - 3) * K
seg((pts_l[-1][0], floor_y), (pts_r[-1][0], floor_y))
GS = {k: gummy(k, 2) for k in ['mush', 'acv', 'mel', 'cre', 'gold']}
N = 73
kinds = (['mush'] * 19 + ['acv'] * 18 + ['mel'] * 18 + ['cre'] * 18)[:N]   # GOLD FIX: the 3 gold gummies are now product gummies (still 73)
random.shuffle(kinds)   # (shuffle had slipped into the comment in batch_v2: types poured in blocks)
T_POUR0, T_POUR1 = 0.25, 7.3   # pour starts right away (reel lesson: motion from frame 0)
spawn_t = sorted(random.uniform(T_POUR0, T_POUR1) for _ in range(N))
bodies = []
mouth_l, mouth_r = pts_l[0][0] + 40, pts_r[0][0] - 40
ROT = {}
def rot(k, ang):
    q = int(round(math.degrees(ang) / 15.0)) * 15 % 360
    key = (k, q)
    if key not in ROT: ROT[key] = GS[k].rotate(-q, resample=Image.NEAREST, expand=True)
    return ROT[key]
# guides
CY_IDLE = idle('cyrus', 4); HO_IDLE = idle('hollow', 4)
hollow_eat = seq(SP + 'fork3/hollow_eat', 3, 1)
F80 = F(64); HX, HFEET = 618, 1497
w = Writer('v65_noaudio.mp4'); events = []; DUR = 10.9; T_SWAP = 8.3; NF = int(DUR * FPS)
landed = set(); bob = {}
for f in range(NF):
    t = f / FPS
    while len(bodies) < N and spawn_t[len(bodies)] <= t:
        k = kinds[len(bodies)]; g = GS[k]; r = min(g.width, g.height) * 0.46
        b = pymunk.Body(1, pymunk.moment_for_circle(1, 0, r)); b.position = (random.uniform(mouth_l, mouth_r), JY - 260 - random.uniform(0, 80))
        b.velocity = (random.uniform(-60, 60), random.uniform(200, 400)); b.angular_velocity = random.uniform(-6, 6)
        s = pymunk.Circle(b, r); s.friction = 0.7; s.elasticity = 0.15; space.add(b, s); bodies.append((b, k))
    for _ in range(4): space.step(1 / FPS / 4)
    img = BG.copy()
    # spotlight on the jar
    cf = CY_IDLE[int(t * 8) % len(CY_IDLE)]; img.alpha_composite(cf, (-28, CTY - 78 * 4 + 90))
    img.alpha_composite(CT, (0, CTY)); img.alpha_composite(FL, (0, FLY))
    # the Hollow: customer side, standing on the shop floor in front of the counter (feet y1497)
    layer(img, lambda d: d.ellipse([HX + 116, HFEET - 12, HX + 264, HFEET + 10], fill=(0, 0, 0, 110)))
    hf = HO_IDLE[int(t * 8) % len(HO_IDLE)]; img.alpha_composite(hf, (HX, HFEET - 78 * 4))
    layer(img, lambda d: d.ellipse([JX - 20, JBOT - 22, JX + JF.width + 20, JBOT + 22], fill=(0, 0, 0, 90)))
    img.alpha_composite(JB, (JX, JY))
    for b, k in bodies:
        gi = rot(k, b.angle); x, y = b.position
        img.alpha_composite(gi, (int(x - gi.width / 2), int(y - gi.height / 2)))
        if id(b) not in landed and y > JY + 60 and abs(b.velocity.y) < 120:
            landed.add(id(b))
            if len(landed) % 3 == 1: events.append((round(t, 3), 'tick_8bit'))
    img.alpha_composite(JF, (JX, JY))
    # header
    if t >= T_SWAP:
        if not any(e[1] == 'ding_8bit' for e in events): events.append((round(t, 3), 'ding_8bit'))
    img.alpha_composite(HOOK if t < T_SWAP else HOOK2)
    w.write(img)
    if f % 45 == 0: img.convert('RGB').resize((270, 480)).save(f'p_{f:04d}.png')
w.close()
top = min(b.position.y for b, k in bodies)
print('count', len(bodies), 'top of pile', round(top), 'rim', JY, 'escaped', sum(1 for b, k in bodies if b.position.y > JBOT + 20 or b.position.x < JX or b.position.x > JX + JF.width))
json.dump(events, open('v65_ev.json', 'w')); print('JX', JX, 'JY', JY, 'JBOT', JBOT, 'HB', HB)
