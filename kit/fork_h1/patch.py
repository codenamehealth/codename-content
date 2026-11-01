import re
P = "import sys as _hw; _hw.path.insert(0, '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h1'); from hookw import hook_fade_w\n"
def sub(fn, old, new, count=1):
    s = open(fn).read(); assert s.count(old) == count, (fn, old, s.count(old)); s = s.replace(old, new); open(fn, 'w').write(s)
OLDS = 'fork_hfg1/v15/'
# 009
sub('r9.py', "END_HOOK, EHB = hook_fade(", P + "HOOK, HG = hook_fade_w(['WHERE WOULD', 'YOU LIVE?'], ['LIVE?'], size=68, fade_to=HB + 110); print('new hook', HG)   # fork_h1 Oct 29: hook text only\nEND_HOOK, EHB = hook_fade(")
# 015
sub('r15.py', "OUTD = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_hfg1/v15/'", "OUTD = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_h1/'")
sub('r15.py', "HOOK, HB = hook_fade(['PICK A GUIDE'], accent=0, size=80)\n", "HOOK, HB = hook_fade(['PICK A GUIDE'], accent=0, size=80)\n" + P + "HOOK, HG = hook_fade_w(['WHO ESCAPES', 'THE MAZE?'], ['MAZE?'], size=56, y=262, lh_k=1.2, fade_to=HB + 110); print('new hook', HG)   # fork_h1: 2 lines above the status icons (HB unchanged)\n")
# 032
sub('r32.py', "HB -= 6; print('hook bottom', HB)", "HB -= 6; print('hook bottom', HB)\n" + P + "HOOK, HG = hook_fade_w([\"WHAT'S BEHIND\", 'THE GLASS?'], ['GLASS?'], size=64, glyph_bottom=425, fade_to=554, strength=215); print('new hook', HG)")
# 035
sub('r35.py', "text_layer(HOOK, [(W / 2, HB0 + 4, 'BEFORE THE DARK RISES', 44, (215, 180, 255), 7, 255)])\n", P + "HOOK, HG = hook_fade_w(['WHO OUTRUNS', 'THE DARK?'], ['DARK?'], size=72, glyph_bottom=HB0 + 4 + 44, fade_to=HB0 + 170); print('new hook', HG)   # fork_h1: replaces PICK A GUIDE + sub, same bottom\n")
# 061
sub('r61.py', "print('HB', HB)", P + "import os as _o; HOOK, HG = hook_fade_w(['IF YOU KNOW HIM', 'YOU KNOW HIS PICK'], ['PICK'], size=64, glyph_bottom=(None if _o.environ.get('TOP') else 460), fade_to=HB + 110); print('HB', HB, 'new hook', HG)")
sub('r61.py', "OUT = SP + 'fork_hfg6/v61/'", "OUT = SP + 'fork_h1/'")
# 070
sub('r70.py', "HOOK_B, _ = hook_fade(['WHAT DID', 'YOU GET?'], accent=1)", "HOOK_B, _ = hook_fade(['WHAT DID', 'YOU GET?'], accent=1)\n" + P + "HOOK_A, HG = hook_fade_w(['WHICH CART', 'GETS SLIMED?'], ['SLIMED?'], size=64, fade_to=HB + 110)\nHOOK_B, HGB = hook_fade_w(['DID YOU', 'CALL IT?'], ['CALL', 'IT?'], size=64, fade_to=HB + 110); print('new hook', HG, HGB)")
# 076
sub('r76.py', "text_layer(HOOK_A, [(W / 2, HBF + 12, 'FOLLOW CLEO', 52, (120, 170, 255), 7, 255)])\n", P + "HOOK_A, HG = hook_fade_w(['KEEP YOUR EYES', 'ON CLEO'], ['CLEO'], color=(120, 170, 255), size=64, y=286, fade_to=HBF + 200); print('new hook', HG)   # fork_h1: replaces REMEMBER / THE GUIDES + FOLLOW CLEO; same top as WHERE'S CLEO?\n")
# 096
sub('r96.py', "OUT = SP + 'fork_hfg10/v96/'", "OUT = SP + 'fork_h1/'")
sub('r96.py', "print('hook bottom', HB);", P + "HOOK, HG = hook_fade_w(['WHO DIGS UP', 'THE GUMMIES?'], ['GUMMIES?'], color=(255, 190, 80), size=72, fade_to=HB + 110); print('new hook', HG)\nprint('hook bottom', HB);")
print('ok')
