Build review: r024 (9.0s)
✅ Keep doing
• Rows stack in one by one from 0.5s to 2.0s, so the build is a mini reveal, and the full board is up by 2.5s. Good pause-and-pick format.
• Comment prompt "Comment your combo" is on screen from 2.0s with an example, and the board sits inside the safe zone (right edge clears the 193px lower-right column).
• Four guides read clearly at phone size.

❌ Fix
• 0.0s to 0.5s: title over a still tavern, zero motion (edges.jpg top row is eight identical frames) → start with the guide row already sliding in at frame 1, or drop the empty first beat.
• Realm row (!, @, #, $) and example "2 B @ X": in a comment, "@X" tries to tag a user and "#" starts a hashtag, so the combo the reel asks for breaks in the comment box → relabel the realm row with plain characters (5, 6, 7, 8 or E, F, G, H) and update the example to match.
• 2.5s to 9.0s: 6.5s static hold with no state change → add a highlight that hops one cell per row every 0.5s, slot-machine style, and freezes on a random combo near the end. Viewers pause to "lock in" theirs and rewatch to land a different one.
• Gummy row (0.5s on): each cell is led by a potion bottle with the gummy tucked beside it, so the row labeled GUMMY reads as potions → make the gummy the hero icon and drop or shrink the bottle.
• Item X: the glowing gold blob reads as a gold nugget at phone size → swap for a gummy or a clearly non-currency item.
• Row labels GUIDE, GUMMY, REALM, ITEM are about 24px tall and the realm thumbnails are hard to tell apart at phone size; "LIKE 2 B @ X" is small → bump labels to about 40px and give realms a one-word caption.
• Premise: title asks "which vibe do I give off" but the CTA says "your combo" → pick one framing so commenters know whose vibe they are describing.
• Loop: last frame is the full board, first frame is the empty title, so the rebuild replays cleanly. Keep it.

🎯 Priority order
1. Replace @ and # in the realm keys and the example
2. Add the hopping highlight during the hold
3. Motion in the first frame
4. Gummy as the hero icon, swap item X
5. Label and realm legibility
6. Align title and CTA framing
Target length: 8s, payoff at 6.5s (highlight lands on a combo)
