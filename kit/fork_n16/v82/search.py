import sys, collections, sim82 as S
print('GAPB', sorted(S.GAPB), [S.KMAX[b] for b in range(60)], flush=True)
c = collections.Counter()
for s in range(int(sys.argv[1]), int(sys.argv[2])):
    r = S.sim(s); c[r['fail']] += 1
    if not r['fail']:
        kp = S.place_king(r)
        print(s, round(r['esc'], 2), len(r['events']), sum(1 for g in r['gums'] if g['got']), r['post_contacts'], r.get('pending_at_esc'),
              kp and [round(v) for v in kp[1:]], max(b[1] for b in r['bricks']), [round(v) for v in r['esc_state'][2:]], flush=True)
print(c, flush=True)
