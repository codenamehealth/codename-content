Build review: 055 who would win the race (12.03s)

Verdict: FIX FIRST

✅ Keep doing
• Hook is live on frame 1: GO! with Cyrus already moving, and the title question is a clean pick-a-side prompt that stays up all reel.
• Distractions land one at a time with ~2s spacing: camera slime on Cyrus 1.0s, dancing slimes on Joy 3.3s, Cleo STRENGTH 5.1s, Rayleigh wakes 6.9s. Reads as intended, not chaotic.
• SPEED on Cyrus (mushroom) and STRENGTH on Cleo match their gummies.
• Rayleigh waking (! at 6.9s, poof at 7.3s) and closing on Cleo makes 8 to 10.5s a real race instead of dead time. Photo finish at 10.6 to 10.9s is good.
• Loop: cuts straight from the win back to the GO! start state.

❌ Fix
• 5.77 to 5.90s: Cleo turns to face LEFT, away from the rock, swings, and her sprite overlaps the rock as it breaks. The strike lands behind her. → Keep her facing right toward the rock, plant for the full beat, swing into it with the blade/shield meeting the rock edge (no overlap), and break the rock on the contact frame.
• 11.0 to 12.03s: CLEO WINS! is on screen only ~1.0s before the loop cut. → Hold it at least 1.5s (end at ~12.6s).
• 11.0 to 12.03s: the "!" of CLEO WINS! sits on top of Rayleigh's sprite. → Move the stamp clear of both racers (open track to the left, around y 1100 to 1200).
• 5.9 to 6.6s: rock debris is flat grey squares that drift. → Use rock-colored chunks that arc out and drop to the ground, then fade.
• 0.6 to 0.7s: GO! is still fading while SPEED! pops (two stamps at once), and SPEED! sits over Joy's sprite 0.8 to 1.4s. → Clear GO! before SPEED! appears; nudge SPEED! off Joy.

🎯 Priority order
1. Cleo's strike direction and overlap (5.77s)
2. CLEO WINS! hold to 1.5s+
3. Move CLEO WINS! off Rayleigh
4. Rock debris physics
5. GO!/SPEED! overlap

Target length: 12.6s, payoff at 10.9s
