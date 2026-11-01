# #61 If you know him: FULL REDO (Bennett: "silly as is; slowly go through the characters one at a time, slow deliberate reveal").
# Character-select screen kept (Hollow = PLAYER 2 doing the choosing), but the P2 selector now walks the 4 cards ONE AT A TIME:
# glide -> press -> the card flips and the big preview reveals that guide (silhouette -> flash -> full colour, name types in,
# guild line, gummy pops) -> hold ~1.7s -> next. Ends on all 4 guides + WHO IS HE CHOOSING? / TAG HIM BELOW, then the loop
# cuts back to the opening (selector on card 1, cards face down).
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
import numpy as np
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_fade
OUT = SP + 'fork_h1/'
HOOK, HB = hook_fade(['IF YOU KNOW HIM', 'YOU KNOW WHICH', "GUIDE HE'S CHOOSING"], accent=1)   # Oct 29: the post hook in a soft fade, no box
import sys as _hw; _hw.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h1'); from hookw import hook_fade_w
import os as _o; HOOK, HG = hook_fade_w(['IF YOU KNOW HIM', 'YOU KNOW HIS PICK'], ['PICK'], size=64, glyph_bottom=(None if _o.environ.get('TOP') else 460), fade_to=HB + 110); print('HB', HB, 'new hook', HG)
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
GUILD = {'joy': 'FOUNDATION', 'cleo': 'VITALITY', 'cyrus': 'ENERGY', 'ray': 'RECOVERY'}
COL = {'joy': (120, 200, 90), 'cleo': (110, 160, 255), 'cyrus': (255, 160, 50), 'ray': (205, 125, 245)}
DARK = {'joy': (74, 124, 58), 'cleo': (46, 93, 168), 'cyrus': (217, 122, 31), 'ray': (107, 45, 107)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel'}
REALM = {'joy': 'found_hd.gif', 'cleo': 'vit_hd.gif', 'cyrus': 'sun_hd.gif', 'ray': 'recov_hd.gif'}
# Oct 29 full-bleed: each realm fills the whole 1080x1920 frame (no preview panel over a blurred hub); the crop puts the realm's
# ground at the guide's feet (FEET). The cards sit on the scene as UI; TAG HIM BELOW plate cut.
PX0, PY0, PW, PH = 0, 0, W, H; FEET = 1100; NAMEY = FEET + 6   # name types in under the guide's feet (not under the hook, where it read as a 4th hook line)
def rbox(y0): w_ = int(round((1080 - y0) * W / H)); x0 = (1920 - w_) // 2; return (x0, y0, x0 + w_, 1080)
RY0 = {'joy': 0, 'cleo': 78, 'cyrus': 0, 'ray': 368}
RB = {g: bg_frames(REALM[g], (W, H), box=rbox(RY0[g]), step=2, bright=0.85) for g in G}
RBD = {g: [ImageEnhance.Brightness(f).enhance(0.28) for f in RB[g]] for g in G}
BIG = {g: idle(g, 7) for g in G}; SM = {g: idle(g, 3) for g in G}; END5 = {g: idle(g, 5) for g in G}
def tint(fr, col):
    s = Image.new('RGBA', fr.size, col + (255,)); s.putalpha(fr.getchannel('A')); return s
SIL = {g: [tint(f, tuple(int(c * 0.6) for c in DARK[g])) for f in BIG[g]] for g in G}   # guild-tinted silhouette (not a dark Hollow-like shape)
WHT = {g: [tint(f, (255, 255, 255)) for f in BIG[g]] for g in G}
GUMB = {g: gummy(GK[g], 3) for g in G}; GUMS = {g: gummy(GK[g], 2) for g in G}
BACK = bg_frames('hub.gif', (W, H), box=rbox(290), step=2, bright=0.85)   # end lineup stands in the village, sharp
hi = idle('hollow', 1)[0]; bb = hi.getbbox(); hc = (bb[0] + bb[2]) // 2
HFACE = up(hi.crop((hc - 16, 10, hc + 16, 42)), 3)            # Hollow portrait in the P2 tag (UI, not standing in the scene)
HFS = up(hi.crop((hc - 16, 10, hc + 16, 42)), 2)              # small portrait on the TAG HIM BELOW plate
# ---------------- timeline
STEP = 2.7; R = [0.2 + i * STEP for i in range(4)]             # reveal moments (same slow 2.7s per guide; first press already under way on frame 0)
GL = 0.55                                                      # selector glide
T_END = R[3] + 2.25; DUR = T_END + 1.4; N = int(round(DUR * FPS))
print('reveals', R, 'end panel', round(T_END, 2), 'dur', round(DUR, 2))
CW = 186; CX = [79 + CW / 2 + i * (CW + 18) for i in range(4)]; CY0, CY1 = 1220, 1494; CH_ = CY1 - CY0   # shorter cards (no 16-24px text) make room for TAG HIM BELOW
def ease(u): u = max(0, min(1, u)); return u * u * (3 - 2 * u)
def sel_x(t):
    x = CX[0]
    for i in range(1, 4):
        g0 = R[i] - 0.15 - GL
        if t >= g0: x = CX[i - 1] + (CX[i] - CX[i - 1]) * ease((t - g0) / GL)
    return x
def cur_guide(t):
    """index of the guide shown in the preview (the one being / just revealed)"""
    k = 0
    for i in range(1, 4):
        if t >= R[i] - 0.15 - GL: k = i
    return k
# ---------------- card art
def card_face(g, t):
    c = Image.new('RGBA', (CW, CH_), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, CW - 1, CH_ - 1], 18, fill=DARK[g] + (175,))
    s = SM[g][int(t * 6 + G.index(g)) % 6]; c.alpha_composite(s, (int(CW / 2 - s.width / 2), CH_ - 18 - 234))
    gs = GUMS[g]; c.alpha_composite(gs, (int(CW / 2 + 58 - gs.width / 2), 14))
    d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, CW - 1, CH_ - 1], 18, outline=COL[g], width=4)
    return c
def card_back(g, t, i):
    c = Image.new('RGBA', (CW, CH_), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle([0, 0, CW - 1, CH_ - 1], 18, fill=(26, 20, 40, 230), outline=(120, 110, 150), width=4)
    for k in range(5):
        d.rounded_rectangle([14 + k * 6, 14 + k * 6, CW - 15 - k * 6, CH_ - 15 - k * 6], 12, outline=(60, 50, 86), width=2)
    ctext(d, CW / 2, 95 + 6 * math.sin(t * 3 + i), '?', F(84), (232, 182, 76), 7)
    return c
# ---------------- render
rng = random.Random(61); MOTES = [(rng.uniform(80, 1000), rng.uniform(560, 1100), rng.uniform(0, 6.3)) for _ in range(22)]
ev = []
def evt(t, n):
    if t >= 0 and not any(abs(e[0] - t) < 0.01 and e[1] == n for e in ev): ev.append((round(t, 3), n))
for i in range(4):
    if i: evt(R[i] - 0.15 - GL, 'swish')
    evt(R[i] - 0.12, 'reeltick_8bit'); evt(R[i], 'twinkle'); evt(R[i] + 0.98, 'coin_8bit')
evt(T_END, 'ding_8bit'); evt(T_END + 0.1, 'cheer')
w = Writer(OUT + 'v61_noaudio.mp4')
for f in range(N):
    t = f / FPS; img = BACK[int(t * 6) % len(BACK)].copy()
    if t < T_END:
        k = cur_guide(t); g = G[k]; u = t - R[k]                 # u < 0: silhouette waiting, u >= 0: revealed
        fi = int(t * 6) % 6
        if u < 0:
            img.paste(RBD[g][int(t * 6) % len(RBD[g])], (PX0, PY0))
        else:
            a = ease(u / 0.35); pv = Image.blend(RBD[g][int(t * 6) % len(RBD[g])], RB[g][int(t * 6) % len(RB[g])], a); img.paste(pv, (PX0, PY0))
        cx_, cy_ = W / 2, FEET - 230
        if u >= 0:                                           # slow light rays in the guild colour behind the guide
            ra = int(70 * min(1, u / 0.3))
            def rays(dd):
                for q in range(12):
                    a0 = q * math.pi / 6 + t * 0.35
                    dd.polygon([(cx_, cy_), (cx_ + 900 * math.cos(a0 - 0.09), cy_ + 900 * math.sin(a0 - 0.09)), (cx_ + 900 * math.cos(a0 + 0.09), cy_ + 900 * math.sin(a0 + 0.09))], fill=COL[g] + (ra,))
            Lr = Image.new('RGBA', (W, H), (0, 0, 0, 0)); rays(ImageDraw.Draw(Lr))
            img.alpha_composite(Lr)
        # the guide
        if u < 0:
            b = SIL[g][fi]
        elif u < 0.12:
            b = WHT[g][fi]
        else:
            b = BIG[g][fi]
            if u < 0.4: b = Image.blend(WHT[g][fi], BIG[g][fi], ease((u - 0.12) / 0.28))
        sc = 1.0
        if 0 <= u < 0.25: sc = 1.0 + 0.06 * math.sin(u / 0.25 * math.pi)
        if sc != 1.0: b = b.resize((int(b.width * sc), int(b.height * sc)), Image.NEAREST)
        layer(img, lambda dd: dd.ellipse([W / 2 - 150, FEET - 22, W / 2 + 150, FEET + 10], fill=(0, 0, 0, 90)))
        img.alpha_composite(b, (int(W / 2 - b.width / 2), int(FEET - 546 * sc)))
        if u < 0:
            text_layer(img, [(W / 2, FEET - 330 + 8 * math.sin(t * 4), '?', 110, (232, 182, 76), 9, 255)])
        if 0 <= u < 0.7:                                     # reveal burst
            v = u / 0.7
            def burst(dd):
                for q in range(14):
                    a0 = q * math.pi / 7; r_ = 60 + 420 * v
                    x_, y_ = cx_ + r_ * math.cos(a0), cy_ + r_ * math.sin(a0) * 0.8
                    dd.rectangle([x_ - 9, y_ - 9, x_ + 9, y_ + 9], fill=(COL[g] if q % 2 else (255, 240, 180)) + (int(255 * (1 - v)),))
            Lb = Image.new('RGBA', (W, H), (0, 0, 0, 0)); burst(ImageDraw.Draw(Lb)); img.alpha_composite(Lb.crop((PX0, PY0, PX0 + PW, PY0 + PH)), (PX0, PY0))
        if u >= 0.3:                                         # floating motes
            layer(img, lambda dd: [dd.rectangle([x, y - (t * 30 + p * 40) % 200, x + 6, y + 6 - (t * 30 + p * 40) % 200], fill=COL[g] + (int(120 + 100 * math.sin(t * 3 + p)),)) for x, y, p in MOTES if y - (t * 30 + p * 40) % 200 > HB + 20])
        d = ImageDraw.Draw(img)
        # name band: name types in, then guild, then gummy
        # name types in above the guide's head (no band); the gummy pops beside it
        if u >= 0:
            nl = NAME[g][:max(0, min(len(NAME[g]), int((u - 0.35) / 0.07) + 1))] if u >= 0.35 else ''
            full_w = d.textlength(NAME[g], font=F(48))
            if nl:
                d.text((W / 2 - full_w / 2, NAMEY), nl, font=F(48), fill=(255, 255, 255), stroke_width=7, stroke_fill=(20, 15, 35))
            if u >= 0.98:
                p = min(1, (u - 0.98) / 0.18); gb = GUMB[g]
                if p < 1: gb = gb.resize((max(1, int(gb.width * (0.4 + 0.6 * p + 0.15 * math.sin(p * math.pi)))), max(1, int(gb.height * (0.4 + 0.6 * p + 0.15 * math.sin(p * math.pi))))), Image.NEAREST)
                img.alpha_composite(gb, (int(W / 2 + full_w / 2 + 60 - gb.width / 2), int(NAMEY + 24 - gb.height / 2 + 6 * math.sin(t * 4))))
        # PLAYER 2 tag (Hollow portrait = the player doing the choosing)
        TX, TYP = 84, HB + 40   # P2 tag: framed Hollow portrait + P2, no plate
        d = ImageDraw.Draw(img); d.rounded_rectangle([TX, TYP, TX + HFACE.width + 6, TYP + HFACE.height + 6], 10, fill=(40, 34, 60), outline=(232, 182, 76), width=4)
        img.alpha_composite(HFACE, (TX + 3, TYP + 3)); d = ImageDraw.Draw(img)
        d.text((TX + 118, TYP + 20), 'P2', font=F(60), fill=(232, 182, 76), stroke_width=6, stroke_fill=(10, 6, 18))
    else:
        # end panel: all four, who is he choosing?
        u = t - T_END
        # Oct 29: no dark panel, no WHO IS HE CHOOSING? (the hook asks); all four stand in the village
        floor = FEET
        for i, g in enumerate(G):
            hop = int(40 * math.sin(math.pi * min(1, max(0, (u - i * 0.08) / 0.3))))
            fr = END5[g][int(t * 6 + i) % 6]
            x = 70 + 940 * (i + 0.5) / 4
            layer(img, lambda dd: dd.ellipse([x - 90, floor - 14, x + 90, floor + 8], fill=(0, 0, 0, 110)))
            img.alpha_composite(fr, (int(x - fr.width / 2), int(floor - 390 - hop)))
    # cards
    for i, g in enumerate(G):
        x = CX[i]; ru = t - R[i]
        if t >= T_END or ru >= 0.15: c = card_face(g, t)
        elif ru < -0.15 or t < R[i] - 0.15: c = card_back(g, t, i)
        else: c = card_back(g, t, i) if ru < 0 else card_face(g, t)
        fx = 1.0
        if -0.15 <= ru < 0.15 and t < T_END: fx = max(0.04, abs(ru) / 0.15)
        press = 1.0
        if -0.25 <= ru < -0.05: press = 1 - 0.06 * math.sin((ru + 0.25) / 0.2 * math.pi)
        cw = max(2, int(CW * fx * press)); chh = int(CH_ * press)
        ci = c.resize((cw, chh), Image.NEAREST)
        img.alpha_composite(ci, (int(x - cw / 2), int(CY0 + (CH_ - chh) / 2)))
    d = ImageDraw.Draw(img)
    if t < T_END:
        x = sel_x(t); pulse = 5 + int(3 * (math.sin(t * 10) + 1))
        d.rounded_rectangle([x - CW / 2 - 7, CY0 - 7, x + CW / 2 + 7, CY1 + 7], 22, outline=(255, 230, 120), width=pulse)
        d.rounded_rectangle([x - CW / 2 + 2, CY0 - 40, x - CW / 2 + 112, CY0 + 20], 10, fill=(255, 230, 120), outline=(20, 15, 35), width=4)
        d.text((x - CW / 2 + 13, CY0 - 30), 'P2', font=F(44), fill=(20, 15, 35))
    else:
        u = t - T_END
        for i, g in enumerate(G):
            on = (int(u * 4) + i) % 4 == 0
            d.rounded_rectangle([CX[i] - CW / 2 - 6, CY0 - 6, CX[i] + CW / 2 + 6, CY1 + 6], 22, outline=(255, 230, 120) if on else COL[g], width=6)
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (0, 12, 20, 40, 75, 110, int((R[2] + 0.2) * FPS), int((T_END + 1) * FPS)): img.convert('RGB').save(OUT + f'k61_{f}.png')
w.close(); json.dump({'events': sorted(ev)}, open(OUT + 'v61_ev.json', 'w')); print('done', round(DUR, 2), len(ev))
