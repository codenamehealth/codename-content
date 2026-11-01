import sys
p='r19.py'; s=open(p).read()
def rep(a,b):
    global s
    assert s.count(a)==1, a[:60]; s=s.replace(a,b)
rep("D19 = SP + 'fork_hf1/v19/'", "D19 = SP + 'fork_n3/v19/'")
rep("IDLE = idle('joy', K)\n", """IDLE = idle('joy', K)
# Oct 29 (Bennett #19): the top Joy meets a different disaster each run. Existing PixelLab assets only:
# joy_ko tumble (pixellab/king/joy_ko, same 64px body as the run cycle), King Slime (pixellab/king/king_idle + king_land, 3x),
# landing dust (king/dust_cands/00), floor spikes (pixellab/plat/spike_cands/04, spike rows only, 5x).
def _ko(p):
    im = Image.open(p).convert('RGBA'); return up(im, K), im.getbbox()[3] * K
KO = [_ko(p) for p in sorted(glob.glob(PL + 'king/joy_ko/*.png'))]
KS = 3
KIDLE = seq(PL + 'king/king_idle', KS, 0); KLAND = seq(PL + 'king/king_land', KS, 0)
DUST = crop(Image.open(PL + 'king/dust_cands/00.png').convert('RGBA'))
_sp = Image.open(PL + 'plat/spike_cands/04.png').convert('RGBA').crop((20, 9, 84, 31)); SPK = up(_sp, 5)
""")
rep("""CYC = [(0.0, 2.2, 1.0), (3.6, 1.7, 0.8), (6.6, 1.7, 0.8)]
T_MISS = CYC[0][0] + CYC[0][1] + 0.35   # as she drops into the pit
""", """# Oct 29: three different disasters (was the same cliff fall three times), no MISSED! stamp. Each ends with Joy popping back in at the start.
# A cliff: run 0-2.1s, off the edge, fall to 3.0, pop in 3.0
# B King Slime: run from 3.4, he drops in front of her at 3.95 (squish, shake), roars at 4.42: the roar blasts her back
#   (tumble, flat on her back 4.95, stars) and he slurps up the loot gummy; he hops off at 5.5; poof 5.9, pop in 5.95
# C spikes: run from 6.25, spikes shoot up at 6.72 right in front of her, she runs into them at 6.9 and is flung backwards in a
#   spinning arc under the title band, lands flat at 7.45 (dust, stars); poof 9.0, pop in 9.05 (ends in the frame-0 pose for the loop)
TA_RT, TA_FT = 2.1, 0.9
TB0, TB_LAND, TB_ROAR, TB_FLAT, TB_HOP, TB_POOF = 3.4, 3.95, 4.42, 4.95, 5.5, 5.9
TC0, TC_SPK, TC_HIT, TC_FLAT, TC_POOF = 6.25, 6.72, 6.9, 7.45, 9.0
SPEED = 330.0; KX = 630; KBOT = GL1 + 14; SX0 = 420
""")
rep("""for (c, rt, ft) in CYC:
    events += [(c + rt, 'jump'), (c + rt + 0.3, 'whoosh_8bit'), (c + rt + ft + 0.05, 'poof')]
events += [(T_MISS, 'buzz_8bit'), """, """events += [(TA_RT, 'jump'), (TA_RT + 0.3, 'whoosh_8bit'), (TA_RT + TA_FT + 0.05, 'poof'),
           (TB_LAND - 0.3, 'whoosh_8bit'), (TB_LAND, 'boom'), (TB_ROAR, 'punch'), (TB_FLAT, 'stomp_8bit'), (TB_HOP, 'jump'), (TB_POOF, 'poof'),
           (TC_SPK, 'sword_shing'), (TC_HIT, 'boing'), (TC_FLAT, 'stomp_8bit'), (TC_POOF, 'poof'),
           """)
a = s.index("    c0 = max([c for c in CYC"); b = s.index("    # ---------- panel 2: plant the tree")
s = s[:a] + open('top.py.txt').read() + s[b:]
a = s.index("    if T_MISS <= t < T_MISS + 0.85:"); b = s.index("    img.alpha_composite(HOOK)")
s = s[:a] + s[b:]
open(p,'w').write(s)
