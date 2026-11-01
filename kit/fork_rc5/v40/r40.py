import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1')
from common import *
import os; os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SP + 'fork_rc1'); from hook2 import hook_layer2
HOOK, HB = hook_layer2(['NPCS BLOCKING', 'THE ONLY PATH'], accent=1, sub='Name a worse NPC'); print('HB', HB)
K = 7; FOOTY = 78 * K   # 5x -> 7x (1.4x)
BG = bg_frames('vit_hd.gif', (W, H), box=(1241, 448, 1575, 1043), step=1)
RUN = seq(PL + 'maze/anim/hollow_srun', K)
BONK = seq(SP + 'fork_a4/hollow_bonk', K)               # 12 frames (1..12)
BLOCK = seq(SP + 'fork_a4/cleo_block', K)
CIDLE = idle('cleo', K)
GROUND = 1130
GUMS = [gummy(k, 2) for k in ('mush', 'acv', 'mel', 'cre')]
def put(img, spr, cx, foot=GROUND): img.alpha_composite(spr, (int(cx - spr.width / 2), int(foot - FOOTY)))
def box(img, name, text, n, col):
    L = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    x0, y0, x1, y1 = 76, 1196, 880, 1466
    d.rectangle([x0 + 6, y0 + 6, x1 + 6, y1 + 6], fill=(0, 0, 0, 120))
    d.rectangle([x0, y0, x1, y1], fill=(16, 18, 44, 245), outline=(235, 235, 255, 255), width=6)
    d.rectangle([x0 + 10, y0 + 10, x1 - 10, y1 - 10], outline=(90, 100, 160, 255), width=3)
    tw = d.textlength(name, font=F(40)); d.rectangle([x1 - tw - 70, y0 - 52, x1 - 20, y0 + 6], fill=col + (255,), outline=(235, 235, 255, 255), width=4)
    d.text((x1 - tw - 45, y0 - 40), name, font=F(40), fill=(255, 255, 255))
    lines = text[:n].split('\n'); y = y0 + 50
    for ln in lines: d.text((x0 + 40, y), ln, font=F(48), fill=(255, 255, 255)); y += 74
    img.alpha_composite(L)
T_BLOCK, T_HIT = 0.95, 1.30
X_CLEO = 715; X_HIT = X_CLEO - 294
LINES = [(1.85, 'You need a pass.'), (3.55, '...Still need\na pass.')]   # Cleo's line, can't read as the Hollow talking
TE = 5.2; NF = int(TE * FPS); wr = Writer('v40_noaudio.mp4'); ev = []
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
        x = -40 + (X_HIT + 40) * (t / T_HIT)
        put(img, RUN[int(t * 14) % len(RUN)], x)
    else:
        u = t - T_HIT; k = min(11, 8 + int(u / 0.11))
        x = X_HIT - min(1, u / 0.45) * 110
        spr = BONK[k]; put(img, spr, x)
        if u > 0.5:   # dazed: tiny gummies orbit his head
            for i, g in enumerate(GUMS):
                a = u * 4 + i * math.pi / 2; gx = x - 100 + 100 * math.cos(a); gy = GROUND - 250 + 28 * math.sin(a)
                img.alpha_composite(g, (int(gx - g.width / 2), int(gy - g.height / 2)))
    items = []
    if T_HIT <= t < T_HIT + 0.7:
        a = int(255 * min(1, (T_HIT + 0.7 - t) / 0.3)); items.append((X_HIT + 60, GROUND - 470 - (t - T_HIT) * 80, 'BONK!', 84, (255, 220, 60), 10, a))
    text_layer(img, items)
    for i, (ts, txt) in enumerate(LINES):
        tend = LINES[i + 1][0] if i + 1 < len(LINES) else 99
        if ts <= t < tend:
            n = int((t - ts) * 32) + 1
            box(img, 'CLEO', txt, n, (46, 93, 168))
            if n <= len(txt) and int((t - ts) * 32) != int((t - ts - 1 / FPS) * 32) and int((t - ts) * 32) % 2 == 0: ev.append((round(t, 3), 'tick_8bit'))
    img.alpha_composite(HOOK)
    wr.write(img)
    if f in (20, 45, 70, 150): img.convert('RGB').save(f'prev/d40_{f:04d}.png')
wr.close()
ev += [(round(T_HIT, 3), 'boing'), (round(T_HIT + 0.02, 3), 'punch'), (round(T_HIT + 0.5, 3), 'twinkle')]
json.dump({'events': ev}, open('v40_ev.json', 'w')); print('done', len(ev))
