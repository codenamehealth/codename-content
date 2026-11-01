Build review: m06_DMOEx9VvQTm (70.9s)

Verdict: FIX FIRST. Two of the client's three standing complaints are back: the board is small with dead space above and below it, and Rayleigh is the only box left for the last 11.2s. Physics is clean. Audio meets spec.

✅ Keep doing
• Mechanics match the reference: staircase, pencil tips that kill, solid rising water, X markers left on the board, one-box exit slot. The water timing scales correctly (11.8 px/s on a 920 px board is about 16 px/s at the reference's 1270 px).
• Pencil deaths are real touches. At 16.50 (Cyrus) and 36.47 (Cleo) the box meets the tip cone and freezes there. The nearest non-lethal pass is 11 px (5.9s, 8.0s), so no near-miss looks like a hit.
• Physics checks pass. Direction changes without contact: 0. Wall overlap frames: 0. Max movement 6.7 px/frame at a constant 200 px/s. No teleports.
• Joy's crush at 56.73 is a real pin: her top edge (y 666) is against the step's underside and the water is at her bottom edge.
• Hook WHO OUTRUNS / THE WATER? sits in the soft top fade from frame 0, at y 300-425 and x 188-883. It isn't a pick-a-guide hook, and it doubles as the comment prompt.
• Audio: -15.0 LUFS integrated, true peak -1.7 dBTP, music running from frame 0 (mean -11 dB in the first 0.5s). The kill SFX rise 5-8 dB RMS over the bed at 16.55, 36.55 and 56.8.

❌ Fix
• 56.73-67.93: Joy's added water crush leaves Rayleigh alone for 11.2s, so the winner is obvious through the whole last 10s, which is the exact client complaint. In the reference, red and blue share the top room from about 33s to the cut. In ours, two boxes share the top room only from 53.0 to 54.2. → Re-seed for Rayleigh with two or more boxes alive and both in the top room for at least the last 15s. If you keep the crush, it can only take a third box while two remain.
• Whole reel: the board is squashed to y 470-1390, 48% of the frame height against the reference's 66% (y 230-1500). That leaves dark empty bands from 0-300 and 1500-1920. → Restore the reference proportions with the board at about y 250-1500. Lay the hook over the solid upper-left wall: it spans x 188-883 and the wall runs x 23-892 in the top rows, so it clears the stairs. Stack the roster chips on the same wall mass below the hook.
• 0.0-1.0: the boxes spawn touching (38.5 px pitch for 38 px boxes). They jostle in place for about 0.4s with headings flipping almost every frame, and Joy and Cleo hug the floor until about 1.0s. In the reference the cluster is clearly moving by frame 3. → Spawn with gaps of about 4 px and give the trio one shared 45-degree up-right velocity, with Rayleigh apart, as in the reference. The current headings are 33 and 50 degrees, which isn't 45.
• All: the speed is 200 px/s against the reference's 277 on the same 1034 px board width. This deviation isn't listed. It is why the first KO lands at 16.5 instead of 9.17, leaving no state change for the first 16s. → Use about 277 px/s and aim for KOs near 9s and 13-20s.
• All: the trails are 5 faint ghosts (about 30 px). The boxes are 38 px, about 14 pt on a phone, so the faces can't be read and colour is the only way to tell them apart. → Use solid guide-colour trails at about 4 box lengths and 60-70% opacity, like the reference.
• Roster at y 1404-1494: the Rayleigh chip (x 801-1048) sits mostly under the lower-right action rail (x 887 and up), and the Joy chip starts at x 30, inside the 70 px left margin. → Keep the chips within x 70-887, or move them as described in the board fix.
• Ticks: 156 bounce ticks about 0.43s apart, each about 22 dB over the bed above 3 kHz, steady and not synced to the music. This is judged from the spectrum, not by ear. They are likely to grate over 68s. → Lower them about 4 dB and vary the pitch by ±2 semitones. Keep them, because they are the reference's signature.

🎯 Priority order
1. Ending with two finalists in the top room (re-seed)
2. Board back to reference proportions, with the hook and roster on the wall mass
3. Speed to 277 px/s and an early first KO
4. Clean 45-degree cluster launch
5. Stronger trails
6. Roster safe zone
7. Quieter, varied ticks

Target length: about 70s (the water rise sets it, so keep it for fidelity). Payoff at about 68s, matching the reference's cliffhanger at 72s.

---

## Appendix A: beat table (reference vs ours)

| Beat | Reference | Ours | Status |
|---|---|---|---|
| Launch | Cluster leaves at 0.1s at 277 px/s, long trails | Jostle 0-0.4s; Joy and Cleo near the floor until ~1s; 200 px/s | Changed (worse) |
| Water starts | 0.3s | 0.3s | Match |
| First pencil KO | Yellow 9.17s | Cyrus 16.50s | Changed, 7.3s late (not a listed deviation) |
| Second pencil KO | Green 13.15s | Cleo 36.47s | Changed (listed) |
| Leader tops the stairs, comes back down | Blue at 19s, down 21-23s | Rayleigh top room 12.0-15.4s, back down | Match (earlier) |
| Two finalists in the top room | ~33s to the end (39s of duel) | Joy alone 34.5-45.1; Rayleigh from 48.8; together only 53.0-54.2 | Missing |
| Water crush | None | Joy 56.73s | Added (listed) |
| Water enters the top room | ~60s | ~57s | Match |
| Exit | Blue ~71.9s, hard cut at 72.1, no text | Rayleigh 67.93s, gold ring, victory card 68.43-70.93 | Changed (coordinator's ending) |
| Text | Watermark only | Hook, roster, RAYLEIGH WINS! | Changed (brief) |
| Audio | Hit blips, no music | Rhythmania 1, ticks, kill SFX | Changed (brief) |

Known deviations:
- **Squashed board: hurts.** It brings back complaint #1, and it wasn't needed because the hook and roster fit on the board's own wall mass.
- **Later second pencil death: hurts on net.** It spreads events out, but together with the unlisted late first KO it means there is no state change for 16.5s. The reference lands two KOs in 13s.
- **Added water crush: the mechanic helps but the timing hurts.** It pays off "outruns the water", but where it lands it removes the last opponent and makes the ending obvious.

## Appendix B: rubric scores (out of 10)

| # | Item | Score | Note |
|---|---|---|---|
| 1 | Hook | 6 | Text and board on screen from frame 0; first 0.4s barely moves |
| 2 | Dead time | 5 | No KO until 16.5; 20s gaps 16.5-36.5 and 36.5-56.7; Rayleigh alone 56.7-67.9 |
| 3 | Payoff | 6 | 96%, same as the reference (intended); the last 11s has no contest |
| 4 | Legibility | 4 | Board 48% of the frame height; 38 px boxes; faces unreadable at phone size |
| 5 | Stamps | 7 | X marker, burst and roster OUT at each KO; no overlaps |
| 6 | Ending | 6 | Victory pose held 2.5s; no loop |
| 7 | Comment trigger | 7 | The hook asks the question |
| 8 | Gummy powers | n/a | None in the reference, correctly |

Fidelity to the reference: 6/10.

## Appendix C: brand checks

- Guide faces only.
- No hashtags or em dashes on screen.
- Hook and win text are inside the safe zone. The roster is not (see Fix).

Client-rejection risks:
1. Winner obvious for the last 11s.
2. Small board with dead bands.
3. Slow, static-looking first second.

Evidence is in this folder:
- `_cmp/sbs/` holds the 1 fps side-by-sides (reference left).
- `_cmp/dense/` holds every frame at the start, each death and the win.
- `_cmp/phone_size_30s.png` compares both reels at phone size.
