Build review: r055 (14.6s)
✅ Keep doing
• Premise and question are on screen from frame 0 ("WHO WOULD WIN THE RACE?" plus "GO!"), and the caption hook matches.
• Something happens every second: SPEED (0.5), STRONG/SMASH (2.0 to 4.0), BOOM (5.5), SHIELD (6.5), SLEEP/BLOCKED (8.5), WINNER (11.0). No dead time.
• Gummy powers are all correct: Cyrus mushroom SPEED, Cleo creatine STRONG smashes the rock, Cleo ACV SHIELD, Rayleigh melatonin SLEEP puts the others out with Zzz and the shield blocks it. That last beat is a great twist.
• Big high-contrast stamps for every rule event, and the ending loops cleanly: the last frames are the GO! start state (edges.jpg).
• "Who did you pick?" on the end card matches the pick-a-side goal.
❌ Fix
• 0.0 to 1.0: "PICK YOUR RUNNER!" is only in the thin ticker bar at about 30px tall and is gone by 1.0 → show it as a large stamp under the title for the first second, so the pick happens before the race starts.
• 0.0 to 11.0: runners are about 150px tall in a 1080x1920 frame and the track only spans roughly y 600 to 1500; speech bubbles ("TOO EASY!", "FOR MY FANS!", "WAIT... CLEO?!") are about 24px tall → scale the track and sprites up about 1.4x into the empty grass band, and enlarge bubbles or cut them to the two that carry the story.
• 1.0 to 11.0: the ticker changes about every second (eight different lines) in small type, too much to read → keep it to three lines: "CYRUS ATE A SPEED GUMMY!", "RAYLEIGH: SLEEP GUMMY!", "CLEO WINS!", and let the stamps carry the rest.
• 5.5: "BOOM! CYRUS GOT HIT!" has no visible cause in the frames → show the smashed rock debris flying from Cleo's lane into Cyrus, since STRONG is what should hit him.
• 12.0 to 14.5: 2.5s dimmed end card → trim to 1.5s.
🎯 Priority order
1. Bigger sprites and track
2. "PICK YOUR RUNNER!" as a big early stamp
3. Thin the ticker
4. Make the hit on Cyrus readable
5. Shorter end card
Target length: 13s, payoff at 10s
Series note: rotate race winners across posts so Cleo is not the default champion.
