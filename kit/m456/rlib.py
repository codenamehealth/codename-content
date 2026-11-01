# Render helpers shared by the m04-m06 recreations (built on fork1/common.py and the n03c look)
import sys, os, math, random
S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, S_ + 'fork1'); from common import *
sys.path.insert(0, S_ + 'pixellab/safezone'); from hook import hook_fade
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
COL = {'joy': (100, 200, 70), 'cleo': (70, 135, 255), 'cyrus': (255, 145, 30), 'ray': (180, 95, 235)}
STR_COL = (255, 92, 70)
FACE = {}
for g, fn in [('joy', 'idle_0.gif'), ('cyrus', 'idle_1.gif'), ('ray', 'idle_2.gif'), ('cleo', 'idle_3.gif')]:
    im = Image.open(A + fn); im.seek(0); im = im.convert('RGBA').resize((92, 92), Image.NEAREST)
    cx = 46 if g != 'cleo' else 47
    FACE[g] = im.crop((cx - 12, 15, cx + 12, 39))
ROSTER_FACE = {g: up(FACE[g], 3) for g in G}
def box_img(g, n, dark=0.0, x_mark=False):
    """face box n px: dark frame, guild-colour rim, Syeda face crop (nearest) filling the inside"""
    b = Image.new('RGBA', (n, n), (14, 10, 20, 255)); dd = ImageDraw.Draw(b)
    k = max(1, (n - 6) // 24); fc = up(FACE[g], k)
    if fc.width > n - 6: fc = fc.resize((n - 6, n - 6), Image.NEAREST)
    bg_ = Image.new('RGBA', fc.size, tuple(int(v * 0.55) for v in COL[g]) + (255,)); bg_.alpha_composite(fc)
    if fc.width < n - 6:                                  # scale the last bit with nearest so the face fills the box
        bg_ = bg_.resize((n - 6, n - 6), Image.NEAREST)
    b.alpha_composite(bg_, (3, 3))
    dd = ImageDraw.Draw(b); dd.rectangle([1, 1, n - 2, n - 2], outline=COL[g] + (255,), width=3)
    dd.rectangle([4, 4, 10, 6], fill=(255, 255, 255, 170))
    if dark > 0: b = Image.blend(b, Image.new('RGBA', b.size, (30, 16, 50, 255)), dark)
    if x_mark:
        b = Image.blend(b, Image.new('RGBA', b.size, (20, 14, 26, 255)), 0.35); dd = ImageDraw.Draw(b)
        dd.line([4, 4, n - 5, n - 5], fill=(235, 50, 60, 255), width=5); dd.line([4, n - 5, n - 5, 4], fill=(235, 50, 60, 255), width=5)
    return b
def stone_tile(tone, seed):
    rr = random.Random(seed); t_ = Image.new('RGBA', (32, 32), tone + (255,)); px = t_.load()
    gr = tuple(int(v * 0.86) for v in tone); hi = tuple(min(255, int(v * 1.05)) for v in tone)
    for i in range(32):
        px[i, 31] = gr + (255,); px[31, i] = gr + (255,); px[i, 0] = hi + (255,); px[0, i] = hi + (255,)
    for n in range(22):
        x, y = rr.randint(2, 29), rr.randint(2, 29); px[x, y] = (tuple(int(v * 0.93) for v in tone) if n % 2 else tuple(min(255, int(v * 1.04)) for v in tone)) + (255,)
    return t_
TONES = [(226, 199, 152), (216, 187, 141)]
def floor_layer(mask_fn, x0, y0, x1, y1, tile=32, tones=TONES):
    """warm sandstone floor drawn wherever mask_fn(x, y) (world px, tile centres sampled per 11px cell by the caller)"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    tiles = [stone_tile(tones[k % 2], k * 31 + 7) for k in range(6)]
    for ty in range(y0, y1, tile):
        for tx in range(x0, x1, tile):
            L.alpha_composite(tiles[((tx // tile) + (ty // tile)) % 2 + 2 * (((tx // tile) * 7 + (ty // tile) * 3) % 3 == 0)], (tx, ty))
    return L
def checker_bg(c1, c2, s=60, bright=1.0):
    im = Image.new('RGBA', (W, H), c1 + (255,)); d = ImageDraw.Draw(im)
    for y in range(0, H, s):
        for x in range(0, W, s):
            if (x // s + y // s) % 2: d.rectangle([x, y, x + s - 1, y + s - 1], fill=c2 + (255,))
    return im
def shadow_tex(w, h):
    NZ = Image.effect_noise((max(1, w // 4), max(1, h // 4)), 60).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6))
    a = np.array(NZ).astype(float) / 255.0; c = np.zeros((h, w, 4), np.uint8)
    c[..., 0] = (20 + 30 * a).astype(np.uint8); c[..., 1] = (9 + 12 * a).astype(np.uint8); c[..., 2] = (38 + 50 * a).astype(np.uint8); c[..., 3] = 250
    return Image.fromarray(c)
def roster(img, RY0, outs, t, win=None, win_t=None):
    """outs: {g: t_out or None}"""
    for i, g in enumerate(G):
        x0 = 30 + i * 257; x1 = x0 + 247
        out = outs.get(g) is not None and outs[g] <= t
        w_ = win is not None and win_t is not None and t >= win_t and g == win
        layer(img, lambda dd, x0=x0, x1=x1, w_=w_, g=g: dd.rounded_rectangle([x0, RY0, x1, RY0 + 90], 14, fill=(14, 10, 22, 230), outline=(255, 214, 60, 255) if w_ else COL[g] + (255,), width=6 if w_ else 4))
        fc = ROSTER_FACE[g]
        if out: fc = ImageEnhance.Brightness(ImageEnhance.Color(fc).enhance(0.15)).enhance(0.45)
        img.alpha_composite(fc, (x0 + 9, RY0 + 9))
        nm = NAME[g]; fs_ = 26 if len(nm) <= 5 else 18
        d_ = ImageDraw.Draw(img); d_.text((x0 + 88, RY0 + 24 + (26 - fs_) // 2), nm, font=F(fs_), fill=(120, 110, 130) if out else COL[g], stroke_width=4, stroke_fill=(10, 6, 16))
        if out:
            d_.line([x0 + 10, RY0 + 10, x0 + 80, RY0 + 80], fill=(230, 50, 60), width=7); d_.line([x0 + 10, RY0 + 80, x0 + 80, RY0 + 10], fill=(230, 50, 60), width=7)
            d_.text((x0 + 90, RY0 + 58), 'OUT', font=F(20), fill=(240, 70, 70), stroke_width=3, stroke_fill=(10, 6, 16))
def vic_frames(g, k):
    im = Image.open(A + VIC[g]); out = []
    for i in range(im.n_frames): im.seek(i); out.append(up(im.convert('RGBA').resize((92, 92), Image.NEAREST), k))
    return out
def sparkle(dd, x, y, s_, a_):
    col = (255, 236, 150, a_); dd.rectangle([x - s_, y - 1, x + s_, y + 1], fill=col); dd.rectangle([x - 1, y - s_, x + 1, y + s_], fill=col); dd.rectangle([x - 1, y - 1, x + 1, y + 1], fill=(255, 255, 255, a_))
GUMI = up(Image.open(PL + 'gummies/pick_cre.png').convert('RGBA'), 2)
def burst(img, x, y, u, col, seed, n=14, R=110):
    rr = random.Random(seed); pts = [(rr.uniform(0, 6.283), rr.uniform(0.6, 1.0)) for _ in range(n)]
    layer(img, lambda dd: [dd.rectangle([x + (30 + R * u * sp) * math.cos(a) - 6 + int(3 * u), y + (30 + R * u * sp) * math.sin(a) - 6 + int(3 * u),
                                         x + (30 + R * u * sp) * math.cos(a) + 6 - int(3 * u), y + (30 + R * u * sp) * math.sin(a) + 6 - int(3 * u)],
                                        fill=tuple(min(255, v + 40) for v in col) + (int(255 * (1 - u)),)) for a, sp in pts])
def stamp(img, text, col, u, en, yy):
    al = int(255 * max(0, min(1, en / 0.2))); fs_ = min(48, int(860 / max(1, len(text)))); sc = 1 + 0.15 * max(0, 1 - u / 0.12); fs2 = int(fs_ * sc)
    tw_ = len(text) * fs2
    layer(img, lambda dd: dd.rounded_rectangle([540 - tw_ / 2 - 22, yy - 18, 540 + tw_ / 2 + 22, yy + fs2 + 18], 16, fill=(14, 8, 22, int(225 * al / 255))))
    text_layer(img, [(540, yy, text, fs2, col, 8, al)])
# ---------------- v2 (reference-proportion boards): hook on the board's solid wall, roster at given spots, solid colour trails
from hook import FONT as HOOK_FONT
from PIL import ImageFont
def hook_wall(lines, cx, y, size, floor_mask, accent=1, color=(255, 214, 60), lh=1.3, fade_strength=170, band=False):
    """Hook text centred on cx at y, over the board's solid wall mass. A soft dark fade from the top sits behind it,
    masked off the open floor (dilated) so it never darkens play. Returns (layer, bottom_y)."""
    f = ImageFont.truetype(HOOK_FONT, size); L = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    bottom = int(y + (len(lines) - 1) * size * lh + size); fe = bottom + 70
    g = Image.new('L', (1, H), 0)
    for yy in range(H):
        if band: v = max(0.0, min(1.0, (yy - (y - 50)) / 40, ((bottom + 50) - yy) / 40))     # soft band just behind the lines
        else: v = max(0.0, min(1.0, (fe - yy) / max(1, fe - 200)))                       # soft fade from the top
        g.putpixel((0, yy), int(fade_strength * v))
    g = g.resize((W, H))
    fm = floor_mask.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(4))
    g = ImageChops.multiply(g, ImageChops.invert(fm))
    sh = Image.new('RGBA', (W, H), (8, 6, 16, 255)); sh.putalpha(g); L.alpha_composite(sh)
    d = ImageDraw.Draw(L)
    for i, l in enumerate(lines):
        w = d.textlength(l, font=f)
        d.text((cx - w / 2, y + i * size * lh), l, font=f, fill=color if i == accent else (255, 255, 255), stroke_width=6, stroke_fill=(12, 8, 20))
    return L, bottom
def roster_at(img, spots, outs, t, win=None, win_t=None, cw=247, ch=90, compact=False):
    """spots: {g: (x0, y0)} chip top-left corners. Same chip look as roster(); compact = face on top, name under it."""
    if compact:
        for g in G:
            x0, y0 = spots[g]; out = outs.get(g) is not None and outs[g] <= t
            w_ = win is not None and win_t is not None and t >= win_t and g == win
            layer(img, lambda dd, x0=x0, y0=y0, w_=w_, g=g: dd.rounded_rectangle([x0, y0, x0 + cw, y0 + ch], 14, fill=(14, 10, 22, 230), outline=(255, 214, 60, 255) if w_ else COL[g] + (255,), width=6 if w_ else 4))
            fc = ROSTER_FACE[g]
            if out: fc = ImageEnhance.Brightness(ImageEnhance.Color(fc).enhance(0.15)).enhance(0.45)
            fx, fy = x0 + (cw - fc.width) // 2, y0 + 8; img.alpha_composite(fc, (fx, fy))
            d_ = ImageDraw.Draw(img); nm = NAME[g]; fs_ = 14 if len(nm) > 5 else 18; tw = d_.textlength(nm, font=F(fs_))
            d_.text((x0 + (cw - tw) / 2, y0 + ch - 12 - fs_), nm, font=F(fs_), fill=(120, 110, 130) if out else COL[g], stroke_width=3, stroke_fill=(10, 6, 16))
            if out:
                d_.line([fx + 2, fy + 2, fx + 70, fy + 70], fill=(230, 50, 60), width=7); d_.line([fx + 2, fy + 70, fx + 70, fy + 2], fill=(230, 50, 60), width=7)
        return
    for g in G:
        x0, RY0 = spots[g]; x1 = x0 + cw
        out = outs.get(g) is not None and outs[g] <= t
        w_ = win is not None and win_t is not None and t >= win_t and g == win
        layer(img, lambda dd, x0=x0, x1=x1, RY0=RY0, w_=w_, g=g: dd.rounded_rectangle([x0, RY0, x1, RY0 + ch], 14, fill=(14, 10, 22, 230), outline=(255, 214, 60, 255) if w_ else COL[g] + (255,), width=6 if w_ else 4))
        fc = ROSTER_FACE[g]
        if out: fc = ImageEnhance.Brightness(ImageEnhance.Color(fc).enhance(0.15)).enhance(0.45)
        img.alpha_composite(fc, (x0 + 9, RY0 + (ch - fc.height) // 2))
        nm = NAME[g]; fs_ = 26 if len(nm) <= 5 else 18
        d_ = ImageDraw.Draw(img); d_.text((x0 + 88, RY0 + 24 + (26 - fs_) // 2), nm, font=F(fs_), fill=(120, 110, 130) if out else COL[g], stroke_width=4, stroke_fill=(10, 6, 16))
        if out:
            fy = RY0 + (ch - fc.height) // 2
            d_.line([x0 + 10, fy + 1, x0 + 80, fy + 71], fill=(230, 50, 60), width=7); d_.line([x0 + 10, fy + 71, x0 + 80, fy + 1], fill=(230, 50, 60), width=7)
            d_.text((x0 + 90, RY0 + 58), 'OUT', font=F(20), fill=(240, 70, 70), stroke_width=3, stroke_fill=(10, 6, 16))
def trails(img, FRS, f, G_, HS, live, n_box=2.0, spd=277.0, fps=30, alpha=0.75):
    """Short tapered trail behind each live box (~n_box box lengths), drawn as straight segments between the recorded
    positions, so every bounce shows as a hard corner (no smoothing). Width tapers from 0.8 box at the head to ~0 at the tail."""
    nfr = max(2, int(round(n_box * 2 * HS / spd * fps)))
    for g in G_:
        if not live(g): continue
        pts = []
        for q in range(nfr, -1, -1):
            i = f - q
            if i < 0 or i >= len(FRS): continue
            s0 = FRS[i][0][g]
            if s0[4] is not None or s0[5] is not None: pts = []; continue
            pts.append((q, s0[0], s0[1]))
        if len(pts) < 2: continue
        bx0 = int(min(p_[1] for p_ in pts) - HS - 2); by0 = int(min(p_[2] for p_ in pts) - HS - 2)
        bx1 = int(max(p_[1] for p_ in pts) + HS + 3); by1 = int(max(p_[2] for p_ in pts) + HS + 3)
        L = Image.new('RGBA', (bx1 - bx0, by1 - by0), (0, 0, 0, 0)); dd = ImageDraw.Draw(L)
        for k in range(len(pts) - 1):
            q, x, y = pts[k]; q2, x2, y2 = pts[k + 1]
            dx, dy = x2 - x, y2 - y; n = math.hypot(dx, dy)
            if n < 1e-6: continue
            nx, ny = -dy / n, dx / n
            w1 = HS * 0.8 * (1 - q / nfr); w2 = HS * 0.8 * (1 - q2 / nfr)
            dd.polygon([(x - bx0 + nx * w1, y - by0 + ny * w1), (x2 - bx0 + nx * w2, y2 - by0 + ny * w2),
                        (x2 - bx0 - nx * w2, y2 - by0 - ny * w2), (x - bx0 - nx * w1, y - by0 - ny * w1)], fill=COL[g] + (255,))
            if k > 0: dd.rectangle([x - bx0 - w1, y - by0 - w1, x - bx0 + w1, y - by0 + w1], fill=COL[g] + (255,))   # square joint = hard corner
        a = L.getchannel('A').point(lambda v: int(v * alpha)); L.putalpha(a)
        cx0, cy0 = max(0, bx0), max(0, by0)
        img.alpha_composite(L.crop((cx0 - bx0, cy0 - by0, min(W, bx1) - bx0, min(H, by1) - by0)), (cx0, cy0))
TICKS = ['rtick_m2', 'rtick_m1', 'rtick_0', 'rtick_p1', 'rtick_p2']
BTICKS = ['btick_m2', 'btick_m1', 'btick_0', 'btick_p1', 'btick_p2']   # block-hit ticks: the same pitches, +14 dB over rtick
def btick_name(t): return BTICKS[int(abs(math.sin(t * 12.9898) * 43758.5453)) % 5]
def tick_name(t):
    """bounce tick: -4 dB vs reeltick_8bit, pitch varied within +-2 semitones (deterministic per time)"""
    return TICKS[int(abs(math.sin(t * 12.9898) * 43758.5453)) % 5]
# ---------------- Code Name castle kit (shared by the m05/m06 reskins; palette from Liza's Realm art, pause/assets/scene_castle.png)
def castle_backdrop(dim=0.62, blur=4):
    """the Realm castle scene filling the frame behind the board, blurred and dimmed (like the race backdrop)"""
    sc = Image.open(S_ + 'pause/assets/scene_castle.png').convert('RGB')
    k = H / sc.height; sc = sc.resize((int(sc.width * k), H), Image.LANCZOS)
    x0 = (sc.width - W) // 2; sc = sc.crop((x0, 0, x0 + W, H)).filter(ImageFilter.GaussianBlur(blur))
    sc = ImageEnhance.Color(ImageEnhance.Brightness(sc).enhance(dim)).enhance(0.85).convert('RGBA')
    g = Image.new('L', (1, H)); [g.putpixel((0, y), int(30 + 50 * abs(y - H / 2) / (H / 2))) for y in range(H)]
    sh = Image.new('RGBA', (W, H), (8, 6, 16, 255)); sh.putalpha(g.resize((W, H))); sc.alpha_composite(sh)
    return sc
def vignette(strength=120):
    v = Image.new('L', (W // 8, H // 8), 0)
    for yy in range(H // 8):
        for xx in range(W // 8):
            dx_, dy_ = (xx - W / 16) / (W / 16), (yy - H / 16) / (H / 16)
            v.putpixel((xx, yy), int(min(1.0, max(0.0, (dx_ * dx_ + dy_ * dy_) ** 0.5 - 0.55) / 0.75) * strength))
    L = Image.new('RGBA', (W, H), (6, 4, 12, 255)); L.putalpha(v.resize((W, H), Image.BILINEAR)); return L
FLAG = [(148, 126, 98), (139, 118, 92), (156, 133, 103), (132, 112, 88), (144, 123, 97)]
def flagstones(x0, y0, x1, y1, seed=3):
    """irregular courtyard flagstones: varied widths per course, mortar joints, edge light/shade, a few cracks, light dust"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = random.Random(seed)
    d.rectangle([x0, y0, x1, y1], fill=(84, 64, 50, 255))
    y = y0 - rr.randint(0, 20)
    while y < y1:
        h = rr.randint(30, 46); x = x0 - rr.randint(0, 40)
        while x < x1:
            w = rr.randint(34, 78); c = rr.choice(FLAG); c = tuple(max(0, min(255, v + rr.randint(-6, 6))) for v in c)
            a, b, e, f = x + 2, y + 2, x + w - 1, y + h - 1
            d.rectangle([a, b, e, f], fill=c + (255,))
            d.rectangle([a, b, e, b + 1], fill=tuple(min(255, v + 18) for v in c) + (255,)); d.rectangle([a, b, a + 1, f], fill=tuple(min(255, v + 10) for v in c) + (255,))
            d.rectangle([a, f - 1, e, f], fill=tuple(max(0, v - 24) for v in c) + (255,)); d.rectangle([e, b, e, f], fill=tuple(max(0, v - 14) for v in c) + (255,))
            for _ in range(rr.randint(2, 6)):                       # dust / grit
                px_, py_ = rr.randint(a + 3, max(a + 3, e - 3)), rr.randint(b + 3, max(b + 3, f - 3)); d.rectangle([px_, py_, px_ + 1, py_], fill=tuple(min(255, v + 22) for v in c) + (255,))
            if rr.random() < 0.10 and w > 40:                        # crack
                cx_, cy_ = rr.randint(a + 6, e - 6), b + 2; pts = [(cx_, cy_)]
                while cy_ < f - 4: cy_ += rr.randint(4, 8); cx_ += rr.choice([-3, -2, 2, 3]); pts.append((cx_, min(cy_, f - 3)))
                d.line(pts, fill=tuple(max(0, v - 48) for v in c) + (255,), width=1)
            x += w
        y += h
    return L
STONES2 = [(170, 160, 150), (158, 149, 140), (180, 170, 158), (148, 140, 134), (164, 152, 140), (154, 146, 140)]
def castle_bricks(x0, y0, x1, y1, seed=7):
    """40x20 castle bricks with variation: darker bricks, a few cracked ones, moss patches"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L); rr = random.Random(seed)
    for by in range(y0, y1, 20):
        off = 0 if ((by - y0) // 20) % 2 == 0 else -20
        for bx in range(x0 + off, x1, 40):
            c = rr.choice(STONES2)
            if rr.random() < 0.12: c = tuple(max(0, v - 26) for v in c)
            a, b, e, f = bx, by, bx + 39, by + 19
            d.rectangle([a, b, e, f], fill=(86, 78, 84, 255))
            d.rectangle([a + 2, b + 2, e - 1, f - 1], fill=c + (255,))
            d.rectangle([a + 2, b + 2, e - 1, b + 3], fill=tuple(min(255, v + 24) for v in c) + (255,))
            d.rectangle([a + 2, b + 2, a + 3, f - 1], fill=tuple(min(255, v + 14) for v in c) + (255,))
            d.rectangle([a + 2, f - 2, e - 1, f - 1], fill=tuple(max(0, v - 30) for v in c) + (255,))
            for _ in range(3):
                px_, py_ = rr.randint(a + 5, e - 5), rr.randint(b + 5, f - 5); d.rectangle([px_, py_, px_ + 1, py_ + 1], fill=tuple(max(0, v - 16) for v in c) + (255,))
            if rr.random() < 0.06:
                cx_ = rr.randint(a + 8, e - 8); d.line([(cx_, b + 3), (cx_ + 3, b + 8), (cx_ - 1, b + 12), (cx_ + 2, f - 3)], fill=tuple(max(0, v - 55) for v in c) + (255,), width=1)
    for _ in range(int((x1 - x0) * (y1 - y0) / 26000)):              # moss patches
        mx, my = rr.randint(x0, x1), rr.randint(y0, y1)
        for _ in range(rr.randint(14, 34)):
            px_, py_ = mx + int(rr.gauss(0, 7)), my + int(rr.gauss(0, 4)); col = rr.choice([(92, 132, 70), (110, 150, 80), (72, 108, 58)])
            d.rectangle([px_, py_, px_ + 2, py_ + 1], fill=col + (255,))
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0)); out.paste(L.crop((x0, y0, x1, y1)), (x0, y0)); return out   # clipped to the board
def ledge_shadow(Wd_, OX_, OY_, C_, isw):
    """darker band on the floor just under every ceiling (wall directly above), for depth"""
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for r in range(1, Wd_.rows):
        for c in range(Wd_.cols):
            if not isw(r, c) and isw(r - 1, c):
                for k in range(4): d.rectangle([OX_ + c * C_, OY_ + r * C_ + 2 * k, OX_ + c * C_ + C_ - 1, OY_ + r * C_ + 2 * k + 1], fill=(26, 14, 10, 92 - k * 22))
    return L
def banner(d, x, y, w=64, h=150):
    """Realm-blue banner with gold trim and crest, hung from an iron rod"""
    d.rectangle([x - 8, y - 6, x + w + 8, y - 1], fill=(40, 36, 44, 255)); d.rectangle([x - 10, y - 8, x - 6, y + 1], fill=(200, 160, 70, 255)); d.rectangle([x + w + 6, y - 8, x + w + 10, y + 1], fill=(200, 160, 70, 255))
    d.polygon([(x, y), (x + w, y), (x + w, y + h), (x + w // 2, y + h - 22), (x, y + h)], fill=(22, 30, 70, 255))
    d.polygon([(x + 3, y), (x + w - 3, y), (x + w - 3, y + h - 6), (x + w // 2, y + h - 26), (x + 3, y + h - 6)], fill=(34, 52, 122, 255))
    d.rectangle([x + 6, y + 4, x + w - 7, y + 6], fill=(224, 176, 72, 255)); d.line([(x + 6, y + 6), (x + 6, y + h - 12)], fill=(224, 176, 72, 255), width=2); d.line([(x + w - 7, y + 6), (x + w - 7, y + h - 12)], fill=(224, 176, 72, 255), width=2)
    cx, cy = x + w // 2, y + h // 2 - 8
    d.polygon([(cx, cy - 22), (cx + 16, cy), (cx, cy + 22), (cx - 16, cy)], fill=(224, 176, 72, 255)); d.polygon([(cx, cy - 13), (cx + 9, cy), (cx, cy + 13), (cx - 9, cy)], fill=(34, 52, 122, 255))
    d.rectangle([cx - 2, cy - 4, cx + 2, cy + 4], fill=(250, 214, 120, 255))
    d.line([(x + 10, y + 20), (x + 10, y + h - 20)], fill=(28, 42, 100, 255), width=2)
def sconce(d, x, y):
    """static iron sconce + wooden torch handle (flame is drawn per frame by torch_flame)"""
    d.rectangle([x - 7, y + 10, x + 7, y + 26], fill=(40, 36, 44, 255)); d.rectangle([x - 5, y + 12, x + 5, y + 24], fill=(70, 64, 72, 255))
    d.rectangle([x - 4, y - 2, x + 4, y + 12], fill=(30, 26, 32, 255)); d.rectangle([x - 2, y, x + 2, y + 12], fill=(122, 80, 44, 255))
    d.rectangle([x - 6, y - 4, x + 6, y], fill=(52, 46, 54, 255))
_GLOW = None
def torch_flame(img, x, y, t, ph=0.0):
    global _GLOW
    if _GLOW is None:
        g = Image.new('L', (160, 160), 0); gd = ImageDraw.Draw(g)
        for r in range(80, 0, -4): gd.ellipse([80 - r, 80 - r, 80 + r, 80 + r], fill=int(70 * (1 - r / 80) ** 1.5))
        _GLOW = Image.new('RGBA', (160, 160), (255, 170, 70, 255)); _GLOW.putalpha(g)
    fl = 0.85 + 0.15 * math.sin(t * 13 + ph) * math.sin(t * 7.3 + ph * 2)
    img.alpha_composite(_GLOW, (int(x - 80), int(y - 86)))
    hgt = int(18 * fl); sway = int(round(2 * math.sin(t * 9 + ph)))
    def blob(dd):
        dd.polygon([(x - 7, y - 4), (x + 7, y - 4), (x + 3 + sway, y - 4 - hgt), (x + sway, y - 8 - hgt), (x - 3 + sway, y - 4 - hgt)], fill=(232, 96, 30, 255))
        dd.polygon([(x - 4, y - 4), (x + 4, y - 4), (x + 1 + sway, y - 2 - int(hgt * 0.75)), (x - 1 + sway, y - 2 - int(hgt * 0.75))], fill=(255, 180, 60, 255))
        dd.rectangle([x - 2, y - 9, x + 1, y - 4], fill=(255, 242, 190, 255))
    layer(img, blob)
def portal_frame(d, x0, y0, x1, y1, side):
    """stone arch frame + raised iron portcullis around an exit opening; side = which edge opens into the play area ('right' or 'bottom')"""
    if side == 'right':
        for k, yy in enumerate(list(range(y0 - 40, y0 - 10, 12)) + list(range(y1 + 2, y1 + 34, 12))):   # arch stones on the wall face above/below the mouth
            d.rectangle([x1 - 15, yy, x1 - 2, yy + 10], fill=(200, 188, 170, 255) if k % 2 else (178, 166, 150, 255), outline=(90, 82, 86, 255))
        d.rectangle([x0, y0 - 10, x1, y0 - 1], fill=(60, 56, 64, 255))
        for xx in range(x0 + 6, x1 - 4, 12): d.rectangle([xx, y0 - 1, xx + 3, y0 + 9], fill=(70, 66, 76, 255)); d.polygon([(xx, y0 + 9), (xx + 3, y0 + 9), (xx + 1, y0 + 14)], fill=(70, 66, 76, 255))
    else:
        for k, xx in enumerate(range(x0 - 14, x1 + 14, 12)):
            d.rectangle([xx, y1 - 2, xx + 10, y1 + 10], fill=(196, 184, 166, 255) if k % 2 else (176, 164, 148, 255), outline=(90, 82, 86, 255))
        d.rectangle([x0, y0, x1, y0 + 8], fill=(60, 56, 64, 255))
        for xx in range(x0 + 5, x1 - 3, 10): d.rectangle([xx, y0 + 8, xx + 3, y0 + 16], fill=(70, 66, 76, 255)); d.polygon([(xx, y0 + 16), (xx + 3, y0 + 16), (xx + 1, y0 + 21)], fill=(70, 66, 76, 255))
def portal_glow(img, x0, y0, x1, y1, t, toward):
    """animated golden light inside the exit (brightest at the far end), drifting motes"""
    w, h = int(x1 - x0), int(y1 - y0); L = Image.new('RGBA', (w, h)); px = L.load()
    pul = 0.9 + 0.1 * math.sin(t * 3)
    for j in range(h):
        for i in range(w):
            u = (1 - i / max(1, w - 1)) if toward == 'left' else (1 - j / max(1, h - 1))
            u = u ** 1.4 * pul
            px[i, j] = (int(110 + 145 * u), int(74 + 166 * u), int(40 + 140 * u), 255)
    rs = random.Random(5); dd = ImageDraw.Draw(L)
    for k in range(10):
        ph = rs.random(); s_ = (t * 0.35 + ph) % 1.0
        if toward == 'left': mx, my = int(w * (1 - s_)), int(h * rs.random())
        else: mx, my = int(w * rs.random()), int(h * (1 - s_))
        dd.rectangle([mx, my, mx + 2, my + 2], fill=(255, 246, 200, int(255 * (1 - abs(0.5 - s_) * 2))))
    img.alpha_composite(L, (int(x0), int(y0)))
