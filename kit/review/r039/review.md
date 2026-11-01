Build review: r039 (12.6s)
✅ Keep doing
• Split screen with one clear question on top; both Hollows are moving by 1.0s and the shortcut fails fast (STUCK! at 3.5s).
• Long road has a visible progress meter (XP 0/4 to 4/4, +1 XP pops at 2.5, 4.5, 5.0, 7.0s), so the bottom panel never stalls.
• Last frames (12.1 to 12.6s) return to the exact start state, so the loop is seamless.

❌ Fix
• 0.0 to 0.9s: both Hollows stand still at their start marks; the first second is a static layout → start both mid-stride on frame 1 (shortcut Hollow already stepping toward the swamp).
• 3.5 to 12.6s: the shortcut panel is frozen on STUCK! for 9s, half the screen dead → have the stuck Hollow sink a little further or struggle every 2s, so that panel keeps changing.
• 9.5 to 12.6s: the MADE IT! stamp is covered by the blue castle banner between "MADE" and "IT!", and it overlaps the "THE LONG ROAD" label → move the stamp to center of the bottom panel, above all scenery layers, and hide the panel label once it fires.
• 10.5s: "Which road are you on?" arrives at 83% of the reel in small text → show it from 0s under the banner, at banner size.
• Whole reel: "THE SHORTCUT" and "THE LONG ROAD" labels start about 36px from the left edge (inside the 70px zone); "XP 4/4" and "THE CASTLE" sit inside the right 193px zone of the lower half → inset all panel labels 80px left and 200px right.
• Whole reel: the Hollow is about 150px tall; "THE SWAMP" and "THE CASTLE" tags are unreadable on a phone → crop each panel tighter so the Hollow is 1.5x larger; drop the location tags.

🎯 Priority order
1. Comment prompt visible from 0s
2. Unblock the MADE IT! stamp
3. Keep the stuck panel moving after 3.5s
4. Inset labels out of the edge zones
5. Bigger Hollows, motion on frame 1

Target length: 11s, payoff at 8.5s

Series note: if the long road always wins, alternate with a version where the shortcut pays off so the pick-a-side stays open.
