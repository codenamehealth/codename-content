Build review: m01_DaG5nn5v8AP v2 "Who escapes the shadow" (54.57s, ref 54.27s)

Verdict: FIX FIRST (one blocker: the ending). Fidelity 7/10 (pass 1: 6).

## Pass-1 fixes
| Fix | Landed | Evidence |
|---|---|---|
| Spawn teleport, 2 per chamber | YES | 0-1.0s at 15fps (dense/d_start.jpg): one box per chamber, first motion 0.27s, Joy bounces off its own chamber's left wall at ~0.35s. No jumps. |
| Gates too fast / 4.4-13s dead | YES | Last brick of each gate: 1.73, 4.60, 9.73-9.80, 16.60-16.67s (ref 2.5/4.5/10.5/15.5). Every break has a box in contact (d_g1..d_g4). Dead stretch gone. |
| Board and faces too small | YES | Board fills the ref rectangle (53-1027, 396-1524) almost exactly (layout_t0.5.jpg). Faces 40px with distinct border colours; roster sits in the dead wall area left of the chambers. |
| Pickup late, no knockout | MOSTLY | Cleo breaks D3 37.33, touches the gummy 37.40, stamp 37.40-38.5. 37.47 is 3.3s after the ref sword (34.2) and just outside the 32-37 target. KO at 39.17 is a real corner-to-corner touch (d_ko1_30.jpg). |
| Near-miss reading as a hit | YES | Gummy badge now inside the box (red outline plus icon). No holder near-miss in any dense window. |
| Crunch SFX quiet | MOSTLY | 1.5-8kHz lift over the prior 1.2s: gates +7 to +9 dB, D3 +7.7, crush +9.9, D4 +10.0/+10.8, KO Cyrus +7.8, win +13.2. KO Rayleigh 39.17 only +2.3 dB (+3.6 vs the 38.5-39.1 bed); pickup sting tail and music mask it. |

## New issues, ranked
1. BLOCKER, 42.87-51.57s: the ending is a foregone conclusion. After Joy is crushed (42.87) it is Cleo, holding the kill-on-touch gummy and about one cell from the exit, vs unarmed Cyrus 10+ cells back in the left room. Cyrus's only way to "compete" is to reach Cleo, and touching her kills him (50.50). Then Cleo walks out alone (51.57). Nobody is ever ahead of Cleo after 37.5s. This is exactly the "too obvious who wins in the last 10s" complaint.
   The reference does the opposite: the sword holder (yellow) gets both kills (36.9, 37.7), then the UNARMED red beats the holder into the checker at 53.27 with yellow right behind. The upset is the payoff.
   Fix: keep Cleo as winner but take the gummy off her. Seed-search so another guide (Cyrus or Rayleigh) picks it up around 33-35s and gets the knockouts. Cleo then enters the checker unarmed with the holder alive and within ~1s / 3 cells behind. Reject seeds where the winner leads alone for the final 10s. Also update intents.json, which still says "First box into the exit wins: Joy."
2. 43.0-49.8s: the exit's bottom cell breaks at 43.0 (Cleo, with the gummy) and nothing else happens for 6.8s. Cleo bounces next to an open exit while the flood creeps up. Ref D4 goes at 48.5 with two live boxes racing. Fix (same seed search): last D4 cell no earlier than ~47.5s, with two boxes alive in corridors C/D.
3. 39.17s: KO squish is the quietest event (+2 to +4 dB). Add +4 dB, or a 150ms bed duck like the other events.
4. Minor: the freeze before the pose card is 0.47s (51.57-52.03); ref holds 1.0s. Hold 1.0s before the card.
5. Minor: the flood and walls are both near-black indigo, so once flooded (45s onward) the maze structure disappears into one dark mass. The ref's purple on beige keeps the corridors readable. Optional: lift the flood's lightness or keep a lighter wall edge.
6. Minor, unchanged from pass 1: the exit and win sit in the lower-right action-rail zone (x 910-1024), same as the ref. Mono AAC.

## Physics by eye (dense windows: 0-1, 1.2-2, 4.2-5, 9.2-10, 16.2-17, 37-37.8, 38.8-39.6 at 30fps, 42.4-43.2, 43-51 at 2fps, 49-50.2, 50.1-50.9, 50.9-52.3, 51.43-52.13 at 30fps; everything else 1fps)
- No teleports, jumps, boxes in walls or direction changes without contact in any dense window. Cleo's x-flip at 39.33 is a touch against the left end of the corridor-C wall. Cyrus's y-flip at ~39.36 is a touch on Rayleigh's X'd box. Both are legit.
- Deaths: Rayleigh 39.17, holder touch (real). Joy 42.87: rides the flood front down the right column, slides along the wall and is X'd when pinned in the corner (an honest crush). Cyrus 50.50: holder touch (real).
- D4 is broken cell by cell (bottom 43.0, top 49.8), not opened. One hit per cell with STRENGTH, consistent.
- Win: Cleo is fully inside the checker at 51.56, the board freezes, a gold ring expands, then the pose card at 52.06.

## Phone legibility
- Board fill now matches the ref; no dead space inside the board. Faces read by border colour plus hair. The holder state (red outline and trail) reads at a glance.
- Text: hook y ~255-385, stamp mid-board, CLEO WINS! / DID YOUR GUIDE WIN? inside the board area, roster x ~70-204 (at the left safe-zone edge). Nothing important in the bottom 420px. No hashtags or em dashes on screen.

## Audio
- ebur128: I -15.1 LUFS (pass), TP -2.3 dBTP (pass, limit -1.5), LRA 3.5.

## Files
- 1fps side-by-sides (ref left, ours right): grid_0..9.jpg
- Layout overlay: layout_t0.5.jpg
- Dense windows: dense/*.jpg
