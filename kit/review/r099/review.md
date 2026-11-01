Build review: r099 (9.99s)
✅ Keep doing
• Hook is moving from frame 0: digits tick 00.00, 00.03, 00.07 across the first 0.5s. Premise is one read: "PAUSE IT AT EXACTLY 10.00".
• Loop seam is clean on the counter: 09.99 straight into 00.00, never reaching 10.00. Exactly the intent; the trap only works because it never shows 10.
• "Comment your time" is on screen from 0.0s and matches the hook. Every pause attempt becomes a comment.
• Counter digits are large and high contrast, well inside the safe zone.

❌ Fix
• 9.99 to 0.00 seam: the black clock hand sits at roughly 10 o'clock in the last frame and snaps back to 12 in the first (edges.jpg). A visible jump tells sharp viewers where the loop is. → Time the hand to complete exactly one turn in 9.99s so it lands back at 12 on the seam.
• 0.0 to 9.99s: "Comment your time" is about 36px tall white text on sand, unreadable at thumbnail size. → Bump to about 60px and put it on the same dark plate as the counter.
• 0.0 to 9.99s: the only state change is the counter; Rayleigh, the gummy and the scene are static for 10s. → Add tension in the last stretch without touching 10.00: from 9.00 the digits turn red and pulse, Rayleigh leans in or raises his staff. This makes the near-miss feel urgent and rewards rewatching.
• Composition sits left of center (clock center about x 455, counter box left-aligned) with empty cobblestone below 1430px. → Center the clock and counter on x 540; scale both up 10 to 15% into the free space above 1500px.

🎯 Priority order
1. Make the clock hand complete one exact turn so the seam is invisible.
2. Bigger "Comment your time" on a plate.
3. Red pulse escalation from 9.00 to 9.99.
4. Center and enlarge clock and counter.

Target length: 9.99s (keep), payoff at none (by design, the viewer's pause is the payoff)
