# Safe-zone + hook spec (Bennett, Oct 28)

1. SAFE ZONE (1080x1920): unsafe = y < 250, y > 1500, x < 70, x > 1025 for 250<=y<=1110, x > 887 for 1110<y<=1500.
   All text, characters, key action and puzzle content inside. Backgrounds may stay full-bleed.
   Check with: python3 scratchpad/pixellab/safezone/audit.py out.jpg video.mp4
2. HOOK (the text at the top) is the most important thing: "a good hook makes or breaks a video".
   - Must stand out and be instantly readable on a phone.
   - Starts at y>=262, max 2 lines, big: PressStart2P 64-80px for the main line (never under ~56px),
     key word/line in a bright accent color (gold #FFD63C or the guild color), white for the rest.
   - Thick dark stroke (8-10px) plus a solid dark band or strong dark gradient behind it (alpha >= 200),
     high contrast against any background. No busy art directly behind the letters.
   - Keep it short (use the original post's hook words). Secondary line (if any) >= 34px and clearly
     secondary. Never a small news-headline/ticker style hook.
   - On screen from frame 0 and stays readable the whole video (don't fade it under overlays until the end card).
3. CHARACTERS big enough on a phone: focus guides 3x+ (~190px+), multi-character games >= 2x and bigger where
   possible, balls/orbs >= ~100px with readable faces, hidden targets findable at phone size. Integer scaling only.
4. Keep concept, beats, winner and puzzle answers unless told otherwise; one-frame puzzles keep exactly one
   valid frame, never reveal answers. Loudness about -14 LUFS, music baked in.
5. Use the shared hook module for a consistent look: safezone/hook.py -> hook_layer(lines, accent, color, sub) returns (layer, bottom_y); composite it last on every frame; content goes below bottom_y and above 1500.
6. Videos are NUMBERED #1-#108 (pixellab/numbering.json: num, manifest index, slot, hook, file). Output: scratchpad/pixellab/batch_v2/NNN_<slug>.mp4 (e.g. 001_which_jar_is_cyruss.mp4, slug from numbering.json 'file' without the MMDD_HHMM_ prefix) and append a line to batch_v2/log.txt: NNN | file | what changed | any outcome change. #4 (birth month) is cut: skip it.
7. Earlier safe-zone-only versions exist for #1-#3, #6-#12 in pixellab/batch_safe/ (scripts were edited in the fork dirs; batch_safe/log.txt says what changed). Start from those edits and add the hook.
8. GLOBAL RULE (Bennett): the Hollow is always the player (like Soap from CoD), never an NPC, and NEVER talks: no dialogue lines, speech bubbles or name-tagged quotes from the Hollow in any video. Emotes (sweat drop, "!", "?", hearts) are fine. If a video gives the Hollow lines, move them to a guide.
   Sam's canon (FAQ "Why the Hollow?"): the Hollow is the silent protagonist, no face, no backstory, no dialogue; transparent because he's the character YOU play. He's the player on day one, with four guides around him. So: never an opponent, rival, villain or NPC; never a "pick" option among guides; never speaks. He can be the one the viewer controls/roots for.
9. Guides must never be hidden behind props/foreground objects (Bennett on #105/#106). Draw characters above scenery or keep props out of their path.
10. METRICOOL (Bennett Oct 28): no Side Quest / "QUEST" CTA on YouTube, neither caption nor pinned/first comment. Schedule YouTube as its own post (providers youtube only) with the QUEST line stripped; FB/IG post keeps it; TikTok keeps its DM version. Never use the "No AI anywhere" line.
11. Never shrink characters below their current size to fit the safe zone; shrink panels/backgrounds or drop the hook sub line instead.
12. GUMMY POWERS (Bennett, global, applies to every video with gummy pickups/power-ups; must be OBVIOUS on screen):
   - Creatine (Vitality, Cleo blue): makes them STRONGER: can hit/shove others out of the way, break obstacles.
   - Mushroom / Energy (Cyrus orange): makes them FASTER (speed lines, dust trail).
   - Melatonin / Recovery (Rayleigh purple): STUNS everyone else, puts them to SLEEP for ~1s (Zzz over their heads, they stop).
   - ACV / Foundation (Joy green): SHIELD (approved by Bennett 4:17pm): green bubble that blocks the next hit/stun/slow and cures any debuff. Use this unless he says otherwise.
   Label each pickup briefly when it fires (e.g. "STRONG!", "SPEED!", "SLEEP!", "SHIELD!") so the effect is unmistakable.
13. Characters must stand on ground: never floating over backgrounds; props (torches etc.) on stands, never floating.

UPDATE Oct 29 (Bennett): the safe zone is a GUIDELINE for focus, not a wall. "Just because something's not in the safe zone doesn't
mean it can't exist. It just means it's not the thing people should focus on." Scenes fill the whole frame (no boxed scenes); keep
hooks out of the very top and keep the focus (characters, key action, text) inside the safe zone. Hook style and text rules:
S/pixellab/safezone/HOOKFADE_BRIEF.md ("Do what serves the video").
