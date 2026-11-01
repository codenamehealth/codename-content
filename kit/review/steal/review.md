Build review: steal (27.2s)
✅ Keep doing
• Premise is readable in one glance: "WHOEVER GETS 3 GUMMIES WINS" sits below the 250px line, big and two-tone.
• "PICK A PLAYER!" on frame 1 is the right comment trigger and matches the caption.
• From 3.0s to 23.5s something changes every half second: +1 pops, YOINK! stamps, steal counter climbing. No dead stretch in the match itself.
• "JOY WINS!" at 24.0s is large, centered, with the rest of the frame dimmed. Clean win stamp.
❌ Fix
• 0.0s to 27.2s: the Hollow is a fifth competitor (left spawn, his own basket, fifth HUD slot, he steals and scores). Intent says the 4 guides only, Hollow never a competitor or pickable. → Remove him from the arena and the HUD; four spawns, four baskets, four HUD slots.
• 0.0s to 2.5s: every frame of the first 0.5s is identical and nobody moves until about 2.5s. → Start the run toward the picnic blanket on frame 1 with "PICK A PLAYER!" over the moving action.
• 24.0s (88% of runtime): the win lands too late; 28 steals with nobody visibly close to 3 makes 8s to 23s feel like a loop with no progress. → Cap the match so someone hits 3 by about 12s; flash a "2/3!" stamp over whoever is one away so viewers sweat their pick.
• 24.0s to 27.2s: 3.2s static hold on the dimmed win frame, then the reel jumps to the bright pre-game setup. → Hold "JOY WINS!" 1.0s, then cut straight to the frame-0 setup so it loops.
• Throughout: "Stealing is allowed" (about 24px tall), the HUD gummy dots, the timer, the steal counter and "YOINK!"/"+1" (about 30px) are too small for a phone. Characters are about 100px tall. → Double YOINK! and +1, make the HUD dots read as counts (1/3, 2/3), drop the subtitle into the title line or cut it, and zoom the arena about 20%.
🎯 Priority order
1. Remove the Hollow as a competitor (4 guides only).
2. Payoff earlier: winner by about 12s, plus a "one away" stamp.
3. Motion on frame 1.
4. 1s win hold then cut to the start state for the loop.
5. Bigger stamps, HUD counts and characters.
Target length: 14s, payoff at 12s
Series note: rotate the winner across posts so Joy doesn't become the default pick.
