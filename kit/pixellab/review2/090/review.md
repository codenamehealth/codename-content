Build review: 090 slimes eat all the glass (11.77s)

Verdict: FIX FIRST

✅ Keep doing
• Satisfying progress loop: GLASS % falling and the castle scene revealing behind the pane gives a state change every half second from 0 to 10s.
• Slimes pile on the floor and stack up the window believably.
• Cleo raising her sword at 10.8s is a nice closer.
• Loop: hard cut from the finished scene back to one slime and 99% glass.

❌ Fix
• 10.7 to 11.77s: ALL GONE! is up ~1.1s, and it is the same small size as the counter line it replaces (~55px). The payoff barely registers. → Make ALL GONE! a large stamp (title size or bigger) and hold it at least 1.5s (end at ~12.3s).
• ~6.5 to 9.0s: the glass shards churn as a cloud that hangs mid-window instead of falling. At 30fps the cloud stays at the same height for over a second and covers Cleo and the castle. → Give each shard gravity so it drops to the floor or slime pile, and spawn fewer at once so each break reads.
• 5.5 to 10.6s: the SLIMES counter freezes at 64 for ~5s. The premise is doubling every second, so the stall reads like the count broke. → Keep doubling (128, 256, 512) through the end, or reach ALL GONE sooner.
• 10.0 to 10.6s: GLASS sits at 2% for 0.6s, then jumps to ALL GONE!. → Tick 1%, 0%, then the stamp.
• 0 to 1.0s: the opening is one ~70px slime at the bottom of a blank pane. → Make the first bite pop (bigger crack or crunch flash), or scale the whole window up ~15%; the bottom ~450px of frame is empty wall.

🎯 Priority order
1. ALL GONE! size and 1.5s+ hold
2. Shards fall with gravity
3. Counter keeps doubling
4. 2% to 0% tick
5. Stronger first bite / bigger window

Target length: 12.3s, payoff at 10.7s

Series note: no on-video comment prompt here, unlike the other three.
