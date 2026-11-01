Build review: r088 (17.3s)
✅ Keep doing
• Rotating ring maze with "PICK A GUIDE!" and an ATTEMPTS counter: simple premise, a new attempt every ~1.5s (1.5s, 3.0s, 4.0s, 6.0s, 7.5s, 9.0s, 10.5s, 12.0s, 13.5s), so no dead stretch.
• Failed guides piling up in the center builds tension nicely.
• 13.5s: the mushroom gummy gives Cleo "SPEED!" and she breaks out. Power matches type, and "CLEO ESCAPED! on attempt 9" is a clear, high-contrast win stamp.

❌ Fix
• 0.0 to 1.0s: empty maze, no guide and no visible ring movement (edges.jpg top row is identical). → Launch the first guide on frame 0 with PICK A GUIDE! already on screen.
• Guides are ~66px tall on a 1080 frame, and once grey in the center pile nobody can tell who failed. → Scale guides up ~40%, and keep a colored ring on each failed head so the pile still reads as Joy/Cyrus/Cleo/Rayleigh.
• Failed guides show small "z" marks (e.g. 2.0s, 9.5s). Sleep is melatonin's effect in this world, so it reads like a power-up. → Use a plain grey-out or a small X instead.
• 14.0s payoff lands at 81%. → Cut to 6 or 7 attempts at a slightly faster launch rate so the escape lands near 11s.
• "SPEED!" at 13.5s is tiny and right next to the pile. → Make it a full-width stamp above the maze for 0.7s; it is the twist.
• "on attempt 9" is small lowercase. → Bump it to ~2x and uppercase, or fold it into one line: "CLEO ESCAPED ON TRY 9!".
• 14.0 to 17.3s: 3.3s dimmed static hold with no comment prompt, and it does not lead back into the empty start. → Hold 1.5s with "Who did you pick?" under the win stamp, then cut to the empty maze as the next guide launches.

🎯 Priority order
1. Motion from frame 0
2. Bigger guides and readable failed pile
3. Shorter run, escape near 11s
4. Big SPEED! stamp, end prompt, loop to start
5. Swap the "z" fail marks

Target length: 13s, payoff at 11s
