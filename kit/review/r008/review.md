Build review: r008 (13.2s)
✅ Keep doing
• Strong hook: the search starts at 0.0s, the crowd is already bobbing and the timer bar drains from the first frame. No countdown.
• "FIND CLEO" reference card with her sprite tells a stranger exactly what to look for without sound.
• Difficulty is right for "feel smart": her blue armor stands out from the brown crowd once you scan the middle, and she sits around y=1215, clear of the bottom UI zone.
• Timer bar shifting green, orange, red (0.0s to 10.5s) keeps a constant state change.
• Answer is never revealed; the end card is a question, as intended.
❌ Fix
• 10.5s to 13.2s: "TIME'S UP!" holds for 2.7s over a dimmed crowd → trim to about 1.2s, then hard cut to frame 1 so the replay restarts with a full bar.
• 10.5s: "Did you find her?" is a yes/no → change to "How many seconds did it take you?" Numbers drive comments and nobody has to spoil her spot.
• 0.0s to 10.5s: subline "YOU HAVE 10 SECONDS" is about 45px tall at full res and repeats what the bar shows → drop it and let the title box shrink, which pulls the crowd field up and gives more search area.
• 0.0s to 10.5s: Cleo is about 60px wide at full res → keep her this size (do not shrink), but consider moving her a little off-center (left or right third) so the center-first scan does not find her in under 2s.
🎯 Priority order
1. Trim the end hold and loop back to the full-bar start.
2. Swap the end question to a number prompt.
3. Remove the redundant subline.
4. Nudge Cleo off-center.
Target length: 12s, payoff ("TIME'S UP!") at 10.5s
