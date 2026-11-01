Build review: r011 (21.4s)
✅ Keep doing
• Opening moves: in the first 0.5s the card flips open from a thin line into silhouette 1. The premise reads instantly.
• The named four-guide lineup gives the answer options without spelling anything out. Answers are never revealed, so replays stay alive.
• The draining timer bar and a card flip each round (3.5s, 7.0s, 11.0s, 14.5s) set a clear rhythm.
• The 1 to 5 end card is an easy comment, and all UI is inside the safe zone.

❌ Fix
• Each round runs about 3.5s, and only the timer and "?" particles move. That's 17.5s of near-identical holds. → Cut each round to 2.5s. Pausers lose nothing, and skimmers stay.
• 18.0 to 21.4s: 3.4s static end card. → Hold 1.5s, then collapse it into the thin vertical line from 0.0s so it loops into the round 1 flip.
• "Comment your score" first appears at 18.0s (84%). → Make the banner subline "COMMENT YOUR SCORE" from 0.0s.
• Text around 24px at full size: the "PAUSE IF YOU NEED MORE TIME" bar label, the lineup names, and "5/5 earns the golden gummy". → Raise to at least 40px, or drop the pause label.
• Lineup portraits are about 180px tall, small next to the 580px card. → Scale the lineup about 1.3x into the empty space above 1500px.
• 18.0s: "HOW MANY CAN YOU GET?" sits right above "HOW MANY DID YOU GET?" → Hide the banner subline on the end card.
• Optional: a "TIME!" stamp when the bar hits red, before each flip.

🎯 Priority order
1. Shorten rounds to 2.5s.
2. Move "comment your score" into the opening banner.
3. Shorten the end card and loop it into the opening flip.
4. Enlarge the small labels and the lineup.

Target length: 14s, payoff (round 5 and the comment card) at 10s
