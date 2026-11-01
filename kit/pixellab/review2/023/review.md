Build review: 023 (6.0s)
✅ Keep doing
• The title is the comment prompt, and the board stays empty as intended.
• The dragon sitting on a gummy hoard as the odd entry gives people something to argue about.
• Clean loop: rows slide out and the lineup shrinks away at 5.5 to 6.0s, mirroring the slide-in at 0 to 0.5s.
❌ Fix
• 1.0 to 5.0s: 4s with no state change beyond gummies bobbing. → Give each character one beat in turn, about 0.7s each, from their existing sprite animations (one at a time, left to right, dragon last).
• Name labels are about 30px tall at full res, in two staggered rows (CLEO, RAYLEIGH, JOY on top; CYRUS, DRAGON below). Unreadable on a phone, and the zigzag makes names hard to match. Characters are about 210px tall. → One row, each name centered under its character at about 50px, and scale the lineup about 1.3x.
• 0.5 to 5.5s: Joy holds a red apple above her head while the others have gummies. → Swap it for her gummy.
• 1.0 to 5.0s: the tier row fills are near-transparent, and rows C and D disappear into the brick wall. → Darken the row fill to about 70% so the empty board reads as a board to fill.
• Joy's staff reaches about 908px, into the lower-right 193px zone. → Shift the lineup about 30px left when enlarging.
🎯 Priority order
1. Fill the 1.0 to 5.0s dead stretch
2. Bigger names in one row, bigger lineup
3. Apple to gummy
4. Row contrast
Target length: 6s, payoff at 1s (full lineup visible; no ranking shown by design)
