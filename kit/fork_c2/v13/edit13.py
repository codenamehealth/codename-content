p='r13.py'; s=open(p).read()
NEW_HEAD = '''K = 8
_SRC = Image.open(S0 + 'forkA/assets/slot_pick.png').convert('RGBA')
# split the lever (arm + ball head) off the cabinet so it can be pulled
_body = _SRC.copy(); _lev = Image.new('RGBA', _SRC.size, (0, 0, 0, 0))
for y in range(0, 74):
    for x in range(88, 112):
        px = _SRC.getpixel((x, y))
        if px[3]: _lev.putpixel((x, y), px); _body.putpixel((x, y), (0, 0, 0, 0))
HEAD = _lev.crop((0, 0, 112, 57)); STICK = _lev.crop((0, 57, 112, 74))
CAB = up(_body, K)
def lever_img(sy):
    # sy 1 = up, smaller = pulled toward the viewer (stick foreshortened, head rides down with it)
    L = Image.new('RGBA', _SRC.size, (0, 0, 0, 0))
    sh = max(1, round(STICK.height * sy)); st = STICK.resize((112, sh), Image.NEAREST)
    top = 74 - sh; L.alpha_composite(st, (0, top)); L.alpha_composite(HEAD, (0, top - 57))
    return up(L, K)
LEVS = {}
def lever_at(t):
    T0, T1, T2, T3 = 0.10, 0.33, 0.45, 0.85
    if t < T0 or t >= T3: sy = 1.0
    elif t < T1: u = (t - T0) / (T1 - T0); sy = 1 - 0.94 * u * u
    elif t < T2: sy = 0.06
    else: u = (t - T2) / (T3 - T2); sy = 0.06 + 0.94 * (1 - (1 - u) ** 2)
    sy = round(sy * 17) / 17
    if sy not in LEVS: LEVS[sy] = lever_img(sy)
    return LEVS[sy], sy
SPIN0 = int(0.33 * FPS)   # reels start when the lever bottoms out
CX0, CY0 = 100, 455   # 8x cabinet (was 7x): reels y831-1047; turret spires tuck under the hook band, base plinth runs 43px past y1500; lever/hub stay out of the lower-right notch'''
rep=[
("""K = 7
CAB = up(Image.open(S0 + 'forkA/assets/slot_pick.png').convert('RGBA'), K)
CX0, CY0 = 90, 1500 - 136 * 7   # 7x cabinet: base ends at y1500, right edge x874 clears the notch; turret tips tuck under the hook band""", NEW_HEAD),
("SYM = [face(n, 48) for n in ['joy', 'cyrus', 'cleo', 'ray', 'hollow']] + [up(Image.open(P + f'gummies/pick_{k}.png').convert('RGBA'), 3)",
 "SYM = [face(n, 56) for n in ['joy', 'cyrus', 'cleo', 'ray', 'hollow']] + [up(Image.open(P + f'gummies/pick_{k}.png').convert('RGBA'), 4)"),
("'slot_v2_noaudio.mp4'","'v13_noaudio.mp4'"),("'slot_v2_events.json'","'v13_events.json'"),
("""    img.alpha_composite(CAB, (CX0, CY0))
    s = seq[f]""","""    img.alpha_composite(CAB, (CX0, CY0))
    LV, lsy = lever_at(t); img.alpha_composite(LV, (CX0, CY0))
    if 0.10 <= t < 0.36:   # motion streaks above the ball on the down stroke
        def streak(dd):
            by = CY0 + (74 - round(17 * lsy) - 57 + 36) * K
            for k, dx in enumerate((-30, 0, 30)):
                dd.rectangle([CX0 + 103 * K + dx - 4, by - 120 + k * 14, CX0 + 103 * K + dx + 4, by - 30], fill=(255, 245, 210, 200))
        layer(img, streak)
    s = seq[f] if f >= SPIN0 else seq[0]"""),
("        spinning = f < STOP[r]","        spinning = SPIN0 <= f < STOP[r]"),
("gs, oy in ((prv, -120), (nxt, 120))","gs, oy in ((prv, -140), (nxt, 140))"),
("pd.rounded_rectangle([CX0 + 32, 1150, CX0 + 752, 1390], 24,","pd.rounded_rectangle([CX0 + 4, 1160, CX0 + 684, 1400], 24,"),
("ctext(pd, CX0 + 392, 1185, 'SO CLOSE!'","ctext(pd, CX0 + 344, 1195, 'SO CLOSE!'"),
("ctext(pd, CX0 + 392, 1290, 'Did you catch it?'","ctext(pd, CX0 + 344, 1300, 'Did you catch it?'"),
("img.convert('RGB').resize((360, 640)).save(f'mv_{f - MATCH:+d}.png')","img.convert('RGB').save(f'prev/mv_{f - MATCH:+d}.png')"),
]
for a,b in rep:
    assert s.count(a)==1,a; s=s.replace(a,b)
open(p,'w').write(s)
