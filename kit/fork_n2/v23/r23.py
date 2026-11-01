# #23 Rank the guides -- review recut (fork_rc4). Approved video: legibility + universal fixes + gold hoard -> gummy pile.
import sys, math, json, random, os, glob
SP_ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/'
sys.path.insert(0, SP_ + 'fork1'); from common import *
sys.path.insert(0, SP_ + 'pixellab/safezone'); from hook import hook_fade
sys.path.insert(0, SP_ + 'fork_rc3'); from rc3 import acv_gummy_strong
os.chdir(os.path.dirname(os.path.abspath(__file__)))
PREVIEW = [float(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else None
# Oct 29 hookfade pass: boxed band + 'COMMENT YOUR RANKING' cut; soft fade; rows are edge-to-edge strips over the undimmed courtyard
HOOK, HB = hook_fade(['RANK THE', 'GUIDES'], accent=1, size=64)
print('HB', HB)
BG = bg_frames('bg_castle.gif', (W, H), box=(300, 0, 806, 900), step=1, bright=0.85, blur=0)   # crop moved left: Liza's background Hollow (peeked over the shelf) is out of frame
DRH = 262
DR = [Image.open(p).convert('RGBA') for p in sorted(glob.glob(SP_ + 'fork_rc4/v23/dragon/*.png'))]          # gold coins -> gummy pile (fork_c7/degold)
DR = [d.resize((int(d.width * DRH / d.height), DRH), Image.NEAREST) for d in DR]
K = 4
ROWA = int(os.environ.get('ROWA', '232'))   # review: tier rows darker (190 -> 232 alpha, ~91%; 215 still let the brick through) so the empty board reads; C and D were vanishing into the brick
# order + slots chosen so 44px names fit in two staggered rows inside x70-887
CH = [('cleo', 'CLEO', 'cre', 160, 0), ('cyrus', 'CYRUS', 'mush', 310, 1), ('ray', 'RAYLEIGH', 'mel', 462, 0), ('dragon', 'DRAGON', None, 636, 1), ('joy', 'JOY', 'acv', 800, 0)]
NCOL = {'joy': (90, 200, 80), 'cyrus': (255, 160, 40), 'cleo': (90, 150, 255), 'ray': (190, 90, 240), 'dragon': (235, 70, 60)}   # guide ring colours (RING); dragon in its own red
IDL = {g: idle(g, K) for g, *_ in CH if g != 'dragon'}
GM = {k: gummy(k, 2) for k in ('cre', 'mush', 'mel')}; GM['acv'] = up(acv_gummy_strong(), 2)
TIERS = [('S', (235, 70, 70)), ('A', (245, 150, 50)), ('B', (245, 210, 60)), ('C', (110, 200, 90)), ('D', (80, 150, 240))]
X0, X1 = 76, 880; RY0 = HB + 14; RH = 96; GAPR = 8           # rows end at x880 (clear of the lower-right buttons)
SHY = RY0 + 5 * (RH + GAPR) + 6; SHB = 1497; SX0, SX1 = 76, 881
FEET = SHB - 112
DUR = 6.0; T_OUT = DUR - 0.45
wr = None if PREVIEW else Writer('v23_noaudio.mp4'); events = []
rng = random.Random(4); SPK = [(rng.uniform(0, W), rng.uniform(0, H), rng.uniform(0, 6.28)) for _ in range(40)]
for i in range(5): events.append((round(0.02 + i * 0.07, 3), 'tick_8bit'))
for j in range(5): events.append((round(0.3 + j * 0.11, 3), 'coin_8bit'))
events.append((T_OUT, 'swish'))
HOP0, HOPDT = 1.25, 0.85        # idle beat: each candidate hops + its gummy pulses in turn (keeps the hold alive)
HOPORD = [2, 4, 0, 3, 1]
for f in ([int(round(x * FPS)) for x in PREVIEW] if PREVIEW else range(int(DUR * FPS))):
    t = f / FPS
    img = BG[int(t * 6) % len(BG)].copy()
    layer(img, lambda d: [d.rectangle([x - 2, y - 2 + 14 * math.sin(t + p), x + 2, y + 2 + 14 * math.sin(t + p)], fill=(255, 240, 190, int(120 + 100 * math.sin(t * 3 + p)))) for x, y, p in SPK])
    for i, (lt, col) in enumerate(TIERS):
        # frame 0: rows already half in (motion from frame 0); outro slides them back to half so the loop joins
        u = min(1, max(0, (t - i * 0.07) / 0.3)); ease = 0.5 + 0.5 * (1 - (1 - u) ** 3)
        if t >= T_OUT: v = min(1, max(0, (t - T_OUT - (4 - i) * 0.03) / 0.3)); ease = 1 - 0.5 * (v * v)
        off = int((1 - ease) * -W)
        y = RY0 + i * (RH + GAPR)
        def row(d, y=y, off=off, col=col):
            d.rectangle([off, y, W + off, y + RH], fill=(12, 9, 22, ROWA))
            d.rounded_rectangle([X0 + off + 8, y + 8, X0 + off + 8 + RH - 16, y + RH - 8], 12, fill=col + (255,), outline=(20, 15, 35, 255), width=4)
            for k in range(5): d.rectangle([X0 + off + RH + 12 + k * 140, y + 14, X0 + off + RH + 12 + k * 140 + 128, y + RH - 14], outline=(110, 100, 140, 170), width=2)
        layer(img, row)
        text_layer(img, [(X0 + off + 8 + (RH - 16) / 2, y + 18, lt, 60, (255, 255, 255), 7, 255)])
    # (shelf panel removed: the candidates stand on the courtyard dirt; soft ground shadows instead)
    names = []
    for j, (g, nm, gk, cx, nrow) in enumerate(CH):
        u = min(1, max(0, (t - 0.3 - j * 0.11) / 0.22))
        if t >= T_OUT: u = min(u, max(0, 1 - (t - T_OUT - 0.05 - j * 0.04) / 0.22))
        if u <= 0: continue
        sc = 0.4 + 0.6 * u
        hop = 0; pulse = 1.0
        if HOP0 <= t < T_OUT:
            n = int((t - HOP0) / HOPDT); ph = (t - HOP0) - n * HOPDT
            if n < len(HOPORD) and HOPORD[n] == j and ph < 0.36:
                hop = int(34 * math.sin(math.pi * ph / 0.36)); pulse = 1.0 + 0.5 * math.sin(math.pi * ph / 0.36)
        if g == 'dragon': s = DR[int(t * 8) % len(DR)]
        else: s = IDL[g][int(t * 8 + j) % len(IDL[g])]
        if sc < 1: s = up(s, sc)
        layer(img, lambda d, cx=cx, u=u: d.ellipse([cx - 62 * u, FEET - 12, cx + 62 * u, FEET + 10], fill=(0, 0, 0, int(80 * u))))
        if g == 'dragon': img.alpha_composite(s, (int(cx - s.width / 2), int(FEET + 26 - s.height * 1.0) - hop))
        else: img.alpha_composite(s, (int(cx - s.width / 2), int(FEET - 78 * K * sc) - hop))
        if gk and u >= 1:
            gg = GM[gk]
            if pulse > 1: gg = gg.resize((int(gg.width * pulse), int(gg.height * pulse)), Image.NEAREST)
            bob = int(5 * math.sin(t * 4 + j)); gy = FEET - 64 * K - 66 - hop
            img.alpha_composite(gg, (int(cx - gg.width / 2), int(gy + bob - (gg.height - GM[gk].height) / 2)))
        names.append((cx, FEET + 10 + nrow * 48, nm, 36, NCOL[g], 5, int(255 * u)))   # Oct 29 notes: each name in its guide's ring colour, smaller (44 -> 36px)
    text_layer(img, names)
    img.alpha_composite(HOOK)
    if PREVIEW: img.convert('RGB').save(f'p_{f:03d}.png')
    else: wr.write(img)
if not PREVIEW:
    wr.close(); json.dump({'events': events}, open('v23_events.json', 'w')); print('done')
