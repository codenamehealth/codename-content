# n9 review2: two-line hook PAUSE WHEN IT'S / IN THE BOTTLE (BOTTLE accent), text bottom kept at the old hook's (row 507)
from hook import hook_fade, _fit, X0, X1, W
from PIL import ImageDraw
import numpy as np
LINES = ["PAUSE WHEN IT'S", 'IN THE BOTTLE']; G = (140, 230, 90); FADE_TO = 286 + 2 * 84 + 70 + 110
def _rows(L):
    a = np.asarray(L); m = (a[..., 3] > 0) & ~((a[..., 0] == 8) & (a[..., 1] == 6) & (a[..., 2] == 16)); r = np.where(m.any(1))[0]; return r.min(), r.max()
def make(y):
    L, b = hook_fade(LINES, y=y, fade_to=FADE_TO)
    f, s = _fit([l.upper() for l in LINES], X1 - X0 - 20, 64, 40); lh = int(s * 1.32); d = ImageDraw.Draw(L)
    full = LINES[1]; x = W / 2 - d.textlength(full, font=f) / 2 + d.textlength('IN THE ', font=f)
    d.text((x, y + lh), 'BOTTLE', font=f, fill=G, stroke_width=6, stroke_fill=(12, 8, 20))
    return L, b
_L, _ = make(286); _top, _bot = _rows(_L); Y = 286 + (507 - _bot)
HK, HB0 = make(Y)
