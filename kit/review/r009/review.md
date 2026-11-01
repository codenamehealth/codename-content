Build review: r009 (19.5s)
✅ Keep doing
• Clear tour structure: numbered badge plus realm name per scene, each guide walking into their own realm with their gummy floating beside them.
• Pixel-dissolve transitions (3.0s, 6.5s, 9.5s, 13.0s, 16.0s) give a real state change every 3s, so no stretch goes dead mid-tour.
• End grid (16.5s) is a clean summary: five cards, big numbered badges, "Comment 1 to 5". That is the right comment trigger.
• Guides are about 330px tall at full res and read fine on a phone.
❌ Fix
• 16.5s: the choice prompt arrives at 85% of runtime, so most viewers never see the ask → put "Comment 1 to 5" as a small line under the title from 0.0s, and keep the grid as the closer.
• 0.0s to 0.5s: frame 1 is an empty village with the Hollow only half in frame at the left edge → start with him already mid-stride at center, or open on a 0.6s flash of the five-card grid before the tour.
• Each realm runs about 3.2s, with 1.0s to 1.5s of standing idle at the end (5.0s to 6.0s, 8.5s to 9.0s, 11.5s to 12.5s, 14.5s to 16.0s) → cut each realm to about 2.2s by trimming the idle.
• 16.5s to 19.5s: grid holds static for 3s → trim to 1.5s, then dissolve straight back into the village opening so it loops.
• 0.0s to 16.0s: subline under each realm name ("Joy's realm", "Every journey starts here") is about 21px tall at full res, and the realm name about 30px → realm name to 60px+, drop the subline or raise it to 40px.
• 16.5s to 19.5s: "WHICH ONE IS YOURS?" (about 42px) and "Comment 1 to 5" (about 33px) are small for the money line → double both.
• Optional: the floating gummy in each realm is never touched; a 0.3s grab with a sparkle would give each scene a mini payoff.
🎯 Priority order
1. Show "Comment 1 to 5" from the first second.
2. Trim realm idles to get the whole tour under 12s.
3. Bigger realm names and end-card text.
4. Motion or grid flash in frame 1.
5. Shorter end hold, dissolve back to the start.
Target length: 13s, payoff (choice grid) at 11s
