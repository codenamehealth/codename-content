"""Shared helpers for fork_rc12 review recuts (r100-r105)."""
import sys
SP = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP + 'fork_rc2'); sys.path.insert(0, SP + 'fork_rc1')
from rc2 import gummy_src, acv_tag, acv_gloss, FF
from hook2 import hook_layer2
from PIL import Image, ImageDraw

def zone_xmax(y): return 1025 if y <= 1110 else 887

def plate(img, x, y, text, size, color=(255, 255, 255), a=255, border=None, scale=1.0, pad=18):
    """centred text (top at y) on its own dark plate, clamped inside the safe zone; returns (x0, y0, x1, y1)"""
    s = max(8, int(size * scale)); f = FF(s)
    L = Image.new('RGBA', img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    tw = d.textlength(text, font=f); w = tw + 2 * pad; h = s + 2 * pad
    while w > zone_xmax(y + size / 2 + h / 2) - 4 - 74 and s > 24:      # never wider than the safe zone
        s -= 2; f = FF(s); tw = d.textlength(text, font=f); w = tw + 2 * pad; h = s + 2 * pad
    yc = y + size / 2; y0 = yc - h / 2
    y0 = max(254, min(1496 - h, y0))
    xmax = zone_xmax(y0 + h) - 4
    x0 = max(74, min(xmax - w, x - w / 2))
    d.rounded_rectangle([x0, y0, x0 + w, y0 + h], 14, fill=(14, 10, 24, int(232 * a / 255)), outline=(border or color)[:3] + (a,), width=5)
    d.text((x0 + pad, y0 + pad), text, font=f, fill=tuple(color[:3]) + (a,), stroke_width=max(4, s // 10), stroke_fill=(10, 6, 18, a))
    img.alpha_composite(L)
    return (x0, y0, x0 + w, y0 + h)

class Stamps:
    """one stamp at a time. add(t, text, color, x, y, prio, dur); higher prio cuts a lower one short; low prio is dropped when busy."""
    def __init__(self, gap=0.04):
        self.items = []; self.gap = gap
    def build(self, evs, min_show=0.45):
        """evs: list of (t, text, color, x, y, prio, dur). Returns schedule list of [start, end, text, color, x, y, prio].
        Stamps show on time: an important one (prio>=2) cuts the current one short (after at least min_show);
        a cosmetic one (prio 1) is dropped while another is up."""
        out = []
        for (t, tx, c, x, y, pr, du) in sorted(evs, key=lambda e: (e[0], -e[5])):
            if out and out[-1][1] > t:
                last = out[-1]
                if tx == last[2] and x == last[4]: last[1] = max(last[1], t + du); continue   # same stamp again: just extend it
                if pr < 2: continue
                t = max(t, last[0] + min_show); last[1] = t
            out.append([t, t + du, tx, c, x, y, pr])
        self.items = out; return out
    def draw(self, img, t, size=60):
        for (a, b, tx, c, x, y, pr) in self.items:
            if a <= t < b:
                u = t - a; sc = 1.25 - 0.25 * min(1, u / 0.12)
                al = int(255 * min(1, (b - t) / 0.12))
                plate(img, x, y, tx, size, c, al, scale=sc)
