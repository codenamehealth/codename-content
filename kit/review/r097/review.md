Build review: r097 (13.6s)
✅ Keep doing
• "PICK ONE!" plus a 4-lane board is a clear pick-a-side premise in frame one.
• The race stays close (final 8 / 7 / 7 / 9) with lead changes: Joy leads at 5.5s, Rayleigh overtakes at 8.5s. Good argument fuel.
• "RAYLEIGH WINS! / Did your guide win?" is high contrast, one line, inside the safe zone, and the comment prompt matches the hook.
• Ticking 0:09 to 0:00 clock gives a reason to stay.

❌ Fix
• 0.0 to 1.5s: board is frozen (all edges.jpg first-row frames identical, first pickup appears at 2.0s). → Start gummies falling and guides moving at frame 0, keep "PICK ONE!" over the action, fade it by 1.0s.
• 10.5 to 13.6s: 3.1s static win hold (only sparkles move), and the last frame (Rayleigh solo) does not lead back to the 0:09 start state. → Hold the win 1.2s, then hard cut to the 0:09 four-lane start frame so it loops.
• 7.5 to 8.0s: "FINAL 3!" is thin red text over busy lanes and is gone within 0.5s. → Make it a white or yellow stamp on a dark plate, center board, hold 1.0s.
• 2.0s onward, Joy lane: the red pickup reads as a fruit apple at phone size, not a gummy. → Use a gummy sprite (apple-shaped gummy with gummy sheen/outline is fine) so every pickup reads as a gummy.
• 3.5s and 9.0s: green slimes fall out the bottom of the board into the street below (y around 1700). → Clip hazards at the board edge.
• Comment ask only arrives at 10.5s. → Add a small "comment your pick" line under the scoreboard from 0.5s to 3s.
• Rayleigh lane's right border sits at about x 888, right on the 193px lower-right UI zone edge. → Shrink the board 10 to 15px or shift it left.

🎯 Priority order
1. Motion from frame 0 (hook).
2. Shorten end hold and cut back to start state (loop).
3. Stronger "FINAL 3!" stamp.
4. Gummy-only pickups in Joy's lane.
5. Early comment prompt.
6. Clip slimes and nudge board off the right UI edge.

Target length: 11.5s, payoff at 9.5s

Series note: rotate the winning guide across race posts so Rayleigh is not the default winner.
