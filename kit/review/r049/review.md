Build review: r049 (10.6s)
✅ Keep doing
• Clear one-line challenge, a visible draining timer bar (5 to 1, 2.5 to 7.0s), and the bar turning red as it runs out.
• The A to J / 1 to 8 grid coordinates are a great comment mechanic: answers are short and easy to type, and they spark arguments.
• No answer reveal. The reel ends on the question as intended.

❌ Fix
• 0.0 to 2.5s: blank board, then a 3, 2, 1 countdown. A quarter of the reel shows no puzzle, so scrollers leave before the gummies appear (edges.jpg: frames 0 to 6 are an empty tan box) → put the full grid on screen at frame 0 and run the timer from there. Cut the countdown, or overlay a quick "3 2 1" on top of the grid.
• 2.5 to 7.0s: I could not find the odd gummy in the provided 360px frames, even zoomed 3x. The only candidate was G3 (its highlight pattern may be mirrored), and I only saw that at 6x zoom. This is inferred, not confirmed. If the difference is that subtle, phone viewers will fail and feel dumb, not smart → make the odd gummy differ in one bold way (shape notch, color shift or missing shine) that still reads at phone size.
• 7.5 to 8.0s: "TIME'S UP!" is small red text inside the thin timer bar → make it a big centered stamp over the grid for 0.6s.
• 8.5 to 10.6s: "COMMENT WHERE IT IS (LIKE B4)" is the smallest text in the reel and arrives at 80% → make it a full-width line at title-subline size, and show it from about 1s under the title.
• Loop: the last frame (full grid) cuts to an empty board and a countdown on replay → once the grid opens the reel, the loop is seamless, because the last frame matches the first.

🎯 Priority order
1. Grid on screen at frame 0, cut the countdown
2. Confirm the odd gummy reads at phone size
3. Comment prompt early and larger
4. Big "TIME'S UP!" stamp

Target length: 8s, payoff (time's up) at 5.5s
