# Environment art for the Code Name race reels (r01 water course; reusable for r02).
# Backdrop: Liza's Thornberry Forest scene (pause/assets/found_hd.gif, hand-painted by Liza) as a dimmed parallax layer
# above and below the course band, drawn 1:1 at full resolution. Course props: PixelLab environment tiles (wk_r01/bg/*).
# Water, lane buoy lines, ropes, bars and ledges are drawn natively (pixel grid) and upscaled 4x with the world.
import numpy as np, math, random
from PIL import Image, ImageDraw
S_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
BGD = S_ + 'wk_r01/bg/'
W, H = 1080, 1920
def _crop(p):
    im = Image.open(p).convert('RGBA'); return im.crop(im.getbbox())
DOCK = _crop(BGD + 'dock/00.png'); STONE = _crop(BGD + 'stone2/00.png'); LOG = _crop(BGD + 'log2/00.png')
ROCK = _crop(BGD + 'rock2/00.png'); POST = _crop(BGD + 'post/00.png'); ARCH = _crop(BGD + 'arch2/00.png')
_g = np.array(Image.open(BGD + 'grass/00.png').convert('RGBA')).copy()
_sky = (_g[..., 2].astype(int) > 170) & (_g[..., 2].astype(int) > _g[..., 0].astype(int) + 40)
_g[_sky, 3] = 0
GRASS = _g                                                  # 64x64: rows ~5-24 grass blades, 24-64 dirt
def top_profile(im):
    a = np.array(im)[..., 3] > 0
    return np.array([np.where(a[:, x])[0][0] if a[:, x].any() else im.height for x in range(im.width)])
ROCK_TOP = top_profile(ROCK)
_slc = {}
def sliced(src, cap, w):
    """horizontal 3-slice: left cap, repeated middle, right cap (pixel exact, no scaling)"""
    k = (id(src), cap, int(w))
    if k in _slc: return _slc[k]
    w = max(int(w), 2 * cap + 1); mid = src.crop((cap, 0, src.width - cap, src.height))
    out = Image.new('RGBA', (w, src.height), (0, 0, 0, 0)); out.alpha_composite(src.crop((0, 0, cap, src.height)), (0, 0))
    x = cap
    while x < w - cap:
        out.alpha_composite(mid.crop((0, 0, min(mid.width, w - cap - x), mid.height)), (x, 0)); x += mid.width
    out.alpha_composite(src.crop((src.width - cap, 0, src.width, src.height)), (w - cap, 0))
    _slc[k] = out; return out
# ------------------------------------------------------------------ backdrop (Liza)
_BG = None
BG_FILE = 'pause/assets/found_hd.gif'
def _load_bg():
    global _BG
    g = Image.open(S_ + BG_FILE); fr = []
    for i in range(g.n_frames):
        g.seek(i); a = np.array(g.convert('RGB')).astype(np.float32)
        lum = a.mean(2, keepdims=True); a = (a * 0.78 + lum * 0.22) * 0.74 + np.array([4, 6, 14])   # a bit darker and less saturated than the guides
        a = np.clip(a, 0, 255).astype(np.uint8)
        fr.append(np.concatenate([a, a[:, ::-1]], 1))                                            # mirrored strip for an endless parallax
    _BG = fr
def backdrop(t, cam_native, band_top, band_bot, K=4):
    if _BG is None: _load_bg()
    f = _BG[int(t * 8) % len(_BG)]; Wd = f.shape[1]
    out = np.zeros((H, W, 3), np.uint8)
    px = int(cam_native * K * 0.18) % Wd
    idx = (np.arange(W) + px) % Wd
    top_h = band_top * K; bot_y = band_bot * K
    out[:top_h] = f[1080 - 120 - top_h:1080 - 120][:, idx] if top_h <= 960 else f[:top_h][:, idx]        # canopy, waterfall, mossy bank
    px2 = int(cam_native * K * 0.30) % Wd; idx2 = (np.arange(W) + px2) % Wd
    out[bot_y:] = f[1080 - (H - bot_y):][:, idx2]                                                            # near bank: ferns, grass
    for i in range(24):                                                                                       # soft shade where the band meets the scene
        a = 0.45 * (1 - i / 24)
        if top_h - 1 - i >= 0: out[top_h - 1 - i] = (out[top_h - 1 - i] * (1 - a)).astype(np.uint8)
        if bot_y + i < H: out[bot_y + i] = (out[bot_y + i] * (1 - a)).astype(np.uint8)
    return Image.fromarray(out)
# ------------------------------------------------------------------ water (native)
_rs = np.random.RandomState(11)
_NOISE = _rs.rand(96, 256)
def water(arr, x0, y0, w, h, cam, t, seed=0):
    """fill arr[y0:y0+h, x0:x0+w] (uint8 RGBA native) with shaded, animated water"""
    ys = np.arange(h)[:, None]; xs = (np.arange(w)[None, :] + int(cam)) % 256
    u = ys / max(1, h - 1)
    c_top = np.array([88, 168, 206]); c_bot = np.array([36, 92, 150])
    band = np.floor(u * 5) / 5                                                          # posterised depth bands
    base = c_top[None, None, :] * (1 - band[..., None]) + c_bot[None, None, :] * band[..., None]
    n = _NOISE[(ys + seed * 13) % 96, xs]
    base = base + (n[..., None] - 0.5) * 10
    wv = np.sin((np.arange(w)[None, :] + cam) * 0.21 + ys * 1.7 + t * 2.3 + seed) + np.sin((np.arange(w)[None, :] + cam) * 0.07 - t * 1.3 + ys * 0.5)
    hi = (wv > 1.55) & ((ys % 5) == (seed % 5))
    base[hi] = base[hi] * 0.55 + np.array([214, 240, 255]) * 0.45
    lo = (wv < -1.6) & ((ys % 7) == 3)
    base[lo] = base[lo] * 0.85
    sp = (_NOISE[(ys * 3 + seed) % 96, (xs * 7) % 256] > 0.9988) & (np.sin(t * 5 + xs * 0.37 + ys * 1.3) > 0.75) & (ys < h * 0.6)   # a few twinkling sparkles
    base[sp] = [255, 255, 255]
    arr[y0:y0 + h, x0:x0 + w, :3] = np.clip(base, 0, 255).astype(np.uint8); arr[y0:y0 + h, x0:x0 + w, 3] = 255
def buoys(d, y, cam, t, NW):
    """floating lane line: dark rope with red/white buoys that bob"""
    d.line([0, y + 1, NW, y + 1], fill=(60, 44, 34))
    off = int(cam) % 8
    for xx in range(-off - 8, NW + 8, 8):
        k = (xx + int(cam)) // 8; bob = 1 if math.sin(t * 3 + k * 0.9) > 0.4 else 0
        col = (214, 58, 58) if k % 3 else (240, 240, 232)
        d.ellipse([xx, y - 2 + bob, xx + 4, y + 2 + bob], fill=(48, 24, 24))
        d.ellipse([xx + 1, y - 1 + bob, xx + 3, y + 1 + bob], fill=col)
        d.point((xx + 1, y - 1 + bob), fill=(255, 255, 255))
def ledge(d, y0, y1, NW, cam):
    """mossy stone pool edge"""
    d.rectangle([0, y0, NW, y1], fill=(84, 86, 92))
    off = int(cam) % 14
    for xx in range(-off - 14, NW + 14, 14):
        d.rectangle([xx, y0, xx + 13, y1], fill=(104, 106, 112)); d.line([xx, y0, xx + 13, y0], fill=(140, 142, 146))
        d.line([xx + 13, y0, xx + 13, y1], fill=(62, 62, 70)); d.line([xx, y1, xx + 13, y1], fill=(54, 54, 60))
        d.line([xx + 2, y0, xx + 6, y0], fill=(110, 150, 70))
def rope(d, pts):
    """twisted rope along a polyline"""
    d.line(pts, fill=(70, 46, 30), width=3)
    for i, (a, b) in enumerate(pts):
        if i % 2 == 0: d.point((a, b - 1), fill=(204, 160, 104))
        else: d.point((a, b), fill=(150, 104, 64))
def pole(d, x, y0, y1):
    d.rectangle([x - 2, y0, x + 2, y1], fill=(54, 46, 52)); d.rectangle([x - 1, y0, x + 1, y1], fill=(150, 140, 150)); d.line([x - 1, y0, x - 1, y1], fill=(210, 204, 214))
def bar(d, x0, x1, y):
    d.rectangle([x0, y - 2, x1, y + 1], fill=(54, 46, 52)); d.line([x0, y - 1, x1, y - 1], fill=(206, 200, 210)); d.line([x0, y, x1, y], fill=(130, 122, 132))
def ring(d, x, y):
    d.ellipse([x - 3, y, x + 3, y + 7], outline=(110, 74, 20)); d.ellipse([x - 2, y + 1, x + 2, y + 6], outline=(255, 210, 90)); d.point((x - 2, y + 2), fill=(255, 245, 200))
def deck(arr_img, x0, x1, y0, y1, plank=True):
    """wooden deck block (top-down planks to the standing line, then the front edge)"""
    d = ImageDraw.Draw(arr_img)
    d.rectangle([x0, y0, x1, y1], fill=(120, 80, 48))
    for yy in range(y0, y1, 5):
        d.line([x0, yy, x1, yy], fill=(92, 58, 34)); d.line([x0, yy + 1, x1, yy + 1], fill=(150, 104, 64))
def lawn(img, x0, x1, ytop, yface, ybot, cam):
    """grassy terrace: soft lawn (top) down to the standing line with a fringe of blades, dirt face below"""
    a = np.array(img); xa = max(0, int(x0)); xb = min(a.shape[1], int(x1))
    if xb <= xa: return img
    wx = np.arange(xa, xb) + int(cam); xs = wx % 64
    for yy in range(int(ytop), int(ybot)):
        if yy < 0 or yy >= a.shape[0]: continue
        if yy < yface - 4:
            n = _NOISE[yy % 96, (wx * 3) % 256]
            row = np.stack([74 + n * 14, 116 + n * 18, 54 + n * 10], 1)
            fl = (_NOISE[(yy * 5) % 96, (wx * 11) % 256] > 0.985)
            row[fl] = [236, 226, 150]
            a[yy, xa:xb, :3] = row.astype(np.uint8)
        elif yy < yface: a[yy, xa:xb, :3] = GRASS[14 + (yy - int(yface)) , xs][:, :3]
        else: a[yy, xa:xb, :3] = GRASS[26 + (yy - int(yface)) % 36, xs][:, :3]
        a[yy, xa:xb, 3] = 255
    edge = int(yface)
    if 0 <= edge < a.shape[0]: a[edge, xa:xb, :3] = (a[edge, xa:xb, :3] * 0.6).astype(np.uint8)
    return Image.fromarray(a)
def hill_fill(img, s, cam, li, base, NW):
    a = np.array(img); xa = max(int(s.x0 - cam), 0); xb = min(int(s.x1 - cam), NW - 1)
    for sx in range(xa, xb + 1):
        top = int(s.top(sx + cam)); tx = int(sx + cam) % 64
        for yy in range(top - 4, base):
            if yy < 0 or yy >= a.shape[0]: continue
            r = yy - top
            if r < 0:
                px = GRASS[8 + r + 4, tx]                                  # grass blades poking above the contour
                if px[3] == 0: continue
            elif r < 12: px = GRASS[12 + r, tx]
            else: px = GRASS[26 + (r - 12) % 36, tx]
            a[yy, sx, :3] = px[:3]; a[yy, sx, 3] = 255
    return Image.fromarray(a)
def blend(img, x0, y0, w, h, fn):
    """draw translucent shapes onto a small patch and alpha-composite it (ImageDraw does not blend on RGBA)"""
    x0, y0, w, h = int(x0), int(y0), int(w) + 2, int(h) + 2
    if w <= 0 or h <= 0: return
    p = Image.new('RGBA', (w, h), (0, 0, 0, 0)); fn(ImageDraw.Draw(p))
    cx, cy = max(0, -x0), max(0, -y0)
    if cx >= w or cy >= h or x0 >= img.width or y0 >= img.height: return
    img.alpha_composite(p.crop((cx, cy, w, h)), (max(0, x0), max(0, y0)))
def shadow(d, cx, y, w=18, alpha=80):
    w = max(4, w)
    blend(d._image, cx - w / 2 - 1, y - 3, w + 2, 6, lambda dd: dd.ellipse([1, 1, w + 1, 5], fill=(10, 16, 30, max(0, int(alpha)))))
