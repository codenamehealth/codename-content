Build review: 064 (18.7s)
Verdict: FIX FIRST. Frozen balls hang in mid-air, and the escape and catch lose their physics.

✅ Keep doing
• Hook: the ball is moving inside the spinning ring from frame 0, and the premise reads instantly.
• No dead time. The countdown digit, timer arc and TRY counter change every second.
• FROZEN! and ESCAPED! are high contrast and land on the state change.
• Payoff: the Hollow catches the apple gummy and eats it happily (eyes closed, no teeth, no talking).

❌ Fix
• 4.0 to end, 8.3 to end, 12.5 to end: the frozen balls stay wherever they stopped: one high on the upper left, one floating mid-ring, a third stacked under it. That breaks the no mid-air rule → when a ball freezes, drop it to the ring floor so the frozen balls pile up and tumble as the ring spins.
• 15.75 to 16.0: the gummy stops dead in mid-air when its bubble pops, then falls straight down → keep its exit speed and arc it into the Hollow.
• 16.2 to 16.6: the gummy slides down over the Hollow's face while his arms stay at his sides; his hands only appear at 16.6 → raise his hands to catch it at about 16.2.
• 11.2 to 11.7: SO CLOSE! is printed over the countdown digit ("SO C2LOSE"), and it fires 0.4s after the real near-miss at 10.8 → hide the digit or move the stamp off it, and fire it on the near-miss frame.
• 13.0 to 13.3: the try 4 gummy hangs at spawn for about 0.4s, while the other tries drop at once → drop it immediately.
• 17.5 to 18.7: a 1.2s dimmed hold on ESCAPED ON TRY 4! → cut it to about 0.6s so the loop restarts sooner.
• 0 to 3s: the hook never says the goal → "EACH BALL HAS 4 SECONDS TO ESCAPE".
• There's no on-screen comment prompt; the caption has to carry it.

🎯 Priority order
1. Frozen balls in mid-air
2. Pop stop and catch
3. SO CLOSE! overlap and timing
4. Spawn hover, end hold, hook wording

Target length: 18s, payoff at 15.8s
