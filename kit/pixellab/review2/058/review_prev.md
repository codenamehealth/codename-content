Build review: 058 (12.7s)
Verdict: FIX FIRST. The finish breaks the physics rule: marbles pass through the cork and through each other.

✅ Keep doing
• Hook: marbles and the "?" standings bar are up at frame 0, and GO! lands at 0.2s. Clear job.
• The live standings and the 3, 2, 1 podium reveal (11.0 to 11.4) pay off "call the top 3". The podium order matches the race.
• No dead time. The podium cuts straight back to the start grid, so it loops.

❌ Fix
• 9.3 to 9.4 (Rayleigh), 9.9 to 10.1 (Cleo), 10.5 to 10.7 (Joy): each marble sinks into the solid cork and vanishes. That's clipping at the payoff → pop the cork off on the first arrival, or start with the bottle open so the marbles drop into a visible neck.
• 7.9 to 9.9: marbles interpenetrate in the funnel (Rayleigh and Joy at 8.0 and 8.8 to 9.1, a three-marble stack at 9.0 to 9.2, Cleo and Joy at 9.4 to 9.9) → collide at the full disk edge so they jostle and queue.
• 5.7 to 6.3: spinner blades sweep through Rayleigh's marble → give the blades collision so they bat him away.
• 5.6 to 7.2: Joy hangs still beside the spinner and wall for about 1.5s with nothing under her → knock her loose or let her slide down the wall.
• 0.0 to 0.2: the marbles hang in mid-air before GO! → add a gate bar that drops on GO!.
• 9.2: a white flash with PHOTO FINISH! hides Rayleigh's win, and it isn't close (Cleo is about 0.7s behind) → no flash; stamp a big "1ST!" once he's through.
• 0.6 to 0.8: GO! sits over the marbles and hides the first collision → fade it by 0.5s.
• 9.3 to 10.7: the finish happens at y 1450 to 1500, on the bottom safe-zone line → raise the bottle about 150px.
• 11.0 to 11.4: each guide hard-pops onto the podium → add a short drop-and-land.

🎯 Priority order
1. Cork clipping
2. Funnel overlap
3. Spinner through Rayleigh, and Joy hanging
4. Start gate, finish flash
5. GO! layering, finish height, podium landings

Target length: 12s, payoff at 9s
