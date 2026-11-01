Build review: r007 (18.0s)
✅ Keep doing
• Clean escalation the viewer reads without words: Day 1 / 7 / 30 / 365 counter with matching gummy count, damage 1 → 12 → 240 → 9999.
• King Slime entrance at 10.0s to 10.5s (light burst, crown) is a real state change and a good mid-reel jolt.
• Gummy loot explosion at 12.5s to 13.5s is the most shareable moment and stays on-brand (gummies, not coins).
• Top title and Day counter sit inside the safe zone.
❌ Fix
• 0.0s to 1.5s: slime and knight idle before the first swing → first hit lands at 0.2s, so frame 1 already has motion.
• 14.5s to 18.0s: "SAME QUEST. EVERY DAY." holds static for 3.5s with only a raised-sword idle → cut the hold to 1.5s and end on a hard cut back to the Day 1 frame (counter snapping 365 → 1 reads as a loop).
• 12.5s payoff sits at 69% of runtime → compress Day 1, Day 7 and Day 30 to about 2s each so the 9999 crit lands near 8.5s.
• 1.5s, 4.0s to 6.0s, 7.5s to 9.5s: "1 DMG", "12 DMG", "POWER UP!" are roughly 30px tall at full res and light blue on stone → make damage numbers at least 80px with a dark outline, and drop "POWER UP!" or make it a bold stamp.
• Whole fight lives in a thin band (about y=1110 to 1440) with the knight around 300px tall and the slime smaller → scale the scene up about 1.4x and center it vertically; the middle third is empty wall.
• 12.5s to 13.5s: "9999 DMG / CRITICAL HIT!" overlaps the Day 365 counter and gummy confetti → move the stamp down to about y=900 so it sits on clear wall.
• No comment trigger anywhere → add a small line under the title from 1s: "What day are you on?"
• Minor check: the strength power-up should read as creatine; confirm the pink counter gummy is the creatine one.
🎯 Priority order
1. Trim the end hold and loop back to Day 1.
2. Pull the crit earlier by compressing the early days.
3. Add "What day are you on?" prompt.
4. Scale up characters and damage numbers.
5. Motion in frame 1.
Target length: 12s, payoff (9999 crit) at 8.5s
