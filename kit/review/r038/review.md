Build review: r038 (10.4s)
✅ Keep doing
• Premise is readable at frame 0 and the four cards pop in one by one in the first 0.5s, so there is motion right away (edges.jpg top row).
• One clear question, four labeled options, answer never revealed. Correct per intent.
• Timer bar turning red at 6.5s adds a bit of pressure.
• All panels sit inside the safe zone; bottom 420px is clear.

❌ Fix
• 1.0 to 9.0s: eight seconds where the only state changes are the timer bar shrinking and the outline blinking. Too long for a puzzle this simple. → Cut the timer to about 5s, and add one beat in the middle (around 3s) such as the outline giving a small wobble or the Hollow stepping toward the cards.
• 0.0 to 9.0s: the comment ask ("Comment A, B, C or D") only appears at 9.0s, after most viewers have scrolled. → Add a short line under the title from 0.5s, e.g. "Comment your letter", and keep the end card as is.
• 9.0 to 10.4s: "Comment A, B, C or D" is about 27px tall at full size. → Double it; it is the comment trigger and should read at thumbnail size.
• Throughout: the Hollow at the left edge (about 70px wide at full size, partly in the 70px left margin) is easy to miss and does nothing. → Move him in from the edge and scale him up 1.5x, or cut him.
• 0.0 to 9.0s: option labels (ACV, CREATINE, etc.) are about 27px tall. → Bump to roughly 40px; the letters A to D are what people will comment, so make those the biggest.
• 9.0 to 10.4s: ends on a 1.4s static hold. → Trim to 0.8s so the cut back to the empty-card opening reads as a loop.

🎯 Priority order
1. Shorten the timer and add a mid beat
2. Comment ask visible from 0.5s
3. Bigger comment line and A to D letters
4. Shorter end hold
5. Reposition or cut the Hollow
Target length: 7s, payoff (TIME'S UP) at 6s
