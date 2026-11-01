# Brief: soft-fade hook + less text + full-bleed pass (Code Name viral remakes, Oct 29)

Root S = /tmp/claude-0/-home-claude/3d9a853e-960c-501e-b487-63abffb4f487/scratchpad

Bennett watched the full recut set. His notes, verbatim:
- "The hooks are way too big. Most of them are taking up a 3rd of the screen. The box around it probably needs to go."
- "Just because something's not in the safe zone doesn't mean it can't exist. It just means it's not the thing people should focus on.
  The swimming race for instance, should go the full length. It looks goofy as a square."
- "You also keep putting way too much text on there. Plant the tree or chase the loot, you don't need text underneath them.
  People can figure out which ones which. That's an issue with almost all the videos."
- "The text takes up 50% of the video."
- On the hook style: "Soft fade is fine. It's not a hard rule that it needs to be 1 or two lines. That's where you keep messing up.
  Do what serves the video."

So this pass is judgment, not a checklist. For each reel ask: what does a viewer need to read to get it in one second, and what is
the picture already telling them? Keep that text; cut everything else.

## What to change in each reel
1. Hook: replace the boxed hook (hook_layer / hook_layer2 / custom band) with the approved soft fade:
   `from hook import hook_fade` (S/pixellab/safezone/hook.py) -> `HOOK, HB = hook_fade(lines, accent=i, color=(r,g,b))`, composited last.
   No box, no border. Second approved style (Bennett: "This looked nice too"): a full-width dark translucent strip edge to edge
   behind the hook (no rounded corners, no border), as in the original race reel S/hookmock/approved_band_race_original.png
   (hook_band below). Pick whichever serves the reel: fade over open scenes, strip over busy ones. Use the hook wording that serves the video (usually the post hook; shorten it if a shorter version reads better).
   Number of lines is whatever serves the video, but the hook should be a hook, not a paragraph.
2. Cut text that doesn't earn its place: labels under things the picture already shows (LOOT / TREE, names under obvious guides,
   "PICK ONE" plates that repeat the hook), separate "COMMENT ..." lines (the caption asks for comments) unless the comment ask IS the
   hook or the game, sub-lines that repeat the hook, small explainer lines, extra banners. Keep text that is the game or the payoff:
   timers, scores/standings when the format needs them, big OUT / WIN / power stamps (keep them short), a puzzle's single instruction
   if the hook doesn't already say it, end-card question only if it adds something. When unsure, cut it and look at the frame.
3. Full-bleed scenes: no scene sitting in a box/panel over a dimmed or blurred background. Extend the scene to fill the 1080x1920 frame
   (pool, track, river, arena, panels stacked edge to edge, etc.). Scenery may run into the unsafe areas; only the focus (characters,
   the key action, any text) must stay inside the safe zone (SPEC.md). Use the space the smaller hook frees: move content up and/or
   make characters bigger if it helps.
4. Keep everything else exactly: winners, puzzle answers (never revealed), one-frame puzzles (still exactly one valid frame; verify
   and log the frame index), loops, gummy powers, Hollow rules (player, never NPC/opponent, never talks), no gold/coins, no em dashes.
   Reuse the existing audio with S/pixellab/batch_v2/mux.sh when timing is unchanged; otherwise remix with mix.py (~-14 LUFS, check it).

## Sources and output
- Source = S/pixellab/batch_review/NNN_<slug>.mp4. Its render script is named in that reel's latest line of
  S/pixellab/batch_review/log.txt (fork_rc*/vNN/ or fork_c*/...; the steal/plat/race extras too). Copy the script into your work dir
  and edit the copy. Never overwrite batch_review.
- Output S/pixellab/batch_v3/NNN_<same slug>.mp4 (extras: steal_3_gummies.mp4, plat_pause_when_he_lands.mp4, race_v3.mp4), one line
  per reel in S/pixellab/batch_v3/log.txt: NNN | text cut | hook lines | full-bleed change | anything uncertain.
- What not to do: S/hookmock/too_much_text_018.png (hook + sub + instruction + comment line = five lines; Bennett called this out).
- Examples of the target look (hook C = soft fade): S/hookmock/sheet_swim.jpg (swim pool full length), sheet_nail.jpg, sheet_loot.jpg.

## QA per reel
S/pixellab/safezone/audit.py sheet + one full-size frame at the busiest moment. Check: no box around the hook, no text that the picture
already says, scene fills the frame, focus inside the safe zone, loop intact. Never wait on one command more than ~10 minutes.
Several agents render at once on 2 CPU cores: render one video at a time.

Consistency rule (Oct 29, from the approved #37): no 'ACV GUMMY' tags anywhere; Syeda's ACV gummy art stands on its own. Let the end question replace the hook text (in the same fade) instead of adding an end plate.

Audio mux: use S/fork_hfg5/mux2.sh (keeps every video frame); S/pixellab/batch_v2/mux.sh's -shortest can drop the last frame. #99 must stay exactly 300 frames / 9.99s.

Bennett's reel principle (Oct 29): hook them with something interesting, get them invested in finding the thing they expect, then break the expectation with something completely random that makes people feel good. When a reel has a slow stretch, give that part its own interesting action (e.g. #19 top Joy keeps meeting new disasters, #39 a swamp monster), never a long wait.
Safe zone (Bennett Oct 29): it's where NOT to put the thing people must find or read; scenery and characters can be there. Never leave black boxes or empty blocks there.

Oct 29 2:13pm additions (Bennett):
- The creatine power word is always STRENGTH (STRENGTH!), never STRONG, on every reel.
- Give the audience a job (spot the cheater, look for X, count Y, or a real question), let them get invested in it, then break what they thought they knew. Example he gave: race hook "CAN YOU FIND THE CHEATER?"; viewers spot Cyrus; end cutscene shows Rayleigh paid off the slime to move out of Cyrus's way.
- Guides do the action their option describes (farming = Joy farming), using Syeda's existing sprites/animations only.
- Characters stand on the ground (no floating); don't over-zoom.
- Oct 29 2:19pm: never stand characters on water or a fountain (Bennett: "you keep making them float on the fountain"); they stand on solid ground. Joy's face only as Syeda drew it (no edited/creepy smiles). Distractions/gags happen one at a time, clearly readable, never all at once.
- Oct 29 2:37pm: no more "CHOOSE YOUR GUIDE" / generic "pick one" hooks; the hook gives a job or asks a real question. Physics must look real: no snapping, teleporting or weird movement (stacking, falling, bouncing obey gravity and momentum).
- Oct 29 2:53pm: SHOVES: whenever a character shoves/hits, show a clear shove/attack animation (existing Syeda/PixelLab attack frames) and the shover stops for about a second to perform it. Physics-style reels (escapes, balls, falling blocks, eating glass) need perfect, believable physics. Joy talking = Syeda's talking sprite only, never an edited mouth. Busy backgrounds get calmed (dim/blur slightly) so the focus reads.
