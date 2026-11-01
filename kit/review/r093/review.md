Build review: r093 (27.7s)
✅ Keep doing
• "PICK A PLAYER!" from frame 1 is a strong comment trigger, and the four colored pads make picking a side easy.
• Powers read correctly: SHIELD! BLOCKED!, SPEED!, STRONG!, and SLEEP! with Zzz on the others plus a purple ring (8.0s, 14.0s, 20.0s).
• Constant small events (YOINK!, +1) mean there is no 3s stretch with nothing happening.
• HUD with gummy pips per guide and a steals counter is a nice live scoreboard.

❌ Fix
• 0.0 to 2.5s: nobody moves (edges.jpg top row is identical). → Start the scramble at 0.3s and keep "PICK A PLAYER!" over the action for 1.5s.
• 6.0 to 24.0s: the same roughly 6s beat runs three times: SHIELD/BLOCKED (6.0, 12.0, 18.0), then YOINKs, then STRONG/DENIED, then SLEEP (8.0, 14.0, 20.0). The pips sit at 2 of 3 the whole time, so it reads as a stalemate. → Cut to one full cycle plus one escalation, and let someone hit 3 by about 12s.
• 24.5s: payoff at 88% of runtime. → Land the win at about 12s.
• 24.5 to 27.7s: a 3.2s static hold on a dimmed frame. The "RAYLEIGH WINS!" text is small yellow on a darkened busy board, with leftover "STRON +1" and a stray "D" from DENIED! still on screen. → Clear all floating stamps on the win, put the win on a solid high-contrast banner at about 1.5x size, hold 1.0s, then cut back to the "PICK A PLAYER!" start.
• 8.0s and 14.0s: up to 5 stamps stack on top of each other (DENIED!, SLEEP!, YOINK!, STRONG!, +1) and become unreadable. → Max 2 stamps at once, and give the power stamps priority over YOINK!.
• HUD labels (SHIELD/SPEED/STRONG/SLEEP, the timer, steals) are tiny on a phone. → Bump them about 1.3x, or drop the timer and steals.

🎯 Priority order
1. Cut to one cycle, win at about 12s.
2. Clean win banner, 1s hold, loop back to the start.
3. Motion from frame 1.
4. Cap stacked stamps at 2.
5. HUD size.
Target length: 15s, payoff at 12s
Series note: rotate the winner across race posts so the sleep guide doesn't become the default.
