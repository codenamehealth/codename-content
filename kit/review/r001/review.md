Build review: r001 (10.59s)
✅ Keep doing
• 0.0 to 1.0s: lines draw themselves down from the guides while fish swim. Real motion in the first second and the premise is instantly clear.
• Title is big, two lines, and CYRUS is colored orange in both the title and his name tag, so the target is obvious at a glance.
• Timer bar draining (green to orange at 6.5s) gives the solve window urgency.
• Ends on TIME'S UP with no answer shown. Last frames cut back to the empty dock at 0.0s, so it loops into a fresh line draw.

❌ Fix
• 1.0 to 8.5s: the tangle is only about 270px tall at full res, thin white lines on pale blue water, with roughly a dozen crossings. On a phone this reads as noise, not a puzzle, and viewers bail instead of feeling smart → make the maze about 450 to 500px tall by moving the jars down to about y 1450 (the empty sand band above the bottom safe zone), thicken lines to 6 to 8px, add a dark outline, and cut crossings to about 6.
• 1.0 to 8.5s: fish swim across the lines at 2.0 to 4.5s and sit on line ends at 6.0 to 8.0s, hiding exactly what the viewer is tracing → keep fish below the jars or behind the lines.
• 8.5s: "Comment A, B, C or D" appears only at the end, so most viewers never see the ask → change the subline from 0.0s to "Follow the line. Comment A to D".
• 1.5 to 8.5s: 7s with no state change except the timer → add one mid beat at about 5.0s, e.g. a "5s LEFT" stamp or the bar pulsing red.
• 8.5s: TIME'S UP fades in over about 0.5s → hard pop or quick scale-in so it lands as a stamp.

🎯 Priority order
1. Taller, thicker, simpler maze using the empty sand space
2. Comment prompt in the subline from frame one
3. Fish out of the line paths
4. Mid-point beat at 5.0s
5. Snap the TIME'S UP stamp
Target length: 10s, payoff (TIME'S UP) at 8s
