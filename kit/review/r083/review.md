Build review: r083 (18.1s)
✅ Keep doing
• Clear, replayable premise: five shapes, a dashed center line, and a progress bar per shape make "did I pause on the right frame" easy to judge yourself. Nothing is revealed, which keeps replays alive.
• Shape counter "SHAPE 1/5" plus a name under the frame gives a steady state change every ~2.5 to 3s (1.5s, 4.5s, 7.0s, 9.5s, 12.5s). No dead stretch inside the game.
• Five different subjects keep each round fresh.
• End card asks for a 0 to 5 score: a good low-effort comment trigger.

❌ Fix
• 0.0 to 1.5s: static empty frame with "PLAY ALONG", nothing moves (edges.jpg top row is identical). → Start shape 1 sliding in at 0.0s and drop the PLAY ALONG card, or float PLAY ALONG over the moving apple for 0.5s.
• 15.0 to 18.1s: 3.1s dimmed static end card. → Hold it 1.5s max, then cut straight back to the shape 1 start so the loop runs.
• 15.5s: "Comment how many you nailed (0 to 5)" is small yellow text sitting on the dark frame, hard to read at phone size. → Make it one line, "Comment your score: 0 to 5", at roughly 2x size in white or purple on a dark pill.
• Comment trigger only appears in the last 3s. → Add a small "Score yourself 0 to 5" chip under the progress bar from 1.5s so viewers who drop early still know what to comment.
• Whole layout: the mirror ends near y=1260 and the floor below it to the 1500 safe line is empty, while the guide beside the frame is tiny. → Scale the mirror up about 15% and nudge it down; enlarge the guide so it reads at phone size.
• Title banner starts at about y=264, just inside the 250px safe line. → Drop it ~30px for margin.

🎯 Priority order
1. Motion from frame 0 (cut the static PLAY ALONG open)
2. Shorten the end hold and loop back to shape 1
3. Bigger, single-line comment prompt, shown early
4. Enlarge the mirror and guide into the empty floor

Target length: 15s, payoff (shape 5 mirror) at 12s
