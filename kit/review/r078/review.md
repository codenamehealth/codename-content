Build review: r078 (11.0s)
✅ Keep doing
• The question is the hook and reads in one glance. "ONLY GENIUSES GET IT RIGHT" is the right ego bait.
• The countdown bar with a color shift (green, orange, red) adds pressure through 1.5 to 8.0s.
• The stray pink gummy outside the tray (bottom right of the frame) is a fair gotcha that rewards careful viewers and drives "you missed one" comments.
• "TIME'S UP! COMMENT YOUR NUMBER" covers the tray and no answer is shown. Correct for the intent. Cutting from that banner back to the full tray invites an instant recount.
❌ Fix
• 0.0 to 1.5s: nothing moves (edges.jpg shows identical frames), and the timer only appears at 1.5s → start the bar at frame 1, or drop the gummies into the tray over the first 0.5s.
• 1.5 to 8.5s: 7s with only the bar draining, the Hollow and Rayleigh frozen → give both a light idle bob and pulse the seconds number on each tick. Don't move the gummies.
• 8.5 to 11.0s: TIME'S UP holds static for 2.5s → cut to 1.2s so the loop back to the tray comes sooner.
• Tray fills only about 60% of the frame width; gummies are about 75px at full size → scale the tray up about 20% (there's room above the characters) so the count feels fair on a phone.
• Timer seconds label ("7s") and the "COUNT CAREFULLY..." bubble text are small → enlarge both about 40%.
• "COMMENT YOUR NUMBER" first shows at 8.5s → also put it under the timer from 0.0s, or swap Rayleigh's line for "Comment your number."
• Rayleigh's right edge is close to the lower right safe line (about 870px of 887px) → nudge him 30px left.
🎯 Priority order
1. Motion at frame 1 (timer or gummy drop).
2. Shorter TIME'S UP hold for a tighter loop.
3. Bigger tray and gummies.
4. Early comment prompt.
Target length: 9s, payoff (TIME'S UP) at 7.5s
