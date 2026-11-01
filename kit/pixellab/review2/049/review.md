Build review: 049 (6.4s)
✅ Keep doing
• Difficulty is right for the intent. The bitten gummy (D7, small notch top right) is findable in 5s on a phone but not instant.
• The grid coordinates (A to J, 1 to 8) make answering effortless in comments.
• The timer bar going green to yellow to red with the 5 to 1 countdown builds pressure without covering the grid.
• The answer is never revealed. The jump from "TIME'S UP!" back to a full timer reads as a restart, which is good for replays.
• Title and grid sit inside the safe zone; the bottom of the grid is around 1430px.

❌ Fix
• 0.0 to 0.5s: the opening is fully static apart from a slow timer bar; edges.jpg shows identical frames → add one synced idle bob or shimmer to all 80 gummies (same timing, so the odd one isn't singled out), or a 0.3s pop-in of the grid that settles by 0.4s.
• 5.0 to 6.4s: a static 1.4s hold on "TIME'S UP!" delays the replay → cut the hold to about 0.7s.
• 5.0s: no on-screen ask to answer → at "TIME'S UP!" swap the title to one short line such as "WHICH SQUARE?" (same title swap pattern the race and path reels use).
• 5.0s: "TIME'S UP!" appears twice, in the bar and as a stamp over rows E to F → keep only the bar version so the grid stays clean for the final look.

🎯 Priority order
1. Motion in the first 0.5s
2. "WHICH SQUARE?" title swap at time's up
3. Shorten the end hold to about 0.7s
4. Drop the duplicate "TIME'S UP!" stamp

Target length: 5.8s, payoff at 5.0s (question end, no reveal)
