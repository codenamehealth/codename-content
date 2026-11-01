Build review: r005 (20.53s)
✅ Keep doing
• "PICK ONE!" inside the globe at 0.0 to 1.5s matches the caption and gets people choosing before the action starts.
• Real lead changes: Joy leads early (3.0 to 5.5s), Rayleigh pulls away (6.0 to 13.5s), Cyrus comes back late (14.0 to 17.0s). That's the arc that makes people pick a side and rewatch.
• Big "CYRUS WINS! 31 GUMMIES" card with the guide sprite is clear and well inside the safe zone.

❌ Fix
• 0.0 to 1.5s: the globe is static, just the spinner and a few gummies, so there's no motion in the first second → start the spinner turning and the first drops falling at 0.0s, with PICK ONE! on top.
• 17.5 to 20.53s: a 3s dimmed static hold on the winner card, then a hard cut to the bright start → hold the winner for about 1.0s, then empty the globe back to the PICK ONE! state so it loops.
• Payoff at 17.5s is 85% through a 20.5s reel, so most viewers never see the winner → speed up the fill about 1.4x so the comeback lands at about 10s and the win at about 12.5s.
• Whole race: the scoreboard (about 36px numbers) is the only way to follow the race, and it's small. The pile is mostly orange, but those pieces score for Rayleigh while Cyrus is the orange guide, so the pile actively misleads → double the scoreboard size, and give each guide's gummies a thin outline in that guide's color.
• 6.0s and 14.5 to 15.5s: lead changes happen silently → add a high-contrast stamp ("RAYLEIGH TAKES THE LEAD", "CYRUS PASSES!") for about 0.6s each.
• Whole race: the +4/+5 pops are small and low-contrast purple and green on orange → make them 2x bigger with a dark outline.
• 1.5 to 10.0s: Cleo sits at 3 for 9s and finishes with 8. She's never in it, so Cleo pickers check out → give her one early surge so all four look alive.
• 17.5s: Joy jumps from 21 to 26 on the same frame as the win, which reads like a glitch → settle all scores before the win stamp.

🎯 Priority order
1. Cut to about 13s with the win at about 12.5s
2. Replace the static winner hold with a reset loop
3. Bigger scoreboard plus guide-color outlines on gummies
4. Lead-change stamps
5. Moving opener, bigger pops, Cleo surge
Target length: 13s, payoff at 12.5s

Series note: rotate the winner across machine posts.
