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
