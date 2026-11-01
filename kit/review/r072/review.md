Build review: r072 (15.6s)
✅ Keep doing
• Classic shell game, instantly understood: gummy over the middle knight, it drops in at 1.5s to 2.0s, then the shuffle starts.
• Escalating speed x1, x1.5, x2, x3 builds pressure, and the dodge rolls at 5.0s, 7.0s and 11.5s add chaos that makes tracking harder.
• Answer never revealed; ends on "Comment A, B or C".
• Loop is excellent: the last frame (three knights in a row) matches the first frame, so the restart is close to seamless.
❌ Fix
• 0.0s to 1.5s: the gummy only bobs over a still lineup; 1.5s before anything happens → drop the gummy into the knight by 0.5s and start shuffling by 1.0s.
• 4.5s, 6.5s, 9.5s: speed changes only show as small text in the sub-banner → flash a large "SPEED x2" stamp mid-screen for 0.4s at each change, then let the banner keep it.
• 12.0s to 15.6s: 3.6s with the knights standing still → trim to about 1.5s after the A, B, C labels land (end around 14.0s).
• 0.0s to 2.5s and 12.5s to 15.6s: "Remember the gummy" and "Comment A, B or C" are small sub-banner text → bump to the size of "WATCH" and keep each to one line.
• 12.0s to 15.6s: the lineup sits left of center (about x 120 to 810), leaving the right side empty → center the three knights and scale them up about 20% so A, B and C read clearly at phone size.
• 0.0s to 15.6s: the knights are about 180px tall and play out in the upper-middle band; the lower third is unused dirt → move the play area down and enlarge, staying above y 1500.
🎯 Priority order
1. Faster start: gummy in by 0.5s, shuffle by 1.0s.
2. Trim the end hold to about 1.5s.
3. Big speed-up stamps.
4. Center and enlarge the final lineup.
5. Larger prompt text.
Target length: 13s, payoff (lineup and question) at 11s
