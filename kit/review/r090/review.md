Build review: r090 (21.7s)
✅ Keep doing
• Clear one-line premise in the title and a live GLASS LEFT counter. The doubling SLIMES count (1, 2, 4, 8... 64) is a good "how fast does this go" hook.
• 12.0s to 18.5s is the best stretch: the slime arch sweeps across while the hidden castle scene comes through.
• ALL GONE! at 19.0s is a clean, high-contrast stamp, and the knight raising his sword gives it a beat.
• All text clears the safe zone.

❌ Fix
• 0.0 to 1.0s: empty glass with nothing moving (edges.jpg top row is 8 identical frames), and the first slime is a few pixels wide at the bottom left. → Drop the first slime in at frame 1, big and centered, with a visible first bite.
• 1.0 to 7.5s: dead in practice. Glass goes 100% to 92% in 6.5s, and on a phone it all reads as one tiny green blob in the corner. → Start at 4 to 8 slimes, or speed up the doubling so the counter is under 85% by 3s.
• 0 to 21.7s: the window takes about 2/3 of the frame width, and roughly the bottom 450px is empty brick. → Scale the window up about 20% and move it down. Slimes and the reveal are the payoff, so they should fill the screen.
• 19.0 to 21.7s: payoff lands at 88% of runtime, and 21.0 to 21.7s is a static hold (edges.jpg bottom row is identical). → Trim the end to about 1s after ALL GONE!, then hard cut to the empty glass so it loops.
• No comment trigger. → Add a short line under the counter early, e.g. "Guess the % at 10s", to match a caption question.

🎯 Priority order
1. Compress 1.0 to 7.5s (start with more slimes or double faster).
2. Motion in frame 1.
3. Trim the end hold and cut back to the empty glass.
4. Scale the window up.
5. Add the guess prompt.
Target length: 15s, payoff at 12s
