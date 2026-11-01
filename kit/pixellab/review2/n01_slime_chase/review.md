Build review: n01_slime_chase (19.8s)
Verdict: FIX FIRST (small retiming, no rework)

✅ Keep doing
• 0.0s: wall already creeping under GO!, so there's motion and a premise on frame 1. The hook stays up the whole race.
• 5.2 to 6.1s: Cyrus's punch is planted (about 0.9s stop) with no backward jump at the attack start or end, checked at 30fps.
• 16.0 to 17.3s: the wall pulls back, slime hats, hearts land one at a time. A clean break. DID YOU CALL IT? holds 2.25s, then a hard cut to GO! loops well.

❌ Fix
• 3.40 to 3.80s: JOY: SHIELD gets about 0.3s alone before Rayleigh's SLEEP wave covers the screen (3.7s), and it fades under the purple rings. That's two powers at once, and the shield can't be read. → Give SHIELD at least 1.2s on its own, then fire SLEEP.
• 3.40 to 8.10s: SHIELD never pays off. The green bubble is gone by 3.7s, and Joy is the first one caught (8.1s) with nothing blocked. → Keep the bubble on Joy and have it pop on the wall's first grab around 8.0s, then she gets caught on the second grab.
• 3.10 to 3.38s: the red ACV gummy Joy knocks loose flies up into Rayleigh's lane and exits left behind him. It reads as Rayleigh taking it. → Arc the gummy into Joy before her stamp.
• 2.20 to 2.60s: Cleo's crate hop puts her sprite fully on top of Cyrus in the lane above for about 0.35s. → Shift Cyrus about 120px ahead during the hop, or lower the jump so it stays in her lane.
• 7.10 to 10.30s: CLEO: STRENGTH lands 3.2s before its only use (the crate smash at 10.3s). The effect doesn't read as caused by the gummy. → Move the crate so the smash comes within about 1s of the stamp.
• 8.1s, 12.1s, 13.1s: the pink "CAUGHT!" stamps sit on red roof tiles with low contrast. → Use white or yellow fill.

🎯 Priority order
1. Split SHIELD and SLEEP (3.4s)
2. Make the shield block a grab
3. Send the ACV gummy to Joy
4. Fix the Cleo/Cyrus overlap at 2.2s
5. Tighten the STRENGTH payoff
6. Stamp contrast
Target length: 19.8s (keep), payoff at 16.0s
