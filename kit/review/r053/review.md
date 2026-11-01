Build review: r053 (19.9s)
✅ Keep doing
• Three-act structure (stick fails, shield stalls, creatine wins) is easy to follow and holds the best chest until last.
• Creatine gummy gives STRONG then POW at 13.5s to 15.5s. Power matches type, and the dragon's hoard reads as gummies.
• "WHICH CHEST DID YOU PICK?" end card with all three results and "Comment 1, 2 or 3" is a strong comment trigger.
• Loop is clean: the last frame cuts back to the opening three closed chests.

❌ Fix
• 0.0s to 2.5s: fully static (Hollow standing, closed chests, small caption); nothing moves until chest 1 opens at 2.5s → have the chests rattle or glow from frame 1 and open chest 1 by 0.8s.
• 7.5s to 12.0s: chest 2 is a plain shield icon, not a gummy → make chest 2 an ACV gummy that grants the SHIELD (stamp "SHIELD!" on pickup), and label it "ACV GUMMY" on the end card.
• 6.0s to 6.5s: "OOPS..." starts about 24px from the left edge, outside the 70px safe zone → move it right to at least x 90, or center it over the Hollow.
• 10.0s to 12.0s: 2s "STALEMATE..." with no motion → cut to about 1s.
• 2.5s to 3.5s, 7.0s to 8.0s, 12.0s to 12.5s: each chest-open interstitial plus fade costs about 1s → trim each by about 0.4s.
• 0.0s and 16.5s: "Comment your number" and the end card item labels (STICK, SHIELD, CREATINE GUMMY) are about 30px and 20px → enlarge to about 50px.
• 16.5s to 19.5s: 3s end card hold is fine for reading but trim to about 2.5s once labels are bigger.

🎯 Priority order
1. Motion and first chest open inside 1s.
2. Make the shield chest an ACV gummy.
3. Move "OOPS..." into the safe zone.
4. Trim stalemate and interstitials.
5. Enlarge prompt and end card labels.

Target length: 15s, payoff at 11s

Series note: if more chest reels follow, vary which number holds the winning gummy so "always pick 3" never becomes the pattern.
