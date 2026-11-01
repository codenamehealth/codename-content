import sys; sys.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork1'); from common import *
sys.path.insert(0, SP + 'pixellab/safezone'); from hook import hook_layer
os.chdir(SP + 'fork_b6'); OUT = SP + 'fork_sz56/v61/'
HOOK, HB = hook_layer(['IF YOU KNOW HIM', 'YOU KNOW'], accent=1, sub="WHICH GUIDE HE'S CHOOSING")
print('HB', HB)
G = ['joy', 'cleo', 'cyrus', 'ray']
NAME = {'joy': 'JOY', 'cleo': 'CLEO', 'cyrus': 'CYRUS', 'ray': 'RAYLEIGH'}
GUILD = {'joy': 'FOUNDATION', 'cleo': 'VITALITY', 'cyrus': 'ENERGY', 'ray': 'RECOVERY'}
COL = {'joy': (120, 200, 90), 'cleo': (110, 160, 255), 'cyrus': (255, 160, 50), 'ray': (205, 125, 245)}
DARK = {'joy': (74, 124, 58), 'cleo': (46, 93, 168), 'cyrus': (217, 122, 31), 'ray': (107, 45, 107)}
GK = {'joy': 'acv', 'cleo': 'cre', 'cyrus': 'mush', 'ray': 'mel'}
REALM = {'joy': 'found_hd.gif', 'cleo': 'vit_hd.gif', 'cyrus': 'sun_hd.gif', 'ray': 'recov_hd.gif'}
PX0, PY0, PW, PH = 70, HB + 12, 940, 1108 - (HB + 12); BAND = 106
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
CW = 186; CX = [79 + CW / 2 + i * (CW + 18) for i in range(4)]; CY0, CY1 = 1126, 1488
w = Writer(OUT + 'v61_noaudio.mp4')
for f in range(N):
    t = f / FPS; img = BACK[int(t * 6) % len(BACK)].copy()
    hv = hovered(t) if t < T_END else None
    # preview window
    if hv is not None:
        g = G[hv]; pv = RB[g][int(t * 6) % len(RB[g])].copy()
        img.paste(pv, (PX0, PY0))
        layer(img, lambda dd: dd.rectangle([PX0, PY0 + PH - BAND, PX0 + PW, PY0 + PH], fill=(12, 10, 26, 190)))
        b = BIG[g][int(t * 6) % len(BIG[g])]
        hop_t = max(h for h, i in hops if h <= t); pop = min(1, (t - hop_t) / 0.12)
        if pop < 1: b = b.resize((max(1, int(b.width * (0.85 + 0.15 * pop))), max(1, int(b.height * (0.85 + 0.15 * pop)))), Image.NEAREST)
        img.alpha_composite(b, (int(W / 2 - b.width / 2), int(PY0 + PH - BAND + 4 - b.height * 546 / 644)))
        d = ImageDraw.Draw(img)
        ctext(d, W / 2 - 80, PY0 + PH - BAND + 10, NAME[g], F(48), (255, 255, 255), 7)
        ctext(d, W / 2 - 80, PY0 + PH - 38, GUILD[g] + ' GUILD', F(26), COL[g], 5)
        gb = GUMB[g]; img.alpha_composite(gb, (int(PX0 + PW - 110 - gb.width / 2), int(PY0 + PH - BAND / 2 - gb.height / 2 + 6 * math.sin(t * 4))))
    else:
        layer(img, lambda dd: dd.rectangle([PX0, PY0, PX0 + PW, PY0 + PH], fill=(12, 10, 26, 200)))
        if t >= T_END:
            u = t - T_END
            for i, g in enumerate(G):
                sil = SM[g][int(t * 6) % 6]
                sil = sil.resize((int(sil.width * 1.6), int(sil.height * 1.6)), Image.NEAREST); a = sil.getchannel('A')
                s2 = Image.new('RGBA', sil.size, DARK[g] + (255,)); s2.putalpha(a)
                x = PX0 + PW * (i + 0.5) / 4; img.alpha_composite(s2, (int(x - s2.width / 2), int(PY0 + 270 - s2.height * 0.85)))
            d = ImageDraw.Draw(img)
            ctext(d, W / 2, PY0 + 290, 'WHO IS HE', F(56), (255, 255, 255), 7)
            ctext(d, W / 2, PY0 + 368, 'CHOOSING?', F(56), (232, 182, 76), 7)
            ctext(d, W / 2, PY0 + 470, 'TAG HIM BELOW', F(40), (255, 255, 255), 6)
    d = ImageDraw.Draw(img)
    d.rectangle([PX0, PY0, PX0 + PW, PY0 + PH], outline=(232, 182, 76), width=6)
    if t < 1.2:
        ctext(d, W / 2, PY0 + 210, 'SELECT', F(70), (255, 255, 255), 7); ctext(d, W / 2, PY0 + 310, 'YOUR GUIDE', F(56), (232, 182, 76), 7)
    # P2 tag with the Hollow
    if t < T_END:
        layer(img, lambda dd: dd.rounded_rectangle([PX0 + 14, PY0 + 14, PX0 + 286, PY0 + 70], 14, fill=(12, 10, 26, 210)))
        d = ImageDraw.Draw(img); d.text((PX0 + 40, PY0 + 27), 'PLAYER 2', font=F(28), fill=(232, 182, 76))
        hi = HICON[int(t * 6) % 6]; img.alpha_composite(hi, (PX0 + 230, PY0 + 170 - 156))
    # cards
    def cards(dd):
        for i, g in enumerate(G):
            x = CX[i]; dd.rounded_rectangle([x - CW / 2, CY0, x + CW / 2, CY1], 18, fill=DARK[g] + (150,))
    layer(img, cards); d = ImageDraw.Draw(img)
    for i, g in enumerate(G):
        x = CX[i]
        s = SM[g][int(t * 6 + i) % 6]; img.alpha_composite(s, (int(x - s.width / 2), CY0 + 262 - 234))
        gs = GUMS[g]; img.alpha_composite(gs, (int(x + 56 - gs.width / 2), CY0 + 16))
        d = ImageDraw.Draw(img)
        ctext(d, x, CY0 + 278, NAME[g], F(24 if g != 'ray' else 18), (255, 255, 255), 4)
        ctext(d, x, CY0 + 318, GUILD[g], F(16), COL[g], 3)
        d.rounded_rectangle([x - CW / 2, CY0, x + CW / 2, CY1], 18, outline=COL[g], width=4)
    if hv is not None:
        x = CX[hv]; pulse = 4 + int(3 * (math.sin(t * 20) + 1))
        d.rounded_rectangle([x - CW / 2 - 6, CY0 - 6, x + CW / 2 + 6, CY1 + 6], 22, outline=(255, 230, 120), width=pulse)
        d.text((x - CW / 2 + 12, CY0 + 14), 'P2', font=F(26), fill=(255, 230, 120), stroke_width=4, stroke_fill=(20, 15, 35))
    if t >= T_END:
        u = t - T_END; k = int(u * 6) % 4
        for i, g in enumerate(G):
            x = CX[i]; on = (int(u * 8) + i) % 2 == 0
            d.rounded_rectangle([x - CW / 2 - 6, CY0 - 6, x + CW / 2 + 6, CY1 + 6], 22, outline=(255, 230, 120) if on else COL[g], width=6)
    img.alpha_composite(HOOK)
    w.write(img)
    if f in (20, 90, 200, 300): img.convert('RGB').save(OUT + f'k61_{f}.png')
w.close(); json.dump({'events': ev}, open(OUT + 'v61_ev.json', 'w')); print('hops', len(hops))
