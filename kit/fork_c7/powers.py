"""Shared gummy-power FX (SPEC 12), same look as fork_c5b/v46 (#46): STRONG blue aura, SPEED orange afterimages +
speed lines + dust, SLEEP purple rings + Zzz, SHIELD green bubble, BONK burst, dizzy stars, pop labels."""
import math, random
from PIL import Image, ImageDraw
import sys
sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import layer, text_layer
POWER = {'mush': ('SPEED!', (255, 160, 40)), 'mel': ('SLEEP!', (190, 120, 255)), 'cre': ('STRONG!', (90, 160, 255)), 'acv': ('SHIELD!', (110, 230, 90))}
SFX = {'mush': 'powerup_8bit', 'cre': 'powerup2', 'acv': 'twinkle', 'mel': 'poof'}

def tinted(spr, col, a):
    t_ = Image.new('RGBA', spr.size, col + (255,)); t_.putalpha(spr.getchannel('A').point(lambda p: int(p * a / 255))); return t_

def aura(img, spr, x0, y0, col=(90, 160, 255), a=200):
    tt = tinted(spr, col, a)
    for ox, oy in ((-6, 0), (6, 0), (0, -6), (0, 6), (-4, -4), (4, 4), (-4, 4), (4, -4)): img.alpha_composite(tt, (int(x0 + ox), int(y0 + oy)))

def afterimages(img, ghosts):
    """ghosts: list of (spr, x0, y0) oldest first (not including the current frame)."""
    for i_, (gs, gx, gy) in enumerate(ghosts):
        img.alpha_composite(tinted(gs, (255, 170, 50), int(255 * (0.14 + 0.09 * i_))), (int(gx), int(gy)))

def speed_lines(img, x, yfoot, sgn, t, h=200):
    """sgn = direction of travel (+1 right, -1 left); lines + dust behind the runner. x,yfoot = feet centre."""
    b = -sgn
    def fn(dd):
        for q in range(4):
            xa = x + b * (50 + 30 * q); ln = 70 + (q * 37 + int(t * 60)) % 50; xb = xa + b * ln
            yy = yfoot - h * 0.62 + q * h * 0.16
            lo, hi = max(70, min(xa, xb)), min(1010, max(xa, xb))
            if hi > lo: dd.rectangle([lo, yy - 3, hi, yy + 3], fill=(255, 240, 200, 210))
        for q in range(3):
            cx = x + b * (30 + q * 26)
            if not 84 < cx < 1000: continue
            dd.ellipse([cx - 14 + q * 2, yfoot - 12 - q * 4, cx + 14, yfoot + 8], fill=(210, 190, 150, 160 - q * 45))
    layer(img, fn)

def zzz(img, x, ytop, u):
    text_layer(img, [(x + 30 + 18 * k_, ytop - 10 - ((u * 1.6 + k_ * 0.33) % 1) * 70 - k_ * 14, 'Z', 30 + 8 * k_, (220, 200, 255), 5,
                      int(255 * (1 - (u * 1.6 + k_ * 0.33) % 1))) for k_ in range(3)])

def sleepy(img, spr, x0, y0):
    img.alpha_composite(spr, (int(x0), int(y0))); img.alpha_composite(tinted(spr, (40, 20, 90), 90), (int(x0), int(y0)))

def sleep_wave(img, x, y, u, big=900):
    layer(img, lambda dd: [dd.ellipse([x - r_, y - r_ * 0.7, x + r_, y + r_ * 0.7], outline=(190, 120, 255, int(220 * (1 - u))), width=10) for r_ in (60 + big * u, 20 + big * 0.66 * u)])

def shield(img, x, yfoot, h, w=70):
    layer(img, lambda dd: (dd.ellipse([x - w, yfoot - h + 6, x + w, yfoot + 18], fill=(110, 230, 90, 55), outline=(150, 255, 120, 220), width=6),
                           dd.arc([x - w * 0.74, yfoot - h + 24, x + w * 0.15, yfoot - h + 90], 200, 260, fill=(230, 255, 220, 230), width=5)))

def shield_pop(img, x, yfoot, h, u, w=70):
    """bubble bursting (u 0..1)"""
    r = 1 + 0.5 * u
    layer(img, lambda dd: [dd.rectangle([x + w * r * math.cos(q * 0.785) - 6, yfoot - h / 2 + h / 2 * r * math.sin(q * 0.785) - 6,
                                         x + w * r * math.cos(q * 0.785) + 6, yfoot - h / 2 + h / 2 * r * math.sin(q * 0.785) + 6], fill=(150, 255, 120, int(255 * (1 - u)))) for q in range(8)])

def bonk_burst(img, cx, cy, u):
    layer(img, lambda dd: [dd.polygon([(cx + math.cos(q * 0.785) * 30, cy + math.sin(q * 0.785) * 30), (cx + math.cos(q * 0.785 + 0.2) * (60 + 60 * u), cy + math.sin(q * 0.785 + 0.2) * (60 + 60 * u)),
                                       (cx + math.cos(q * 0.785 + 0.39) * 30, cy + math.sin(q * 0.785 + 0.39) * 30)], fill=(255, 255, 255, int(255 * (1 - u)))) for q in range(8)])

def dizzy(img, x, yhead, t):
    layer(img, lambda dd: [dd.polygon([(x + 34 * math.cos(t * 9 + q * 2.09) + dx_, yhead + 10 * math.sin(t * 9 + q * 2.09) + dy_) for dx_, dy_ in ((0, -9), (3, -3), (9, -2), (4, 2), (6, 9), (0, 5), (-6, 9), (-4, 2), (-9, -2), (-3, -3))], fill=(255, 230, 60, 255)) for q in range(3)])

def burst(img, x, y, u, col, n=10, r0=20, r1=120):
    layer(img, lambda dd: [dd.rectangle([x + (r0 + r1 * u) * math.cos(q * 6.283 / n) - 6, y + (r0 + r1 * u) * math.sin(q * 6.283 / n) - 6,
                                         x + (r0 + r1 * u) * math.cos(q * 6.283 / n) + 6, y + (r0 + r1 * u) * math.sin(q * 6.283 / n) + 6], fill=col + (int(255 * (1 - u)),)) for q in range(n)])

class Pops:
    """pop labels that never overlap each other (stacked upward), clamped inside the safe zone."""
    def __init__(self, dur=1.1, xmin=70, xmax=1010, ymin=262):
        self.P = []; self.dur = dur; self.xmin, self.xmax, self.ymin = xmin, xmax, ymin
    def add(self, t0, x, y, text, col, size=36): self.P.append((t0, x, y, text, col, size))
    def items(self, t, avoid=()):
        act = [p for p in sorted(self.P, key=lambda p: p[0]) if 0 <= t - p[0] < self.dur]; placed = list(avoid); out = []
        for t0, x, y, text, col, size in act:
            u = t - t0; sy = y - u * 30; w = len(text) * size + 20; hh = size + 16
            xmax = self.xmax if sy < 1110 else min(self.xmax, 880)
            sx = min(max(x, self.xmin + w / 2), xmax - w / 2)
            for _ in range(10):
                if any(abs(sx - px) < (w + pw) / 2 and abs(sy - py) < (hh + ph) / 2 for px, py, pw, ph in placed): sy -= hh + 4
                else: break
            sy = max(sy, self.ymin + hh / 2)
            placed.append((sx, sy, w, hh)); al = int(255 * min(1, (self.dur - u) / 0.3)); sc = 1 + 0.3 * max(0, 1 - u / 0.15)
            out.append((sx, sy - hh / 2, text, int(size * sc), col, 6, al))
        return out

def strong_aura(img, spr, x0, y0, t, r1=9, r2=5):
    """bright two-tone creatine aura that reads on any background (also blue water)."""
    pu = 0.5 + 0.5 * math.sin(t * 14)
    tt = tinted(spr, (200, 235, 255), int(190 + 65 * pu))
    for k_ in range(12):
        a_ = k_ * math.pi / 6; img.alpha_composite(tt, (int(x0 + r1 * math.cos(a_)), int(y0 + r1 * math.sin(a_))))
    tt = tinted(spr, (60, 130, 255), 255)
    for k_ in range(8):
        a_ = k_ * math.pi / 4; img.alpha_composite(tt, (int(x0 + r2 * math.cos(a_)), int(y0 + r2 * math.sin(a_))))
