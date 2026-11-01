Build review: 104_who_survives_the_flood (11.3s)
Verdict: fix first

✅ Keep doing
• Hook moves from frame 0: the wave rolls in from the left and the "!" reactions ripple across by 1.0s. The setup reads in 1.5s.
• "WHO SURVIVES THE FLOOD?" invites a pick from 0s, and "DID YOURS LIVE?" at 9.5s closes it.
• SLEEP reads instantly (2.33 to 3.17s): Rayleigh keeps digging while the other three freeze under Zzz.
• Eliminations get their own stamp one at a time (6.17, 7.0, 7.67s), and the tracker icons get an X.
• The rewind wipe at 10.3 to 11.3s lands on the exact start state, so it loops cleanly.

❌ Fix
• 6.2 to 10.0s: the eliminated guides float in bubbles on the water surface for up to 4s, which breaks the never-float-on-water rule. → Have each bubble rise and pop into its X'd tracker icon within about 0.5s.
• 8.5 to 9.5s: Rayleigh's shaft is full of water but the chamber he broke into stays dry, so the water hangs in the air over an open hole. → Let the water spill into the chamber behind him as he reaches the portal.
• 6.5 to 7.0s: BLOCKED! then JOY OUT! 0.5s later, so the shield looks useless. → Show the bubble crack and pop, then hold about 1s before JOY OUT.
• 4.0s: Cleo's STRENGTH sparks are still up when SHIELD fires. → Let them finish first.
• 1.67 and 2.17s: Cyrus digs with a fiery slash before he has a gummy, which muddies SPEED at 5.0s. → Give him the plain dig effect.
• 10.9 to 11.1s: the "!" reaction plays in the rewind and again at 0.5s, so it doubles on every loop. → Drop it from the rewind.

🎯 Priority order
1. Ghost bubbles floating on the water
2. Water hanging over the dry chamber
3. Shield pops with no visible benefit
4. STRENGTH and SHIELD overlap at 4.0s
5. Cyrus's fire dig and the doubled "!"

Target length: 11s, payoff at 9.3s (keep as is)
