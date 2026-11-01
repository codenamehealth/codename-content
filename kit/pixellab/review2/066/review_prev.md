Build review: 066 (8.4s)
✅ Keep doing
• Hook moves from frame 1: Rayleigh's magic circle fires at 0.0s and the outline draws itself over 0.0 to 3.0s, so the premise and the motion land together.
• Question text sits at roughly y 300 to 405 of 1920, inside the safe zone, readable at thumbnail size.
• A/B/C/D labels give viewers a one-letter comment answer from second one.
• Countdown bar colors shift green to orange to red (3.0 to 6.5s), so there is a state change every second and no dead time.
• Never reveals the answer, and the loop cuts from TIME'S UP back to an empty outline being drawn, so a replay has a reason to start.
❌ Fix
• 3.0 to 7.0s: the outline is a coarse 12-point polygon blown up about 2.5x, so at phone size it reads as a generic dome that A, B and D could each plausibly fit. The intent wants a real look, not a guess → make the one feature that separates the right gummy (its bottom lip, top curve or side angle) show as a clear notch or bend in the outline, so a careful viewer can be sure and feel smart.
• 3.0 to 6.5s: the countdown number box ends at x 909, about 22px inside the right-side UI column in the lower half → shift the bar and box left so the box ends by x 880.
• 7.0 to 8.4s: TIME'S UP holds static for 1.4s → trim to about 0.8s so the loop restarts sooner.
🎯 Priority order
1. Make the outline's distinguishing feature legible at phone size.
2. Trim the TIME'S UP hold.
3. Nudge the countdown box out of the right UI column.
Target length: 8s, payoff at 7s
