Build review: r061 (13.3s)
✅ Keep doing
• The character-select framing ("PLAYER 2", the cursor moving across the cards, names typing in) reads instantly as a game menu, and the header states the premise from frame 0.
• Each guide reveal is a clear state change (silhouette, then portrait, name, guild, gummy), with big portraits that read well on a phone.
• Ends on the question, "WHO IS HE CHOOSING? TAG HIM BELOW", with no pick revealed, which fits the intent.
• Loop works: the last frame is the full roster on the same select screen and frame 0 is that screen reset to empty cards (edges.jpg).
❌ Fix
• 0.0 to 0.5: all opening frames are the same still green silhouette → open on the cursor already moving or the Joy portrait flashing in at frame 0.
• 1.0 to 2.4, 3.5 to 4.9, 6.5 to 7.9, 9.0 to 10.0: each guide holds about 1.5s after its name finishes, four times in the same rhythm, so the middle feels slow and predictable → cut each hold to about 0.6s so the cursor feels like an indecisive player browsing; that takes the reveal section from about 10s to about 6s.
• 10.5: the panel goes blank for a beat with just a tiny sprite at the left edge before the lineup appears → cut straight to the four-guide lineup.
• 11.0 to 13.3: 2.3s static end card → trim to about 1.2s; the loop does the rest.
• 0.5 to 13.3: the guild lines under the card names ("FOUNDATION", "VITALITY") are about 18px tall at 1080 wide and can't be read → drop them from the small cards; the big panel already shows the guild.
• "TAG HIM BELOW" only appears at 10.5 (79% in) → add it as a small line under the header from about 3s so the tag ask lands on the first watch.
🎯 Priority order
1. Shorten the four reveal holds
2. Motion on frame 0
3. "TAG HIM BELOW" visible early
4. Cut the blank panel at 10.5 and trim the end hold
5. Drop the tiny guild text on the cards
Target length: 9s, payoff (the "who is he choosing?" lineup) at 7.5s
