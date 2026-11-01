Build review: n03_box_maze (19.8s)
Verdict: FIX FIRST (one must-fix)

✅ Keep doing
• Hook reads at frame 0: WHO ESCAPES THE SHADOW? plus a serpentine maze that matches the reference layout. Gates glow and boxes pop on every count (0.0, 0.67, 1.2, 1.87s).
• Wall breaks at 2.0 to 3.8s with debris resting on the floor. Each catch gets one OUT stamp plus the roster X/OUT tag on the same frame (Rayleigh 4.73s, Cleo 6.0s). Stamps never stack, and both catches happen while the box overlaps the shadow.
• STRENGTH pickup at 11.4s, then the exit smash at 15.53s with a full-frame flash and burst.
• Win freezes everything at 15.87s and only Cyrus gets through. The pose replaces his box at 16.53s and the card holds to 19.3s. The tail keeps moving (bob, sparkles, gummy toss at 17.4 to 17.9s) and dissolves into the frame-0 state.
• SFX hit on cue: GO tone, a buzzer on each OUT, a rumble when the eyes appear (5.35s), crack transients on the wall hits, the power-up arpeggio, the smash, the cross sting and the win fanfare.

❌ Fix
• 4.9 to 15.9s: Joy and Cyrus travel as one rigid pair for 11s. They keep the same velocity and a fixed gap of about 10px, and they curve smoothly around every corner without ever touching a wall. That is path-following, not passive bouncing, and it breaks the intent ("nobody steers; luck decides"). It also kills the race, because there are no lead changes, and it creates a 5s stretch from 6.1 to 11.3s with no event. → Give each box its own ballistic velocity with wall reflections, like the reference, so they separate and swap the lead. Keep Cyrus first through the exit and keep everything else as is.

🎯 Priority order
1. Break up the lockstep pair (above).

Optional
• 19.77s: the last frame still shows a faint ghost of CYRUS WINS and DID YOUR GUIDE WIN? (mean diff from frame 0 is 5.7, versus 1.9 between adjacent frames). Finish the dissolve one frame earlier.
• 16.5 to 19.8s: DID YOUR GUIDE WIN? runs to x 989 at y 1292 to 1333, inside the lower-right 193px rail. Shrink it about 10% so it ends before x 887.

Target length: 19 to 20s, payoff at 15.5s (fine for this format)

Requested checks: winding maze PASS · exit mid-right at y 1010 to 1070 PASS · win on first crossing, freeze, one box through PASS · solid dragon and pile PASS · OUT only on overlap, one stamp plus roster tag PASS · real floor tile (the checker is only the finish cell, as in the reference) PASS · gummy pile, no coins PASS · lanes in roster order, RAYLEIGH spelled out PASS · smash flash PASS · card about 3s PASS · roster above the caption zone (bottom edge y 1497) PASS · countdown motion PASS · SFX on events PASS (cracks inferred from the spectrogram, not listened to) · moving tail that loops PASS · passive bouncing FAIL · clipping, stuck boxes, floating debris PASS · stamps never stack PASS · pose replaces the box PASS · dead stretch over 3s FAIL (6.1 to 11.3s, caused by the pair)
