# Brief for a review-recut agent (Code Name viral remakes)

Root S = /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad

An independent reviewer watched each finished reel and wrote notes. Your job: recut each assigned reel to fix what the review
found, after vetting. Bennett (the founder) reviews your recuts tomorrow, side by side with the current version, so quality matters
more than speed, and each change must be a clear improvement.

Read first, in full:
1. S/pixellab/safezone/AGENT_BRIEF.md (how videos are built: scripts, hook.py, audio/mux/mix, QA). Its "no content changes" line does NOT apply.
2. S/pixellab/safezone/SPEC.md items 1-13 (safe zone, hook, sizes, Hollow rules, gummy powers, nothing floating). Still binding.
3. S/pixellab/safezone/CONTENT_BRIEF.md (gummy powers + the "reel-review lessons" at the end).
4. For each reel NNN: S/review/rNNN/review.md (the review), S/review/VETTING.md (lines for that reel and the cross-reel lines: they
   override the review), S/review/intents.json (the reel's intent), and every line for #NNN in S/pixellab/safezone/NOTES_part1.md
   (Bennett's own notes; they always win over the review).

Source version: S/pixellab/batch_final/NNN_*.mp4 if it exists, else S/pixellab/batch_v2/NNN_*.mp4. Find its render script
(grep -rl the slug or hook in S/fork_c*/ S/fork_sz*/ S/fork_fix*/; the log lines in S/pixellab/batch_final/log.txt and batch_v2/log.txt
name the dirs). Copy the script into your own work dir and edit the copy. Never overwrite batch_v2 or batch_final.

Vetting rules (apply before changing anything):
- Never contradict Bennett's notes, the intent, or SPEC. Never reveal a puzzle answer. One-frame puzzles keep exactly one valid frame.
- If Bennett said he loves/approved a video, keep its concept, winner and feel; apply only fixes for bugs, rule violations
  (Hollow, gummy powers/types, gold coins, safe zone, legibility) and the universal lessons below.
- Do not redraw or replace Syeda's or Liza's art. The ACV gummy is Syeda's apple-shaped gummy: keep it, add a short
  "ACV GUMMY" label on first appearance and a gummy shine so it reads as a gummy.
- Ignore series-level notes (rotate winners etc.).
Universal lessons (apply to every reel where relevant):
- Motion from frame 0 (no static title/countdown/line-up > ~0.5s; a countdown may run over moving action, max ~1s).
- End: hold the result/question ~1.2-1.5s, then cut back to the opening state so it loops seamlessly (check first vs last frames).
- Payoff earlier: for reels over ~20s, cut dead stretches so the payoff lands by ~60-70% and total length drops, without breaking the
  story (re-simulate if needed; keep the same winner). Don't cut below what the concept needs.
- Comment prompt early (from ~0.5-1s), big, one line, matching the hook/caption.
- Big high-contrast stamps for OUT/eliminations/rule events; no overlapping stamps; small text (<~44px at 1080) made bigger or cut.
- Gummy powers match type (creatine STRONG, mushroom SPEED, melatonin SLEEP stops everyone else with Zzz, ACV SHIELD), never a fixed
  repeating order, no other power names. No "z"/Zzz marks for anything except melatonin sleep.

QA per reel: audit.py sheet, 3 full-size frames (opening, payoff, ending), first vs last frame for the loop, ffprobe duration.
Audio: remix with S/pixellab/mix.py at about -14 LUFS when timing changes (keep the same music track unless the old one is reused a lot).

Output: S/pixellab/batch_review/NNN_<same slug>.mp4 and one line per reel in S/pixellab/batch_review/log.txt:
NNN | fixes applied (by review point) | fixes dropped and why | outcome changes (length, winner) | anything uncertain.
If a reel needs no changes after vetting, don't render it; log "NNN | no change needed | why".
Only 2 CPU cores and another agent is rendering: render one video at a time.

Final report (short): per reel, path or "no change", the 2-3 most important changes, anything uncertain.

Added after checking the first recuts: the small line under the hook ("Follow it. Comment A-D", "Comment your time") is still too small.
Comment prompts must be at least 44px tall at 1080 wide, on their own dark plate if needed (or merged into the hook band as a real second line).
Guides who appear in a scene should be at least 4x (about 250px tall) unless the format needs many characters on screen.

Added Oct 28 7:40pm: anything Bennett asked for in a reel's spec (NOTES_part1.md, intents.json, or the reel's line in VETTING.md) is never removed because a review says so. If a review point conflicts with his spec, keep his spec and log the dropped review point. Before removing any element, grep his notes and the intent for it.

Audio: never repeat the same bright 8-bit SFX (whoosh_8bit etc.) on a fixed short interval through a reel; Bennett said #2's metronome whooshes over the music 'sounds like a fire alarm'. Use SFX on real events only.

Loudness: mix.py can land at -15 to -16 LUFS on short reels; measure every output and if it's below about -14.5, run S/fork_rc2/loudfix.sh to bring it to about -14.

Agents: never wait on one command more than ~10 minutes; if a render or tool hangs, kill it and move on (an agent stalled 70+ min on Oct 28).
