import sys
src = open('/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1/race/render_race3.py').read().split('#### ---- v2 render follows')[0]
__file__ = '/tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/fork_rc1/race/render_race3.py'
exec(src)
for sd in map(int, sys.argv[1:]):
    st, tl = run_sim(sd); ch = st['cyrus']['sneak']; cf = st['cyrus']['fin']; rf = st['ray']['fin']
    A = 6.6 + (ch - 0.6 - 11.2) / 2.6; fo = A + 1.4 + (cf - ch - 0.8) / 1.4
    print(sd, 'sneak', round(ch, 2), 'cfin', round(cf, 2), 'rfin', round(rf, 2), 'A', round(A, 2), 'finO', round(fo, 2), 'joy/cleo x at land', round(tl[int(T_LAND*FPS)]['joy'][0]), round(tl[int(T_LAND*FPS)]['cleo'][0]))
