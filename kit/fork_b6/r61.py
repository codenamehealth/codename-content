import sys; sys.path.insert(0, '../fork1'); from common import *
os.chdir(os.path.dirname(os.path.abspath(__file__)))
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
GUILD = {'joy': 'FOUNDATION', 'cleo': 'VITALITY', 'cyrus': 'ENERGY', 'ray': 'RECOVERY'}
COL = {'joy': (120, 200, 90), 'cleo': (110, 160, 255), 'cyrus': (255, 160, 50), 'ray': (205, 125, 245)}
DARK = {'joy': (74, 124, 58), 'cleo': (46, 93, 168), 'cyrus': (217, 122, 31), 'ray': (107, 45, 107)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel'}
REALM = {'joy': 'found_hd.gif', 'cleo': 'vit_hd.gif', 'cyrus': 'sun_hd.gif', 'ray': 'recov_hd.gif'}
PX0, PY0, PW, PH = 40, 400, 1000, 780
RB = {g: bg_frames(REALM[g], (PW, PH), box=(285, 0, 1635, 1080), step=2, bright=0.85) for g in G}
BIG = {g: idle(g, 7) for g in G}; SM = {g: idle(g, 3) for g in G}
GUMB = {g: gummy(GK[g], 3) for g in G}; GUMS = {g: gummy(GK[g], 2) for g in G}
BACK = bg_frames('hub.gif', (W, H), box=(656, 0, 1264, 1080), step=2, bright=0.35, blur=3)
HICON = idle('hollow', 2)
DUR = 11.0; N = int(DUR * FPS)
# cursor hops: slow to fast
hops = []; t = 1.2; gap = 0.62; rng = random.Random(11); cur = 0
while t < 8.6:
    hops.append((t, cur)); nxt = rng.choice([i for i in range(4) if i != cur]); cur = nxt
    t += gap; gap = max(0.075, gap * 0.86)
T_END = 8.7
ev = [(h[0], 'reeltick_8bit') for h in hops] + [(T_END, 'ding_8bit'), (0.3, 'whoosh_8bit')]
def hovered(t):
    c = None
    for ht, i in hops:
        if ht <= t: c = i
    return c
CX = [W / 2 + (i - 1.5) * 252 for i in range(4)]; CY0, CY1 = 1300, 1700
w = Writer('v61_noaudio.mp4')
for f in range(N):
    t = f / FPS; img = BACK[int(t * 6) % len(BACK)].copy()
    hv = hovered(t) if t < T_END else None
    # header
    layer(img, lambda d: d.rectangle([0, 90, W, 330], fill=(12, 10, 26, 210)))
    d = ImageDraw.Draw(img)
    ctext(d, W / 2, 125, 'IF YOU KNOW HIM,', F(50), (255, 255, 255), 6)
    ctext(d, W / 2, 200, 'WHICH GUIDE IS', F(50), (232, 182, 76), 6)
    ctext(d, W / 2, 265, 'HE CHOOSING?', F(50), (232, 182, 76), 6)
    # preview window
    if hv is not None:
        g = G[hv]; pv = RB[g][int(t * 6) % len(RB[g])].copy()
        img.paste(pv, (PX0, PY0))
        layer(img, lambda dd: dd.rectangle([PX0, PY0 + PH - 170, PX0 + PW, PY0 + PH], fill=(12, 10, 26, 190)))
        b = BIG[g][int(t * 6) % len(BIG[g])]
        hop_t = max(h for h, i in hops if h <= t); pop = min(1, (t - hop_t) / 0.12)
        if pop < 1: b = b.resize((max(1, int(b.width * (0.85 + 0.15 * pop))), max(1, int(b.height * (0.85 + 0.15 * pop)))), Image.NEAREST)
        img.alpha_composite(b, (int(W / 2 - b.width / 2), int(PY0 + PH - 168 - b.height * 546 / 644)))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2 - 80, PY0 + PH - 150, NAME[g], F(56), (255, 255, 255), 7)
        ctext(d, W / 2 - 80, PY0 + PH - 76, GUILD[g] + ' GUILD', F(30), COL[g], 5)
        gb = GUMB[g]; img.alpha_composite(gb, (int(PX0 + PW - 150 - gb.width / 2), int(PY0 + PH - 85 - gb.height / 2 + 6 * math.sin(t * 4))))
    else:
        layer(img, lambda dd: dd.rectangle([PX0, PY0, PX0 + PW, PY0 + PH], fill=(12, 10, 26, 200)))
        if t >= T_END:
            u = t - T_END
            for i, g in enumerate(G):
                sil = SM[g][int(t * 6) % 6]
                sil = sil.resize((int(sil.width * 1.6), int(sil.height * 1.6)), Image.NEAREST); a = sil.getchannel('A')
                s2 = Image.new('RGBA', sil.size, DARK[g] + (255,)); s2.putalpha(a)
                x = PX0 + PW * (i + 0.5) / 4; img.alpha_composite(s2, (int(x - s2.width / 2), int(PY0 + 560 - 234 * 2 * 0 - s2.height * 0.85)))
            d = ImageDraw.Draw(img)
            ctext(d, W / 2, PY0 + 600, 'WHO IS HE', F(62), (255, 255, 255), 7)
            ctext(d, W / 2, PY0 + 690, 'CHOOSING?', F(62), (232, 182, 76), 7)
    d = ImageDraw.Draw(img)
    d.rectangle([PX0, PY0, PX0 + PW, PY0 + PH], outline=(232, 182, 76), width=6)
    if t < 1.2:
        ctext(d, W / 2, PY0 + 330, 'SELECT', F(70), (255, 255, 255), 7); ctext(d, W / 2, PY0 + 430, 'YOUR GUIDE', F(56), (232, 182, 76), 7)
    # P2 tag with the Hollow
    layer(img, lambda dd: dd.rounded_rectangle([58, 418, 330, 474], 14, fill=(12, 10, 26, 210)))
    d = ImageDraw.Draw(img); d.text((84, 431), 'PLAYER 2', font=F(28), fill=(232, 182, 76))
    hi = HICON[int(t * 6) % 6]; img.alpha_composite(hi, (300, 474 - 156 + 40))
    # cards
    def cards(dd):
        for i, g in enumerate(G):
            x = CX[i]; dd.rounded_rectangle([x - 118, CY0, x + 118, CY1], 18, fill=DARK[g] + (150,))
    layer(img, cards); d = ImageDraw.Draw(img)
    for i, g in enumerate(G):
        x = CX[i]
        s = SM[g][int(t * 6 + i) % 6]; img.alpha_composite(s, (int(x - s.width / 2), CY0 + 300 - 234))
        gs = GUMS[g]; img.alpha_composite(gs, (int(x + 60 - gs.width / 2), CY0 + 20))
        d = ImageDraw.Draw(img)
        ctext(d, x, CY0 + 315, NAME[g], F(24 if g != 'ray' else 20), (255, 255, 255), 4)
        ctext(d, x, CY0 + 352, GUILD[g], F(16), COL[g], 3)
        d.rounded_rectangle([x - 118, CY0, x + 118, CY1], 18, outline=COL[g], width=4)
    if hv is not None:
        x = CX[hv]; pulse = 4 + int(3 * (math.sin(t * 20) + 1))
        d.rounded_rectangle([x - 128, CY0 - 10, x + 128, CY1 + 10], 22, outline=(255, 230, 120), width=pulse)
        tri_y = CY0 - 40 + int(6 * math.sin(t * 10))
        d.polygon([(x - 26, tri_y), (x + 26, tri_y), (x, tri_y + 26)], fill=(255, 230, 120), outline=(20, 15, 35))
        d.text((x - 22, tri_y - 40), 'P2', font=F(26), fill=(255, 230, 120), stroke_width=4, stroke_fill=(20, 15, 35))
    if t >= T_END:
        u = t - T_END; k = int(u * 6) % 4
        for i, g in enumerate(G):
            x = CX[i]; on = (int(u * 8) + i) % 2 == 0
            d.rounded_rectangle([x - 128, CY0 - 10, x + 128, CY1 + 10], 22, outline=(255, 230, 120) if on else COL[g], width=6)
        layer(img, lambda dd: dd.rounded_rectangle([90, 1740, 990, 1860], 24, fill=(12, 10, 26, 225)))
        d = ImageDraw.Draw(img); d.rounded_rectangle([90, 1740, 990, 1860], 24, outline=(232, 182, 76), width=5)
        ctext(d, W / 2, 1772, 'TAG HIM BELOW', F(52), (255, 255, 255), 6)
    w.write(img)
    if f in (20, 90, 200, 300): img.convert('RGB').save(f'k61_{f}.png')
w.close(); json.dump(ev, open('v61_ev.json', 'w')); print('hops', len(hops))
