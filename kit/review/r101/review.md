Build review: r101 (21.4s)
✅ Keep doing
• "WHO ESCAPES THE LAVA?" is a clear pick-a-side premise, large, inside the safe zone.
• Lava flooding the maze from 3.5s is a constant, visible state change; the board gets visibly worse every half second.
• "ERUPTION!" at 9.0 to 10.0s is a proper mid-reel rule stamp and resets attention.
• Final escape at 18.0s is close: three guides cornered, Cleo reaches the portal last-second.

❌ Fix
• 0.0 to 3.0s: guides stand still with "PICK ONE!" over them; no lava until 3.5s (edges.jpg first row identical). → Open with lava already pouring from the top-left at frame 0 and guides running.
• 15.0, 16.5, 17.5s: eliminations only show as a tiny red X on the portrait row (about 40px). On the board, Cyrus at 15.0s looks like he is safe on a stone disc, arms up. → On each elimination, flash a "CYRUS OUT!" stamp at the guide's position (white on dark plate, 0.8s) and grey out or sink the sprite.
• 18.5s payoff lands at 86% of the reel. → Cut the 11.0 to 15.0s stretch (lava creeping with no rule event) to about 1.5s and land the escape around 12s.
• 8.5s: the blue portal (the goal) first appears halfway through. → Show the portal from frame 0 with a small "EXIT" tag so the race has a visible target.
• 7.0 to 8.0s: "SPEED!" callouts are about 30px with no plate. → Double size, dark outline, attach to Cleo.
• 18.5 to 21.4s: 2.9s static dimmed win hold, last frame does not lead back to the bright start board. → Hold 1.2s, then cut to the frame 0 board.
• No comment prompt after "PICK ONE!" fades. → Add "Who did you pick?" on the win card.
• Guides are about 135px tall inside a busy maze. → Zoom the board 10 to 15% (crop the top dead rows) so sprites read at phone size.

🎯 Priority order
1. Clear elimination stamps on the board.
2. Cut to about 14s with the escape around 12s.
3. Motion and visible exit from frame 0.
4. Win card comment prompt, shorter hold, loop cut.
5. Bigger callouts and sprites.

Target length: 14s, payoff at 12s
