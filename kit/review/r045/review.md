Build review: r045 (27.7s)
✅ Keep doing
• Clear premise: "WHICH GUILD ARE YOU?" plus a four-row legend tying each guide to a color, potion and gummy by 1.0s.
• Whip transitions with a new background per question (3.0, 7.0, 10.5, 14.5, 18.0s) and a draining timer bar keep rounds feeling fresh.
• "COMMENT YOUR GUILD" on the final grid is an easy, answerable comment ask that matches the caption.

❌ Fix
• 18.0 to 21.0s: Q5 (Gym First vs Coffee First) repeats the Q2 matchup, Vitality vs Energy. Over 5 rounds, Vitality and Energy appear 3 times while Foundation and Recovery appear twice, so "count your colors" is rigged toward blue and orange → cut Q5. Q1 to Q4 give every guild exactly 2 appearances with no repeat pairing.
• 0.0 to 0.5s: the title sits over a static background with nothing moving → start the legend mid-slide on frame 0.
• 22.0 to 27.7s: 5.7s static end card on flat black, lower 40% empty, and it does not lead back into the opening (edges.jpg) → hold 2.5s, scale the grid up to fill the frame, then slide back into the opening legend so the last frame matches frame 0.
• 3.5 to 21.0s: each question holds about 3s with only the bar moving → trim to 2.5s.
• 0.5s onward: "Pick one each round. Count your colors.", the "___ GUILD" sublines and "QUESTION 1/5" are tiny on a phone → enlarge at least 1.5x, or drop the guild sublines (the card color already says it).
• 0.5s: "COMMENT YOUR GUILD" first appears at 22.5s → add it under the legend so the ask is known before round one.
• 6.5s and 14.0s: the "OR" badge floats alone on an empty background for a frame → animate it out with the cards.

🎯 Priority order
1. Cut Q5 (fixes balance and length)
2. Loop the end card into the opening
3. Motion on frame 0
4. Trim holds to 2.5s
5. Bigger small text, comment ask up front

Target length: 17s, payoff at 13.5s
