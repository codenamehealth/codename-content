import sys, os; os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '../../fork1')
from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer
B7 = '../../fork_b7/'
HOOK, HB = hook_layer(['FIND 3', 'DIFFERENCES'], accent=0)
import numpy as np, colorsys
PW, PH = 750, 430   # panel window 1000x660 -> 750x430 (same 1:1 temple scale, cropped; all sprites keep their size)
SUN = bg_frames('sun_hd.gif', (1920, 1080), step=2)
SUN = [s.crop((585, 495, 585 + PW, 495 + PH)) for s in SUN]
ALT = up(crop(Image.open(B7 + 'altar/02.png').convert('RGBA')), 3)
BAN = up(crop(Image.open(B7 + 'banner/03.png').convert('RGBA')), 3)
def hue(im, shift):
    a = np.array(im).astype(float) / 255; out = a.copy()
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mask = (a[..., 3] > 0) & (r > g + 0.12) & (r > b + 0.2)
    for (y, x) in zip(*np.where(mask)):
        h, s, v = colorsys.rgb_to_hsv(r[y, x], g[y, x], b[y, x]); out[y, x, :3] = colorsys.hsv_to_rgb((h + shift) % 1, s, v)
    return Image.fromarray((out * 255).astype(np.uint8))
BAN2 = hue(BAN, 0.72)
from stand import stand_torch   # #69 note: torches were floating wall sconces; now standing torches on iron tripod stands on the floor
TOR = [up(stand_torch(Image.open(p)), 3) for p in sorted(glob.glob(PL + 'maze/torch_anim/*.png'))]
TBASE = 40 + 88 * 3   # stand feet y in the panel
def unlit(im):
    a = np.array(im).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (a[..., 3] > 0) & (r > 170) & (r >= g) & (g > b + 20); a[m, 3] = 0
    return Image.fromarray(a.astype(np.uint8))
TOR_OFF = unlit(TOR[0])
CY = idle('cyrus', 3)
G = {k: gummy(k, 2) for k in GUMK}
def panel(t, alt):
    p = SUN[int(t * 6) % len(SUN)].copy()
    # banners hanging from the top
    p.alpha_composite(BAN2 if alt else BAN, (24, 0)); p.alpha_composite(BAN, (PW - 24 - BAN.width, 0))
    # torches flanking the stairs
    tf = TOR[int(t * 10) % len(TOR)]
    layer(p, lambda d: [d.ellipse([cx - 52, TBASE - 4, cx + 52, TBASE + 14], fill=(40, 20, 0, 90)) for cx in (215, PW - 215)])
    p.alpha_composite(tf, (215 - tf.width // 2, 40)); p.alpha_composite(TOR_OFF if alt else tf, (PW - 215 - tf.width // 2, 40))
    # altar with four gummies
    ax, ay = PW // 2 - ALT.width // 2, PH - ALT.height - 16
    layer(p, lambda d: d.ellipse([ax - 20, ay + ALT.height - 30, ax + ALT.width + 20, ay + ALT.height + 16], fill=(0, 0, 0, 80)))
    p.alpha_composite(ALT, (ax, ay))
    kinds = ['acv', 'cre' if alt else 'mush', 'mel', 'cre']   # GOLD FIX: 4th altar gummy gold -> creatine (same in both panels)
    for i, k in enumerate(kinds):
        g = G[k]; gx = ax + 34 + i * (ALT.width - 68) / 3; p.alpha_composite(g, (int(gx - g.width / 2), int(ay + 12 - g.height + 8)))
    cf = CY[int(t * 8) % len(CY)]; p.alpha_composite(cf, (ax - cf.width + 30, PH - 16 - 78 * 3))
    # shared sparkles
    rr = random.Random(int(t * 4))
    L = Image.new('RGBA', p.size); d = ImageDraw.Draw(L)
    for _ in range(10):
        x, y = rr.uniform(0, PW), rr.uniform(0, PH * 0.7); d.rectangle([x, y, x + 5, y + 5], fill=(255, 250, 200, 180))
    p.alpha_composite(L)
    return p
def frame(img, x0, y0):
    layer(img, lambda d: (d.rounded_rectangle([x0 - 14, y0 - 14, x0 + PW + 14, y0 + PH + 14], 18, outline=(255, 214, 60, 255), width=10),
                          d.rounded_rectangle([x0 - 4, y0 - 4, x0 + PW + 4, y0 + PH + 4], 10, outline=(120, 70, 20, 255), width=4)))
    d = ImageDraw.Draw(img)
    for (cx, cy) in ((x0 - 8, y0 - 8), (x0 + PW + 8, y0 - 8), (x0 - 8, y0 + PH + 8), (x0 + PW + 8, y0 + PH + 8)):
        for k in range(8):
            a = k * math.pi / 4; d.line([cx, cy, cx + 22 * math.cos(a), cy + 22 * math.sin(a)], fill=(255, 214, 60), width=6)
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 190, 40), outline=(140, 80, 20), width=4)
BGF = bg_frames('sun_hd.gif', (3413, 1920), step=4, bright=0.35, blur=6)
BGF = [b.crop((1166, 0, 1166 + W, H)) for b in BGF]
T_CD, T_TIMER1, DUR = 2.4, 12.4, 15.0
w = Writer('v69_noaudio.mp4'); events = []
X0 = 100; Y1 = HB + 34; Y2 = Y1 + PH + 56
PCX = X0 + PW // 2
print('HB', HB, 'Y1', Y1, 'Y2', Y2, 'bottom', Y2 + PH)
for f in range(int(DUR * FPS)):
    t = f / FPS; img = BGF[int(t * 3) % len(BGF)].copy()
    img.alpha_composite(panel(t, False), (X0, Y1)); img.alpha_composite(panel(t, True), (X0, Y2))
    frame(img, X0, Y1); frame(img, X0, Y2)
    d = ImageDraw.Draw(img)
    if t < T_CD:
        img.alpha_composite(Image.new('RGBA', (W, H), (10, 6, 2, 150)))
        n = 3 - int(t / (T_CD / 3)); u = (t % (T_CD / 3)) / (T_CD / 3)
        text_layer(img, [(PCX, Y2 - 150 - 20 * (1 - u), str(n), int(200 * (1.3 - 0.3 * u)), (255, 214, 60), 12, 255)])
        if u < 1 / FPS * 1.5 / (T_CD / 3): events.append((round(t, 3), 'tick_8bit'))
    elif t < T_TIMER1:
        if t - T_CD < 1 / FPS: events.append((round(t, 3), 'go_8bit'))
        u2 = (t - T_CD) / (T_TIMER1 - T_CD); col = (90, 220, 120) if u2 < 0.6 else (255, 200, 60) if u2 < 0.85 else (240, 80, 80)
        d = ImageDraw.Draw(img)
        # vertical timer bar right of the top panel (upper band, clear of the buttons)
        d.rounded_rectangle([910, Y1, 950, Y1 + PH], 14, fill=(30, 20, 10), outline=(255, 214, 60), width=4)
        hh = int((PH - 12) * (1 - u2)); d.rounded_rectangle([916, Y1 + PH - 6 - hh, 944, Y1 + PH - 6], 10, fill=col)
        secs = int(math.ceil(T_TIMER1 - t)); ctext(d, 930, Y1 + PH + 16, f'{secs}', F(36), (255, 255, 255), 5)
        if secs <= 3 and abs((T_TIMER1 - t) - secs) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
    else:
        u = t - T_TIMER1
        layer(img, lambda dd: dd.rounded_rectangle([88, 820, 868, 1100], 26, fill=(20, 12, 4, 225), outline=(255, 214, 60, 255), width=6))
        text_layer(img, [(478, 855, "TIME'S UP!", int(70 * (1 + 0.2 * max(0, 1 - u / 0.2))), (255, 214, 60), 8, 255), (478, 960, 'How many did you find?', 32, (255, 255, 255), 5, 255), (478, 1025, 'Comment 0, 1, 2 or 3', 32, (255, 235, 200), 5, 255)])
        if u < 1 / FPS: events.append((round(t, 3), 'buzz_8bit'))
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (30, 210, 420): img.convert('RGB').save(f'k69_{f}.png')
w.close(); json.dump(events, open('v69_ev.json', 'w')); print(len(events))
