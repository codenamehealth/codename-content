Build review: r104 (13.60s)
✅ Keep doing
• Clear pick-a-side setup: four guides, four colored columns, a gummy in each, "WHO SURVIVES THE FLOOD?" plus "PICK ONE!" on screen from frame 1.
• Powers match type: apple gummy gives Joy SHIELD! and BLOCKED! (5.5 to 7.5s), mushroom gives Cyrus SPEED!, Cleo STRONG!, Rayleigh SLEEP! with Zzz on the others (7.0 to 7.5s).
• Twist works: Cyrus got speed and still goes out first (8.0s); the sleeper wins.
• Short runtime; the winner lands at 10.5s.
❌ Fix
• 0.0 to 3.0s: nothing moves (edges.jpg first row is identical) while "PICK ONE!" sits there → keep the 2s pick window but put motion under it: water seeping at the top, gummies bobbing, a crack on the dam.
• 0.0 to 2.0s and 3.5 to 4.5s: the blue portal sprite sits on top of "PICK ONE!" and "THE DAM BROKE!" ("PICK [portal] ONE!") → move the text box above the portal or drop the portal behind it.
• 5.5 to 7.5s: SHIELD!, STRONG!, SPEED!, BLOCKED!, SLEEP! are about 36px tall at 1080 and overlap each other → one stamp at a time, at least 2x larger, centered over the guide.
• 8.0 to 10.0s: eliminations are only a tiny red X on the portrait bar → add a big "CYRUS OUT!" style stamp for each.
• Whole reel: the win condition (reach the portal before the water) is never said, so the race reads as random → add one short line at 3.5s: "First to the portal lives".
• 10.5 to 13.6s: 3s dimmed static hold on "RAYLEIGH SURVIVED!"; the last frame does not lead back to the start → hold 1.5s, then cut to the full columns with "PICK ONE!".
• 5.0 to 13.6s: empty dark text box stays on screen under the columns → hide it when it has no text.
🎯 Priority order
1. Motion under the first 3s.
2. Big elimination stamps.
3. Clear portal from the text boxes.
4. Bigger, one-at-a-time power stamps.
5. Shorter end hold, loop to start.
6. State the portal goal.
Target length: 12s, payoff at 9.5s
Series note: rotate which guide survives across flood posts.
