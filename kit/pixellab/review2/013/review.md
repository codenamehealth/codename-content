Build review: 013 (9.3s)
✅ Keep doing
• Hook is moving from frame 1: the lever pulls within the first 0.2s (edges.jpg) and the reels spin under the "ONLY 1%" line, which is the right feel-smart framing.
• The jackpot never shows in any 2 fps sample and is never highlighted, as intended.
• 7.0 to 8.0s near miss is the best beat: two gummies lock, then the third reel ticks from Cleo to Cyrus. SO CLOSE! lands right on it.
• Perfect loop: the end state (two gummies plus Cyrus) is the start state, and the lever pulls again.
• No dead time; the 8.0 to 9.3s hold is short.

❌ Fix
• Spin section, 0.5 to 7.0s: if the jackpot is held for a single video frame (33ms), pausing on it is close to impossible on Reels or TikTok, which have no frame stepping. Viewers who can't land it feel dumb, not smart → hold the three-match for 3 to 4 frames (about 0.1s). Still never highlighted.
• 0.5s, 1.5s, 2.0s, 2.5s, 4.0s, 5.0s: one reel symbol is a red apple, not a gummy → swap it for the ACV gummy.
• 8.0 to 8.9s: SO CLOSE! is yellow on the machine's gold trim and is the lowest-contrast text in the reel → put it on a soft dark strip, or move it up into the dark area just under the reel windows.
• Whole reel: no on-screen comment prompt → optionally change SO CLOSE! to "DID YOU HIT IT?" so the near miss asks the viewer directly. Keep it one line.
• Minor: the machine sits left of center and the lever ball touches the right 55px margin. It isn't text, so leave it unless you're already re-rendering.

🎯 Priority order
1. Hold the jackpot for 3 to 4 frames so a pause can catch it.
2. Swap the apple symbol for a gummy.
3. Contrast strip behind SO CLOSE!, or swap it for the comment prompt.
Target length: 9s, payoff at 7.5s
