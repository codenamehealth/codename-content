import sys; sys.path.insert(0, '../fork1')
from common import *
K = 5; FOOTY = 78 * K
BG = bg_frames('vit_hd.gif', (W, H), box=(1205, 300, 1611, 1020), step=1)
RUN = seq(PL + 'maze/anim/hollow_srun', K)
BONK = seq('hollow_bonk', K)               # 12 frames (1..12)
BLOCK = seq('cleo_block', K)
CIDLE = idle('cleo', K)
GROUND = 1330
GUMS = [gummy(k, 1) for k in ('mush', 'acv', 'mel', 'cre')]
def put(img, spr, cx, foot=GROUND): img.alpha_composite(spr, (int(cx - spr.width / 2), int(foot - FOOTY)))
def box(img, name, text, n, col):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0, x1, y1 = 60, 1520, W - 60, 1790
    d.rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], fill=(0, 0, 0, 120))
    d.rectangle([x0, y0, x1, y1], fill=(16, 18, 44, 245), outline=(235, 235, 255, 255), width=6)
    d.rectangle([x0 + 10, y0 + 10, x1 - 10, y1 - 10], outline=(90, 100, 160, 255), width=3)
    tw = d.textlength(name, font=F(30)); d.rectangle([x1 - tw - 70, y0 - 40, x1 - 20, y0 + 6], fill=col + (255,), outline=(235, 235, 255, 255), width=4)
    d.text((x1 - tw - 45, y0 - 30), name, font=F(30), fill=(255, 255, 255))
    lines = text[:n].split('\n'); y = y0 + 50
    for ln in lines: d.text((x0 + 40, y), ln, font=F(44), fill=(255, 255, 255)); y += 70
    img.alpha_composite(L)
T_BLOCK, T_HIT = 0.95, 1.30
X_CLEO = 690; X_HIT = X_CLEO - 210
LINES = [(1.85, 'You need a pass.'), (3.55, '...Okay.\nThat one hurt.')]
TE = 5.9; NF = int(TE * FPS); wr = Writer('v40_noaudio.mp4'); ev = []
for f in range(NF):
    t = f / FPS; img = BG[int(t * 12) % len(BG)].copy()
    # Cleo
    if t < T_BLOCK: put(img, CIDLE[int(t * 8) % len(CIDLE)], X_CLEO)
    else:
        k = min(len(BLOCK) - 1, int((t - T_BLOCK) / 0.3 * len(BLOCK)))
        sh = 0
        if T_HIT <= t < T_HIT + 0.18: sh = int(8 * math.sin((t - T_HIT) * 90))
        put(img, BLOCK[k], X_CLEO + sh)
    # Hollow
    if t < T_HIT:
        x = -120 + (X_HIT + 120) * (t / T_HIT)
        put(img, RUN[int(t * 14) % len(RUN)], x)
    else:
        u = t - T_HIT; k = min(11, 8 + int(u / 0.11))
        x = X_HIT - min(1, u / 0.45) * 90
        spr = BONK[k]; put(img, spr, x)
        if u > 0.5:   # dazed: tiny gummies orbit his head
            for i, g in enumerate(GUMS):
                a = u * 4 + i * math.pi / 2; gx = x - 90 + 75 * math.cos(a); gy = GROUND - 175 + 20 * math.sin(a)
                img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    items = [(W / 2, 250, 'NPCs blocking', 50, (255, 255, 255), 7, 255), (W / 2, 320, 'the only path', 50, (255, 255, 255), 7, 255)]
    if T_HIT <= t < T_HIT + 0.7:
        a = int(255 * min(1, (T_HIT + 0.7 - t) / 0.3)); items.append((X_HIT + 40, GROUND - 360 - (t - T_HIT) * 80, 'BONK!', 60, (255, 220, 60), 8, a))
    text_layer(img, items)
    for i, (ts, txt) in enumerate(LINES):
        tend = LINES[i + 1][0] if i + 1 < len(LINES) else 99
        if ts <= t < tend:
            n = int((t - ts) * 32) + 1
            box(img, 'CLEO', txt, n, (46, 93, 168))
            if n <= len(txt) and int((t - ts) * 32) != int((t - ts - 1 / FPS) * 32) and int((t - ts) * 32) % 2 == 0: ev.append((round(t, 3), 'tick_8bit'))
    wr.write(img)
    if f % 15 == 0: img.convert('RGB').resize((270, 480)).save(f'prev/p40_{f:04d}.png')
wr.close()
ev += [(round(T_HIT, 3), 'boing'), (round(T_HIT + 0.02, 3), 'punch'), (round(T_HIT + 0.5, 3), 'twinkle')]
json.dump(ev, open('v40_ev.json', 'w')); print('done', len(ev))
