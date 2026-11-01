Build review: r062 (13.5s)
✅ Keep doing
• Clear premise: one pedestal, gummies stacking, a question that makes everyone call a number before it drops.
• Steady state change every 0.5s to 1s from 1.0s to 9.0s; the tower visibly leans at 8.5s, which builds real tension.
• "TIMBER!" at 9.0s is a big red stamp and the gummies raining onto the guides is a fun payoff.
• Answer stays a guess: the deciding gummy is never named.
❌ Fix
• 0.0s to 1.0s: empty pedestal and still guides, first gummy only appears at 1.0s → have gummy #1 already falling at frame one.
• 0.5s to 8.0s: the "#1 ACV", "#2 CREATINE" labels are small colored text, hard to read on a phone and fading fast → make them one larger white-outlined line next to the stack, or a running count ("8 STACKED") in one fixed spot.
• 8.0s to 8.5s: the final gummy drops behind the "Comment your guess" box and the top of the stack runs up into the title. The climax is partly hidden → move "Comment your guess" below the guides (around y 1450 to 1500) or drop it after 1.5s, and start the stack lower so the top stays clear of the title.
• 10.5s to 13.5s: 3s with no state change after the pile settles → cut at about 11.5s, right after "Did you guess right?" lands.
• 11.5s: "Did you guess right?" is small body text → same size as the title's second line, one line.
• 13.5s to 0.0s: hard jump from pile to empty pedestal → a 0.2s sweep of the gummies off-screen would make the loop seamless.
• Guides are about 150px tall and sit in a row at the bottom of the action; the lower fifth of the frame is empty → scale the whole scene up about 15% and move it down a little.
🎯 Priority order
1. Clear the final drop: move "Comment your guess" off the stack's path.
2. Gummy falling at frame one.
3. Trim the 3s hold to end at 11.5s.
4. Bigger gummy labels and end line.
5. Smoother loop back to the empty pedestal.
Target length: 11.5s, payoff (TIMBER) at 8.5s
