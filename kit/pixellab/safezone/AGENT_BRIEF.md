# Brief for a safe-zone + hook agent (Code Name viral remakes)

You are fixing short vertical pixel-art videos (1080x1920, 30fps) for Code Name, a pixel-art gummy brand.
Root: /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad (call it S).

Read first, in full: S/pixellab/safezone/SPEC.md (the rules, items 1-11). Everything you need is there.

How each video was built:
- S/pixellab/numbering.json maps video number -> manifest index, slot, hook, file name.
- The original remakes are zips in S/pixellab/batch/<file>_remake.zip (contain the mp4); S/pixellab/batch/log.txt
  describes each one (manifest index | file | details | music).
- Render scripts + assets live in S/fork*/ (fork1-4, forkA, fork_a2-a11, fork_b5-b11), usually named rNN.py or vNN/
  (NN = manifest index or video number, check). Find them with grep -rli "<keyword from the hook>" --include=*.py S/fork*.
  Prefer the most recent safe-zone version if one exists (S/fork_sz*/).
- Render scripts draw frames with PIL and pipe to ffmpeg (libx264 veryfast crf 18, 1080x1920, 30fps).
  PIL gotcha: ImageDraw on RGBA does not alpha-blend; draw translucent shapes on a separate layer and alpha_composite.
- Hook: S/pixellab/safezone/hook.py hook_layer(lines, accent=None, color=(255,214,60), sub=None, ...) -> (RGBA layer, bottom_y). Composite LAST on every frame; content goes between bottom_y and y1500.
- Audio: if the new video has the same length/timing, reuse the old mixed audio: S/pixellab/batch_v2/mux.sh new_noaudio.mp4 old.mp4 out.mp4.
  If timing changes, remix with S/pixellab/mix.py (events json; see a recent fork dir for an example) at about -14 LUFS, and vary the music track.
- Good recent examples of finished work: S/fork_sz44/ and S/fork_sz38/ (scripts + audit sheets), and the lines in S/pixellab/batch_v2/log.txt.
- Copy the source script into your own work dir S/fork_<yourname>/ and edit the copy; never edit other dirs.

QA (be efficient with image reads, but never skip QA):
- Run python3 S/pixellab/safezone/audit.py out.jpg video.mp4 (4-frame sheet with the unsafe area in red) and look at it.
- Look at ONE full-size frame at the busiest moment (extract with ffmpeg) to check hook readability and character size.
- Fix and re-check only what failed. Don't re-read images you've already seen.

Output: S/pixellab/batch_v2/NNN_<slug>.mp4 and append one line to S/pixellab/batch_v2/log.txt
(NNN | file | what changed | any outcome change). Only 2 CPU cores and one other agent is rendering: render one video at a time.

Content rules in this pass: no content changes EXCEPT these, which you must fix now if present:
the Hollow never talks or has speech bubbles, and is never an opponent/NPC/racer/pickable option/prize (remove him from that role);
coins/gold pickups become gummies (no "gold rush"); guides never hidden behind props; never shrink characters.

Final report (short): per video, path, what changed, anything uncertain or any outcome change (winner, length).
