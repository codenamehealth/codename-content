# SPEC DcTTWN-zR6S (117.47s, 1080x1920, 60fps)

Measured from frames (1fps overall, 5-10fps per phase, 60fps at the first HP hit, the yellow crush and both knife kills), pixel runs on frame 0, flood-area timeline (fl_dct.txt).

## Layout
- Red/orange checker background. Board = dark green walls (32,88,48) on light grey floor, outer frame x 52-1027, y 108-1533.
- Top room x 67-926, y 123-654. Grey bevelled block fills its right part (x ~560-905, from the room top down to one square above the floor), leaving a one-square slot under it that runs to the right wall. A gap at the top-right (y 123-~200) joins the room to the outer column (unreachable for squares, it is behind the block).
- Band (wall) y 654-797.
- Middle strip x 67-1012, y 797-972 (3.1 squares tall), open at its right end into the outer column. From the left: knife (x ~80-250, lying, blade right), 999 block x 265-487 full strip height, then open floor.
- Band y 972-1115.
- Bottom room x 67-926, y 1115-1518. 67 block in its right half (x ~476-911, near full height). Gap at the bottom-right (y ~1470-1518) into the outer column.
- Outer right column x 951-1012 (one square wide), y 123-1518, joining top room (top), middle strip (side) and bottom room (bottom).

## Squares
- ~56px, flat colour, black outline, two black eyes (blink), coloured trail. Speed constant ~340 px/s. Yellow alone in the top room; red, blue, green in the bottom room (start top-left, together).
- Bounce on contact with walls, blocks, other squares and the flood front. Squares collide with each other.

## HP blocks
- 67 (bottom): -1 per contact; jams create many contacts in a few frames (67->66->63->62->59->56->53->52 within 0.15s at 1.1s). Each hit pops the block (scales up ~15%, number turns white and larger, fades back ~0.3s, wall wobble). Broken at 7.8s: shatters into white shards; room opens.
- Top block: never breaks. Its number climbs ~5,100/s from 102 at t=0 (5113 at 1s, 81071 at 16s...) and pops on each yellow hit. It is a joke wall; the flood is drawn over it.
- 999 (middle): -1 per contact (999 at 54s, 716 at 90s, 513 at 105s) until the flood packs the three squares against it (3 stacked = strip height) and the count runs down fast (334 at 111, 94 at 113, 0 at 113.4). Shatters.

## Flood (orange 216,112,16)
- Starts ~1s at the left wall of the top and bottom rooms; full-height vertical fronts advance right at ~17 px/s, continuous. Drawn over blocks (it submerges the top block; blocks do not stop it).
- Reaches the right ends ~51s, pours into the outer column through the top-right and bottom-right gaps, fills it from both ends (~51-90s), then enters the middle strip from its right end (~90s) and advances left ~16 px/s, packing the squares into the 999 block (111-113s) and continuing after it breaks.
- Solid for squares (they bounce off it).

## Kills (measured)
- Yellow, 50.9s: CRUSHED by the flood. Yellow was trapped in the slot under the top block from ~22s, bouncing between the front and the right wall; the gap shrank below one square and it was crushed against the right wall. "K.O." label + ring burst, yellow box turns into an X marker that stays.
- Red, 114.62s: the knife. The three move left as a stack after the 999 breaks; the knife jumps into red, red becomes an X marker (skull emoji over it, devil emoji over the holder). Which square triggered it is not fully readable (red's front reached the knife tip that frame; the devil appears over the top square).
- Green, 115.85s: blue touches the lying knife at 115.77 (it swings up beside blue, held), blue's next contact is green -> green becomes an X marker; knife drops and lies there.
- Rule used for the recreation: touching the lying knife = pick it up; the holder's next contact with another square knocks that square out; the knife then lies at that spot. Crush by the flood is the other kill. Last square standing wins.

## Path of the run
- 0-7.8 three squares chip the 67 block; 7.8 it shatters.
- 8-50 three bounce in the bottom room as the flood closes in; pushed into the strip at the right wall ~45s; escape through the bottom-right gap 50-51s, up the outer column, into the middle strip 52-55s.
- 22-50.9 yellow trapped under the top block, crushed 50.9.
- 55-111 three in the middle strip hitting 999 (slow count), flood fills the column then the strip from the right.
- 111-113.4 packed, 999 -> 0; 114.6 red out; 115.85 green out; blue wins.

## On-screen text and ending
- No hook or countdown. "K.O." at the yellow crush (51s). "WIN" burst over blue 115.9-116.4, confetti, neon "BLUE WINS" (pink glow, 2 lines) under the board from 116.0 to the end. Ends 117.47 (1.5s after the win).
- Audio: no music bed (long near-silent stretches 55-110 between hit blips); constant fast hit sound while yellow rattles under the block (20-50s); burst sounds on breaks and kills; win sting.

## Recreation notes (Code Name)
- Yellow's trapped role -> one guide alone in the top room (not Cleo-specific), three in the bottom room. Flood = the shadow. Knife -> creatine gummy (STRENGTH!), same rule. Emoji reactions dropped (X markers and K.O. kept). Winner card text above the roster (the reference's text sits in the caption zone). Rooms widened and the bands thinned to fit y ~466-1394. Hook (coordinator): soft fade job hook, e.g. WHO SURVIVES / THE SHADOW?
