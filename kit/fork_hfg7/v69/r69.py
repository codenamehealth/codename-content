import sys, os; os.chdir(os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, '../../fork1')
from common import *
sys.path.insert(0, '../../pixellab/safezone'); from hook import hook_layer, hook_fade
B7 = '../../fork_b7/'
HOOK, HB = hook_fade(['FIND 3', 'DIFFERENCES'], accent=0)   # hfg7: soft fade
HOOK_END, _ = hook_fade(["TIME'S UP!", 'HOW MANY?'], accent=0)   # hfg7: end question replaces the hook (no end card)
HB = HB  # 504
import numpy as np, colorsys
PW, PH = 1080, 530   # hfg7: full-width panels (was 750x430 framed); same 1:1 temple scale, all sprites keep their size
DX, DY = 165, 100     # content offset vs the old 750x430 window (same composition, more temple around it)
GX0, GY0 = 585 - DX, 495 - DY   # gif crop origin of the comparable window
SUN = bg_frames('sun_hd.gif', (1920, 1080), step=2)

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
TBASE = 40 + 88 * 3 + DY   # stand feet y in the panel
def unlit(im):
    a = np.array(im).astype(int); r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = (a[..., 3] > 0) & (r > 170) & (r >= g) & (g > b + 20); a[m, 3] = 0
    return Image.fromarray(a.astype(np.uint8))
TOR_OFF = unlit(TOR[0])
CY = idle('cyrus', 3)
G = {k: gummy(k, 2) for k in GUMK}
def panel(t, alt, ext_top=0, ext_bot=0):
    """hfg7: full-width window; ext_top/ext_bot extend the same temple above/below the comparable window (full bleed)"""
    src = SUN[int(t * 6) % len(SUN)]; y0g = GY0 - ext_top; y1g = GY0 + PH + ext_bot
    p = Image.new('RGBA', (PW, PH + ext_top + ext_bot))
    p.alpha_composite(src.crop((GX0, max(0, y0g), GX0 + PW, min(src.height, y1g))), (0, max(0, -y0g)))
    if y1g > src.height:   # below the gif: the floor continues (mirrored rows), darkening into the caption area
        need = y1g - src.height; m = src.crop((GX0, src.height - need, GX0 + PW, src.height)).transpose(Image.FLIP_TOP_BOTTOM)
        p.alpha_composite(m, (0, p.height - need))
        g = Image.new('L', (1, need)); [g.putpixel((0, k), int(150 * k / need)) for k in range(need)]
        sh = Image.new('RGBA', (PW, need), (20, 10, 4, 255)); sh.putalpha(g.resize((PW, need))); p.alpha_composite(sh, (0, p.height - need))
    q = Image.new('RGBA', (PW, PH)); OX, OY = DX, DY   # content layer in window coordinates (old layout + offset)
    # banners (on their wall rods)
    q.alpha_composite(BAN2 if alt else BAN, (24 + OX, OY)); q.alpha_composite(BAN, (750 - 24 - BAN.width + OX, OY))
    # torches flanking the stairs (on their stands)
    tf = TOR[int(t * 10) % len(TOR)]
    layer(q, lambda d: [d.ellipse([cx - 52, TBASE - 4, cx + 52, TBASE + 14], fill=(40, 20, 0, 90)) for cx in (215 + OX, 750 - 215 + OX)])
    q.alpha_composite(tf, (215 + OX - tf.width // 2, 40 + OY)); q.alpha_composite(TOR_OFF if alt else tf, (750 - 215 + OX - tf.width // 2, 40 + OY))
    p.alpha_composite(q, (0, ext_top)); return panel_rest(p, q, t, alt, ext_top)
def panel_rest(p, q, t, alt, ext_top):
    OX = DX
    # altar with four gummies
    q = Image.new('RGBA', (PW, PH))
    ax, ay = 375 + OX - ALT.width // 2, PH - ALT.height - 16
    layer(q, lambda d: d.ellipse([ax - 20, ay + ALT.height - 30, ax + ALT.width + 20, ay + ALT.height + 16], fill=(0, 0, 0, 80)))
    q.alpha_composite(ALT, (ax, ay))
    kinds = ['acv', 'cre' if alt else 'mush', 'mel', 'cre']   # GOLD FIX: 4th altar gummy gold -> creatine (same in both panels)
    for i, k in enumerate(kinds):
        g = G[k]; gx = ax + 34 + i * (ALT.width - 68) / 3; q.alpha_composite(g, (int(gx - g.width / 2), int(ay + 12 - g.height + 8)))
    cf = CY[int(t * 8) % len(CY)]; q.alpha_composite(cf, (ax - cf.width + 30, PH - 16 - 78 * 3))
    # shared sparkles
    rr = random.Random(int(t * 4))
    L = Image.new('RGBA', q.size); d = ImageDraw.Draw(L)
    for _ in range(10):
        x, y = rr.uniform(0, 750) + OX, rr.uniform(0, 430 * 0.7) + DY; d.rectangle([x, y, x + 5, y + 5], fill=(255, 250, 200, 180))
    q.alpha_composite(L)
    p.alpha_composite(q, (0, ext_top))
    return p
def frame(img, x0, y0):
    layer(img, lambda d: (d.rounded_rectangle([x0 - 14, y0 - 14, x0 + PW + 14, y0 + PH + 14], 18, outline=(255, 214, 60, 255), width=10),
                          d.rounded_rectangle([x0 - 4, y0 - 4, x0 + PW + 4, y0 + PH + 4], 10, outline=(120, 70, 20, 255), width=4)))
    d = ImageDraw.Draw(img)
    for (cx, cy) in ((x0 - 8, y0 - 8), (x0 + PW + 8, y0 - 8), (x0 - 8, y0 + PH + 8), (x0 + PW + 8, y0 + PH + 8)):
        for k in range(8):
            a = k * math.pi / 4; d.line([cx, cy, cx + 22 * math.cos(a), cy + 22 * math.sin(a)], fill=(255, 214, 60), width=6)
        d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 190, 40), outline=(140, 80, 20), width=4)
# BGF = bg_frames('sun_hd.gif', (3413, 1920), step=4, bright=0.35, blur=6)
# BGF = [b.crop((1166, 0, 1166 + W, H)) for b in BGF]
T_TIMER1, T_HOLD, DUR = 8.0, 1.4, 9.6   # recut: no countdown; timer live from frame 0 (~8s), TIME'S UP held 1.4s, last 0.2s = opening state (loop)
w = Writer('v69_noaudio.mp4'); events = [(0.0, 'go_8bit')]
X0 = 0; Y1 = 395; SEAMH = 20; Y2 = Y1 + PH + SEAMH   # hfg7: panels edge to edge, 20px seam carries the timer
PCX = X0 + PW // 2
PY = Y2 + PH
print('HB', HB, 'Y1', Y1, 'Y2', Y2, 'bottom', Y2 + PH, 'plate', PY)
FT = F(84)
def timer(img, t):
    u2 = t / T_TIMER1; left = T_TIMER1 - t
    col = (90, 220, 120) if left > 5 else (255, 200, 60) if left > 3 else (240, 70, 70)
    flash = left <= 3 and int(left * 6) % 2 == 0
    d = ImageDraw.Draw(img); sy = Y1 + PH + SEAMH // 2   # hfg7: horizontal bar on the seam (was a vertical bar beside boxed panels)
    bx0, bx1 = 80, 900
    d.rounded_rectangle([bx0, sy - 15, bx1, sy + 15], 12, fill=(30, 20, 10), outline=(255, 255, 255) if flash else (255, 214, 60), width=4)
    ww = int((bx1 - bx0 - 12) * (1 - u2))
    if ww > 4: d.rounded_rectangle([bx0 + 6, sy - 9, bx0 + 6 + ww, sy + 9], 8, fill=(255, 255, 255) if flash else col)
    secs = int(math.ceil(left - 1e-6)); ph = left - (secs - 1)   # 1 -> 0 within each second
    pulse = 1 + 0.35 * max(0, (ph - 0.75) / 0.25); sz = int(80 * pulse)
    text_layer(img, [(962, sy - sz / 2, str(secs), sz, (255, 255, 255) if left > 3 else (255, 90, 90), 9, 255)])
for f in range(int(round(DUR * FPS))):
    t = f / FPS; tt = t if t < DUR - 0.2 else 0.0      # last 0.2s cuts back to the opening state
    img = Image.new('RGBA', (W, H), (12, 8, 4, 255))
    img.alpha_composite(panel(tt, False, ext_top=Y1), (X0, 0)); img.alpha_composite(panel(tt, True, ext_bot=H - Y2 - PH), (X0, Y2))
    layer(img, lambda dd: dd.rectangle([0, Y1 + PH, W, Y2 - 1], fill=(30, 18, 8, 255)))   # seam
    # hfg7: frames, blurred backdrop and the COMMENT HOW MANY plate cut
    if tt < T_TIMER1:
        timer(img, tt)
        if t < DUR - 0.2:
            for k in (3, 2, 1):
                if abs((T_TIMER1 - t) - k) < 0.5 / FPS: events.append((round(t, 3), 'tick_8bit'))
    else:
        u = t - T_TIMER1
        pass   # hfg7: TIME'S UP! / HOW MANY? replace the hook text (HOOK_END); end card + COMMENT 0, 1, 2 OR 3 cut
        if u < 0.5 / FPS: events.append((round(t, 3), 'buzz_8bit'))
    img.alpha_composite(HOOK_END if T_TIMER1 <= tt else HOOK)
    w.write(img)
    if f in (0, 90, 200, 260, 287): img.convert('RGB').save(f'k69_{f}.png')
w.close(); json.dump({'events': events}, open('v69_ev.json', 'w')); print(len(events), events)
