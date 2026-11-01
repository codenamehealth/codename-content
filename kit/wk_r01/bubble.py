# Pixel speech bubbles (on-screen text only; the guides never have voices). Drawn on the native 4px grid, game font inside.
from PIL import Image, ImageDraw, ImageFont
import math
FONT = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/npmfont/ps/package/files/PressStart2P.ttf'
_f = {}
def F(s):
    if s not in _f: _f[s] = ImageFont.truetype(FONT, s)
    return _f[s]
SAFE = (80, 262, 880, 1480)
def draw(big, text, head, side, t, t0, dur, K=4, px=48):
    """big: full-res RGBA frame; head: speaker's head point (full res); side: 'right'|'left'|'up'"""
    u = t - t0
    if not (0 <= u < dur): return None
    f = F(px); tw = int(ImageDraw.Draw(big).textlength(text, font=f))
    bw = (tw + 2 * 24) // K * K + K; bh = (px + 2 * 20) // K * K
    hx, hy = head
    if side == 'right': bx, by = hx + 70, hy - bh - 24
    elif side == 'left': bx, by = hx - 70 - bw, hy - bh - 24
    elif side == 'leftlow': bx, by = hx - 90 - bw, hy + 40
    else: bx, by = hx - bw / 2, hy - bh - 70
    bx = max(SAFE[0], min(SAFE[2] - bw, bx)); by = max(SAFE[1], min(SAFE[3] - bh, by))
    pop = [-8, 4, 0][min(2, int(u * 30))] if u < 0.1 else 0                      # 3-frame pop
    if u > dur - 0.1: pop = 0
    by += pop; bx, by = int(bx // K * K), int(by // K * K)
    L = Image.new('RGBA', big.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    ol, fill = (28, 20, 40, 255), (250, 248, 240, 255)
    # tail: from the bubble's lower edge toward the head (stepped on the 4px grid)
    tx0 = min(max(hx, bx + 28), bx + bw - 28); ty0 = by + bh - K
    dx, dy = hx - tx0, hy - ty0; n = max(1, int(math.hypot(dx, dy) * 0.45 / K))
    for i in range(n):
        u2 = i / n; cx, cy = tx0 + dx * u2 * 0.45, ty0 + dy * u2 * 0.45; w = max(1, int((1 - u2) * 4)) * K
        d.rectangle([cx - w // 2 - K, cy - K, cx + w // 2 + K, cy + 2 * K], fill=ol)
    for i in range(n):
        u2 = i / n; cx, cy = tx0 + dx * u2 * 0.45, ty0 + dy * u2 * 0.45; w = max(1, int((1 - u2) * 4)) * K
        d.rectangle([cx - w // 2, cy, cx + w // 2, cy + K], fill=fill)
    d.rectangle([bx + K, by, bx + bw - K, by + bh], fill=ol); d.rectangle([bx, by + K, bx + bw, by + bh - K], fill=ol)
    d.rectangle([bx + 2 * K, by + K, bx + bw - 2 * K, by + bh - K], fill=fill); d.rectangle([bx + K, by + 2 * K, bx + bw - K, by + bh - 2 * K], fill=fill)
    d.rectangle([bx + 2 * K, by + bh - 2 * K, bx + bw - 2 * K, by + bh - K], fill=(214, 208, 196, 255))
    d.text((bx + (bw - tw) / 2, by + (bh - px) / 2 + 2), text, font=f, fill=(40, 26, 50))
    big.alpha_composite(L)
    return (bx, by, bx + bw, by + bh)
