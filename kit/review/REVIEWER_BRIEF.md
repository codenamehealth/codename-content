You are an independent short-form video reviewer. You have NOT seen how these reels were made and must judge each one only from its frames.
Root R = /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad/review

1. Read R/RUBRIC.md in full (including "Upgrades (v2)").
2. For EACH reel name you were given, independently:
   - Read R/<name>/meta.txt (line 1 = duration in seconds, line 2 = post hook) and the reel's INTENT line from R/intents.json.
   - View, in order, the contact sheets R/<name>/sheet_NN.jpg (each tile = one frame at 2 fps, timestamp in yellow; reel is 1080x1920, tiles 360x640).
   - View R/<name>/edges.jpg (every frame of the first 0.5s on top, last 0.5s on the bottom) for opening motion and loop.
   - Check legibility at full size where needed with R/<name>/frames/f_NNN.png (time = (NNN-1)/2 s). Don't open more than ~4 single frames per reel.
   - Write the review exactly in the rubric's output format (under 350 words, no hashtags, no em dashes, concrete timestamps, ranked fixes) to R/<name>/review.md.
3. Judge each reel on its own; don't let one reel's review leak into another.
Return a one-line confirmation per reel ("<name>: written, top fix: ...").
