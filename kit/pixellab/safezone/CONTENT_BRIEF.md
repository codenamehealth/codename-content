# Brief for a content-notes agent (Code Name viral remakes)

Root S = /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad

You are applying Bennett's (the founder's) review notes to short vertical pixel-art videos (1080x1920, 30fps).
Every video already has a safe-zone + hook version in S/pixellab/batch_v2/NNN_<slug>.mp4. Start from THAT version:
its render script is in S/fork_sz*/ (find it with grep -rl "<slug or hook keyword>" S/fork_sz*/ or check the log line
in S/pixellab/batch_v2/log.txt). Copy the script into your own work dir and edit the copy.

Read first, in full:
1. S/pixellab/safezone/AGENT_BRIEF.md (how videos are built, hook.py, audio/mux, QA). Its "no content changes" line does NOT apply to you.
2. S/pixellab/safezone/SPEC.md items 1-13 (safe zone, hook, sizes, Hollow rules, gummy powers, nothing floating). Every output must still meet all of them.
3. Your videos' notes in S/pixellab/safezone/NOTES_part1.md (search "#NN " for each of your numbers; a number can have more than one line, including "follow-up" lines from earlier passes). Apply every note for your videos.

Gummy powers (SPEC 12) apply to every video with gummy pickups or power-ups: make each gummy's effect match its type and be OBVIOUS
(creatine STRONG: shoves/hits others or smashes obstacles; mushroom SPEED: speed lines + dust; melatonin SLEEP: everyone else
stops ~1s with Zzz; ACV SHIELD: green bubble that blocks the next hit/sleep/slow), with a short pop label when it fires.

Animation: Syeda's sprites + existing PixelLab animations in S/pixellab/maze/anim, S/fork*/ dirs. If you truly need a new motion,
you may generate it with PixelLab (S/pixellab/jobs.py: upload + run_one with animate_image_pixminimax, see S/cyrus_gif/gen.py for a
working example), up to ~6 generations per video; check quality closely and never use a bad-looking result.

Quality bar is high (Bennett: "I'd rather pay if it means it's done right"). For each video: audit.py sheet + look at 2-3 full-size
frames at key moments (the note's moment especially). Puzzles never reveal answers; one-frame puzzles keep exactly one valid frame.
Audio: reuse via S/pixellab/batch_v2/mux.sh if timing is unchanged, else remix with S/pixellab/mix.py at about -14 LUFS, varied track.

Output: S/pixellab/batch_final/NNN_<same slug as batch_v2>.mp4, and append a line to S/pixellab/batch_final/log.txt:
NNN | what you changed for each note | outcome changes | anything you could not do and why.
Only 2 CPU cores and another agent is rendering: render one video at a time.

Final report (short): per video, path, how each note was addressed, anything uncertain.

Reel-review lessons (apply to every video): opening frames must already have motion (no static title/idle line-up longer than ~0.5s);
endings that hold a static card should cut back to the opening state so the reel loops; elimination/OUT/win moments get big
high-contrast stamps (same weight as the win stamp); never let two stamps overlap; power-ups must not fire in a fixed repeating order.

Audio: never repeat the same bright 8-bit SFX (whoosh_8bit etc.) on a fixed short interval through a reel; Bennett said a metronome of whooshes over the music sounds like a fire alarm. SFX on real events only.

Loudness: mix.py can land at -15 to -16 LUFS on short reels; measure every output and if it's below about -14.5, run S/fork_rc2/loudfix.sh to bring it to about -14.
