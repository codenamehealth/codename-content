# Oct 29 notes2 review fix (shared by #56 #59 #63 #80): planted hits.
# The attacker stops, stands planted (attack frame 0, facing the target) for PLANT s, then plays Syeda's 12-frame attack
# at its own pace; the hit lands on the impact frame. Total stop = PLANT + ANIM (~1.3 s).
PLANT, ANIM = 0.6, 0.7
ATK_D = PLANT + ANIM
IMPACT = {'joy': 2, 'cyrus': 2, 'cleo': 3, 'ray': 2}          # first frame where the vine / fist / sword / bolt is fully out
REACH = {'joy': 80, 'cyrus': 82, 'cleo': 37, 'ray': 84}       # native px from body centre at the impact frame (x scale for screen)

def hit_at(n): return PLANT + (IMPACT[n] + 0.5) / 12 * ANIM

def frame_idx(u, nframes=12):
    if u < PLANT: return 0
    return min(nframes - 1, int((u - PLANT) / ANIM * nframes))
