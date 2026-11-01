Build review: r006 (15.6s)
✅ Keep doing
• Premise is instantly clear: title, "10 SEC OR YOU'RE AN NPC" and two stacked village panels say exactly what to do.
• Draining timer bar that shifts green, orange, red (3.0s to 13.0s) gives a steady state change, so the search window never feels dead.
• Differences are findable (pot vs apple at the well, yellow vs blue awning), so viewers feel smart. Answer is never revealed, as intended.
• All text sits inside the safe zone (title ends around y=570, panels end around y=1476).
❌ Fix
• 0.0s to 3.0s: a 3-2-1 countdown over dimmed, static panels is the weakest possible hook; the first 3 seconds are 19% of the reel with nothing to do → cut the countdown to a single 0.5s "GO!" flash over full-brightness panels, timer starting at 0.5s.
• 13.0s to 15.6s: "TIME'S UP!" card holds static for 2.6s → trim to 1.2s, enough to read it, then cut straight to the first frame so the replay starts immediately.
• 13.0s: "Did you find all 3?" is a yes/no question → change to "How many did you find? 0, 1, 2 or 3?" so the reply is a number people comment.
• 3.0s to 13.0s: timer digit inside the bar is about 24px tall, unreadable on a phone → either drop it or put a big digit (120px+) at the bar's right end.
• Panels fill only about 67% of the width (roughly 720x405 each) → shrink the title box to two lines and grow each panel to about 820px wide; differences are small sprites and every pixel helps.
🎯 Priority order
1. Kill the 3s countdown, open on bright panels and a moving timer.
2. Trim the end hold to about 1.2s and loop back to frame 1.
3. Number-based comment prompt.
4. Larger panels.
5. Bigger or no timer digit.
Target length: 12s, payoff ("TIME'S UP!") at 10.5s

Series note: keep the "or you're an NPC" framing; it works as the comment bait.
