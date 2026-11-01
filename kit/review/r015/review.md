Build review: r015 (14.8s)
✅ Keep doing
• "PICK A GUIDE / BEFORE THE MAZE STARTS" plus the four face icons sets up the bet in frame 1 and matches the post hook.
• The rising void (3.5s onward) is a great clock: it visibly closes in and creates real tension around 9.0 to 11.0s.
• BUMP! collisions (3.5 to 9.5s) keep state changing every half second during the run.
• Ending cuts back to the starting lineup, so it loops.
❌ Fix
• 0.0 to 2.5s: guides stand still through "PICK ONE!" and a 3, 2, 1. Weak hook. → Open on GO at about 0.5s with the void already creeping in at the bottom edge, and keep "PICK ONE!" up over the moving run.
• Whole reel: the maze uses about 70% of the width, and guides are only about 120px tall at 1080x1920. Collisions read as a blur on a phone. → Scale the maze up about 20% to fill the safe zone width (70 to 1025px), or tighten the camera on the pack.
• About 3.0s: the red pickup near Cyrus is about 30px and doesn't read as a gummy, and "SPEED!" doesn't appear until 6.5s, so cause and effect are lost. → Make it a large mushroom gummy, with a pop on pickup and SPEED! firing on the same beat.
• 10.0, 10.5, 11.5s: eliminations only show as tiny red "OUT" over the top icons while each guide sinks into the void. → Add a big stamp in the maze per elimination ("JOY OUT!", "CYRUS OUT!", "RAYLEIGH OUT!"), 0.4s each.
• 11.5 to 14.8s: 3.3s static dimmed hold on "CLEO ESCAPED!" with a small "Did your guide win?" line. → Cut the hold to about 1.2s and make "DID YOUR GUIDE WIN?" the large line.
• Payoff (Cleo escapes at 11.5s) is at 78% of runtime. → After the cuts above, the escape lands near 9s of an 11s reel.
🎯 Priority order
1. Moving opening, countdown removed or folded into the run.
2. Shorten the end hold.
3. Bigger maze and sprites.
4. Elimination stamps.
5. Readable mushroom gummy tied to SPEED!.
Target length: 11s, payoff at 9s
