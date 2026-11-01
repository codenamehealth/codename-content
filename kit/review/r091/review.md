Build review: r091 (9.6s)
✅ Keep doing
• Strong opening: the grid builds itself diagonally in the first 0.5s (edges.jpg top row), so there is motion from frame 1 and the premise reads right away.
• The timer bar going green, then yellow at 5.0s, then red at 7.0s is good tension, and it changes state every 1 to 2s, so there is no real dead time.
• TIME'S UP! / "Did you find it?" at 8.0s ends on the question with no reveal, as intended. The cut from the full grid back to the empty grid loops cleanly.
• Hollow standing at START as the player is right.

❌ Fix
• 0.0 to 9.6s: the grid is only about 55% of the frame width and everything below about y 1400 is empty forest. Cells are about 75px on a phone, and choco vs apple tiles are close in tone at thumbnail size. → Scale the grid, START/END and the Hollow up about 20 to 25% and move them down into the empty space (still above y 1500).
• 0.0 to 9.6s: the "YOU MUST GO:" row is the whole rule but it is the smallest thing on screen (icons about 45px, label tiny). → Make the sequence row about 1.5x taller with bigger icons, and drop the "YOU MUST GO:" label if space is tight.
• 1.0 to 9.6s: "Diagonals not allowed" is very small body text. → Merge it into the title's second line or make it the same size as "ONLY 1% CAN FIND IT".
• 8.0 to 9.6s: a 1.6s hold on TIME'S UP. That is acceptable, but trimming to about 1.0s gets the loop back faster.
• Comment trigger only appears at 8.0s. → Optional: a small "Comment your path" line under the timer from 1.0s, to match the caption.

🎯 Priority order
1. Scale the grid and sequence row up.
2. Make "Diagonals not allowed" readable.
3. Trim the end hold to 1.0s.
4. Add an early comment prompt.
Target length: 9s, payoff (TIME'S UP) at 7.5s
