Build review: m01_DaG5nn5v8AP "Who escapes the shadow" (56.63s, ref 54.27s)

Verdict: FIX FIRST. Fidelity 6/10.

✅ Keep doing
• Grid, corridor serpentine, dark brick doors, gummy in the left room, checker exit: same 19x22 layout as the ref.
• Box speed 296px/s at u=46 = 6.43u/s (ref 6.4u/s), always 45 degree diagonals in every dense window checked.
• Flood schedule tracks the ref closely (chamber tops 0.3-10s, hall to ~24s, corridors fast after).
• Both deaths are honest crushes (40.63s Rayleigh pinned to the east wall by the B front; 42.93s Cyrus pressed into the right column floor). Exit brick is broken (Cleo STRENGTH, 50.97s), not opened.
• Last 10s stays open: Cleo (STRENGTH) leads at 50-51s, Joy passes at ~52s, Joy wins 53.63s with Cleo alive behind. Good mirror of the ref's red vs sword-holder finish.
• Creatine gummy art, STRENGTH word, hook is not a generic pick hook, no hashtags, no em dashes on screen.

❌ Fix
• 0.17s to 0.20s: Joy and Cyrus teleport ~78px through the solid divider walls into chambers 2 and 4 on the first motion frame. Chambers 1 and 3 sit empty for the rest of the run. → Spawn each box fully inside its own chamber (box right edge at least 0.05u left of the divider; START x 5.55 plus JIT 0.25 overlaps the wall, inferred cause) and assert frame 0 positions equal sim step 1 within one frame of travel.
• 1.0s to 4.4s: all four gates are gone (3 of 4 by 1.9s). Ref: red 2.5, cyan 4.5, green 10.5, yellow 15-16s. Leaves 4.4s to 13.0s with no brick event at all (8.6s dead). → One box per chamber plus gate HP raised (3 to 4 hits per cell) and seed-search for gate breaks within 1.5s of the ref schedule.
• Board is 874x1011px (u=46) vs ref 974x1128 (u=51.26): 20% less area, 412px empty under the roster. Repeats the "board too small" complaint. → Use the ref placement exactly: u=51.26, origin (53,396).
• Faces 28px (about 10pt on a phone): identity reads by border colour only. → 40px faces (+43%, 0.78u) with the larger board.
• 47.33s gummy pickup is 13s later than the ref sword (34.2s) and never knocks anyone out; the STRENGTH spike lands at 84% of the run. → Seed-search for a pickup between 32-37s.
• 52.16s: Cleo's gummy badge (drawn outside the box, top right) overlaps Joy's box on a 3px corner near-miss; reads as a STRENGTH touch with no knockout. → Draw the badge inside the box bounds, or reject seeds with a STRENGTH near-miss under 8px.
• 1.2s, 39.17s (D3) and 50.97s (exit break): crunch SFX lift under 2dB over the bed. → +5dB on crunch, or 3dB bed duck for 150ms.

🎯 Priority order
1. Kill the 0.2s teleport, one guide per chamber.
2. Gate HP and seed to the ref break schedule (fixes the 4-13s dead stretch).
3. Ref board scale (u=51.26) and 40px faces.
4. Gummy pickup at 32-37s.
5. Gummy badge inside the hitbox.
6. Crunch SFX level.
Target length: 56.5s (ref 54.3s plus the 2.5s pose hold), payoff (win) at ~53.3s.

---

## Appendix A: beat-by-beat (ref vs ours)

| Beat | Ref | Ours | Status |
|---|---|---|---|
| Start, all move | 0.2s, one box per chamber, down-left in sync | 0.2s, but Joy and Cyrus snap into the next chamber; 2 boxes per chamber | CHANGED (bug) |
| Gate 1 breaks | red 2.5s | 3 gates gone 1.0-1.9s | CHANGED (too early) |
| Gate 2 | cyan 4.5s | (above) | CHANGED |
| Gate 3 | green 10.5s | (above) | MISSING as a beat |
| Gate to right room | yellow 15-16s | bottom brick 2.45s, rest 4.4s | CHANGED (13s early) |
| D1 to corridor A | 17.5s | cracks 13.0-14.1s, last cell 18.0s | MATCH (close) |
| Flood chamber tops / hall | 0.3-10.4 / 10.4-23.7s | about the same | MATCH |
| D2 | 23.3s | 23.9s, last cell 26.0s | MATCH |
| Flood corridors A, B | 26.4-40.7s | about the same | MATCH |
| D3 to left room | about 33s | 37.6-39.2s, rest 44.6-45.4s | CHANGED (6s late) |
| Pickup | sword 34.2s | gummy 47.33s, "CLEO: STRENGTH!" stamp | CHANGED (13s late) |
| Deaths | 36.9s, 37.7s by sword | 40.63s, 42.93s by flood crush | CHANGED (cause and +4s); matches the client's crush belief |
| Exit brick | 48.5s | top cell 50.97s by STRENGTH, bottom 53.6s | MATCH (2.5s late) |
| Win | red 53.27s, sword-holder right behind | Joy 53.63s, STRENGTH holder alive behind | MATCH |
| End | freeze 1.0s, no text | freeze 0.5s, then JOY WINS! pose card 54.13-56.63s | CHANGED (intended brand tweak) |

Side-by-sides (ref left, ours right), one per second: _cmp/sbs/sbs_00..56.jpg, grouped as _cmp/grid_00..14.jpg.

## Appendix B: physics by eye
- Checked frame by frame: 0-0.8s (_cmp/dense_start.jpg, dense_snap.jpg), 1.0-3.0s gates (dense_gates.jpg), 40.2-41.1s (dense_kill1.jpg), 42.5-43.25s (dense_kill2.jpg), 47.0-47.8s pickup (dense_pickup.jpg), 50.4-54.3s finish (dense_win.jpg), 51.93-52.23s near-miss (dense_contact.jpg). The rest was checked at 1fps only, so I cannot rule out a single-frame glitch outside those windows.
- Teleport through walls at 0.20s (Joy ch1 to ch2, Cyrus ch3 to ch4), faint trail remnants left in ch1 and ch3 at 0.27-0.33s.
- No steering seen: every box keeps a 45 degree heading between contacts in the dense windows.
- No pass-through seen after 0.2s. Rayleigh reaches the right room at ~2.5s through the gap from the broken bottom gate brick (legit).
- Kills: both pinned. Rayleigh's box is half below the B flood edge when X'd (40.63s), so it reads as a corner squeeze rather than flush; acceptable. The X'd box draws on top of the flood until ~41.1s (ref: covered by the flood). Minor.
- 52.16s Joy and Cleo pass corner to corner with about 3px between the boxes; the gummy badge overlaps Joy. Physics is consistent (no contact), the read is not.

## Appendix C: phone legibility
- Board: ours x 103-977, y 425-1436 (81% width, 53% height). Ref x 53-1027, y 396-1524 (90% width, 59% height). Ours is about 10% smaller per side, 20% less area.
- Dead space: 412px of plain background under the roster (y 1508-1920), plus the board inset 50px from the ref on each side.
- Faces 28px = 0.61u (ref squares 26px = 0.51u). At phone width the face art is a smudge; you can tell guides apart only by border colour (green, blue, orange, purple, all distinct). Recommend 40px at u=51.26 (0.78u, corridor 154px so still 3.8 box widths of room).
- Roster: RAYLEIGH chip runs to x=1048 (in the right 12%). Shrink chips to fit x 75-945.
- The exit (x 925-1027 at ref scale) sits under the right-side action rail, same as the ref. Optional tweak: mirror the board horizontally so the exit and win land bottom left. Not required for a 1:1 copy.

## Appendix D: audio (ffmpeg ebur128)
- Integrated -15.3 LUFS (target -15 +-0.3: passes at the edge). True peak -2.8 dBTP (pass). Track is mono AAC (minor).
- First 0.5s: music is already in (RMS -12.4dB in the first 0.1s). Pass.
- SFX lift over the bed in the 1.5-8kHz band (measured, not listened): win sting +18dB, powerup +7dB, D1 crunch +7dB, D2 +6dB, kill squish/buzz +3dB broadband. Weak: gate crunch 1.2s +0.9dB, D3 39.17s -1.9dB, exit break 50.97s +1.8dB. The exit break is a story beat and is likely masked.

## Appendix E: brand checks
- Our four guide faces only: pass. Pickup is the creatine gummy (pick_cre.png): pass.
- Text: hook y 255-385 (inside safe zone), stamp mid-board, JOY WINS / DID YOUR GUIDE WIN? inside the board area: pass. Roster chip in right 12%: minor fail.
- No hashtags, no em dashes, hook is not CHOOSE A GUIDE: pass.

## Rubric scores
1 Hook: premise and board visible at 0.0s, motion at 0.2s, but the first motion is the teleport. 2/3 once fixed, 1/3 now.
2 Dead time: 4.4-13.0s (no brick event). 30.0-37.6s has flood chase motion only; acceptable since the ref has a similar chase.
3 Payoff: win at 95% is the format; the mid spike (pickup) needs to move back to ~63% like the ref.
4 Legibility: board and faces too small (see C).
5 Stamps: STRENGTH stamp is clear. Kills only show a tiny X and the roster OUT; optional matching "CRUSHED!" stamp, not in the ref.
6 Ending: 2.5s pose hold, hard cut back to the start state loops fine.
7 Comment trigger: DID YOUR GUIDE WIN? at the end; hook implies the pick. OK.
8 Gummy: STRENGTH smashes the exit brick in one hit (reads). Never knocks anyone out.
Series note: rotate winners across the race reels.
