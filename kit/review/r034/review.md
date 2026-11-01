Build review: r034 (13s)
✅ Keep doing
• Shell game anyone gets in one look: gummy, three vases, shuffle, "Comment 1, 2 or 3".
• The shuffle runs nonstop from 3.0 to 10.0s, so the middle has no dead time.
• Never lifts a vase. The loop restarts on the gummy above Cyrus, which invites a replay to track it again. Matches the intent.
• Numbered vases make answering effortless.

❌ Fix
• 0.0 to 1.0s: the gummy just hovers over Cyrus, and almost nothing moves. → Have the gummy already falling at 0.0s, vases slam down by 0.6s, shuffle starts by 1.0s.
• 2.5 to 3.0s: "Keep your eye on it..." is tiny (about 24px at full res), off-center, and gone in under a second. → Cut it, or center it at 40px or more for 1s.
• 3.0 to 10.0s: gold vases on a gold floor are low contrast and hard to track on a phone. → Add a dark outline or strong drop shadow to the vases, or dim the floor behind the vase row about 30%.
• 3.0 to 10.0s: a 7s shuffle loses most people, which works against "feel smart". → Trim to about 5s with fewer, readable swaps.
• 10.0 to 13.0s: "Comment 1, 2 or 3" is about 27px tall on a translucent box, and only appears at 10s. → Make it the main line at 48px or more, and flash "COMMENT 1, 2 OR 3" under the title during the shuffle too.
• 10.0 to 13.0s: a 3s hold where only Cyrus idles. → Cut the hold to 1.5s.
• Throughout: the gummy is about 75px. → Scale it up 1.5x so the drop under the vase reads clearly.

🎯 Priority order
1. Faster opening (gummy dropping at 0s, shuffle by 1s)
2. Vase contrast against the gold floor
3. Big comment prompt, visible during the shuffle
4. Trim the shuffle to 5s and the end hold to 1.5s
5. Bigger gummy, fix or cut "Keep your eye on it..."

Target length: 9s, payoff at 7s (question card)
