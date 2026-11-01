Build review: n02_race (17.97s)

Verdict: FIX FIRST (two small fixes, then ship)

✅ Keep doing
• 0.6 to 0.7s: Cyrus breaks on "1", GO! lands at 0.9s. Findable on a rewatch, which is the whole job.
• Attacks are planted and sequential: Cyrus stands 1.5 to 2.55s, Joy 2.85 to 3.95s, Cleo 7.3 to 8.35s (about 1s each, no overlap). Each slime pops in its own lane on the contact frame (2.07, 3.37, 7.90).
• Stamps run one at a time: CYRUS WINS! 9.3, whistle beat 11.63 to 12.07, FALSE START! 12.07, CLEO WINS! 13.17, DID YOU SEE IT? 15.5. Nothing stacks.
• Crown drops straight onto Cyrus (10.53 to 10.93) and arcs to Cleo on a clean parabola (12.53 to 13.17). Winner poses swap in as single sprites (Cyrus 10.97, Cleo 13.20).
• King Slime heart break at 14.5 to 15.5, DID YOU SEE IT? holds 2.47s, cut back to the countdown makes a good rewatch loop.

❌ Fix
• 5.43 to 5.53: King Slime landing z-order flicker. 5.43 King Slime is drawn over Joy with Rayleigh's legs poking out below it; 5.47 Joy stands on King Slime's crown in her run pose; 5.50 she is hidden behind the crown; 5.53 she is back on top tumbling. → On the impact frame switch Joy and Rayleigh to their knocked sprites at their own lane positions, keep them layered in front of King Slime from contact on, and launch them from there. No frame where Joy stands on the crown.
• Camera lurches when it retargets: 0.77 (0 to 18 px/frame), 2.13 to 2.17 (4 to 36), 6.30 to 6.33 (18 to 38), and 9.30 to 9.33 at the finish (14 to 69 px/frame, the whole scene jumps). → Ease the camera in over 6 to 8 frames on every retarget instead of starting at full speed and easing out.
• 6.0 to 6.85: JOY & RAYLEIGH OUT! stamp border reaches y 1523, about 25px into the bottom 420px. → Move it up 40px.

🎯 Priority order
1. King Slime landing flicker (5.43 to 5.53)
2. Camera ease-in, finish line first (9.30)
3. OUT! stamp up 40px

Target length: 18s, payoff at 14.5s

Previous must-fixes
• Hits landing on slimes: fixed. One attack each, same lane, pop on contact, no fist sinking in.
• All four guides fighting at once: fixed. Three solo attacks, Rayleigh does not attack.
• Black bars in screen shake (5.5 to 5.9, 14.57 to 14.8): fixed. No dark edge pixels in any frame.
• Crown floating sideways: fixed. Symmetric arc, apex 12.70, steady sideways speed.
• FALSE START! and FOUL! stacked: fixed. FOUL! is gone, FALSE START! stands alone.
• Length about 18.5s: 17.97s, fine.
