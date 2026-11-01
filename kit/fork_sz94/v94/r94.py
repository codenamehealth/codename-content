# #94 He does not run: recast. The Hollow is the silent player (emotes only); Cyrus is the escort NPC who does not run (cape joke + all dialogue).
import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_a7')
from common7 import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
HOOK, HB = hook_layer(['HE DOES', 'NOT RUN'], accent=1, sub='EVERY ESCORT MISSION EVER'); print('hook bottom', HB)
K = 5
def g92(name):
    im = Image.open(A + name); fr = []
    for i in range(im.n_frames): im.seek(i); fr.append(im.convert('RGBA').resize((92, 92), Image.NEAREST))
    return fr
H_IDLE = g92('idle_9.gif'); H_WALK = g92('hollow-walk-side.gif'); C_IDLE = idle('cyrus', 1); C_WALK = g92('cyrus-walk-side.gif')
RED, RED2, GOLD = (178, 36, 48, 255), (120, 20, 34, 255), (240, 196, 70, 255)
def cape_front(t):
    c = Image.new('RGBA', (92, 92), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    w = [int(2 * math.sin(t * 9 + k)) for k in range(4)]
    d.polygon([(36, 35), (56, 35), (65 + w[0], 74), (57, 77 + w[1]), (46, 75 + w[2]), (35, 77 + w[3]), (27 - w[0], 74)], fill=RED)
    d.line([(46, 40), (46, 74)], fill=RED2, width=2); d.line([(40, 40), (32, 73)], fill=RED2, width=1); d.line([(52, 40), (60, 73)], fill=RED2, width=1)
    return c
def cape_side(t, strength=1.0):
    c = Image.new('RGBA', (92, 92), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    f = [int(strength * 3 * math.sin(t * 11 + k * 1.3)) for k in range(4)]
    d.polygon([(41, 34), (47, 35), (44, 52), (40 + f[0], 66), (32 + f[1], 75), (22 + f[2], 71), (27 + f[3], 58), (35, 43)], fill=RED)
    d.line([(41, 39), (30 + f[1], 71)], fill=RED2, width=2)
    return c
def with_cape(spr, cape, clasp=None):
    o = Image.new('RGBA', (92, 92), (0, 0, 0, 0)); o.alpha_composite(cape); o.alpha_composite(spr)
    if clasp: ImageDraw.Draw(o).rectangle([clasp[0], clasp[1], clasp[0] + 2, clasp[1] + 1], fill=GOLD)
    return up(o, K)
GROUND = 1120
# Liza forest re-cropped (scale 2.3) so the grass in front of the door sits at GROUND (src y 731)
BG = bg_frames('found_hd.gif', (W, H), box=(370, 731 - int(GROUND / 2.3), 370 + 470, 731 - int(GROUND / 2.3) + 835), step=1)
FACE_C = C_IDLE[0].crop((28, 10, 64, 46))
LINES = [(0.25, 1.35, 'QUEST', 'Escort Cyrus.'), (1.45, 2.55, 'CYRUS', "I don't run."), (2.65, 3.75, 'CYRUS', 'I have a cape.'), (4.15, 5.9, 'CYRUS', '...Wait for me.')]
DUR = 6.2; T_GO = 3.85
BX0, BX1, BY0, BY1 = 72, 882, 1170, 1410
def emote(img, x, ytop, kind, t0, t):
    u = t - t0; pop = min(1.0, u / 0.12); yy = ytop - 20 * (1 - pop)
    if kind == 'drop':
        def dr(d):
            cx, cy = x + 70, yy + 40
            d.polygon([(cx, cy - 34), (cx - 18, cy), (cx + 18, cy)], fill=(120, 200, 255, 255)); d.ellipse([cx - 18, cy - 16, cx + 18, cy + 20], fill=(120, 200, 255, 255))
            d.rectangle([cx - 8, cy - 6, cx - 2, cy + 4], fill=(230, 245, 255, 255))
        layer(img, dr)
    else:
        text_layer(img, [(x, yy, kind, 72, (255, 214, 60) if kind == '!' else (255, 255, 255), 8, 255)])
out = Writer('noaudio.mp4'); ev = []
for f in range(int(DUR * FPS)):
    t = f / FPS
    img = BG[int(t * 8) % len(BG)].copy()
    # the Hollow (player): eager, then sprints off to the right
    if t < T_GO:
        hx = 660; hop = int(abs(math.sin(t * 12)) * 26) if 0.25 <= t < 1.35 else 0
        hs = up(H_IDLE[int(t * 6) % len(H_IDLE)], K); hy = GROUND - 78 * K - hop
    else:
        u = t - T_GO; hx = 660 + 1100 * u; hs = up(H_WALK[int(u * 18) % len(H_WALK)], K); hy = GROUND - 79 * K - int(abs(math.sin(u * 18)) * 10)
    # Cyrus (escort NPC) with the cape
    if t < T_GO + 0.3:
        cx = 300; cs = with_cape(C_IDLE[int(t * 6) % len(C_IDLE)], cape_front(t * (2.2 if 2.65 <= t < 3.75 else 1.0)), (45, 37))
        cy = GROUND - 78 * K
    else:
        u = t - T_GO - 0.3; cx = 300 + 40 * u; cs = with_cape(C_WALK[int(u * 4) % len(C_WALK)], cape_side(t, 0.6)); cy = GROUND - 79 * K
    def fx(d):
        if 2.65 <= t < 3.75:
            for k in range(5):
                ph = (t * 3 + k * 0.2) % 1.0; y = GROUND - 270 + k * 36; x = cx - 260 + ph * 180
                d.line([(x, y), (x + 80, y)], fill=(255, 255, 255, int(200 * (1 - ph))), width=5)
            for k in range(6):
                a = t * 4 + k; d.rectangle([cx + 130 * math.cos(a) - 5, GROUND - 230 + 70 * math.sin(a) - 5, cx + 130 * math.cos(a) + 5, GROUND - 230 + 70 * math.sin(a) + 5], fill=(255, 230, 120, 220))
        if t >= T_GO:
            for k in range(8):
                u = t - T_GO - k * 0.06
                if 0 <= u < 0.7:
                    px = 660 + 1100 * (k * 0.06); r = 16 + u * 70
                    d.ellipse([px - r, GROUND - 20 - r * 0.6, px + r, GROUND - 20 + r * 0.6], fill=(220, 200, 160, int(170 * (1 - u / 0.7))))
            u = t - T_GO
            if u < 0.9:
                for k in range(5):
                    y = GROUND - 300 + k * 55; x = 660 + 1100 * u - 160 - (k % 2) * 60
                    d.line([(x - 140, y), (x, y)], fill=(255, 255, 255, int(220 * (1 - u / 0.9))), width=6)
    layer(img, fx)
    img.alpha_composite(cs, (int(cx - cs.width / 2), cy))
    if hx < W + 300: img.alpha_composite(hs, (int(hx - hs.width / 2), hy))
    # Hollow emotes only (he never talks)
    htop = GROUND - 78 * K + 14 * K - 110
    if 0.25 <= t < 1.4: emote(img, hx, htop, '!', 0.25, t)
    elif 1.6 <= t < 2.6: emote(img, hx, htop, '?', 1.6, t)
    elif 2.9 <= t < 3.85: emote(img, hx - 60, htop + 30, 'drop', 2.9, t)
    # dialogue box
    cur = [l for l in LINES if l[0] <= t < l[1]]
    layer(img, lambda d: d.rectangle([BX0, BY0, BX1, BY1], fill=(14, 16, 48, 235)))
    d = ImageDraw.Draw(img)
    d.rectangle([BX0, BY0, BX1, BY1], outline=(240, 236, 220), width=6); d.rectangle([BX0 + 10, BY0 + 10, BX1 - 10, BY1 - 10], outline=(70, 80, 140), width=3)
    if cur:
        t0, t1, who, txt = cur[0]
        n = min(len(txt), int((t - t0) * 24) + 1); shown = txt[:n]
        fx0, fy0 = BX0 + 26, BY0 + 40
        d.rectangle([fx0, fy0, fx0 + 152, fy0 + 152], fill=(40, 44, 90), outline=(240, 196, 70), width=4)
        if who == 'CYRUS': img.alpha_composite(up(FACE_C, 4), (fx0 + 4, fy0 + 4))
        else: text_layer(img, [(fx0 + 78, fy0 + 36, '!', 80, (255, 214, 60), 8, 255)])
        d = ImageDraw.Draw(img)
        d.text((BX0 + 200, BY0 + 96), shown, font=F(40), fill=(255, 214, 60) if who == 'QUEST' else (255, 255, 255))
        tw = d.textlength(who, font=F(28)); d.rectangle([BX1 - 20 - tw - 30, BY0 - 44, BX1 - 20, BY0 + 6], fill=(14, 16, 48), outline=(240, 196, 70), width=4)
        d.text((BX1 - 20 - tw - 15, BY0 - 32), who, font=F(28), fill=(255, 214, 60))
        if n == len(txt) and int(t * 3) % 2: d.polygon([(BX1 - 50, BY1 - 44), (BX1 - 20, BY1 - 44), (BX1 - 35, BY1 - 26)], fill=(255, 214, 60))
        if abs(t - t0) < 0.5 / FPS: ev.append((round(t0, 3), 'tick_8bit'))
    if abs(t - T_GO) < 0.5 / FPS: ev.append((T_GO, 'whoosh_8bit'))
    if abs(t - 2.65) < 0.5 / FPS: ev.append((2.65, 'twinkle'))
    img.alpha_composite(HOOK)
    out.write(img)
out.close(); json.dump(ev, open('ev.json', 'w')); print('ok', ev)
