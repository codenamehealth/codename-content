# Common rules for Oct 29 fix agents (read fully first)
S = /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad
Read: S/pixellab/safezone/HOOKFADE_BRIEF.md (all of it, incl. appended rules), S/pixellab/safezone/SPEC.md, S/pixellab/safezone/NOTES_part1.md (Bennett's notes, newest at bottom).
- Source = the current S/pixellab/batch_v3/NNN_*.mp4. Its render script + run command are in the reel's LATEST line of S/pixellab/batch_v3/log.txt. Copy the script into your own work dir (given below) and edit the copy; never edit another agent's dir.
- Before overwriting, copy the current file to S/pixellab/batch_v3/prev/ (don't clobber an existing prev copy: add a suffix).
- Output overwrites S/pixellab/batch_v3/NNN_<same slug>.mp4. Append one line per reel to batch_v3/log.txt starting "NNN | Oct 29 notes2: " with what changed, script path + run command, frame count, LUFS, anything uncertain.
- Audio: if timing unchanged, reuse audio with S/fork_hfg5/mux2.sh noaudio src_with_audio out (keeps every frame). If timing changes, remix (see mix.py used by other scripts) to about -14 LUFS, no repeating whoosh/alarm-like SFX, check it.
- Brand: the Hollow is the player, never an NPC/opponent, never talks, no teeth, no angry face. Pickups/payments are gummies, never coins/gold. Powers: creatine STRENGTH!, mushroom SPEED!, melatonin SLEEP!, ACV SHIELD!. No ACV GUMMY tags. Puzzles never reveal the answer; one-frame puzzles keep exactly one valid frame (verify + log). No em dashes. Joy never shows teeth.
- Guide art: only Syeda's sprites/animations that already exist in the project (or PixelLab animations previously built from her files that are already in use in approved reels). Never draw new code-built poses. If a needed action has no existing animation, say so in your report instead of faking it.
- Text: minimal. Soft-fade hook (hook_fade) or full-width strip (hook_band), no boxes. Safe zone = where NOT to put the thing people must find/read; scenery and characters can go there; scenes fill the frame.
- QA each reel: S/pixellab/safezone/audit.py sheet + full-size frames at the key moments; look at them. 2 CPU cores shared with other agents: render one video at a time, never wait >10 min on one command.
- Report back: per reel, what changed, frame count, anything uncertain, and any call Bennett should make.

## Music (added Oct 29 evening): Epidemic Sound pass
- Reels are moving from Adobe Stock beds to Epidemic Sound tracks (see MUSIC_EPIDEMIC_BRIEF.md). Before you re-mix a reel, check its latest batch_v3/log.txt lines: if it already has an Epidemic track (S/epidemic/tracks/...), re-mix with that same track file and offset/edit, never back to music_adobe.
- If it does not have one yet, mix as before; the music agent will move it to Epidemic after you finish. Always keep your events JSON path in the log line so the music agent can re-mix your SFX.

## Level change (Oct 29 5:25pm, Bennett: "maybe a little loud")
- Epidemic mixes: music bed ~3 dB lower vs SFX than first pass; integrated -15.0 LUFS (+-0.3), true peak <= -1.5 dBTP. Applies to every reel from now, including fix-agent re-mixes.

## Endings (Bennett Oct 29 6:19pm: "you keep cutting the ends off")
- Every payoff/end beat holds at least 2.0s readable before the loop. Never trim the ending to hit a length target; trim the middle instead.
- Credits: Bennett says we are using too many credits. Work lean: no exploratory renders, no wide seed searches unless needed, one final render per reel when possible.

## Recreations look (Bennett, Oct 30 3pm) - STANDING RULE
1:1 recreations copy the reference's FORMAT, MECHANICS and TIMING only, never its art style. Every recreation (races and box reels) gets the Code Name look from the first render: Liza's Realm backdrops/palette, castle stone/brick, Realm props (docks, logs, boulders, arches), the shadow as rich dark purple, gummies for pickups, swords/arrows not pencils or real-world objects, Syeda's sprites only. Reference: r01_DerujF_BHAA_bg (race), m06 v3 (stairs).
